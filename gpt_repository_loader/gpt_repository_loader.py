#!/usr/bin/env python3

import os
import sys
import fnmatch
import pyperclip
import io

def get_ignore_list(ignore_file_path):
    ignore_list = []
    with open(ignore_file_path, 'r') as ignore_file:
        for line in ignore_file:
            ignore_list.append(line.strip())
    return ignore_list

def should_ignore(file_path, ignore_list):
    for pattern in ignore_list:
        if fnmatch.fnmatch(file_path, pattern):
            return True
    return False

def process_repository(repo_path, ignore_list, output_stream):
    for root, _, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_file_path = os.path.relpath(file_path, repo_path)

            if not should_ignore(relative_file_path, ignore_list):
                with open(file_path, 'r', errors='ignore') as file:
                    contents = file.read()
                output_stream.write("-" * 4 + "\n")
                output_stream.write(f"{relative_file_path}\n")
                output_stream.write(f"{contents}\n")

def git_repo_to_text(repo_path, preamble_file=None):
    ignore_file_path = os.path.join(repo_path, ".gptignore")

    if os.path.exists(ignore_file_path):
        ignore_list = get_ignore_list(ignore_file_path)
    else:
        ignore_list = []

    output_stream = io.StringIO()

    if preamble_file:
        with open(preamble_file, 'r') as pf:
            preamble_text = pf.read()
            output_stream.write(f"{preamble_text}\n")
    else:
        output_stream.write("The following text is a Git repository with code. The structure of the text are sections that begin with ----, followed by a single line containing the file path and file name, followed by a variable amount of lines containing the file contents. The text representing the Git repository ends when the symbols --END-- are encounted. Any further text beyond --END-- are meant to be interpreted as instructions using the aforementioned Git repository as context.\n")

    process_repository(repo_path, ignore_list, output_stream)

    output_stream.write("--END--")

    return output_stream.getvalue()

def main():
    if len(sys.argv) < 2:
        print("Usage: python git_to_text.py /path/to/git/repository [-p /path/to/preamble.txt]")
        sys.exit(1)

    repo_path = sys.argv[1]
    preamble_file = None
    if "-p" in sys.argv:
        preamble_file = sys.argv[sys.argv.index("-p") + 1]

    repo_as_text = git_repo_to_text(repo_path, preamble_file)

    with open('output.txt', 'w') as output_file:
        output_file.write(repo_as_text)
    print("Repository contents written to output.txt.")

    if "-c" in sys.argv:
        pyperclip.copy(repo_as_text)
        print("Repository contents copied to clipboard.")

if __name__ == "__main__":
    main()