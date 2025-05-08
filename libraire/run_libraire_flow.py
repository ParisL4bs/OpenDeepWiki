import os
import sys
import json # For handling object inputs if they are JSON strings
from jinja2 import Environment, FileSystemLoader
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- BEGIN: Tool Script Placeholders ---
# You will need to replace these with actual imports from your tool files.
# For example: from tools.query_rewrite import rewrite_query

# If your tools are in a 'tools' subdirectory relative to this script:
script_dir = os.path.dirname(os.path.abspath(__file__))
tools_path = os.path.join(script_dir, 'tools')
src_path = os.path.abspath(os.path.join(script_dir, '..', '..', 'src')) # Adjust if src is elsewhere

sys.path.insert(0, tools_path)
sys.path.insert(0, src_path) # For `additional_includes: - ../src`

# --- Placeholder functions for your tools ---
# Replace these with actual imports and ensure your tool functions
# match the expected signatures and return values.

def rewrite_query(user_prompt, symstem_prompt, GEMINI_API_KEY, ANTHROPIC_API_KEY, OPENAI_API_KEY):
    logger.info(f"[TOOL STUB] rewrite_query called with user_prompt: {user_prompt[:50]}...")
    # This should call your actual LLM for rewriting
    # Example:
    # response = call_llm(model="some_model", system_prompt=symstem_prompt, user_prompt=user_prompt, api_key=OPENAI_API_KEY)
    # return {"goal_rewrite": response.text}
    return {"goal_rewrite": f"Rewritten: {user_prompt}"} # Placeholder

def retrieve_library_info(user_prompt, symstem_prompt, documentation, cache_id, GEMINI_API_KEY, ANTHROPIC_API_KEY, OPENAI_API_KEY):
    logger.info(f"[TOOL STUB] retrieve_library_info called with user_prompt: {user_prompt[:50]}...")
    # This should call your actual retrieval logic
    return {"files_list": ["example_lib_file1.py", "example_lib_file2.py"]} # Placeholder

def parse_config_and_docs(symstem_prompt, user_prompt, config_doc, documentation_md, GEMINI_API_KEY, ANTHROPIC_API_KEY, OPENAI_API_KEY):
    logger.info(f"[TOOL STUB] parse_config_and_docs called with user_prompt: {user_prompt[:50]}...")
    # This should call your actual parsing/retrieval logic for config/md
    return {"files_list": ["example_config_info.md"]} # Placeholder

def generate_code(files_list, documentation, documentation_md, config, cache_id, symstem_prompt, user_prompt, files_list_md_config, GEMINI_API_KEY, ANTHROPIC_API_KEY, OPENAI_API_KEY):
    logger.info(f"[TOOL STUB] generate_code called with user_prompt: {user_prompt[:50]}...")
    # This should call your actual code generation LLM
    # Example:
    # context = f"Relevant files: {files_list}, {files_list_md_config}. Docs: {documentation}, {documentation_md}. Config: {config}"
    # code = call_llm(model="code_model", system_prompt=symstem_prompt, user_prompt=user_prompt + "\n\nContext:\n" + context, api_key=OPENAI_API_KEY)
    # return code.text
    return f"# Placeholder code based on: {user_prompt}\n# Relevant files: {files_list}, {files_list_md_config}" # Placeholder

# --- END: Tool Script Placeholders ---


