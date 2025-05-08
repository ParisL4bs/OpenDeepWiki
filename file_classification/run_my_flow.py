# import os
# import sys
# import argparse
# from pathlib import Path
# from jinja2 import Environment, FileSystemLoader
# import dotenv

# dotenv.load_dotenv()

# gemini_api_key = os.getenv("GEMINI_API_KEY")
# anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
# openai_api_key = os.getenv("OPENAI_API_KEY")

# # --- Constants based on your flow.dag.yaml ---
# PROMPT_DIR = Path("prompts")
# TOOL_DIR = Path("tools")
# SRC_DIR_RELATIVE_TO_FLOW = Path("../src") # Relative to where flow.dag.yaml is

# # --- Helper Function to Load Jinja2 Templates ---
# def load_jinja_template(template_path: Path, context: dict = None) -> str:
#     """
#     Loads and renders a Jinja2 template.
#     If context is None, it's rendered with an empty context.
#     """
#     if context is None:
#         context = {}
    
#     # Assuming templates are in a 'prompts' directory relative to this script
#     # or an absolute path is provided.
#     # For this setup, template_path is expected to be like 'prompts/system_prompt_classification.jinja2'
    
#     # Resolve the actual template directory and file name
#     resolved_template_path = Path(template_path)
#     template_dir = resolved_template_path.parent
#     template_file = resolved_template_path.name

#     if not resolved_template_path.exists():
#         raise FileNotFoundError(f"Template file not found: {resolved_template_path}")

#     env = Environment(loader=FileSystemLoader(searchpath=template_dir))
#     template = env.get_template(template_file)
#     return template.render(context)

# # --- Placeholder for your actual tool functions ---
# # You will need to replace these with actual imports and function calls
# # from your tool scripts.

# # Example: if tools/llmclassifier.py has a function `run_classification`
# from tools.llmclassifier import llmclassifier
# def llmclassifier_tool_function(symstem_prompt: str, user_prompt: str, folder_path: str,
#                                 max_workers: int, GEMINI_API_KEY: str,
#                                 ANTHROPIC_API_KEY: str, OPENAI_API_KEY: str,
#                                 trace_id: str):
#     print(f"[INFO] Calling llmclassifier_tool_function with folder_path: {folder_path}")
#     # This is where you'd import and call your actual llmclassifier logic
#     # e.g., from tools.llmclassifier import classify
#     # return classify(symstem_prompt=symstem_prompt, ...)
    
#     # --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
#     output = llmclassifier(symstem_prompt=symstem_prompt, user_prompt=user_prompt, folder_path=folder_path,
#                            max_workers=max_workers, GEMINI_API_KEY=GEMINI_API_KEY,
#                            ANTHROPIC_API_KEY=ANTHROPIC_API_KEY, OPENAI_API_KEY=OPENAI_API_KEY,
#                            trace_id=trace_id)
#     # --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    
#     # Placeholder output:
#     print("⚠️ Placeholder for llmclassifier_tool_function: Returning dummy data.")
#     return output


# # Example: if tools/descriptor.py has a function `generate_docs`
# from tools.descriptor import summerizer
# def descriptor_tool_function(classified_files: dict,
#                              system_prompt_config: str, user_prompt_config: str,
#                              system_prompt_docstring: str, user_prompt_docstring: str,
#                              system_prompt_documentation: str, user_prompt_documentation: str,
#                              GEMINI_API_KEY: str, ANTHROPIC_API_KEY: str, OPENAI_API_KEY: str,
#                              trace_id: str):
#     print(f"[INFO] Calling descriptor_tool_function with classified_files: {classified_files}")
#     # This is where you'd import and call your actual descriptor logic
#     # e.g., from tools.descriptor import generate
#     # return generate(classified_files=classified_files, ...)

