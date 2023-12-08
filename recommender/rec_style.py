import numpy as np
import pandas as pd
import json

styles_df = pd.read_json("finaldata.json")
f = open('keywords.json')
# loads as a list of dictionaries
data = json.load(f)
f.close()
keywords = data.values()

# Replace descriptions with key words
styles_df["keywords"] = keywords
styles_df.drop("descriptions", axis=1, inplace=True)

# Remove spaces in keywords, colors, and brands
styles_df["keywords"] = styles_df["keywords"].apply(lambda x:[i.replace(" ", "") for i in x])
styles_df["key_colors"] = styles_df["key_colors"].apply(lambda x:[i.replace(" ", "") for i in x])
styles_df["brands"] = styles_df["brands"].apply(lambda x:[i.replace(" ", "") for i in x])

# Combine all information into 'tags' and save it in a new dataframe
styles_df["tags"] = styles_df["rel_aesthetics"]+styles_df["key_colors"]+styles_df["brands"]+styles_df["keywords"]
new_df = styles_df[['name', 'tags']]

# Causes problems if it just remains "name"
new_df.rename(columns={'name' : 'style'}, inplace=True)
new_df['tags'] = new_df['tags'].apply(lambda x: ' '.join(x))

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=600, stop_words='english')
cv.fit_transform(new_df['tags']).toarray().shape

vectors = cv.fit_transform(new_df['tags']).toarray()

# Stemmer reduces a word to its stem prefix/suffix/root (lemma)
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

def stem(text):
  y = []
  for i in text.split():
    y.append(ps.stem(i))
  return " ".join(y)

new_df['tags'] = new_df['tags'].apply(stem)

# Measures the similarity between two vectors (often used to measure document similarity in text analysis)
from sklearn.metrics.pairwise import cosine_similarity

similarity = cosine_similarity(vectors)

def recommend(style):
  style_index = new_df[new_df['style']==style].index[0]
  distances = similarity[style_index]
  styles_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

  recommendations = []
  for i in styles_list:
    recommendations.append(new_df.iloc[i[0]].style)
  return recommendations

# save the recommendations for later use
# recommendations = {}
# style_list = list(data.keys())
# for style in style_list:
#   recommendations[style] = recommend(style)
# with open("recommendations.json", "w") as outfile:
#     json.dump(recommendations, outfile)


# Now, create clusters for the fashion styles to aid in the initial photos presented to a user during their test

from sklearn.feature_extraction.text import TfidfTransformer
from scipy.cluster import  hierarchy

# Finish vectorizing
X = cv.fit_transform(new_df['tags']).toarray()

X = TfidfTransformer().fit_transform(X)

# Clustering
X = X.todense()
threshold = 0.94
Z = hierarchy.linkage(X,"average", metric="cosine")
C = hierarchy.fcluster(Z, threshold, criterion="distance")

clusters = {}
for i in range(len(C)):
  cl = C[i]
  if cl in clusters:
    clusters[cl].append(new_df['style'][i])
  else:
    clusters[cl] = [new_df['style'][i]]

cluster_list = list(clusters.values())
with open("clusters.json", "w") as outfile:
    json.dump(cluster_list, outfile)
