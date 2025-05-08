import os
import ast
from typing import List, Dict, Any
from dataclasses import dataclass
import uuid



def generate_trace_id() -> str:
    """Generate a random unique trace ID suitable for use with Langfuse."""
    return str(uuid.uuid4())



@dataclass
class FunctionInfo:
    """Classe pour stocker les informations d'une fonction."""

    name: str
    description: str


@dataclass
class FileInfo:
    """Classe pour stocker les informations d'un fichier."""

    file_name: str
    file_path: str
    functions: List[Dict[str, str]]


class FunctionVisitor(ast.NodeVisitor):
    """Visiteur AST pour extraire les informations des fonctions."""

    def __init__(self):
        self.functions = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Visite chaque définition de fonction dans l'AST."""
        # Extraction de la docstring
        docstring = ast.get_docstring(node) or "Pas de description disponible"

        function_info = {
            "function_name": node.name,
            "function_description": docstring.strip(),
        }

        self.functions.append(function_info)

        # Continue la visite pour les fonctions imbriquées
        self.generic_visit(node)


def analyze_python_file(file_path: str) -> List[Dict[str, str]]:
    """Analyse un fichier Python et retourne les informations sur ses fonctions."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Parse le contenu en AST
        tree = ast.parse(content)

        # Visite l'AST pour extraire les informations
        visitor = FunctionVisitor()
        visitor.visit(tree)

        return visitor.functions

    except Exception as e:
        print(f"Erreur lors de l'analyse de {file_path}: {str(e)}")
        return []


def analyze_codebase(directory_path: str) -> List[Dict[str, Any]]:
    """
    Analyse un dossier et retourne les informations sur toutes les fonctions Python.

    Args:
        directory_path (str): Chemin vers le dossier à analyser

    Returns:
        List[Dict]: Liste de dictionnaires contenant les informations sur les fichiers
                   et leurs fonctions selon la structure demandée
    """
    code_base = []

    # Parcours récursif du dossier
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            # Ne traite que les fichiers Python
            if not file_name.endswith(".py"):
                continue

            file_path = os.path.join(root, file_name)

            # Analyse le fichier
            functions = analyze_python_file(file_path)

            # Si des fonctions ont été trouvées, ajoute les informations du fichier
            if functions:
                file_info = {
                    "file_name": file_name,
                    "file_path": file_path,
                    "functions": functions,
                }
                code_base.append(file_info)

    return code_base


"""results = analyze_codebase("./mon_dossier")

