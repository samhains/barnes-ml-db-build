import requests
import os
import json

headers = {"Ocp-Apim-Subscription-Key": "#"}
SIZE_OF_BING_IMAGE_BATCH = 150


def retrieve_images_for_class(tag_name):
    i = 0
    start = 0
    if not os.path.exists(tag_name):
        os.mkdir(tag_name) 

    url = "https://api.cognitive.microsoft.com/bing/v5.0/images/search?q={}&count=150&offset={}&mkt=en-us".format(tag_name, start)
    r = requests.get(url, headers=headers).json()
    num_images_in_class = r["totalEstimatedMatches"]
    print('tagname:', tag_name, 'has:', num_images_in_class)

    while i < num_images_in_class:
        items = r["value"]
        j = 0

        gen = (item for item in items if j < SIZE_OF_BING_IMAGE_BATCH)
        for item in gen:
            i = i+1
            j = j+1
            print('saving image:',i)
            image_url = item["contentUrl"]

            fmt = "."+item["encodingFormat"]
            print(fmt)
            img_data = requests.get(image_url).content
            with open("./{}/{}_{}{}".format(tag_name,tag_name,i,fmt), 'wb') as handler:
                handler.write(img_data)

        start = start + SIZE_OF_BING_IMAGE_BATCH
        url = "https://api.cognitive.microsoft.com/bing/v5.0/images/search?q={}&count=150&offset={}&mkt=en-us".format(tag_name, start)
        r = requests.get(url, headers=headers).json()
        print('next url starts with:',start)

file = open("barnes_labels.txt","r") 
labels = set(file.read().split(','))
labels = [tag.strip().replace(' ', '+') for tag in labels if tag != ""]

for label in labels:
    retrieve_images_for_class(label)
