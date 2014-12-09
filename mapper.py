#!/usr/bin/env python

from PIL import Image, ImageChops, ImageEnhance, ExifTags
import sys, os, os.path
import json
import uuid
import base64
from subprocess import call
import cStringIO as sio

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
            del img_dict['content']
            data = base64.b64decode(img_data)
            filename = '/tmp/%s' % str(uuid.uuid4())

            im = None
            '''
            f = open(filename, 'wa')
            f.write(data)
            f.flush()
            f.close()
            im = Image.open(filename)
            '''
            stream = sio.StringIO(data)
            im = Image.open(stream)
            edited = False
            try:
                exif_data = im._getexif()
                if exif_data:
                    for k, v in exif_data.items():
                        if k in ExifTags.TAGS:
                            if "MakerNote" != ExifTags.TAGS.get(k):
                                if v and ("photoshop" in str(v).lower() or "microsoft" in str(v).lower()):
                                    img_dict['edited'] = 'yes'
                                    img_dict['reason'] = 'software'
                                    img_dict['software'] = v
                                    edited = True
                                    break
                if not edited:
                    bands = im.getbands()
                    if bands and bands != ('R', 'G', 'B'):
                        img_dict['edited'] = 'yes'
                        img_dict['reason'] = 'not_rgb'
                        edited = True
                '''
                if not edited:
                    im_info = im.info
                    if im_info and ("jfif" in im_info or "jfif_unit" in im_info):
                        img_dict['edited'] = 'yes'
                        img_dict['reason'] = 'jfif'
                        edited = True
                '''
            except:
                pass

            #if not edited:
            resaved = filename + '.resaved.jpg'
            im.save(resaved, 'JPEG', quality=95)
            resaved_im = Image.open(resaved)
            ela_im = ImageChops.difference(im, resaved_im)
            extrema = ela_im.getextrema()
            max_diff = max([ex[1] for ex in extrema])
            img_dict['edited'] = 'notsure'
            img_dict['ela'] = max_diff
            if os.path.exists(resaved):
                os.remove(resaved)

            print json.dumps(img_dict)
