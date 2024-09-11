import os
import datetime


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


def process_folder(folder_path, output_file, file_extensions=None, ignore_folders=None):
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

    with open(output_file, 'w', encoding='utf-8', errors="ignore") as outfile:
        outfile.write("<file_overview>\n")
        outfile.write(f"Total files: {len(all_files)}\n")
        outfile.write(f"Date generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        if file_extensions:
            outfile.write(f"File types included: {', '.join(file_extensions)}\n")
        outfile.write("Folder Structure:\n")
        folder_tree = create_folder_tree(folder_path, file_extensions, ignore_folders)
        outfile.write(folder_tree)
        outfile.write("\nFiles included:\n")
        for file_path in all_files:
            relative_path = os.path.relpath(file_path, folder_path)
            outfile.write(f"- {relative_path}\n")
        outfile.write("</file_overview>\n\n")

        for file_path in all_files:
            try:
                relative_path = os.path.relpath(file_path, folder_path)
                file_stats = os.stat(file_path)
                file_size = file_stats.st_size
                mod_time = datetime.datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')

                outfile.write(f'<file path="{relative_path}" size="{file_size}" modified="{mod_time}">\n')

                with open(file_path, 'r', encoding='utf-8', errors="ignore") as infile:
                    content = infile.read()

                outfile.write(content.strip())
                outfile.write("\n</file>\n\n")
            except Exception as e:
                print(f"Error reading file '{file_path}': {str(e)}")

    print(f"All{'specified' if file_extensions else ''} files have been processed and combined into '{output_file}'.")
