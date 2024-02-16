import csv
import os

import requests
import re
from tqdm import tqdm

import time
import random

# Get the directory of the script
dir = os.path.dirname(os.path.relpath(__file__)) + '/'


docs = "https://docs.google.com"
file = "layoffs.fyi_20240208_004032.csv"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14.3; rv:122.0) Gecko/20100101 Firefox/122.0'}

data = []
empl_list_src = []

with open(dir+file, 'r') as f:

    for l in csv.reader(f, delimiter=';'):
        data.append(l)

for l in data:

    a = 0

    if re.search(docs, l[8]):

        empl_list_src.append(l[8])

empl_list_src = list(dict.fromkeys(empl_list_src))


print("Clearing links")
pat = "((edit.*)|(html.*)|(viewform.*))"
deletion = []
for i in range(len(empl_list_src)):
    empl_list_src[i]: str = re.sub(
        pat, "gviz/tq?tqx=out:csv", empl_list_src[i])
    if "forms" in empl_list_src[i]:
        deletion.append(empl_list_src[i])

for d in deletion:
    empl_list_src.remove(d)

pat = "pub.*"
for i in range(len(empl_list_src)):
    empl_list_src[i] = re.sub(pat, "pub?output=csv", empl_list_src[i])


index = 0
out_dir = dir+"list/"
dirname = os.path.dirname(out_dir)
if not os.path.exists(dirname):
    os.makedirs(dirname)

for item in tqdm(empl_list_src):

    out_file = out_dir+"list_"+str(index)+".csv"

    empl = requests.get(url=item, headers=headers)

    with open(out_file, 'wb') as out:
        out.write(empl.content)

    index += 1
    time.sleep(4+random.random()*10)
