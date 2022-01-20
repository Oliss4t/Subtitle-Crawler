import os
from pathlib import Path
import itertools

#files in ./data/downloads recursive
file_names = list(Path("./data/downloads").rglob("*"))

#anonymous function for file ending filter
#use as input in filter_subtitleids()
ending_filter = lambda x : os.path.splitext(x)[1] == '.txt'

#check if file is matching
def filter_subtitleids(ending_filter, subtitleid,file):
    if ending_filter(file):
        if os.path.basename(file).split(".")[0] == subtitleid:
            return True

#maps every file to the filter_subtitleids function
def check_subtitleid(id, file_names):
    return list(map(filter_subtitleids,
           itertools.repeat(ending_filter, len(file_names)),
           itertools.repeat(id, len(file_names)),
           file_names))

response="SubtitleId is already downloaded" if any(check_subtitleid('48587',file_names)) else "SubtitleId not found"
print(response)