#     # --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
#     # Replace this with your actual tool import and call:
#     output = summerizer(classified_files=classified_files,
#                         system_prompt_config=system_prompt_config, user_prompt_config=user_prompt_config,
#                         system_prompt_docstring=system_prompt_docstring, user_prompt_docstring=user_prompt_docstring,
#                         system_prompt_documentation=system_prompt_documentation, user_prompt_documentation=user_prompt_documentation,
#                         GEMINI_API_KEY=GEMINI_API_KEY, ANTHROPIC_API_KEY=ANTHROPIC_API_KEY, OPENAI_API_KEY=OPENAI_API_KEY,
#                         trace_id=trace_id)
#     # --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

#     # Placeholder output:
#     print("⚠️ Placeholder for descriptor_tool_function: Returning dummy data.")
#     return output


# # --- Main Flow Execution ---
# def run_flow(repo_local_path: str,
#              gemini_api_key: str = "",
#              anthropic_api_key: str = "",
#              openai_api_key: str = "",
#              trace_id: str = ""):
#     """
#     Orchestrates the flow similar to the promptflow definition.
#     """
#     print("--- Starting Flow Execution ---")

#     # 1. Load Prompts (Nodes 1, 2, 4, 5, 6, 7, 8, 9)
#     # These prompts have no inputs, so context is empty.
#     print("Loading prompts...")
#     #pwd
#     print(os.getcwd())

#     system_prompt_classification_output = load_jinja_template("file_classification/prompts/system_prompt_classification.jinja2")
#     prompt_user_classification_output = load_jinja_template("file_classification/prompts/user_prompt_classification.jinja2")
    
#     prompt_system_docstring_output = load_jinja_template("file_classification/prompts/prompt_docstrings/system_prompt_classification.jinja2")
#     prompt_user_docstring_output = load_jinja_template("file_classification/prompts/prompt_docstrings/user_prompt_classification.jinja2")
    
#     system_prompt_configuration_output = load_jinja_template("file_classification/prompts/prompt_configurations/system_prompt_configuration.jinja2")
#     user_prompt_configuration_output = load_jinja_template("file_classification/prompts/prompt_configurations/user_prompt_configuration.jinja2")
    
#     system_prompt_documentation_output = load_jinja_template("file_classification/prompts/prompt_documentations/system_prompt_documentation.jinja2")
#     user_prompt_documentation_output = load_jinja_template("file_classification/prompts/prompt_documentations/user_prompt_documentation.jinja2")
#     print("Prompts loaded.")

#     # 2. File Classifier Node (Node 3)
#     print("Running file classifier...")
#     file_classifier_output = llmclassifier_tool_function(
#         symstem_prompt=system_prompt_classification_output,
#         user_prompt=prompt_user_classification_output,
#         folder_path=repo_local_path,
#         max_workers=10, # As per your YAML
#         GEMINI_API_KEY=gemini_api_key,
#         ANTHROPIC_API_KEY=anthropic_api_key,
#         OPENAI_API_KEY=openai_api_key,
#         trace_id=trace_id
#     )
#     print(f"File classifier output: {str(file_classifier_output)[:200]}...") # Log snippet

#     # 3. Documentation Generation Node (Node 10)
#     print("Running documentation generation...")
#     documentation_generation_output = descriptor_tool_function(
#         classified_files=file_classifier_output, # This is ${file_classifier.output}
#         system_prompt_config=system_prompt_configuration_output,
#         user_prompt_config=user_prompt_configuration_output,
#         system_prompt_docstring=prompt_system_docstring_output,
#         user_prompt_docstring=prompt_user_docstring_output,
#         system_prompt_documentation=system_prompt_documentation_output,
#         user_prompt_documentation=user_prompt_documentation_output,
#         GEMINI_API_KEY=gemini_api_key,
#         ANTHROPIC_API_KEY=anthropic_api_key,
#         OPENAI_API_KEY=openai_api_key,
#         trace_id=trace_id
#     )
#     print(f"Documentation generation output: {str(documentation_generation_output)[:200]}...")

#     # 4. Prepare final outputs
#     final_outputs = documentation_generation_output
    
#     print("--- Flow Execution Finished ---")
#     return final_outputs

