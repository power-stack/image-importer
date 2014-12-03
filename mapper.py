#!/usr/bin/env python

from PIL import Image, ImageChops, ImageEnhance, ExifTags
import sys, os.path
import json
import uuid
import base64
from subprocess import call

reload(sys)
sys.setdefaultencoding('utf8')

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
            photoshopped = False
            try:
                exif_data = im._getexif()
                if exif_data:
                    for k, v in exif_data.items():
                        if k in ExifTags.TAGS:
                            if "MakerNote" != ExifTags.TAGS.get(k):
                                if v and ("photoshop" in str(v).lower() or "microsoft" in str(v).lower()):
                                    print "%s=100" % img_name
                                    photoshopped = True
                bands = im.getbands()
                if bands and bands != ('R', 'G', 'B'):
                    print "%s=100" % img_name
                    photoshopped = True
            except:
                pass
            if not photoshopped:
                im.save(resaved, 'JPEG', quality=95)
                resaved_im = Image.open(resaved)
                ela_im = ImageChops.difference(im, resaved_im)
                extrema = ela_im.getextrema()
                max_diff = max([ex[1] for ex in extrema])
                print "%s=%d" % (img_name, max_diff)
            call(["rm", "-f", "/tmp/%s*" % filename, "&"])
