import json
import os
from PIL import Image
from pynput.keyboard import Key, Listener, Controller

# load keywords
f = open('keywords.json')
data = json.load(f)
f.close()
# load clusters
f = open('clusters.json')
global clusters
clusters = json.load(f)
f.close()

ROOT_PATH = "../image_scraping/style_images/"
styles = {}
global status
global best_ratio
global best_style
best_ratio = -1

for style_name in list(data.keys()):
    try:
        path = ROOT_PATH + style_name + "/"
        pics = os.listdir(path)
        # if there are photos in the file, add it to the list
        if len(pics) > 0:
            styles[style_name] = pics
    except:
        # print(f"No folder: {style_name}")
        pass

with open("pic_names.json", "w") as outfile:
    json.dump(styles, outfile)