# if __name__ == "__main__":
#     # --- Environment Variables ---
#     # These are set based on your flow.dag.yaml
#     # Some might be specific to promptflow/langchain and may not be needed
#     # by your custom tools, but we set them for completeness.
#     os.environ["PROMPTFLOW_NAME"] = "file_classifier"
#     os.environ["PF_DISABLE_TRACING"] = "true" # Promptflow specific
#     os.environ["LANG_DISABLE_TRACING"] = "true" # Langchain specific

#     # --- Additional Includes (sys.path modification) ---
#     # This script assumes it's in the same directory as flow.dag.yaml
#     # and 'prompts', 'tools' are subdirectories.
#     # '../src' means one level up from this script's dir, then into 'src'.
#     current_script_dir = Path(__file__).parent.resolve()
#     src_path_to_add = (current_script_dir / SRC_DIR_RELATIVE_TO_FLOW).resolve()
    
#     # Ensure TOOL_DIR is also in sys.path if your tools import each other relatively
#     # or if you want to `from tools import ...` directly.
#     # Typically, if `tools` is a package (has __init__.py), and this script is outside,
#     # you'd add the parent of `tools` to sys.path.
#     # If this script is at the project root, and `tools` is a subdir, it should be fine.
#     sys.path.insert(0, str(current_script_dir)) # For importing from ./tools
#     sys.path.insert(0, str(src_path_to_add))
#     from src.utils.utils import generate_trace_id

#     print(f"Added to sys.path: {src_path_to_add}")
#     print(f"Added to sys.path: {current_script_dir}")


#     # --- Argument Parsing for Inputs ---
#     parser = argparse.ArgumentParser(description="Python script to mimic promptflow DAG.")
#     parser.add_argument("--repo_local_path", type=str, required=True, help="Local path to the repository.")
#     # parser.add_argument("--GEMINI_API_KEY", type=str, default=os.environ.get("GEMINI_API_KEY", ""), help="Gemini API Key")
#     # parser.add_argument("--ANTHROPIC_API_KEY", type=str, default=os.environ.get("ANTHROPIC_API_KEY", ""), help="Anthropic API Key")
#     # parser.add_argument("--OPENAI_API_KEY", type=str, default=os.environ.get("OPENAI_API_KEY", ""), help="OpenAI API Key")
    
#     args = parser.parse_args()

#     # --- Run the flow ---
#     # Set API keys in environment if provided via args and not already set,
#     # so tools that read from env vars can access them.
#     # if args.GEMINI_API_KEY: os.environ["GEMINI_API_KEY"] = args.GEMINI_API_KEY
#     # if args.ANTHROPIC_API_KEY: os.environ["ANTHROPIC_API_KEY"] = args.ANTHROPIC_API_KEY
#     # if args.OPENAI_API_KEY: os.environ["OPENAI_API_KEY"] = args.OPENAI_API_KEY

#     results = run_flow(
#         repo_local_path=args.repo_local_path,
#         gemini_api_key=gemini_api_key,
#         anthropic_api_key=anthropic_api_key,
#         openai_api_key=openai_api_key,
#         trace_id=generate_trace_id()
#     )

#     # --- Print Outputs ---
#     print("\n--- Final Outputs ---")
#     for key, value in results.items():
#         print(f"{key}:")
#         # Truncate long outputs for display
#         value_str = str(value)
#         if len(value_str) > 300:
#             print(f"{value_str[:300]}...")
#         else:
#             print(value_str)
#         print("-" * 20)

#     # Example: Save outputs to files if needed
#     # output_dir = Path("flow_outputs")
#     # output_dir.mkdir(exist_ok=True)
#     # with open(output_dir / "documentation.txt", "w") as f:
#     #     f.write(results.get("documentation", ""))
#     # with open(output_dir / "documentation.md", "w") as f:
#     #     f.write(results.get("documentation_md", ""))
#     # with open(output_dir / "config.json", "w") as f:
#     #     f.write(results.get("config", ""))
#     # print(f"Outputs saved to {output_dir.resolve()}")





import os
import sys
import argparse
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import dotenv

