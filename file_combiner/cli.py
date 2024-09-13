import argparse
from .combiner import process_folder, create_folder_tree, create_file_list


def file_combiner_command(args):
    if args.mode == "custom" and (not args.custom_output_template or not args.custom_file_template):
        print("Custom mode requires both --custom-output-template and --custom-file-template")
        return

    process_folder(args.folder_path, args.output, args.extensions, args.ignore, args.add_line_numbers,
                   args.mode, args.custom_output_template, args.custom_file_template)


def folder_tree_command(args):
    tree = create_folder_tree(args.folder_path, args.extensions, args.ignore)
    with open(args.output, 'w', encoding='utf-8') as outfile:
        outfile.write(tree)
    print(f"Folder tree has been generated and saved to '{args.output}'.")


def file_list_command(args):
    tree = create_file_list(args.folder_path, args.extensions, args.ignore)
    with open(args.output, 'w', encoding='utf-8') as outfile:
        outfile.write(tree)
    print(f"Folder tree has been generated and saved to '{args.output}'.")


def file_combiner_main():
    parser = argparse.ArgumentParser(description="Process files in a folder and generate an output file.")
    parser.add_argument("folder_path", help="Path to the folder to process")
    parser.add_argument("--output", default="output.txt", help="Name of the output file (default: output.txt)")
    parser.add_argument("--extensions", nargs="*", help="File extensions to include (e.g., .h .cpp)")
    parser.add_argument("--ignore", nargs="*", default=['.git', 'node_modules', '__pycache__'],
                        help="Folders to ignore (default: ['.git', 'node_modules', '__pycache__'])")
    parser.add_argument("--add-line-numbers", action="store_true", help="Add line numbers to the content of each file")
    parser.add_argument("--mode", choices=["xml", "markdown", "custom"], default="xml",
                        help="Output mode: xml, markdown, or custom (default: xml)")
    parser.add_argument("--custom-output-template",
                        help="Path to custom output template file (required if mode is custom)")
    parser.add_argument("--custom-file-template",
                        help="Path to custom file content template file (required if mode is custom)")
    args = parser.parse_args()
    file_combiner_command(args)


def folder_tree_main():
    parser = argparse.ArgumentParser(description="Generate a folder tree")
    parser.add_argument("folder_path", help="Path to the folder to process")
    parser.add_argument("--output", default="folder_tree.txt",
                        help="Name of the output file (default: folder_tree.txt)")
    parser.add_argument("--extensions", nargs="*", help="File extensions to include (e.g., .h .cpp)")
    parser.add_argument("--ignore", nargs="*", default=['.git', 'node_modules', '__pycache__'],
                        help="Folders to ignore (default: ['.git', 'node_modules', '__pycache__'])")
    args = parser.parse_args()
    folder_tree_command(args)


def file_list_main():
    parser = argparse.ArgumentParser(description="Generate a file list")
    parser.add_argument("folder_path", help="Path to the folder to process")
    parser.add_argument("--output", default="file_list.txt",
                        help="Name of the output file (default: file_list.txt)")
    parser.add_argument("--extensions", nargs="*", help="File extensions to include (e.g., .h .cpp)")
    parser.add_argument("--ignore", nargs="*", default=['.git', 'node_modules', '__pycache__'],
                        help="Folders to ignore (default: ['.git', 'node_modules', '__pycache__'])")
    args = parser.parse_args()
    file_list_command(args)
