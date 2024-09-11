import argparse
from file_combiner.combiner import process_folder


def main():
    parser = argparse.ArgumentParser(description="Process files in a folder and generate an output file.")
    parser.add_argument("folder_path", help="Path to the folder to process")
    parser.add_argument("--output", default="output.txt", help="Name of the output file (default: output.txt)")
    parser.add_argument("--extensions", nargs="*", help="File extensions to include (e.g., .h .cpp)")
    parser.add_argument("--ignore", nargs="*", default=['.git', 'node_modules', '__pycache__'],
                        help="Folders to ignore (default: ['.git', 'node_modules', '__pycache__'])")

    args = parser.parse_args()

    process_folder(args.folder_path, args.output, args.extensions, args.ignore)


if __name__ == '__main__':
    main()
