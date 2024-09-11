# File Combiner

File Combiner is a Python package that processes files in a folder and combines them into a single output file, suitable for use with Large Language Models (LLMs).

## Installation

You can install File Combiner using pip:

```
pip install llm_file_combiner
```

## Usage

After installation, you can use the `file-combiner` command from anywhere in your terminal:

```
file-combiner /path/to/folder --output combined_output.txt --extensions .py .txt --ignore venv .git
```

### Arguments:

- `folder_path`: Path to the folder to process (required)
- `--output`: Name of the output file (default: output.txt)
- `--extensions`: File extensions to include (e.g., .py .txt)
- `--ignore`: Folders to ignore (e.g., git node_modules)(default: ['.git', 'node_modules', '__pycache__'])

## Example Usage

```
file-combiner example_folder
```
```
<file_overview>
Total files: 2
Date generated: 2024-09-11 19:46:15
Folder Structure:
├── main.py
└── readme.md

Files included:
- main.py
- readme.md
  </file_overview>

<file path="main.py" size="81" modified="2024-09-11 18:56:34">
def main():
    print("Hello, world!")

if __name__ == "__main__":
main()
</file>

<file path="readme.md" size="613" modified="2024-09-11 18:57:32">
# Hello World Python Script

This is a simple Python script that prints "Hello, world!" when run as the main script.

## Description

The script demonstrates the basic structure of a Python program and the use of the `if __name__ == "__main__":` idiom, which is a common pattern in Python scripts.

</file>

```

## License

This project is licensed under the MIT License.
