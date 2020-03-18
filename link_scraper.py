#!/usr/bin/env python3
'''
 A script to find links in a html page
 and turn it into list in markdown format
 Sid
'''

from html.parser import HTMLParser
import re

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.linklist = list()
        self._a_tag_active = False
        self._theres_text_inside_a = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a' and 'href' in attrs:
            if attrs['href'].startswith('http'):
                self._a_tag_active = True
                linkurl = attrs['href']
                self.linklist.append([])
                self.linklist[-1].append(linkurl)

    def handle_endtag(self, tag):
        if tag == 'a':
            self._a_tag_active = False
            # I KNOW I KNOW, this is idiot... I'm an amateur, man! Forgive me, my brain is foggy right now.
            if not self._theres_text_inside_a:
                self.linklist[-1].append(self.linklist[-1][0])
            # reset the stupid flag
            self._theres_text_inside_a = False

    def handle_data(self, text):
        if self._a_tag_active:
            self._theres_text_inside_a = True
            self.linklist[-1].append(text)
            self.linklist[-1].reverse()
        else:
            # I hate regex
            urls_list = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
            for u in urls_list:
                self.linklist.append([u, u])

def markdown_formatter(linklist):
    md = ''
    for l in linklist:
        print(l)
        md = md + '* [{caption}]({link})\n'.format(caption=l[0], link=l[1])
    return md

if __name__ == '__main__':
    from sys import argv

    if len(argv) != 3:
        print('Usage: {} html_input_file markdown_output_file'.format(argv[0]))
        exit(1)

    with open(argv[1], 'r') as inputfile:
        inputtext = inputfile.read()

    parser = LinkParser()
    parser.feed(inputtext)

    md_formatted = markdown_formatter(parser.linklist)

    with open(argv[2], 'w') as outputfile:
        outputfile.write(md_formatted)

