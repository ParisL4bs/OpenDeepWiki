# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
import concurrent.futures
from typing import List, Dict
import json
import instructor
import google.generativeai as genai
from src.schemas.description import (
    generate_code_structure_model_precise,
    generate_code_structure_model_consize,
    DocumentCompression,
    YamlBrief,
)
from src.utils.utils import list_all_files
import time
import random
import traceback

json

from src.monitor.langfuse import get_langfuse_context, trace
import dotenv
import os

dotenv.load_dotenv()

FILE_SUMMARIZATION_MODEL_0 = os.getenv("FILE_CLASSICATION_MODEL_0")
FILE_SUMMARIZATION_MODEL_1 = os.getenv("FILE_CLASSICATION_MODEL_1")
FILE_SUMMARIZATION_MODEL_2 = os.getenv("FILE_CLASSICATION_MODEL_2")
FILE_SUMMARIZATION_MODEL_3 = os.getenv("FILE_CLASSICATION_MODEL_3")


def process_batch(
    file_batch: str,
    client_gemini,
    model_name,
    system_prompt: str,
    user_prompt: str,
    scores: List[int],
    span=None,
    index=None,
    log_name=None,
    fallback_clients: List[instructor.Instructor] = None,
    fallback_model_names: List[str] = None,
) -> Dict:
    """Process a batch of files using Gemini API with timeout and retries."""
    batch_prompt = ""
    try:
        with open(file_batch, "r") as f:
            batch_prompt = user_prompt + "\n" + f.read()
    except Exception as e:
        print(f"Error reading file {file_batch}: {e}") # Log file reading error
        return None, None

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": batch_prompt},
    ]

    # Simulate a delay with random jitter - Moved outside the retry loop
    # delay = random.uniform(0.1, 0.5)
    # time.sleep(delay) # Consider if this delay is still needed with timeouts

    if log_name == "docstring":
        pydantic_model = generate_code_structure_model_consize(batch_prompt)
    elif log_name == "documentation":
        pydantic_model = DocumentCompression
    else: # config
        pydantic_model = YamlBrief

    # --- Langfuse Span Setup ---
    generation = None
    if span:
        # Create the generation span *before* the retry loop
        generation = span.generation(
            name=f"{log_name}_attempt", # Initial name, might update later
            model=model_name, # Initial model
            model_parameters={"temperature": 0, "top_p": 1, "max_new_tokens": 8000},
            input={"system_prompt": system_prompt, "user_prompt": batch_prompt},
        )

    # --- Retry Logic ---
    max_attempts = 4 # 1 initial + 3 retries
    clients_to_try = [(client_gemini, model_name)] + list(zip(fallback_clients or [], fallback_model_names or []))
    # Ensure we don't try more clients than available or exceed max_attempts
    clients_to_try = clients_to_try[:max_attempts]

    last_exception = None
    last_status_message = ""

    for attempt, (current_client, current_model_name) in enumerate(clients_to_try):
        print(f"Attempt {attempt + 1}/{len(clients_to_try)} for file {file_batch} using model {current_model_name}...")
        try:
            # Function to run the API call, needed for ThreadPoolExecutor
            def api_call_task():
                return current_client.chat.create_with_completion(
                    messages=messages,
                    response_model=pydantic_model,
                    generation_config={
                        "temperature": 0.0,
                        "top_p": 1,
                        "candidate_count": 1,
                        "max_output_tokens": 8000,
                    },
                    max_retries=1, # Reduced internal retries as we have our own loop
                )

            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(api_call_task)
                completion, raw = future.result(timeout=15) # 15-second timeout

            # --- Success ---
            result = completion.model_dump()
            print(f"Success on attempt {attempt + 1} for file {file_batch}")
            if generation:
                # Update generation details for the successful attempt
                generation.model = current_model_name
                generation.end(
                    output=result,
                    usage={
                        "input": raw.usage_metadata.prompt_token_count,
                        "output": raw.usage_metadata.candidates_token_count,
                    },
                    level="DEFAULT", # Explicitly set level to DEFAULT for success
                    status_message=f"Success on attempt {attempt + 1}"
                )
            return result, index

        except concurrent.futures.TimeoutError:
            last_status_message = f"Attempt {attempt + 1} timed out after 15s (Model: {current_model_name})"
            print(last_status_message)
            last_exception = concurrent.futures.TimeoutError(last_status_message) # Store exception type

        except Exception as e:
            last_status_message = f"Attempt {attempt + 1} failed (Model: {current_model_name}): {str(e)}, {traceback.format_exc()}"
            print(last_status_message)
            last_exception = e # Store the exception

        # Update generation span for failed attempt if it exists
        if generation:
             generation.status_message=last_status_message # Keep updating status message on failures
             generation.model = current_model_name # Ensure model name reflects the failed attempt

    # --- All attempts failed ---
    print(f"All {len(clients_to_try)} attempts failed for file {file_batch}. Last error: {last_status_message}")
    if generation:
        generation.end(
            output=None,
            status_message=last_status_message,
            level="ERROR",
        )
    return None, None

