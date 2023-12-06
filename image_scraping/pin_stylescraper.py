import pinscrape
import json

f = open('base_style_data.json')
data = json.load(f)
f.close()
# for style in data["styles"][300:300]:
#     style_name = style["name"]
#     print(style_name + "-fashion")
#     details = pinscrape.scraper.scrape(style_name + "fashion-clothing", "style_images/" + style_name, {}, 10, 20)
#     if not details["isDownloaded"]:
#         print("\n\n**ERROR IN DOWNLOADING STYLE**\n\n")

# style_name = ""
# print(style_name + "-fashion")
# details = pinscrape.scraper.scrape(style_name + "fashion-clothing", "sam_style_images/Worked/" + style_name, {}, 10, 20)
# if not details["isDownloaded"]:
#     print("\n\n**ERROR IN DOWNLOADING STYLE**\n\n")