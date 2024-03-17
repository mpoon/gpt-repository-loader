"""
Parses a Git repository and generates a markdown report with the directory structure and file contents.

The main functions are:

- get_ignore_list: Reads a .gptignore file to get patterns to ignore.
- should_ignore: Checks if a file path should be ignored based on the patterns.  
- print_directory_structure: Recursively prints the directory structure.
- process_repository: Walks the repo to print structure and file contents.
- download_button: Generates a button to download the output.

The main Streamlit UI displays a text input for the repo path, buttons to process, download, and copy the output, and the generated markdown report.
"""
import os
import fnmatch
import streamlit as st
import sys
import base64

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

def process_repository(repo_path, ignore_list):
    structure = "Project Directory Structure:\n"
    contents = ""
    for root, dirs, files in os.walk(repo_path):
        level = root.replace(repo_path, '').count(os.sep)
        indent = '  ' * level
        subindent = '  ' * (level + 1)
        relative_root = os.path.relpath(root, repo_path)
        if not should_ignore(relative_root, ignore_list):
            structure += '{}- {}\n'.format(indent, os.path.basename(root))
            for file in files:
                relative_file_path = os.path.relpath(os.path.join(root, file), repo_path)
                if not should_ignore(relative_file_path, ignore_list):
                    structure += '{}- {}\n'.format(subindent, file)
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', errors='ignore') as file:
                        file_contents = file.read()
                    contents += "-" * 4 + "\n"
                    contents += f"{relative_file_path}\n"
                    contents += f"{file_contents}\n"
    structure += "End Project Directory Structure Visual\n\n"
    return structure, contents

def download_button(object_to_download, download_filename, button_text):
    if isinstance(object_to_download, bytes):
        pass
    elif isinstance(object_to_download, str):
        object_to_download = object_to_download.encode('utf-8')
    else:
        raise ValueError(f"object_to_download must be a str or bytes, got {type(object_to_download)}")

    try:
        b64 = base64.b64encode(object_to_download).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="{download_filename}" class="btn btn-primary" role="button">{button_text}</a>'
        st.markdown(href, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"An error occurred while creating the download link: {e}")

# Streamlit UI
st.title("Git Repository Parser with Web UI")
repo_path = st.text_input("Enter the path to your Git repository:", "")

if st.button("Process Repository"):
    with st.spinner('Processing the repository...'):
        ignore_file_path = os.path.join(repo_path, ".gptignore")
        if sys.platform == "win32":
            ignore_file_path = ignore_file_path.replace("/", "\\")

        if not os.path.exists(ignore_file_path):
            # try and use the .gptignore file in the current directory as a fallback.
            HERE = os.path.dirname(os.path.abspath(__file__))
            ignore_file_path = os.path.join(HERE, ".gptignore")

        if os.path.exists(ignore_file_path):
            ignore_list = get_ignore_list(ignore_file_path)
        else:
            ignore_list = []

        structure, contents = process_repository(repo_path, ignore_list)
        full_output = f"### Project Directory Structure\n{structure}\n### Files Content\n{contents}"

        # Layout for buttons and output
        col1, col2 = st.columns(2)
        with col1:
            download_button(full_output, "repository_output.md", "Download Output as Markdown")
        with col2:
            copy_button = st.button("Copy to Clipboard", key="copy_to_clipboard")

        # Output box
        st.markdown("### Output")
        output_container = st.container()
        with output_container:
            st.markdown("#### Project Directory Structure")
            st.text(structure)
            st.markdown("#### Files Content")
            st.text(contents)

        if copy_button:
            st.sidebar.write("Copied to clipboard!")
            st.sidebar.code(full_output)
            st.experimental_set_query_params(full_output=full_output)
            js = f"navigator.clipboard.writeText(`{full_output}`)"
            st.components.v1.html(f"<script>{js}</script>", height=0, width=0)

        st.success("Process completed. Review the results above.")
