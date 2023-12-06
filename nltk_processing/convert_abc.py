import json

f = open('base_style_data.json')
# loads as a list of dictionaries
data = json.load(f)
f.close()

# covert aesthetics, brands, and colors to list form
for style in data:
    aesthetics = style["rel_aesthetics"]
    if type(aesthetics) == str:
        style["rel_aesthetics"] = aesthetics.split(",")

    brands = style["brands"]
    if type(brands) == str:
        style["brands"] = brands.split(",")

    colors = style["key_colors"]
    if type(colors) == str:
        style["key_colors"] = colors.split(",")

with open("converteddata.json", "w") as outfile:
    json.dump(data, outfile)