# Assuming these imports are still necessary for the tools themselves
# These will be called by our Tool classes
from tools.llmclassifier import llmclassifier
from tools.descriptor import summerizer
# This import will be handled in the main section or by the App class
# from src.utils.utils import generate_trace_id

class Config:
    """
    Manages configuration settings like API keys and directory paths.
    """
    def __init__(self, env_file: Path = None):
        if env_file:
            dotenv.load_dotenv(env_file)
        else:
            dotenv.load_dotenv()

        self.gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
        self.anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
        self.openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

        # --- Constants based on your flow.dag.yaml ---
        # Assuming the script is run from the directory containing flow.dag.yaml
        # or a similar root where 'prompts' and 'tools' are subdirectories.
        self.base_dir: Path = Path(__file__).parent.resolve()
        self.prompt_dir: Path = self.base_dir / "prompts" # Default, can be overridden
        self.tool_dir: Path = self.base_dir / "tools"
        self.src_dir_relative_to_flow: Path = Path("../src") # Relative to where flow.dag.yaml is

        # Resolve src_path for sys.path modification
        # This assumes the script is in the same directory as flow.dag.yaml
        self.src_path_to_add: Path = (self.base_dir / self.src_dir_relative_to_flow).resolve()

    def setup_env_vars_for_promptflow(self):
        """Sets environment variables typically used by Promptflow/Langchain."""
        os.environ["PROMPTFLOW_NAME"] = "file_classifier"
        os.environ["PF_DISABLE_TRACING"] = "true"
        os.environ["LANG_DISABLE_TRACING"] = "true"

    def add_paths_to_sys(self):
        """Adds necessary paths to sys.path for imports."""
        # Add current script's directory for relative imports like `from tools import ...`
        if str(self.base_dir) not in sys.path:
            sys.path.insert(0, str(self.base_dir))
            print(f"[INFO] Added to sys.path: {self.base_dir}")

        # Add the resolved src_path
        if str(self.src_path_to_add) not in sys.path:
            sys.path.insert(0, str(self.src_path_to_add))
            print(f"[INFO] Added to sys.path: {self.src_path_to_add}")


class TemplateManager:
    """
    Handles loading and rendering of Jinja2 templates.
    """
    def __init__(self, default_template_dir: Path):
        self.default_template_dir = default_template_dir

    def load_template(self, template_relative_path: str, context: dict = None) -> str:
        """
        Loads and renders a Jinja2 template.
        template_relative_path is relative to the default_template_dir.
        """
        if context is None:
            context = {}

        # template_relative_path is like 'system_prompt_classification.jinja2'
        # or 'prompt_docstrings/system_prompt_classification.jinja2'
        full_template_path = self.default_template_dir / template_relative_path
        
        template_dir = full_template_path.parent
        template_file = full_template_path.name

        if not full_template_path.exists():
            raise FileNotFoundError(f"Template file not found: {full_template_path}")

        env = Environment(loader=FileSystemLoader(searchpath=str(template_dir)))
        template = env.get_template(template_file)
        return template.render(context)


class BaseTool:
    """
    Base class for tools, potentially defining a common interface.
    """
    def __init__(self, config: Config):
        self.config = config

    def execute(self, *args, **kwargs):
        raise NotImplementedError("Each tool must implement the execute method.")


class LLMClassifierTool(BaseTool):
    """
    Tool for classifying files using an LLM.
    """
    def execute(self, system_prompt: str, user_prompt: str, folder_path: str,
                max_workers: int, trace_id: str) -> dict:
        print(f"[INFO] Calling LLMClassifierTool with folder_path: {folder_path}")
        
        output = llmclassifier(
            symstem_prompt=system_prompt, # Note: original script had a typo "symstem_prompt"
            user_prompt=user_prompt,
            folder_path=folder_path,
            max_workers=max_workers,
            GEMINI_API_KEY=self.config.gemini_api_key,
            ANTHROPIC_API_KEY=self.config.anthropic_api_key,
            OPENAI_API_KEY=self.config.openai_api_key,
            trace_id=trace_id
        )
        print(f"LLMClassifierTool output: {str(output)[:200]}...")
        return output


