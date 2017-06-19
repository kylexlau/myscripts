#!/usr/bin/env python3

import ssl
import re
import sys
import os
from urllib import request
from urllib.error import HTTPError
import argparse
from pathlib import Path

## turn off certificate verify
ssl._create_default_https_context = ssl._create_unverified_context

class Pep:

    def __init__(self, num, editor):
        self.num = int(num)

        if editor is None:
            self.editor = 'less'
        else:
            self.editor = editor

    def get(self):
        url = "https://raw.githubusercontent.com/python/peps/master/pep-%04d.txt" \
              % self.num

        print("Downloading %s..." %url)

        try:
            with request.urlopen(url) as r:
                txt = r.read().decode()
                title = re.findall(r"Title: (.+?)\n", txt)[0]
                self.fname = ".peps/PEP-%04d %s.txt" % (self.num, title)
        except HTTPError as e:
            print(e)
            sys.exit(1)

        try:
            with open(self.fname, 'w') as f:
                f.write(txt)
        except IOError as e:
            print(e)
            sys.exit(1)

    def read(self, p):
        sys.exit(os.system("%s '%s'" % (self.editor, p)))

    def run(self):
        fn = "PEP-%04d*" % self.num
        try:
            p = next(Path('.peps').glob(fn))
            self.read(str(p))
        except StopIteration:
            self.get()
            self.read(self.fname)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get or read a PEP.")
    parser.add_argument('pep_no', help="PEP number")
    parser.add_argument('-e','--editor', help="Choose a editor, default is less.")
    args = parser.parse_args()
    pep = Pep(args.pep_no,args.editor)
    pep.run()
