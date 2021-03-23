#! /usr/bin/env python3

import sys
import os
import subprocess

if len(sys.argv) != 2:
    print('usage:', sys.argv[0], '<filename>')
    exit(-1)

filename = sys.argv[1]
escaped_filename = filename.replace(' ', '''\ ''')
output = []
if os.system(F'ffmpeg -i {escaped_filename} out.srt') == 0:
    with open('out.srt', 'r') as f:
        for i,line in enumerate(f):
            if i % 4 == 2:
                output.append(line.strip())
    os.system('rm out.srt')
    subprocess.run('pbcopy', input=' '.join(output), universal_newlines=True)
    print('\n\nSUCCESS\ncopied transcript to clipboard\n')
else:
    print('FAILED')