class DescriptorTool(BaseTool):
    """
    Tool for generating documentation/descriptors for classified files.
    """
    def execute(self, classified_files: dict,
                system_prompt_config: str, user_prompt_config: str,
                system_prompt_docstring: str, user_prompt_docstring: str,
                system_prompt_documentation: str, user_prompt_documentation: str,
                trace_id: str) -> dict:
        print(f"[INFO] Calling DescriptorTool with classified_files keys: {list(classified_files.keys()) if isinstance(classified_files, dict) else 'N/A'}")
        
        output = summerizer(
            classified_files=classified_files,
            system_prompt_config=system_prompt_config,
            user_prompt_config=user_prompt_config,
            system_prompt_docstring=system_prompt_docstring,
            user_prompt_docstring=user_prompt_docstring,
            system_prompt_documentation=system_prompt_documentation,
            user_prompt_documentation=user_prompt_documentation,
            GEMINI_API_KEY=self.config.gemini_api_key,
            ANTHROPIC_API_KEY=self.config.anthropic_api_key,
            OPENAI_API_KEY=self.config.openai_api_key,
            trace_id=trace_id
        )
        print(f"DescriptorTool output: {str(output)[:200]}...")
        return output


class DocumentationFlow:
    """
    Orchestrates the documentation generation flow.
    """
    def __init__(self, config: Config):
        self.config = config
        # The prompt_dir for TemplateManager should be the one specified in flow.dag.yaml
        # which seems to be 'file_classification/prompts' relative to where prompts are.
        # Let's assume 'prompts' in Config is the root for all prompt types.
        # The original script uses "file_classification/prompts/..."
        # So, the TemplateManager base should be self.config.prompt_dir / "file_classification"
        # Or, we adjust the paths passed to load_template.
        # Let's adjust paths passed to load_template for clarity.
        self.template_manager = TemplateManager(default_template_dir=self.config.base_dir) # base_dir of the script
        self.classifier_tool = LLMClassifierTool(config)
        self.descriptor_tool = DescriptorTool(config)

        # Define prompt paths relative to the script's location (or a configured prompt root)
        # The original script had paths like "file_classification/prompts/system_prompt_classification.jinja2"
        # This implies a structure:
        # <script_dir>/
        #   file_classification/
        #     prompts/
        #       system_prompt_classification.jinja2
        #       ...
        # If PROMPT_DIR in the original script was "prompts", then the paths were relative to that.
        # Let's assume the paths passed to load_jinja_template were relative to the script's CWD at execution.
        # For robustness, we'll make them relative to a known base (e.g., script's dir or config.prompt_dir)

        # The original script used paths like "file_classification/prompts/..."
        # If self.config.prompt_dir is "prompts", then the relative path for the template manager
        # would be "file_classification/system_prompt_classification.jinja2"
        # Let's assume the `load_jinja_template` in the original script expected paths
        # relative to the CWD, and that CWD contained `file_classification/prompts/...`
        # For the TemplateManager, we'll pass paths relative to its `default_template_dir`.
        # If `default_template_dir` is `Path("prompts")`, then paths like `system_prompt_classification.jinja2` are fine.
        # The original script's `load_jinja_template` resolved `template_path.parent` as `template_dir`.
        # If `template_path` was `prompts/system_prompt_classification.jinja2`, then `template_dir` was `prompts`.
        # This means `FileSystemLoader` was initialized with `searchpath='prompts'`.
        # So, `TemplateManager` should be initialized with `config.prompt_dir`.
        # And the paths passed to `load_template` should be relative to that `prompt_dir`.

        # Re-evaluating TemplateManager initialization:
        # Original: load_jinja_template("file_classification/prompts/system_prompt_classification.jinja2")
        # This implies that the CWD or a search path allows finding "file_classification/prompts/..."
        # If we set TemplateManager's base to `Path(".")` (current dir) or `self.config.base_dir`,
        # then the paths passed to `load_template` must be the full "file_classification/prompts/..."
        # This seems most consistent with the original.

        self.prompts_config = {
            "system_classification": "file_classification/prompts/system_prompt_classification.jinja2",
            "user_classification": "file_classification/prompts/user_prompt_classification.jinja2",
            "system_docstring": "file_classification/prompts/prompt_docstrings/system_prompt_classification.jinja2",
            "user_docstring": "file_classification/prompts/prompt_docstrings/user_prompt_classification.jinja2",
            "system_configuration": "file_classification/prompts/prompt_configurations/system_prompt_configuration.jinja2",
            "user_configuration": "file_classification/prompts/prompt_configurations/user_prompt_configuration.jinja2",
            "system_documentation": "file_classification/prompts/prompt_documentations/system_prompt_documentation.jinja2",
            "user_documentation": "file_classification/prompts/prompt_documentations/user_prompt_documentation.jinja2",
        }


    def _load_prompts(self) -> dict:
        """Loads all necessary prompts."""
        print("[INFO] Loading prompts...")
        loaded_prompts = {}
        for key, path in self.prompts_config.items():
            try:
                loaded_prompts[key] = self.template_manager.load_template(path)
            except FileNotFoundError as e:
                print(f"[ERROR] Could not load prompt {key} from {path}: {e}")
                print(f"[DEBUG] TemplateManager base directory: {self.template_manager.default_template_dir.resolve()}")
                # Try to provide more context for debugging path issues
                abs_path_attempted = (self.template_manager.default_template_dir / path).resolve()
                print(f"[DEBUG] Absolute path attempted: {abs_path_attempted}")

                # Check if the path exists relative to common project structures
                script_dir = Path(__file__).parent.resolve()
                alt_path1 = script_dir / path
                print(f"[DEBUG] Checking alternative path: {alt_path1} (Exists: {alt_path1.exists()})")
                
                # If original PROMPT_DIR was "prompts"
                original_prompt_dir_root = script_dir / "prompts"
                alt_path2 = original_prompt_dir_root / Path(path).name # This might be too simplistic if path has subdirs
                # A better interpretation if PROMPT_DIR was "prompts":
                # The original `load_jinja_template` took "prompts/file.jinja2"
                # and set `template_dir` to "prompts".
                # If `self.template_manager.default_template_dir` is set to `script_dir / "prompts"`,
                # then the paths in `self.prompts_config` should be like "system_prompt_classification.jinja2"
                # or "prompt_docstrings/system_prompt_classification.jinja2"
                # Let's adjust `TemplateManager` initialization and prompt paths.

                # Re-adjusting:
                # If `Config.prompt_dir` is `base_dir / "prompts"`,
                # and `TemplateManager` is initialized with `Config.prompt_dir`.
                # Then paths like "file_classification/system_prompt_classification.jinja2"
                # would mean `base_dir / "prompts" / "file_classification" / "..."`
                # This doesn't match the original structure.

                # The original `load_jinja_template` took a path like `p = Path("prompts/system.jinja2")`.
                # Then `p.parent` ("prompts") was used as `searchpath`. `p.name` ("system.jinja2") was the template name.
                # This means `TemplateManager` should be initialized with `searchpath` for each load,
                # or it needs a more flexible way to handle subdirectories if `default_template_dir` is fixed.
                # The current `TemplateManager` implementation correctly uses `full_template_path.parent` as searchpath.
                # So, if `default_template_dir` is `Path(".")` or `script_dir`, then paths like
                # "file_classification/prompts/system_prompt_classification.jinja2" should work.

                raise  # Re-raise the exception after printing debug info
        print("[INFO] Prompts loaded.")
        return loaded_prompts

    def run(self, repo_local_path: str, trace_id: str) -> dict:
        """
        Orchestrates the flow.
        """
        print("--- Starting Flow Execution ---")
        print(f"[INFO] Current working directory: {os.getcwd()}")
        print(f"[INFO] Script base directory: {self.config.base_dir}")
        print(f"[INFO] Template manager base directory: {self.template_manager.default_template_dir.resolve()}")


        prompts = self._load_prompts()

        print("[INFO] Running file classifier...")
        file_classifier_output = self.classifier_tool.execute(
            system_prompt=prompts["system_classification"],
            user_prompt=prompts["user_classification"],
            folder_path=repo_local_path,
            max_workers=10,
            trace_id=trace_id
        )

        print("[INFO] Running documentation generation...")
        documentation_generation_output = self.descriptor_tool.execute(
            classified_files=file_classifier_output,
            system_prompt_config=prompts["system_configuration"],
            user_prompt_config=prompts["user_configuration"],
            system_prompt_docstring=prompts["system_docstring"],
            user_prompt_docstring=prompts["user_docstring"],
            system_prompt_documentation=prompts["system_documentation"],
            user_prompt_documentation=prompts["user_documentation"],
            trace_id=trace_id
        )

        final_outputs = documentation_generation_output
        print("--- Flow Execution Finished ---")
        return final_outputs


