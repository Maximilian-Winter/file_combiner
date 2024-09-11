import os
import datetime
import math
from .combiner_template import CombinerTemplate


# Template for the overall output file
XML_OUTPUT_TEMPLATE = """<file_overview>
Total files: {TOTAL_FILES}
Date generated: {DATE_GENERATED}
Folder Structure:
{FOLDER_TREE}

Files included:
{FILES_INCLUDED}
</file_overview>

{FILE_CONTENTS}"""

# Template for individual file content
XML_FILE_TEMPLATE = """<file path="{FILE_PATH}" lines="{LINES_COUNT}" modified="{MODIFIED_TIME}">
{FILE_CONTENT}
</file>

"""

# Template for the overall output file
MARKDOWN_OUTPUT_TEMPLATE = """# File Overview

- **Total files:** {TOTAL_FILES}
- **Date generated:** {DATE_GENERATED}

## Folder Structure

```
{FOLDER_TREE}
```

## Files Included

{FILES_INCLUDED}

---

{FILE_CONTENTS}
"""

# Template for individual file content
MARKDOWN_FILE_TEMPLATE = """## {FILE_NAME}

- **Path:** `{FILE_PATH}`
- **Lines:** {LINES_COUNT}
- **Modified:** {MODIFIED_TIME}

```
{FILE_CONTENT}
```

---

"""

def is_last_item(current_index, contents, path, file_extensions):
    """Check if the current item is the last visible item in the directory."""
    for i in range(current_index + 1, len(contents)):
        item_path = os.path.join(path, contents[i])
        if os.path.isdir(item_path):
            return False
        if file_extensions is None or any(contents[i].endswith(ext) for ext in file_extensions):
            return False
    return True


def create_folder_tree(path, file_extensions=None, ignore_folders=None, prefix=''):
    if ignore_folders is None:
        ignore_folders = []

    tree = ''
    contents = os.listdir(path)
    contents.sort(key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower()))
    contents = [item for item in contents if item not in ignore_folders]

    for i, item in enumerate(contents):
        item_path = os.path.join(path, item)
        is_last = is_last_item(i, contents, path, file_extensions)

        if os.path.isdir(item_path):
            tree += f"{prefix}{'└── ' if is_last else '├── '}{item}/\n"
            extended_prefix = prefix + ('    ' if is_last else '│   ')
            tree += create_folder_tree(item_path, file_extensions, ignore_folders, extended_prefix)
        elif file_extensions is None or any(item.endswith(ext) for ext in file_extensions):
            tree += f"{prefix}{'└── ' if is_last else '├── '}{item}\n"

    return tree



# XML and Markdown templates remain the same

def process_folder(folder_path, output_file, file_extensions=None, ignore_folders=None, add_line_numbers=False,
                   mode="xml", custom_output_template=None, custom_file_template=None):
    if not os.path.isdir(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return

    if ignore_folders is None:
        ignore_folders = []

    all_files = []
    for root, _, files in os.walk(folder_path):
        if any(ignored in root.split(os.sep) for ignored in ignore_folders):
            continue
        for filename in files:
            if file_extensions is None or any(filename.endswith(ext) for ext in file_extensions):
                all_files.append(os.path.join(root, filename))

    all_files.sort()

    if mode.lower() == "xml":
        output_template = CombinerTemplate(template_string=XML_OUTPUT_TEMPLATE)
        file_template = CombinerTemplate(template_string=XML_FILE_TEMPLATE)
    elif mode.lower() == "markdown":
        output_template = CombinerTemplate(template_string=MARKDOWN_OUTPUT_TEMPLATE)
        file_template = CombinerTemplate(template_string=MARKDOWN_FILE_TEMPLATE)
    elif mode.lower() == "custom":
        if not custom_output_template or not custom_file_template:
            raise ValueError("Custom mode requires both custom output and file templates.")
        output_template = CombinerTemplate.from_file(custom_output_template)
        file_template = CombinerTemplate.from_file(custom_file_template)
    else:
        raise ValueError(f"Invalid mode: {mode}. Choose 'xml', 'markdown', or 'custom'.")

    with open(output_file, 'w', encoding='utf-8', errors="ignore") as outfile:
        folder_tree = create_folder_tree(folder_path, file_extensions, ignore_folders)
        files_included = "\n".join(f"- {os.path.relpath(f, folder_path)}" for f in all_files)

        all_file_contents = []
        for file_path in all_files:
            relative_path = os.path.relpath(file_path, folder_path)
            file_stats = os.stat(file_path)
            mod_time = datetime.datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')

            with open(file_path, 'r', encoding='utf-8', errors="ignore") as infile:
                content = infile.readlines()
            line_count = len(content)
            if add_line_numbers:
                line_number_width = len(str(len(content)))
                numbered_content = [f"{i+1:<{line_number_width}}| {line}" for i, line in enumerate(content)]
                formatted_content = "".join(numbered_content)
            else:
                formatted_content = "".join(content)

            file_content = file_template.generate_output_file_content(
                FILE_PATH=relative_path,
                FILE_NAME=os.path.basename(file_path),
                LINES_COUNT=line_count,
                MODIFIED_TIME=mod_time,
                FILE_CONTENT=formatted_content.rstrip()
            )
            all_file_contents.append(file_content)

        output_content = output_template.generate_output_file_content(
            TOTAL_FILES=len(all_files),
            DATE_GENERATED=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            FOLDER_TREE=folder_tree.strip(),
            FILES_INCLUDED=files_included,
            FILE_CONTENTS="".join(all_file_contents)
        )

        outfile.write(output_content)

    print(f"All files have been processed and combined into '{output_file}' using {mode} mode.")

# Example usage:
# process_folder("/path/to/folder", "output.txt", file_extensions=[".py", ".txt"], ignore_folders=[".git", "venv"],
#                add_line_numbers=True, mode="custom", custom_output_template="path/to/output_template.txt",
#                custom_file_template="path/to/file_template.txt")

# Example usage:
# process_folder("/path/to/folder", "output.txt", file_extensions=[".py", ".txt"], ignore_folders=[".git", "venv"], add_line_numbers=True)
