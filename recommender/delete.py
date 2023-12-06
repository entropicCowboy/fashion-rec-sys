import json
import random
ROOT_PATH = "../image_scraping/style_images/"



class Style:
    def __init__(self, name: str):
        self.name = name
        self.path = ROOT_PATH + self.name + "/"
        self.pics = os.listdir(self.path) # a list of the pic names in the style's folder
        self.num_pics = len(self.pics) # the number of pics the style has in its folder
        self.pics_left = self.pics # the pics that haven't been shown
        self.num_pics_left = self.num_pics # the number of pics that haven't been shown
        self.ratio = 0
        self.has_pics = True
    
    """Picks random image that has not yet been shown from its stash"""
    def get_image(self) -> str:
        if self.has_pics == False:
            raise Exception("No images left to show")
        index = random.randint(0,self.num_pics_left-1)
        # decrement num pics left
        self.num_pics_left -= 1
        if self.num_pics_left == 0:
            self.has_pics = False
        # remove and return style pic
        return self.pics_left.pop(index)
    
    """Updates the style's ratio
        state: 1 if the user liked the image, -1 if they disliked the image"""
    def update_ratio(self, status:int) -> None:
        if status != 1 and status != -1:
            raise Exception("State must be equal to 1 or -1")
        self.ratio += status/self.num_pics
    
    """Updates the equilibrium based on the style's ratio and returns whether that style can be chosen for the user"""
    def equil_reached(self) -> bool:
        # if the style has 5 or less pictures, all must be liked by the user
        if self.num_pics < 6:
            if self.ratio == 1:
                return True
        # if the styles has less than 10 pictures, a greater majority must be liked by the user
        elif self.num_pics < 10:
            if self.ratio >= 0.5:
                return True
        else:
            if self.num_pics >= 0.7:
                return True
        return False

styles = {}

# load keywords
f = open('keywords.json')
data = json.load(f)
f.close()
# load clusters
f = open('clusters.json')
global clusters
clusters = json.load(f)
f.close()

cluster_size = 0
style_size = 0

for style_name in list(data.keys())[:300]:
    try:
        style = Style(style_name)
        # if there are photos in the file, add it to the list
        if style.num_pics > 0:
            styles[style_name] = style
            style_size += 1
    except:
        # print(f"No folder: {style_name}")
        pass
styles = {"fantasy": 1, "coastal cowgirl":2, "autumn academia": 3, "earthcore": 4, "country":5, "club":6}
clusters_copy = []
for i in range(len(clusters)):
    clusters_copy.append([])
    for style in clusters[i]:
        if style in styles:
            clusters_copy[i].append(style)
            
print(clusters_copy)