class App:
    """
    Application class to handle CLI, setup, and execution.
    """
    def __init__(self):
        self.config = Config()
        self.config.setup_env_vars_for_promptflow()
        self.config.add_paths_to_sys()

        # This import needs to happen after sys.path is modified
        try:
            from src.utils.utils import generate_trace_id
            self.generate_trace_id = generate_trace_id
        except ImportError as e:
            print(f"[ERROR] Could not import generate_trace_id from src.utils.utils: {e}")
            print("[INFO] Ensure 'src' directory is correctly placed relative to the script or in PYTHONPATH.")
            print(f"[DEBUG] sys.path: {sys.path}")
            # Fallback if import fails, so the script can still attempt to run
            import uuid
            self.generate_trace_id = lambda: str(uuid.uuid4())
            print("[WARNING] Using fallback UUID for trace_id generation.")


        self.flow = DocumentationFlow(self.config)

    def run_from_cli(self):
        parser = argparse.ArgumentParser(description="Python script to mimic promptflow DAG.")
        parser.add_argument("--repo_local_path", type=str, required=True, help="Local path to the repository.")
        # API keys are now handled by Config via .env
        args = parser.parse_args()

        results = self.flow.run(
            repo_local_path=args.repo_local_path,
            trace_id=self.generate_trace_id()
        )

        self._print_results(results)
        self._save_results(results) # Optional: if you want to save

    def _print_results(self, results: dict):
        print("\n--- Final Outputs ---")
        if results: # Check if results is not None
            for key, value in results.items():
                print(f"{key}:")
                value_str = str(value)
                if len(value_str) > 300:
                    print(f"{value_str[:300]}...")
                else:
                    print(value_str)
                print("-" * 20)
        else:
            print("No results were generated.")


    def _save_results(self, results: dict, output_dir_name: str = "flow_outputs"):
        if not results:
            print("[INFO] No results to save.")
            return

        output_dir = self.config.base_dir / output_dir_name
        output_dir.mkdir(exist_ok=True)

        # Example: Save outputs to files if needed
        # These keys depend on what `descriptor_tool_function` (now `DescriptorTool.execute`) returns
        # Assuming it returns a dictionary with keys like 'documentation', 'documentation_md', 'config'
        if "documentation" in results:
            with open(output_dir / "documentation.txt", "w", encoding="utf-8") as f:
                f.write(str(results.get("documentation", "")))
        if "documentation_md" in results:
            with open(output_dir / "documentation.md", "w", encoding="utf-8") as f:
                f.write(str(results.get("documentation_md", "")))
        if "config" in results: # Assuming 'config' here means some generated configuration string/JSON
            with open(output_dir / "config.json", "w", encoding="utf-8") as f:
                f.write(str(results.get("config", "")))
        print(f"[INFO] Outputs potentially saved to {output_dir.resolve()}")


