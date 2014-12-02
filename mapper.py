#!/usr/bin/env python

from PIL import Image, ImageChops, ImageEnhance
import sys, os.path
import json
import uuid
import base64
from subprocess import call

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    if line:
        img_dict = json.loads(line)
        img_name = img_dict.get('name')
        img_data = img_dict.get('content')
        if img_name and img_data:
            data = base64.b64decode(img_data)
            filename = '/tmp/%s' % str(uuid.uuid4())
            resaved = filename + '.resaved.jpg'
            ela = filename + '.ela.png'
            f = open(filename, 'wa')
            f.write(data)
            f.flush()
            f.close()
            im = Image.open(filename)

            im.save(resaved, 'JPEG', quality=95)
            resaved_im = Image.open(resaved)

            ela_im = ImageChops.difference(im, resaved_im)
            extrema = ela_im.getextrema()
            max_diff = max([ex[1] for ex in extrema])
            scale = 255.0/max_diff

            ela_im = ImageEnhance.Brightness(ela_im).enhance(scale)

            print "%s=%d" % (img_name, max_diff)
            #ela_im.save(ela)
            call(["rm", "-f", "%s*" % filename])
