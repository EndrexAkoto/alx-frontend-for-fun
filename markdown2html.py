#!/usr/bin/python3
"""This script takes 2 files as arguments:
   - First argument: markdown file
   - Second argument: html file"""

from sys import argv, stderr
import os
import re
import hashlib

def print_usage_and_exit():
    print('Usage: ./markdown2html.py README.md README.html', file=stderr)
    exit(1)

def print_missing_file_and_exit(filename):
    print('Missing {}'.format(filename), file=stderr)
    exit(1)

def convert_md5(match):
    content = match.group(1)
    md5_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
    return md5_hash

def remove_characters(match):
    content = match.group(1)
    return re.sub('[cC]', '', content)

if __name__ == "__main__":
    if len(argv) <= 2:
        print_usage_and_exit()
    
    markdown_file = argv[1]
    output_file = argv[2]

    if not os.path.exists(markdown_file):
        print_missing_file_and_exit(markdown_file)

    with open(markdown_file, 'r') as md_file:
        lines = md_file.readlines()

    html_lines = []
    unordered_list = []
    ordered_list = []
    paragraphs = []
    p = []

    for line in lines:
        if line.startswith('#'):
            level = line.count('#')
            html_lines.append('<h{}>{}</h{}>'.format(level, line[level+1:].strip(), level))
        elif line.startswith('- '):
            unordered_list.append('<li>{}</li>'.format(line[2:].strip()))
        elif line.startswith('* '):
            ordered_list.append('<li>{}</li>'.format(line[2:].strip()))
        else:
            paragraphs.append(line.strip())

    if unordered_list:
        html_lines.append('<ul>')
        html_lines.extend(['\t' + item for item in unordered_list])
        html_lines.append('</ul>')

    if ordered_list:
        html_lines.append('<ol>')
        html_lines.extend(['\t' + item for item in ordered_list])
        html_lines.append('</ol>')

    if paragraphs:
        for item in paragraphs:
            if '\n' in item:
                item = item.replace('\n', '<br />')
            html_lines.append('<p>{}</p>'.format(item))

    for i, line in enumerate(html_lines):
        line = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', line)
        line = re.sub(r'__(.+?)__', r'<em>\1</em>', line)
        line = re.sub(r'\[\[(.+?)\]\]', convert_md5, line)
        line = re.sub(r'\(\((.+?)\)\)', remove_characters, line)
        html_lines[i] = line

    with open(output_file, 'w') as html_file:
        html_file.write('\n'.join(html_lines))

    exit(0)