if __name__ == "__main__":
    # Create a dummy .env file for testing if it doesn't exist
    if not Path(".env").exists():
        print("[INFO] Creating a dummy .env file. Please populate it with your API keys.")
        with open(".env", "w") as f:
            f.write("GEMINI_API_KEY=\n")
            f.write("ANTHROPIC_API_KEY=\n")
            f.write("OPENAI_API_KEY=\n")

    # Create dummy tools and prompts structure for the script to run without FileNotFoundError
    # This is for demonstration; in a real setup, these files would exist.
    
    # Dummy tools
    tools_dir = Path(__file__).parent / "tools"
    tools_dir.mkdir(exist_ok=True)
    (tools_dir / "__init__.py").touch(exist_ok=True)
    if not (tools_dir / "llmclassifier.py").exists():
        (tools_dir / "llmclassifier.py").write_text(
            "def llmclassifier(*args, **kwargs):\n"
            "    print('[DUMMY TOOL] llmclassifier called with:', kwargs.get('folder_path'))\n"
            "    return {'classified_file1.py': 'python', 'classified_file2.txt': 'text'}\n"
        )
    if not (tools_dir / "descriptor.py").exists():
        (tools_dir / "descriptor.py").write_text(
            "def summerizer(*args, **kwargs):\n"
            "    print('[DUMMY TOOL] summerizer called with keys:', list(kwargs.get('classified_files', {}).keys()))\n"
            "    return {'documentation': 'Dummy docs', 'documentation_md': '# Dummy MD', 'config': '{\"dummy_key\": \"dummy_value\"}'}\n"
        )

    # Dummy prompts
    # Path structure: file_classification/prompts/...
    fc_prompts_dir = Path(__file__).parent / "file_classification" / "prompts"
    fc_prompts_dir.mkdir(parents=True, exist_ok=True)
    (fc_prompts_dir.parent / "__init__.py").touch(exist_ok=True) # For file_classification package
    (fc_prompts_dir / "__init__.py").touch(exist_ok=True) # For prompts package

    prompt_paths_to_create = [
        "system_prompt_classification.jinja2",
        "user_prompt_classification.jinja2",
        "prompt_docstrings/system_prompt_classification.jinja2",
        "prompt_docstrings/user_prompt_classification.jinja2",
        "prompt_configurations/system_prompt_configuration.jinja2",
        "prompt_configurations/user_prompt_configuration.jinja2",
        "prompt_documentations/system_prompt_documentation.jinja2",
        "prompt_documentations/user_prompt_documentation.jinja2",
    ]
    for p_path_str in prompt_paths_to_create:
        p_path = fc_prompts_dir / p_path_str
        p_path.parent.mkdir(parents=True, exist_ok=True)
        if not p_path.exists():
            p_path.write_text(f"This is a dummy prompt for {p_path.name}")

    # Dummy src/utils/utils.py
    src_utils_dir = Path(__file__).parent / "../src/utils" # As per SRC_DIR_RELATIVE_TO_FLOW
    src_utils_dir.mkdir(parents=True, exist_ok=True)
    (src_utils_dir.parent.parent / "__init__.py").touch(exist_ok=True) # For src package
    (src_utils_dir.parent / "__init__.py").touch(exist_ok=True) # For src/utils package
    if not (src_utils_dir / "utils.py").exists():
        (src_utils_dir / "utils.py").write_text(
            "import uuid\n"
            "def generate_trace_id():\n"
            "    return str(uuid.uuid4())\n"
        )
    
    # Create a dummy repo path for testing
    dummy_repo_path = Path(__file__).parent / "dummy_repo"
    dummy_repo_path.mkdir(exist_ok=True)
    (dummy_repo_path / "sample_code.py").write_text("print('hello world')")


    app = App()
    # To run with CLI args, you would execute this script from terminal:
    # python your_script_name.py --repo_local_path ./dummy_repo
    # For direct execution in an IDE or for testing:
    if len(sys.argv) == 1: # No CLI args provided
        print("[INFO] No CLI arguments provided, running with dummy repo_local_path for testing.")
        sys.argv.append("--repo_local_path")
        sys.argv.append(str(dummy_repo_path)) # Use the dummy repo path

    app.run_from_cli()