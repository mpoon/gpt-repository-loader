"""
Parses a Git repository to extract file contents, while excluding ignored files and directories based on a .gptignore file. 

Iterates through the repository directory structure using os.walk(). Checks each file path against the ignore rules. Opens non-ignored files, reads the contents, and writes the file path and contents to the output file.
"""
#!/usr/bin/env python3

import os
import sys
import fnmatch

def get_ignore_list(ignore_file_path):
    ignore_list = []
    with open(ignore_file_path, 'r') as ignore_file:
        for line in ignore_file:
            if sys.platform == "win32":
                line = line.replace("/", "\\")
            ignore_list.append(line.strip())
    return ignore_list

def should_ignore(file_path, ignore_list):
    for pattern in ignore_list:
        if fnmatch.fnmatch(file_path, pattern):
            return True
    return False

def print_directory_structure(repo_path, ignore_list, output_file, level=0):
    if level == 0:
        output_file.write("Project Directory Structure:\n")
    for item in os.listdir(repo_path):
        item_path = os.path.join(repo_path, item)
        relative_item_path = os.path.relpath(item_path, repo_path)

        if not should_ignore(relative_item_path, ignore_list):
            output_file.write("  " * level + "- " + item + "\n")
            if os.path.isdir(item_path):
                print_directory_structure(item_path, ignore_list, output_file, level + 1)
    if level == 0:
        output_file.write("End Project Directory Structure Visual\n\n")

def process_repository(repo_path, ignore_list, output_file):
    print_directory_structure(repo_path, ignore_list, output_file)
    for root, _, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_file_path = os.path.relpath(file_path, repo_path)

            if not should_ignore(relative_file_path, ignore_list):
                with open(file_path, 'r', errors='ignore') as file:
                    contents = file.read()
                output_file.write("-" * 4 + "\n")
                output_file.write(f"{relative_file_path}\n")
                output_file.write(f"{contents}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python git_to_text.py /path/to/git/repository [-p /path/to/preamble.txt] [-o /path/to/output_file.txt]")
        sys.exit(1)

    repo_path = sys.argv[1]
    ignore_file_path = os.path.join(repo_path, ".gptignore")
    if sys.platform == "win32":
        ignore_file_path = ignore_file_path.replace("/", "\\")

    if not os.path.exists(ignore_file_path):
        # try and use the .gptignore file in the current directory as a fallback.
        HERE = os.path.dirname(os.path.abspath(__file__))
        ignore_file_path = os.path.join(HERE, ".gptignore")

    preamble_file = None
    if "-p" in sys.argv:
        preamble_file = sys.argv[sys.argv.index("-p") + 1]

    output_file_path = 'output.txt'
    if "-o" in sys.argv:
        output_file_path = sys.argv[sys.argv.index("-o") + 1]

    if os.path.exists(ignore_file_path):
        ignore_list = get_ignore_list(ignore_file_path)
    else:
        ignore_list = []

    with open(output_file_path, 'w') as output_file:
        if preamble_file:
            with open(preamble_file, 'r') as pf:
                preamble_text = pf.read()
                output_file.write(f"{preamble_text}\n")
        else:
            output_file.write("The following text is a Git repository with code. The structure of the text are sections that begin with ----, followed by a single line containing the file path and file name, followed by a variable amount of lines containing the file contents. The text representing the Git repository ends when the symbols --END-- are encounted. Any further text beyond --END-- are meant to be interpreted as instructions using the aforementioned Git repository as context.\n")
        process_repository(repo_path, ignore_list, output_file)
    with open(output_file_path, 'a') as output_file:
        output_file.write("--END--")
    print(f"Repository contents written to {output_file_path}.")

