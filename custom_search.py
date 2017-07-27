import requests
import sys
import os
import json

headers = {"Ocp-Apim-Subscription-Key": "#"}
SIZE_OF_BING_IMAGE_BATCH = 150


def retrieve_images_for_class(tag_name):
    i = 0
    start = 0
    if not os.path.exists(tag_name):
        os.mkdir(tag_name) 

    num_of_existing_images_in_class = len([name for name in os.listdir(tag_name) if os.path.isfile("./{}/{}".format(tag_name, name))])
    print(num_of_existing_images_in_class)
    if num_of_existing_images_in_class > 1:
        start = num_of_existing_images_in_class
        i = num_of_existing_images_in_class

    url = "https://api.cognitive.microsoft.com/bing/v5.0/images/search?q={}&count=150&offset={}&mkt=en-us".format(tag_name, start)
    try:
        r = requests.get(url, headers=headers).json()
        num_images_in_class = min(int(r["totalEstimatedMatches"]), 2000)
        print("num_images_in_class: ",tag_name, num_images_in_class)
    except requests.exceptions.Timeout:
        print('timeout error!')
    except requests.exceptions.TooManyRedirects:
        print('too many redirects error!')
    except requests.exceptions.RequestException as e:
        print('catastrophic error', e)
    except:
        print("other weird error")

    print('tagname:', tag_name, 'has:', num_of_existing_images_in_class ) 

    while i < num_images_in_class:
        items = r["value"]

        for item in items:
            i = i + 1
            print('saving image:',i)
            image_url = item["contentUrl"]

            fmt = "."+item["encodingFormat"]
            img_file_path = "./{}/{}_{}{}".format(tag_name,tag_name,i,fmt)
            if not os.path.isfile(img_file_path):
                print('image doesnt already exist')
                try:
                    img_data = requests.get(image_url, headers={'user-agent': 'My app'}).content
                    with open(img_file_path, 'wb') as handler:
                        handler.write(img_data)
                except requests.exceptions.Timeout:
                    print('timeout error!')
                except requests.exceptions.TooManyRedirects:
                    print('too many redirects error!')
                except requests.exceptions.RequestException as e:
                    print('catastrophic error', e)

        start = start + SIZE_OF_BING_IMAGE_BATCH
        url = "https://api.cognitive.microsoft.com/bing/v5.0/images/search?q={}&count=150&offset={}&mkt=en-us".format(tag_name, start)
        r = requests.get(url, headers=headers).json()
        print('next url starts with:',start)

file = open("barnes_labels.txt","r") 
labels = file.read().split(',')
labels = [tag.strip().replace(' ', '+') for tag in labels if tag != ""]
labels = sorted(set(labels))

for idx, label in enumerate(labels):
    if label == "" or idx < 15:
        print("done", label)
    else:
        print("starting", idx, label)
        retrieve_images_for_class(label)
