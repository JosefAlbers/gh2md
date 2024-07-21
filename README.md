# GitHub Repository to Markdown Converter

This Python script allows you to convert an entire GitHub repository (or parts of it) into a single Markdown file. It's useful for creating documentation, code reviews, archiving repositories in a human-readable format, or generating **LLM-consumable content for AI-assisted development and analysis**. By converting a repository to a single Markdown file, you make it easy for both humans and AI language models to process and understand the entire codebase at once. This can be particularly valuable for tasks such as:

- Automated code analysis and suggestions
- Generating summaries or explanations of complex codebases
- Assisting in refactoring or modernization efforts
- Facilitating knowledge transfer and onboarding

## Features

- Clone any public GitHub repository
- Convert repository content to a single Markdown file
- Customizable starting directory within the repository
- Option to include only specific file extensions
- Option to exclude specific file extensions
- Control the depth of directory traversal
- Command-line interface for easy use

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/JosefAlbers/gh2md.git
   cd gh2md
   ```

## Usage

Basic usage:

```
python gh2md.py https://github.com/JosefAlbers/Phi-3-Vision-MLX
```

This will convert the entire repository to a Markdown file named `output_gh2md.md` in the current directory.

### Options

- `-o`, `--output`: Specify the output file name (default: output.md)
- `-s`, `--start-dir`: Start from a specific subdirectory in the repository
- `-b`, `--branch`: Specify the branch to clone (default: main)
- `-e`, `--extensions`: Include only files with specific extensions
- `-x`, `--skip-extensions`: Exclude files with specific extensions
- `-d`, `--max-depth`: Set the maximum depth to traverse in the directory structure

### Examples

1. Convert a specific branch and save to a custom file:
   ```
   python gh2md.py https://github.com/JosefAlbers/Phi-3-Vision-MLX -b gh-pages -o my_repo_doc.md
   ```

2. Start from a specific directory and include only Python and Markdown files:
   ```
   python gh2md.py https://github.com/ml-explore/mlx-examples -s llms/mlx_lm -e .py .md
   ```

3. Exclude specific file types and limit directory depth:
   ```
   python gh2md.py https://github.com/ml-explore/mlx-examples -x .json .jsonl -d 3
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
