# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict
import json
import instructor
import google.generativeai as genai
from pathlib import Path
import sys
SRC_DIR_RELATIVE_TO_FLOW = Path("../../src")
current_script_dir = Path(__file__).parent.resolve()
src_path_to_add = (current_script_dir / SRC_DIR_RELATIVE_TO_FLOW).resolve()

sys.path.insert(0, str(current_script_dir)) # For importing from ./tools
sys.path.insert(0, str(src_path_to_add.parent))

from src.schemas.classif import create_file_classification
from src.utils.utils import list_all_files
import time
import random
import dotenv
import os

dotenv.load_dotenv()
FILE_CLASSICATION_MODEL_0 = os.getenv("FILE_CLASSICATION_MODEL_0")
FILE_CLASSICATION_MODEL_1 = os.getenv("FILE_CLASSICATION_MODEL_2")
FILE_CLASSICATION_MODEL_2 = os.getenv("FILE_CLASSICATION_MODEL_3")
# os.environ["PF_DISABLE_TRACING"] = "true" # Promptflow specific
# os.environ["LANG_DISABLE_TRACING"] = "true" # Langchain specific

from src.monitor.langfuse import get_langfuse_context, trace


def process_batch(
    file_batch: List[str],
    client_gemini,
    model_name,
    symstem_prompt: str,
    user_prompt: str,
    scores: List[int],
    span=None,
) -> Dict:
    """Process a batch of files using Gemini API"""
    batch_prompt = user_prompt + "\n" + f"{file_batch}"

    messages = [
        {"role": "system", "content": symstem_prompt},
        {"role": "user", "content": batch_prompt},
    ]

    # Simulate a delay with random jitter
    delay = random.uniform(0.1, 0.5)
    time.sleep(delay)

    if span:
        generation = span.generation(
            name="gemini",
            model=model_name,
            model_parameters={"temperature": 0, "top_p": 1, "max_new_tokens": 8000},
            input={"system_prompt": symstem_prompt, "user_prompt": batch_prompt},
        )

    try:
        completion, raw = client_gemini.chat.create_with_completion(
            messages=messages,
            response_model=create_file_classification(file_batch, scores),
            generation_config={
                "temperature": 0.0,
                "top_p": 1,
                "candidate_count": 1,
                "max_output_tokens": 8000,
            },
            max_retries=10,
        )
        result = completion.model_dump()
        # if span:
        #     span.score(name="number_try", value=raw.n_attempts)

    except Exception as e:
        if span:
            generation.end(
                output=None,
                status_message=f"Error processing batch: {str(e)}",
                level="ERROR",
            )
        raise Exception(f"Batch processing failed: {str(e)}, {traceback.format_exc()}")

    if span:
        generation.end(
            output=result,
            usage={
                "input": raw.usage_metadata.prompt_token_count,
                "output": raw.usage_metadata.candidates_token_count,
            },
        )

    return result


@trace
def llmclassifier(
    folder_path: str,
    symstem_prompt: str,
    user_prompt: str,
    batch_size: int = 50,  # Number of files to process in each batch
    max_workers: int = 10,  # Number of parallel workers
    GEMINI_API_KEY: str = "",
    ANTHROPIC_API_KEY: str = "",
    OPENAI_API_KEY: str = "",
    trace_id: str = ""
) -> str:
    span = get_langfuse_context().get("span")

    scores = [0]

    # Configure safety settings
    safe = [
        {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]

    # Configure Gemini with API key from request if provided
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
    else:
        # Use default API key from environment
        genai.configure()
        
    client_gemini_0 = instructor.from_gemini(
        client=genai.GenerativeModel(
            model_name=FILE_CLASSICATION_MODEL_0, safety_settings=safe
        ),
        mode=instructor.Mode.GEMINI_JSON,
    )
    client_gemini_1 = instructor.from_gemini(
        client=genai.GenerativeModel(
            model_name=FILE_CLASSICATION_MODEL_1, safety_settings=safe
        ),
        mode=instructor.Mode.GEMINI_JSON,
    )
    client_gemini_2 = instructor.from_gemini(
        client=genai.GenerativeModel(
            model_name=FILE_CLASSICATION_MODEL_2, safety_settings=safe
        ),
        mode=instructor.Mode.GEMINI_JSON,
    )

    clients = {
        0: client_gemini_0,
        1: client_gemini_1,
        2: client_gemini_2,
    }

    model_names = {
        0: FILE_CLASSICATION_MODEL_0,
        1: FILE_CLASSICATION_MODEL_1,
        2: FILE_CLASSICATION_MODEL_2,
    }
    
    

    # Get file names
    files_structure = list_all_files(folder_path, include_md=True)

    file_names = files_structure["all_files_no_path"]
    files_paths = files_structure["all_files_with_path"]

    # Split files into batches
    batches = [
        file_names[i : i + batch_size] for i in range(0, len(file_names), batch_size)
    ]

    all_results = {"file_classifications": []}

    # Process batches in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_batch = {
            executor.submit(
                process_batch,
                batch,
                clients[index % 3],
                model_names[index % 3],
                symstem_prompt,
                user_prompt,
                scores,
                span,
            ): batch
            for index, batch in enumerate(batches)
        }

        for future in as_completed(future_to_batch):
            try:
                result = future.result()
                all_results["file_classifications"].extend(
                    result.get("file_classifications", [])
                )
            except Exception as e:
                raise Exception(f"Batch processing failed: {str(e)}, {traceback.format_exc()}")


    # replace file_name by fileç_path
    for classification in all_results["file_classifications"]:
        classification["file_paths"] = files_paths[classification["file_id"]]

    # Combine all results

    return all_results
