#!/usr/bin/env python3

import datetime
import html.parser
import urllib.request


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
        if self.in_tag:
            if self.result:
                raise ValueError(f'Multiple results found: {[self.result, data]!r}')
            self.result = data


parser = Parser()

with urllib.request.urlopen('https://extensions.gnome.org/extension/3780/ddterm/') as request:
    parser.feed(request.read().decode())

print(datetime.datetime.now(tz=datetime.timezone.utc), parser.result)
