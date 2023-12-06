from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
import nltk.downloader
import json
# import nltk.text

f = open('base_style_data.json')
# loads as a list of dictionaries
data = json.load(f)
f.close()

all_key_descriptors = {}

for style in data:
    descs = style["descriptions"]
    key_descriptors = []
    tagged_words = []
    adjs = []

    # for each description item in descriptions
    for desc in descs:    
        # split into separate words
        tokenized = word_tokenize(desc)
        # if desc was likely describing an article of clothing, add it as is
        if (len(tokenized) <= 4) and (tokenized[0] != '['):
            key_descriptors.append(desc)
        # otherwise, tag parts of speech
        else:
            tagged = pos_tag(tokenized)
            for tup in tagged:
                tagged_words.append(tup)

    # # next, tokenize and tag colors, which could be a single string or a list of strings
    # colors = style["key_colors"]
    # try:
    #     tagged = pos_tag(word_tokenize(colors))
    #     for tup in tagged:
    #         tagged_words.append(tup)
    # except:
    #     for color in colors:
    #         tagged = pos_tag(word_tokenize(colors))
    #         for tup in tagged:
    #             tagged_words.append(tup)

    # pick out key adjs (JJs) in tagged
    adj_tokens = ["JJ", "JJR", "JJS"]
    for tup in tagged_words:
        word = tup[0]
        if (tup[1] in adj_tokens) and (word not in adjs):
            adjs.append(word)
            key_descriptors.append(word)
    
    # # now add in related aesthetics and brands
    # # split on ',' if necessary (both can consist of multiple words)
    # aesthetics = style["rel_aesthetics"]
    # if type(aesthetics) == str:
    #     aesthetics = aesthetics.split(",")

    # brands = style["brands"]
    # if type(brands) == str:
    #     brands = brands.split(",")

    # key_descriptors = key_descriptors + aesthetics
    # key_descriptors = key_descriptors + brands

    all_key_descriptors[style["name"]] = key_descriptors

with open("key_words.json", "w") as outfile:
    json.dump(all_key_descriptors, outfile)