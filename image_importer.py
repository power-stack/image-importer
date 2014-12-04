#!/usr/bin/env python

import base64
from PIL import Image
import numpy as np
import json
import os
import sys


def transfer_pics(input_dir, out_file):
    if not os.path.exists(input_dir):
        print("%s does not exist!" % input_dir)

    image_files = []
    for root, dirs, files in os.walk(input_dir, topdown=False):
        for name in files:
            if name.endswith(".jpg") and not name.startswith("."):

                print('append ' + name)
                image_files.append(os.path.join(root,name))

    image_files.sort()

    fs = open(out_file, "wa")

    for img_file in image_files:
        #line = {}
        file_path = img_file
        print("import file: %s" % file_path)
        imgf = open(file_path, "r")
        data = imgf.read()
        imgf.close()
        data_b64 = base64.b64encode(data)
        img = Image.open(file_path)
        #content = np.asarray(img)
        #line[file_path] = content.tolist()
        #line = json.dumps(dict(name=file_path, content=content.tolist()))
        line = json.dumps(dict(name=file_path, size=img.size, content=data_b64))
        fs.write(line)
        fs.write("\n")
        fs.flush()

    fs.close()

if __name__ == '__main__':
    input_dir = sys.argv[1]
    out_file = sys.argv[2]
    transfer_pics(input_dir, out_file)
