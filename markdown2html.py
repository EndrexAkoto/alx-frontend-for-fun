#!/usr/bin/python3
"""
Module for converting Markdown to HTML.
"""

import sys
import os
import markdown

def convert_markdown_to_html(markdown_file, html_file):
    """
    Converts the content of a Markdown file to HTML and writes it to an output file.
    """
    try:
        with open(markdown_file, 'r') as md_file:
            md_content = md_file.read()
            html_content = markdown.markdown(md_content)
            with open(html_file, 'w') as html_file:
                html_file.write(html_content)
    except FileNotFoundError:
        print(f"Missing {os.path.basename(markdown_file)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    markdown_file = sys.argv[1]
    html_file = sys.argv[2]

    convert_markdown_to_html(markdown_file, html_file)
    sys.exit(0)

