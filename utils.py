#!/usr/bin/env python3
"""
This script is used in filename generation
"""

from datetime import datetime

def get_epochtime_ms():
    return round(datetime.datetime.utcnow().timestamp() * 1000)

def timenow():
    now = datetime.now()
    t = now.strftime('%H_%M_%S_%f')
    return t

def create_file_name(a,ext):
    if len(a) >= 7:
        b = a[0:7]
    else:
        b = a.zfill(7)
    return b+str(timenow())+'.'+ext
