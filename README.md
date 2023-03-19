# gpt-repository-loader

`gpt-repository-loader` is a command-line tool that converts the contents of a Git repository into a text format, preserving the structure of the files and file contents. The generated output can be interpreted by AI language models, allowing them to process the repository's contents for various tasks, such as code review or documentation generation.

## Installation & Usage
`pip install gpt-repository-loader` install the project locally.

Now you'll be able to use the console script `gpt-repository-loader` with any project.

```gpt-repository-loader /path/to/git/repository -c```
this will copy the content of the project into clipboard which you can directly paste into 

You can also now use `gpt-repository-loader` as a library.

```python
from gpt_repository_loader import git_repo_to_text
repo_text = git_repo_to_text('/path/to/repository')
```


## Contributing
Some context around building this is [located here](https://github.com/mpoon/gpt-repository-loader/discussions/18). Appreciate any issues and pull requests in the spirit of having mostly GPT build out this tool. Using [ChatGPT Plus](https://chat.openai.com/) is recommended for quick access to GPT-4.

## Getting Started with contribution

To get started with `gpt-repository-loader`, follow these steps:

1. Ensure you have Python 3 installed on your system.
2. Clone or download the `gpt-repository-loader` repository.
3. Navigate to the repository's root directory in your terminal.
4. Run `gpt-repository-loader` with the following command:

   ```bash
   python gpt_repository_loader.py /path/to/git/repository
   ```
    Replace `/path/to/git/repository` with the path to the Git repository you want to process.

5. The tool will generate an output.txt file containing the text representation of the repository. You can now use this file as input for AI language models or other text-based processing tasks.

## Running Tests

To run the tests for `gpt-repository-loader`, follow these steps:

1. Ensure you have Python 3 installed on your system.
2. Navigate to the repository's root directory in your terminal.
3. Run the tests with the following command:

   ```bash
   python -m unittest test_gpt_repository_loader.py
   ```
Now, the test harness is added to the `gpt-repository-loader` project. You can run the tests by executing the command `python -m unittest test_gpt_repository_loader.py` in your terminal.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
