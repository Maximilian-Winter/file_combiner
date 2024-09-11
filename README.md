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
- `--ignore`: Folders to ignore (e.g., git node_modules) (default: ['.git', 'node_modules', '__pycache__'])
- `--add-line-numbers`: Add line numbers to the content of each file
- `--mode`: Output mode: xml, markdown, or custom (default: xml)
- `--custom-output-template`: Path to custom output template file (required if mode is custom)
- `--custom-file-template`: Path to custom file content template file (required if mode is custom)

## Example Usage

1. Basic usage with default XML mode:
```
file-combiner example_folder
```

2. Using Markdown mode with specific extensions and ignoring certain folders:
```
file-combiner example_folder --mode markdown --output combined_output.md --extensions .py .txt --ignore venv .git
```

3. Using custom templates:
```
file-combiner example_folder --mode custom --output custom_output.txt --custom-output-template my_output_template.txt --custom-file-template my_file_template.txt
```

## Template System

File Combiner uses a flexible template system to format the output. There are three built-in modes:

1. XML (default)
2. Markdown
3. Custom

### XML Mode

The XML mode uses predefined XML templates for the output structure and individual file content. The XML mode is the default mode. To use it explicitly:

```
file-combiner /path/to/folder --mode xml
```

### Markdown Mode

The Markdown mode uses predefined Markdown templates for the output structure and individual file content. To use Markdown mode:

```
file-combiner /path/to/folder --mode markdown --output combined_output.md
```

### Custom Mode

The custom mode allows you to provide your own templates for both the overall output structure and individual file content. To use custom mode:

```
file-combiner /path/to/folder --mode custom --custom-output-template path/to/output_template.txt --custom-file-template path/to/file_template.txt
```

#### Creating Custom Templates

Custom templates use placeholders that are replaced with actual content during processing. Here are the available placeholders:

For the output template:
- `{TOTAL_FILES}`: Total number of processed files
- `{DATE_GENERATED}`: Date and time when the output was generated
- `{FOLDER_TREE}`: Tree structure of the processed folder
- `{FILES_INCLUDED}`: List of processed files
- `{FILE_CONTENTS}`: Combined content of all processed files

For the file content template:
- `{FILE_PATH}`: Relative path of the file
- `{FILE_NAME}`: Name of the file
- `{LINES_COUNT}`: Number of lines in the file
- `{MODIFIED_TIME}`: Last modification time of the file
- `{FILE_CONTENT}`: Content of the file

Example custom output template:
```
# Folder Analysis

Processed on: {DATE_GENERATED}
Total files: {TOTAL_FILES}

## Folder Structure
```
{FOLDER_TREE}
```

## Files Included
{FILES_INCLUDED}

## File Contents
{FILE_CONTENTS}
```

Example custom file content template:
```
### {FILE_NAME}

- Path: `{FILE_PATH}`
- Lines: {LINES_COUNT}
- Modified: {MODIFIED_TIME}

```
{FILE_CONTENT}
```

```

## License

This project is licensed under the MIT License.