class LibraireFlow:
    def __init__(self, prompts_dir="prompts"):
        # Setup Jinja2 environment
        # Assuming prompts_dir is relative to this script's location
        self.prompts_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), prompts_dir)
        self.jinja_env = Environment(loader=FileSystemLoader(self.prompts_path), trim_blocks=True, lstrip_blocks=True)
        logger.info(f"Jinja2 environment loaded from: {self.prompts_path}")

    def _render_prompt(self, template_file, **kwargs):
        template = self.jinja_env.get_template(template_file)
        return template.render(**kwargs)

    def run(self, repository_name, cache_id, documentation, user_problem,
            documentation_md, config, GEMINI_API_KEY, ANTHROPIC_API_KEY, OPENAI_API_KEY):
        """
        Executes the Libraire flow.
        """
        logger.info("--- Starting Libraire Flow ---")

        # 1. prompt_user_rewriter
        logger.info("\n[Node] prompt_user_rewriter")
        prompt_user_rewriter_output = self._render_prompt(
            "prompt_rewrite/user_prompt_rewrite.jinja2",
            user_query=user_problem
        )
        logger.info(f"  Output: {prompt_user_rewriter_output[:100]}...")

        # 2. prompt_system_rewriter
        logger.info("\n[Node] prompt_system_rewriter")
        prompt_system_rewriter_output = self._render_prompt(
            "prompt_rewrite/system_prompt_rewrite.jinja2",
            library_name=repository_name
        )
        logger.info(f"  Output: {prompt_system_rewriter_output[:100]}...")

        # 3. rewriter
        logger.info("\n[Node] rewriter")
        rewriter_output = rewrite_query(
            user_prompt=prompt_user_rewriter_output,
            symstem_prompt=prompt_system_rewriter_output, # Note: DAG uses 'symstem_prompt'
            GEMINI_API_KEY=GEMINI_API_KEY,
            ANTHROPIC_API_KEY=ANTHROPIC_API_KEY,
            OPENAI_API_KEY=OPENAI_API_KEY
        )
        logger.info(f"  Output: {rewriter_output}")
        goal_rewrite = rewriter_output.get("goal_rewrite", "") # Safely get the value

        # 4. prompt_system_librari_retriver
        logger.info("\n[Node] prompt_system_librari_retriver")
        prompt_system_librari_retriver_output = self._render_prompt(
            "system_prompt_librari_retriver.jinja2",
            repository_name=repository_name
        )
        logger.info(f"  Output: {prompt_system_librari_retriver_output[:100]}...")

        # 5. prompt_user_librari_retriver
        logger.info("\n[Node] prompt_user_librari_retriver")
        prompt_user_librari_retriver_output = self._render_prompt(
            "user_prompt_librari_retriver.jinja2",
            user_problem=goal_rewrite
        )
        logger.info(f"  Output: {prompt_user_librari_retriver_output[:100]}...")

        # 6. librairi_retriver
        logger.info("\n[Node] librairi_retriver")
        librairi_retriver_output = retrieve_library_info(
            user_prompt=prompt_user_librari_retriver_output,
            symstem_prompt=prompt_system_librari_retriver_output, # Note: DAG uses 'symstem_prompt'
            documentation=documentation,
            cache_id=cache_id,
            GEMINI_API_KEY=GEMINI_API_KEY,
            ANTHROPIC_API_KEY=ANTHROPIC_API_KEY,
            OPENAI_API_KEY=OPENAI_API_KEY
        )
        logger.info(f"  Output: {librairi_retriver_output}")
        librairi_files_list = librairi_retriver_output.get("files_list", [])

        # 7. user_prompt_config_retriver
        logger.info("\n[Node] user_prompt_config_retriver")
        user_prompt_config_retriver_output = self._render_prompt(
            "prompt_user_config_retriver.jinja2",
            user_problem=goal_rewrite
        )
        logger.info(f"  Output: {user_prompt_config_retriver_output[:100]}...")

        # 8. md_config_retriver
        logger.info("\n[Node] md_config_retriver")
        md_config_retriver_output = parse_config_and_docs(
            symstem_prompt=prompt_system_librari_retriver_output, # Re-using this as per DAG logic
            user_prompt=user_prompt_config_retriver_output,
            config_doc=config,
            documentation_md=documentation_md,
            GEMINI_API_KEY=GEMINI_API_KEY,
            ANTHROPIC_API_KEY=ANTHROPIC_API_KEY,
            OPENAI_API_KEY=OPENAI_API_KEY
        )
        logger.info(f"  Output: {md_config_retriver_output}")
        md_config_files_list = md_config_retriver_output.get("files_list", [])

        # 9. prompt_user_code_generator
        logger.info("\n[Node] prompt_user_code_generator")
        prompt_user_code_generator_output = self._render_prompt(
            "prompt_coder/user_prompt_code_generator.jinja2",
            user_problem=user_problem # Original user problem
        )
        logger.info(f"  Output: {prompt_user_code_generator_output[:100]}...")

        # 10. prompt_system_code_generator
        logger.info("\n[Node] prompt_system_code_generator")
        prompt_system_code_generator_output = self._render_prompt(
            "prompt_coder/system_prompt_code_generator.jinja2",
            repository_name=repository_name
        )
        logger.info(f"  Output: {prompt_system_code_generator_output[:100]}...")

        # 11. code_generator
        logger.info("\n[Node] code_generator")
        code_generator_output = generate_code(
            files_list=librairi_files_list,
            documentation=documentation,
            documentation_md=documentation_md,
            config=config,
            cache_id=cache_id,
            symstem_prompt=prompt_system_code_generator_output, # Note: DAG uses 'symstem_prompt'
            user_prompt=prompt_user_code_generator_output,
            files_list_md_config=md_config_files_list,
            GEMINI_API_KEY=GEMINI_API_KEY,
            ANTHROPIC_API_KEY=ANTHROPIC_API_KEY,
            OPENAI_API_KEY=OPENAI_API_KEY
        )
        logger.info(f"  Output (final response): {code_generator_output[:200]}...")

        logger.info("\n--- Libraire Flow Finished ---")
        return code_generator_output


