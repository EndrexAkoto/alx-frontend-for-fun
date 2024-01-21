#!/usr/bin/python3
"""This script takes 2 files as argumrnts
    first argument: markdown file
    second argument: html file"""

from sys import argv, stderr
import os


if __name__ == "__main__":
    if (len(argv) <= 2):
        print ('Usage: ./markdown2html.py README.md README.html', file=stderr)
        exit(1)
    elif (not os.path.exists(argv[1])):
        print ('Missing {}'.format(argv[1]), file=stderr)
        exit(1)
    else:
        with open(argv[1], 'r') as md_file:
            lines = md_file.readlines()
        L = []
        unordered_list = []
        ordered_list = []
        paragraphs = []
        p = []
        for line in lines:
            if line.startswith('#'):
                level = line.count('#')
                L.append('<h{}>{}</h{}>'.format(level,
                                                line[level+1:],
                                                level))
            elif line.startswith('- '):
                unordered_list.append('<li>{}</li>'.format(line[2:-1]))
            elif line.startswith('* '):
                ordered_list.append('<li>{}</li>'.format(line[2:-1]))
            else:
                paragraphs.append(line)
                s = "".join(paragraphs)
                p = s.split('\n\n')

        if unordered_list != []:
            L.append('<ul>')
            for elm in unordered_list:
                L.append('\t'+elm)
            L.append('</ul>')

        if ordered_list != []:
            L.append('<ol>')
            for elm in ordered_list:
                L.append('\t'+elm)
            L.append('</ol>')

        if p != []:
            for item in p:
                if item != '':
                    if '\n' in item.strip():
                        item = item.replace('\n', '<br />')
                    L.append('<p>')
                    L.append('\t'+item.strip())
                    L.append('</p>')

        for i, item in enumerate(L):
            if "**" in item:
                b = item.split("**")
                L[i] = item.replace("**{}**".format(b[1]),
                                    "<b>{}</b>".format(b[1]))
            if "__" in item:
                b = item.split("__")
                L[i] = item.replace("__{}__".format(b[1]),
                                    "<em>{}</em>".format(b[1]))
        with open(argv[2], 'w') as html_file:
            html_file.writelines('\n'.join(L))
        exit(0)
