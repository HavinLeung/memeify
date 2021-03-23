#! /usr/bin/env python3

import sys
import os
import subprocess

def timestr_to_millis(timestr):
    hours, minutes, millis = timestr.split(':')
    millis = millis.replace(',', '')
    millis = int(millis)
    millis += int(minutes)*60*1000
    millis += int(hours)*60*60*1000
    return millis

def transform(s):
    times, text = s
    start, end = times.split(' --> ')
    start, end = timestr_to_millis(start), timestr_to_millis(end)
    return (start, end, text)

if len(sys.argv) != 2:
    print('usage:', sys.argv[0], '<filename>')
    exit(-1)

filename = sys.argv[1]
escaped_filename = filename.replace(' ', '''\ ''')
if os.system(F'ffmpeg -i {escaped_filename} out.srt') == 0:
    with open('out.srt', 'r') as f:
        output = [l.strip() for l in f.readlines()]
        output = zip(output[1::4], output[2::4])
        output = list(map(transform, output))
        out = []
        for i, (start, _, text) in enumerate(output):
            if i == 0:
                out.append(text)
            else:
                _, end, _ = output[i-1]
                if start - end >= 2.5*1000:
                    out.append(F'\n\n{text}')
                else:
                    out.append(text)

        subprocess.run('pbcopy', input=' '.join(out), universal_newlines=True)
    os.system('rm out.srt')
    print('\n\nSUCCESS\ncopied transcript to clipboard\n')
else:
    print('FAILED')