if __name__ == "__main__":
    # --- Define Default Inputs (as per your DAG) ---
    default_inputs = {
        "repository_name": "Instructor",
        "cache_id": "cachedContents/3xn5x0ed6u62",
        "documentation": {}, # In Python, this is an empty dict
        "user_problem": "You are an expert python developper. I need to get the number of attemps it took the model to get the task rigth",
        "documentation_md": {}, # Empty dict
        "config": {}, # Empty dict
        "GEMINI_API_KEY": os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_KEY_HERE"), # Load from env or use placeholder
        "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY", "YOUR_ANTHROPIC_KEY_HERE"),
        "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", "YOUR_OPENAI_KEY_HERE")
    }

    # Handle object inputs: PromptFlow might pass JSON strings for objects.
    # Here, we assume they are already Python dicts. If they were strings, you'd use json.loads().
    # e.g., default_inputs["documentation"] = json.loads(default_inputs["documentation_str"]) if it was a string.

    logger.info("Running flow with default inputs...")
    flow_runner = LibraireFlow(prompts_dir="prompts") # Assuming 'prompts' is a subdir
    
    try:
        libraire_response = flow_runner.run(**default_inputs)
        logger.info("\n=== Final Libraire Response ===")
        logger.info(libraire_response)
    except FileNotFoundError as e:
        logger.info(f"\nERROR: Could not find a required file. This often means a Jinja template is missing or paths are incorrect.")
        logger.info(f"Details: {e}")
        logger.info(f"Ensure your 'prompts' directory is correctly structured relative to this script ({__file__})")
        logger.info(f"Expected Jinja templates path: {flow_runner.prompts_path}")
    except ImportError as e:
        logger.info(f"\nERROR: Could not import a tool module.")
        logger.info(f"Details: {e}")
        logger.info(f"Ensure your 'tools' directory is correctly structured and contains the necessary Python files with the expected functions.")
        logger.info(f"Tools path added to sys.path: {tools_path}")
        logger.info(f"SRC path added to sys.path: {src_path}")
    except Exception as e:
        logger.info(f"\nAn unexpected error occurred: {e}")
        import traceback
        traceback.logger.info_exc()