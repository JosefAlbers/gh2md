import os
import shutil
import subprocess
import tempfile
import logging
import argparse
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MAX_FILE_SIZE = 1024 * 1024  # 1 MB

def get_file_type(file_path):
    return file_path.suffix[1:] if file_path.suffix else 'txt'

def create_toc(path, prefix='', allowed_extensions=None, skip_extensions=None, max_depth=None, current_depth=0):
    toc = []
    if max_depth is not None and current_depth >= max_depth:
        return toc

    for item in sorted(path.iterdir()):
        if item.name.startswith('.'):  # Skip hidden files/folders
            continue
        if item.is_dir():
            toc.append(f"{prefix}- [{item.name}](#{item.name.lower().replace(' ', '-')})")
            toc.extend(create_toc(item, prefix + '  ', allowed_extensions, skip_extensions, max_depth, current_depth + 1))
        elif (allowed_extensions is None or item.suffix.lower() in allowed_extensions) and \
             (skip_extensions is None or item.suffix.lower() not in skip_extensions):
            toc.append(f"{prefix}- {item.name}")
    return toc

def process_folder(path, level=1, allowed_extensions=None, skip_extensions=None, max_depth=None, current_depth=0):
    content = []
    if max_depth is not None and current_depth >= max_depth:
        return content

    for item in sorted(path.iterdir()):
        if item.name.startswith('.'):  # Skip hidden files/folders
            continue
        if item.is_dir():
            content.append(f"\n{'#' * (level + 1)} {item.name}\n")
            content.extend(process_folder(item, level + 1, allowed_extensions, skip_extensions, max_depth, current_depth + 1))
        elif (allowed_extensions is None or item.suffix.lower() in allowed_extensions) and \
             (skip_extensions is None or item.suffix.lower() not in skip_extensions):
            content.append(f"\n{'#' * (level + 2)} {item.name}\n")

            if item.stat().st_size > MAX_FILE_SIZE:
                content.append("*[File skipped - exceeds size limit]*")
                continue

            try:
                file_content = item.read_text(encoding='utf-8').strip()
                file_type = get_file_type(item)
                content.append(f"~~~{file_type}\n{file_content}\n~~~")
            except UnicodeDecodeError:
                content.append("*[File skipped - unable to read file content]*")

    return content

def repo_to_markdown(repo_url, start_dir=None, branch='main', allowed_extensions=None, skip_extensions=None, max_depth=None):
    with tempfile.TemporaryDirectory() as temp_dir:
        logging.info(f"Cloning repository: {repo_url}")
        try:
            subprocess.run(['git', 'clone', '-b', branch, repo_url, temp_dir], check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to clone repository: {e}")
            logging.error(f"Git output: {e.output}")
            return None

        repo_path = Path(temp_dir)
        if start_dir:
            repo_path = repo_path / start_dir

        if not repo_path.exists():
            logging.error(f"Specified start directory does not exist: {repo_path}")
            return None

        repo_name = repo_url.split('/')[-1]
        markdown_content = [f"# {repo_name}", ""]

        # if allowed_extensions:
        #     markdown_content.append(f"*Showing only files with extensions: {', '.join(allowed_extensions)}*\n")
        # if skip_extensions:
        #     markdown_content.append(f"*Skipping files with extensions: {', '.join(skip_extensions)}*\n")

        logging.info("Creating table of contents")
        toc = create_toc(repo_path, allowed_extensions=allowed_extensions, skip_extensions=skip_extensions, max_depth=max_depth)
        markdown_content.extend(["## Table of Contents", ""] + toc + [""])

        logging.info("Processing folder contents")
        content = process_folder(repo_path, allowed_extensions=allowed_extensions, skip_extensions=skip_extensions, max_depth=max_depth)
        markdown_content.extend(content)

    logging.info("Markdown content generation complete")
    return '\n'.join(markdown_content)

def main():
    parser = argparse.ArgumentParser(description="Convert a GitHub repository to a single Markdown file.")
    parser.add_argument("repo_url", help="URL of the GitHub repository")
    parser.add_argument("-o", "--output", default="output_gh2md.md", help="Output file name (default: output_gh2md.md)")
    parser.add_argument("-s", "--start-dir", default=None, help="Start from a specific subdirectory in the repository")
    parser.add_argument("-b", "--branch", default="main", help="Branch to clone (default: main)")
    parser.add_argument("-e", "--extensions", nargs="*", default=None, help="File extensions to include (e.g., .py .js)")
    parser.add_argument("-x", "--skip-extensions", nargs="*", default=None, help="File extensions to skip (e.g., .ipynb .md)")
    parser.add_argument("-d", "--max-depth", type=int, default=None, help="Maximum depth to traverse")

    args = parser.parse_args()

    logging.info("Starting repository to markdown conversion")

    allowed_extensions = args.extensions
    if allowed_extensions:
        allowed_extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in allowed_extensions]

    skip_extensions = args.skip_extensions
    if skip_extensions:
        skip_extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in skip_extensions]

    markdown_output = repo_to_markdown(
        args.repo_url,
        start_dir=args.start_dir,
        branch=args.branch,
        allowed_extensions=allowed_extensions,
        skip_extensions=skip_extensions,
        max_depth=args.max_depth
    )

    if markdown_output is not None:
        logging.info(f"Writing output to {args.output}")
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(markdown_output)
        logging.info("Conversion complete")
    else:
        logging.error("Failed to generate markdown output")

if __name__ == "__main__":
    main()

# Examples:
# python gh2md.py https://github.com/JosefAlbers/Phi-3-Vision-MLX -x .ipynb
# python gh2md.py https://github.com/ml-explore/mlx-examples -s llms/mlx_lm
