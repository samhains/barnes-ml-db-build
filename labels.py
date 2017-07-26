file = open("barnes_labels.txt","r") 
arr = set(file.read().split(','))
arr = [tag.strip() for tag in arr if tag != ""]
print(len(arr))

new_file = open('labels.txt', 'w')
for tag in arr:
    new_file.write("{}\n".format(tag))
    
