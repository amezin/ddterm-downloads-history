#!/usr/bin/env python3

import csv
import datetime
import html.parser
import re
import sys
import urllib.request


INPUT_RE = re.compile(r'^\s*(\d+)\s+downloads\s*$')


class Parser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()

        self.in_tag = False
        self.result = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.in_tag = tag == 'span' and attrs.get('class') == 'downloads'

    def handle_endtag(self, _):
        self.in_tag = False

    def handle_data(self, data):
        if not self.in_tag:
            return

        if self.result:
            raise ValueError(f'Multiple results found: {[self.result, data]!r}')

        match = INPUT_RE.fullmatch(data)

        if not match:
            raise ValueError(f'Pattern {INPUT_RE!r} not found in {data!r}')

        self.result = int(match.group(1))


parser = Parser()

with urllib.request.urlopen('https://extensions.gnome.org/extension/3780/ddterm/') as request:
    parser.feed(request.read().decode())

if not parser.result:
    raise ValueError('Download counter not found!')

writer = csv.writer(sys.stdout)
writer.writerow((
    datetime.datetime.now(tz=datetime.UTC).replace(tzinfo=None).isoformat(timespec='seconds'),
    parser.result
))
