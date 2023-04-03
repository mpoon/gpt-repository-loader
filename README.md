# gpt-repository-loader

`gpt-repository-loader` is a command-line tool that converts the contents of a Git repository into a text format, preserving the structure of the files and file contents. The generated output can be interpreted by AI language models, allowing them to process the repository's contents for various tasks, such as code review or documentation generation.

## Contributing
Some context around building this is [located here](https://github.com/mpoon/gpt-repository-loader/discussions/18). Appreciate any issues and pull requests in the spirit of having mostly GPT build out this tool. Using [ChatGPT Plus](https://chat.openai.com/) is recommended for quick access to GPT-4.

## Requirements

You'll need following dependencies with Python.

```
pip install tiktoken
```

## Getting Started

To get started with `gpt-repository-loader`, follow these steps:

1. Ensure you have Python 3 installed on your system.
2. Clone or download the `gpt-repository-loader` repository.
3. Navigate to the repository's root directory in your terminal.
4. Run `gpt-repository-loader` with the following command:

   ```bash
   python gpt_repository_loader.py /path/to/git/repository [-p /path/to/preamble.txt] [-o /path/to/output_file.txt]
   ```
    Replace `/path/to/git/repository` with the path to the Git repository you want to process. Optionally, you can specify a preamble file with -p or an output file with -o. If not specified, the default output file will be named output.txt in the current directory.

5. The tool will generate an output.txt file containing the text representation of the repository. You can now use this file as input for AI language models or other text-based processing tasks.

## Token Limit

You can use the token limit parameter to limit the output tokens per file. This is useful if you need to split the 
output to multiple files, so that each request can be split to GPT-4's request limits. Your API may have a 4k, 8k or 
a 32k token limit.

   ```bash
   python gpt_repository_loader.py /path/to/git/repository [-p /path/to/preamble.txt] [-o /path/to/output_file.txt] 
   [-t 8000]
   ```

Above command will output multiple files, starting with an index of 1. Each file will have around 8k tokens. For 
example,

```
/path/to/output_file_1.txt
/path/to/output_file_2.txt
/path/to/output_file_3.txt
/path/to/output_file_4.txt
/path/to/output_file_5.txt
```

By default, the max output is limited to 5 files. Any content that doesn't fit the limit is ignored. You can override 
the max output limit by adding `-m` argument. 
Following example splits the output to 20 files, with each file having a token size of 32k.

   ```bash
   python gpt_repository_loader.py /path/to/git/repository [-p /path/to/preamble.txt] [-o /path/to/output_file.txt] 
   [-t 32000] [-m 20]
   ```

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
