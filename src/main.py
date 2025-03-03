import argparse
import sys

from commands import (copy_file, delete_path, count_files, search_files, add_date_to_filenames, analyse_directory, )


def main():
    parser = argparse.ArgumentParser(description="File System Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Copy
    copy_parser = subparsers.add_parser("copy", help="Copy a file")
    copy_parser.add_argument("source", help="Source file path")
    copy_parser.add_argument("dest", help="Destination path")

    # Delete
    delete_parser = subparsers.add_parser("delete", help="Delete a file or directory")
    delete_parser.add_argument("path", help="Path to delete")

    # Count
    count_parser = subparsers.add_parser("count", help="Count files in a directory")
    count_parser.add_argument("path", help="Directory path")

    # Search
    search_parser = subparsers.add_parser("search", help="Search files by regex")
    search_parser.add_argument("path", help="Directory path")
    search_parser.add_argument("pattern", help="Regex pattern")

    # Add-date
    add_date_parser = subparsers.add_parser(
        "add-date", help="Add creation date to filenames"
    )
    add_date_parser.add_argument("path", help="File or directory path")
    add_date_parser.add_argument(
        "--recursive", action="store_true", help="Recursive processing"
    )

    # Analyse
    analyse_parser = subparsers.add_parser("analyse", help="Analyse directory sizes")
    analyse_parser.add_argument(
        "path", nargs="?", default=".", help="Directory path (default: current)"
    )

    args = parser.parse_args()

    try:
        if args.command == "copy":
            copy_file(args.source, args.dest)
        elif args.command == "delete":
            delete_path(args.path)
        elif args.command == "count":
            print(count_files(args.path))
        elif args.command == "search":
            for file in search_files(args.path, args.pattern):
                print(file)
        elif args.command == "add-date":
            add_date_to_filenames(args.path, args.recursive)
        elif args.command == "analyse":
            analyse_directory(args.path)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
def gui():
    import flet as ft
    from gui import main as gui_main
    ft.app(target=gui_main)

if __name__ == "__main__":
    main()
