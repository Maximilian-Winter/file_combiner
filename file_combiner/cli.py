import argparse
from .combiner import process_folder

def main():
    parser = argparse.ArgumentParser(description="Process files in a folder and generate an output file.")
    parser.add_argument("folder_path", help="Path to the folder to process")
    parser.add_argument("--output", default="output.txt", help="Name of the output file (default: output.txt)")
    parser.add_argument("--extensions", nargs="*", help="File extensions to include (e.g., .h .cpp)")
    parser.add_argument("--ignore", nargs="*", default=['.git', 'node_modules', '__pycache__'],
                        help="Folders to ignore (default: ['.git', 'node_modules', '__pycache__'])")
    parser.add_argument("--add-line-numbers", action="store_true", help="Add line numbers to the content of each file")
    parser.add_argument("--mode", choices=["xml", "markdown", "custom"], default="xml",
                        help="Output mode: xml, markdown, or custom (default: xml)")
    parser.add_argument("--custom-output-template", help="Path to custom output template file (required if mode is custom)")
    parser.add_argument("--custom-file-template", help="Path to custom file content template file (required if mode is custom)")

    args = parser.parse_args()

    if args.mode == "custom" and (not args.custom_output_template or not args.custom_file_template):
        parser.error("Custom mode requires both --custom-output-template and --custom-file-template")

    process_folder(args.folder_path, args.output, args.extensions, args.ignore, args.add_line_numbers,
                   args.mode, args.custom_output_template, args.custom_file_template)

if __name__ == '__main__':
    main()