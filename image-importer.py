#!/bin/python

import base64
from PIL import Image
import numpy as np
import json
import os
import sys

INPUT_DIR = sys.argv[1]
OUT_FILE = sys.argv[2]


if not os.path.exists(INPUT_DIR):
    print("%s does not exist!" % INPUT_DIR)

image_files = []
for root, dirs, files in os.walk(INPUT_DIR, topdown=False):
    for name in files:
        if name.endswith(".jpg") and not name.startswith("."):

            print('append ' + name)
            image_files.append(os.path.join(root,name))

image_files.sort()

fs = open(OUT_FILE, "wa")

for img_file in image_files:
    #line = {}
    file_path = img_file
    print("import file: %s" % file_path)
    imgf = open(file_path, "r")
    data = imgf.read()
    imgf.close()
    data_b64 = base64.b64encode(data)
    #img = Image.open(img_file)
    #content = np.asarray(img)
    #line[file_path] = content.tolist()
    #line = json.dumps(dict(name=file_path, content=content.tolist()))
    line = json.dumps(dict(name=file_path, content=data_b64))
    fs.write(line)
    fs.write("\n")
    fs.flush()

fs.close()