# Affichage des résultats
for file_info in results:
    print(f"\nFichier: {file_info['file_name']}")
    print(f"Chemin: {file_info['file_path']}")
    print("Fonctions:")
    for func in file_info['functions']:
        print(f"\t- {func['function_name']}")
        print(f"\t  Description: {func['function_description']}")"""

# tu peux aussi juste afficher results après l'avoir run


def classify_file(file_name):
    # Extract file extension
    _, extension = os.path.splitext(file_name.lower())

    # Define file type mappings
    code_extensions = [
        ".py",
        ".java",
        ".cpp",
        ".js",
        ".html",
        ".css",
        ".php",
        ".rb",
        ".go",
        ".swift",
    ]
    doc_extensions = [".txt", ".doc", ".docx", ".pdf", ".md", ".rtf"]
    config_extensions = [".json", ".xml", ".yaml", ".yml", ".ini", ".cfg", ".conf"]

    # Classify based on extension
    if extension in code_extensions:
        return "code_file"
    elif extension in doc_extensions:
        return "doc_file"
    elif extension in config_extensions:
        return "configuration_file"
    else:
        return "other"


import os

# List of patterns to ignore
ignore_list = [
    "pycache",
    ".gitignore",
    ".md",
    ".ipynb",
    "venv",
    ".git",
    ".idea",
    "node_modules",
    "build",
    "dist",
    "target",
    ".vscode",
    ".DS_Store",
    ".mypy_cache",
    ".pytest_cache",
    "__init__.py",  # Corrected from "init.py"
    ".txt",
    ".log",
    ".aux",
    ".bbl",
    ".blg",
    ".fdb_latexmk",
    ".fls",
    ".lof",
    ".lot",
    ".out",
    ".toc",
    ".synctex.gz",
    ".egg-info",
    ".coverage",
    ".pytest_cache",
    ".ropeproject",
    ".ipynb_checkpoints",
    ".env",
    ".venv",
    "npm-debug.log",
    "yarn-error.log",
    ".pylintrc",
    ".cache",
    ".settings",
    ".classpath",
    ".project",
    ".metadata",
    "tags",
    "release",
    "debug",
    "bin",
    "obj",
    ".swp",  # Vim swap files
    "~",  # Emacs backup files
    ".swo",  # Vim undo files
    ".swn",  # Vim swap files (alternative)
    ".bak",  # Backup files
    ".tmp",  # Temporary files
    ".orig",  # Original files (often backups)
    ".rej",  # Patch rejection files
    ".lock",  # Lock files (various uses)
    ".log",  # Log files
    ".pdf",  # PDF documents
    ".doc",  # Word documents
    ".docx",  # Word documents (newer format)
    ".xls",  # Excel spreadsheets
    ".xlsx",  # Excel spreadsheets (newer format)
    ".ppt",  # PowerPoint presentations
    ".pptx",  # PowerPoint presentations (newer format)
    ".zip",  # Compressed archives
    ".tar",  # Tape archives
    ".gz",  # Gzip compressed files
    ".rar",  # RAR archives
    ".7z",  # 7-Zip archives
    ".dmg",  # macOS disk images
    ".iso",  # Disk image files
    ".exe",  # Executable files (Windows)
    ".dll",  # Dynamic link libraries (Windows)
    ".app",  # macOS application bundles
    ".pkg",  # macOS installer packages
    ".db",  # Database files (various types)
    ".sqlite",  # SQLite database files
    ".csv",  # Comma-separated value files
    ".json",  # JSON data files
    ".xml",  # XML data files
    ".yaml",  # YAML data files
    ".yml",  # YAML data files (alternative extension)
    ".cfg",  # Configuration files
    ".conf",  # Configuration files (alternative extension)
    ".ini",  # Initialization files
    ".pem",  # Privacy-enhanced mail files (often keys)
    ".crt",  # Certificate files
    ".key",  # Key files
    ".pfx",  # Personal Information Exchange files
    ".jks",  # Java KeyStore files
    ".dat",  # Data files (generic)
    ".bin",  # Binary files (generic)
    ".dump",  # Database or memory dumps
    ".sql",  # SQL scripts
    ".bak",  # Backup files (various types)
    ".old",  # Old versions of files
    ".draft",  # Draft documents
    ".media",  # Media files (generic)
    ".assets",  # Assets files (generic)
    ".resources",  # Resource files (generic)
    ".snap",  # Snapshots (various uses)
    ".image",  # Image files (generic)
    ".backup",  # Backup files (explicit)
    ".temp",  # Temporary files (alternative)
    ".download",  # Downloaded files (incomplete)
    ".part",  # Partially downloaded files
    ".crdownload",  # Chrome download files (incomplete)
    ".unconfirmed",  # Unconfirmed download files
    ".incomplete",  # Incomplete files
    ".journal",  # Journal files (various uses)
    ".fuse_hidden",  # Hidden files related to FUSE mounts
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".tiff",
    ".svg",
    ".mp3",
    ".wav",
    ".srt",
    ".flac",
    ".aac",
    ".ogg",
    ".wma",
    ".mp4",
    ".avi",
    ".mkv",
    ".mov",
    ".wmv",
    ".flv",
    ".m4v",
    ".webm",
    ".m2ts",
    ".mts",
    ".3gp",
    ".m4a",
    ".aif",
    ".aiff",
    ".raw",
    ".psd",
    ".ai",
    ".eps",
    ".indd",
    ".blend",
    ".max",
    ".ma",
    ".mb",
    ".3ds",
    ".obj",
    ".fbx",
    ".dae",
    ".stl",
    ".wrl",
    ".x3d",
    ".ttf",
]


def has_file_extension(filename):
    """
    Check if a file has an extension.

    Args:
        filename (str): Name of the file to check

    Returns:
        bool: True if the file has an extension, False otherwise
    """
    return "." in filename and filename.rsplit(".", 1)[1].strip() != ""


def should_process_file(filepath):
    """
    Determine if a file should be processed based on ignore list and extension presence.

    Args:
        filepath (str): Full path of the file to check

    Returns:
        bool: True if the file should be processed, False otherwise
    """
    filename = os.path.basename(filepath)

    # Check if file matches any pattern in ignore list
    if any(forbidden in filepath for forbidden in ignore_list):
        return False

    # Check if file has an extension
    if not has_file_extension(filename):
        return False

    return True


def list_all_files(folder_path: str, include_md: bool) -> Dict[str, List[str]]:
    """
    Lists all valid files in the given folder and its subdirectories.

    Args:
        folder_path (str): Path to the folder to be analyzed.

    Returns:
        dict: A dictionary containing two lists:
              - 'all_files_with_path': Full paths of all valid files
              - 'all_files_no_path': A list of dictionaries, each with keys
                                    'file_name' and 'file_id'

    Raises:
        FileNotFoundError: If the folder_path doesn't exist
    """
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The path {folder_path} does not exist")

    # Initialize lists to store file paths and names
    all_files_with_path = []
    all_files_no_path = []

    # Remove .md from ignore list if include_md is True
    if include_md:
        if ".md" in ignore_list:
            ignore_list.remove(".md")
        if ".yaml" in ignore_list:
            ignore_list.remove(".yaml")
        if ".yml" in ignore_list:
            ignore_list.remove(".yml")

    try:
        for root, _, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)

                if should_process_file(full_path) and "env_arxflix" not in full_path:
                    all_files_with_path.append(full_path)
                    all_files_no_path.append(
                        {"file_name": file, "file_id": len(all_files_with_path) - 1}
                    )

        return {
            "all_files_with_path": all_files_with_path,
            "all_files_no_path": all_files_no_path,
        }

    except Exception as e:
        raise Exception(f"Error while processing files: {str(e)}")