@trace
def summerizer(
    classified_files: dict,
    system_prompt_docstring: str,
    system_prompt_documentation: str,
    system_prompt_config: str,
    user_prompt_docstring: str,
    user_prompt_documentation: str,
    user_prompt_config: str,
    batch_size: int = 50,  # Number of files to process in each batch
    max_workers: int = 30,  # Number of parallel workers
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
            model_name=FILE_SUMMARIZATION_MODEL_0, safety_settings=safe
        ),
        mode=instructor.Mode.GEMINI_JSON,
    )
    client_gemini_1 = instructor.from_gemini(
        client=genai.GenerativeModel(
            model_name=FILE_SUMMARIZATION_MODEL_1, safety_settings=safe
        ),
        mode=instructor.Mode.GEMINI_JSON,
    )
    client_gemini_2 = instructor.from_gemini(
        client=genai.GenerativeModel(
            model_name=FILE_SUMMARIZATION_MODEL_2, safety_settings=safe
        ),
        mode=instructor.Mode.GEMINI_JSON,
    )
    client_gemini_3 = instructor.from_gemini(
        client=genai.GenerativeModel(
            model_name=FILE_SUMMARIZATION_MODEL_3, safety_settings=safe
        ),
        mode=instructor.Mode.GEMINI_JSON,
    )

    clients = {
        0: client_gemini_0,
        1: client_gemini_1,
        2: client_gemini_2,
        3: client_gemini_3,
    }

    model_names = {
        0: FILE_SUMMARIZATION_MODEL_0,
        1: FILE_SUMMARIZATION_MODEL_1,
        2: FILE_SUMMARIZATION_MODEL_2,
        3: FILE_SUMMARIZATION_MODEL_3,
    }


    # Prepare file lists for each category
    files_structure_docstring = []
    files_structure_documentation = []
    files_structure_config = []

    # Keep track of original indices to update the main dict later if needed
    # or to handle categorization after processing
    original_indices = {}

    for index, file in enumerate(classified_files["file_classifications"]):
        file_path = file["file_paths"]
        file_name = file.get("file_name", "").lower() # Handle potential missing key
        original_indices[file_path] = index # Store index by file_path

        if "code" in file["classification"].lower() and "ipynb" not in file_path and "__init__.py" not in file_path:
            files_structure_docstring.append([file_path, "docstring"])
        elif ".md" in file_path.lower():
            files_structure_documentation.append([file_path, "documentation"])
        elif ".yaml" in file_path.lower() or ".yml" in file_path.lower() or ".yml" in file_name:
             files_structure_config.append([file_path, "config"])


    # Combine all files to process
    all_files_to_process = files_structure_docstring + files_structure_documentation + files_structure_config

    # Temporary storage for results
    results_docstring = {}
    results_documentation = {}
    results_config = {}

    # Process all batches in parallel using a single ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {}
        for i, (file_path, category) in enumerate(all_files_to_process):
            client_index = i % 4
            model_name = model_names[client_index]
            client = clients[client_index]
            fallback_clients = [clients[j] for j in range(4) if j != client_index]
            fallback_model_names = [model_names[j] for j in range(4) if j != client_index]
            if category == "docstring":
                system_prompt = system_prompt_docstring
                user_prompt = user_prompt_docstring
                log_name = "docstring"
            elif category == "documentation":
                system_prompt = system_prompt_documentation
                user_prompt = user_prompt_documentation
                log_name = "documentation"
            else: # category == "config"
                system_prompt = system_prompt_config
                user_prompt = user_prompt_config
                log_name = "config"

            future = executor.submit(
                process_batch,
                file_path,
                client,
                model_name,
                system_prompt,
                user_prompt,
                scores,
                span,
                file_path, # Pass file_path as identifier instead of original index
                log_name=log_name,
                fallback_clients=fallback_clients,
                fallback_model_names=fallback_model_names,
            )
            future_to_file[future] = (file_path, category)

        for future in as_completed(future_to_file):
            file_path, category = future_to_file[future]
            try:
                result, identifier = future.result() # identifier is file_path here
                if result and identifier == file_path: # Check if result is valid and matches the file path
                    if category == "docstring":
                        results_docstring[file_path] = result
                    elif category == "documentation":
                        results_documentation[file_path] = result
                    elif category == "config":
                        results_config[file_path] = result
            except Exception as e:
                print(f"Batch processing failed for {file_path} ({category}): {str(e)}", {traceback.format_exc()})


    # Structure the final output
    output_documentation = []
    output_documentation_md = []
    output_config = []

    processed_indices = set()

    # Populate docstring results
    for file_path, result in results_docstring.items():
         original_index = original_indices.get(file_path)
         if original_index is not None:
             file_data = classified_files["file_classifications"][original_index].copy()
             file_data["documentation"] = result
             file_data["file_id"] = len(output_documentation) # Assign new sequential ID
             output_documentation.append(file_data)
             processed_indices.add(original_index)

    # Populate documentation (.md) results
    for file_path, result in results_documentation.items():
        original_index = original_indices.get(file_path)
        if original_index is not None:
            file_data = classified_files["file_classifications"][original_index].copy()
            file_data["documentation"] = result # Add result under 'documentation' key
            file_data["file_id"] = len(output_documentation_md)
            output_documentation_md.append(file_data)
            processed_indices.add(original_index)

    # Populate config results
    for file_path, result in results_config.items():
        original_index = original_indices.get(file_path)
        if original_index is not None:
            file_data = classified_files["file_classifications"][original_index].copy()
            file_data["documentation_config"] = result # Add result under 'documentation_config' key
            file_data["file_id"] = len(output_config)
            output_config.append(file_data)
            processed_indices.add(original_index)

    # Add any remaining files that weren't processed (e.g., excluded ipynb, init.py)
    # This part might need adjustment based on desired behavior for unprocessed files.
    # Currently, they are implicitly excluded from the output lists.
    # If they need to be included in one of the lists without documentation, add logic here.


    return {
        "documentation": output_documentation,
        "documentation_md": output_documentation_md,
        "config": output_config,
    }
