#!/usr/bin/env python3
import sys
from csv import reader, writer 
with open(sys.argv[1]) as f, open(sys.argv[2], 'w') as fw: 
    writer(fw, delimiter=',').writerows(zip(*reader(f, delimiter=',')))
