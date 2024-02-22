# -*- coding: utf-8 -*-
"""Fashion_Object_Labeling-Miniproject.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DISc8lliEJWP5_s2mAPpAuR0s085Dtaf
"""

from google.colab import drive
drive.mount('/content/drive')

# Install ultralytics
!pip install ultralytics

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

import numpy as np
import matplotlib.pyplot as plt
import random
import os
import cv2
import shutil
import tqdm
import glob

# Check the runtime type
import torch
print(f"Using torch {torch.__version__} ({torch.cuda.get_device_properties(0).name if torch.cuda.is_available() else 'CPU'})")

images_path = '/content/drive/MyDrive/Dataset/Fashion/JPEGImages/'
annotations_path  = '/content/drive/MyDrive/Dataset/Fashion/Annotations_txt/'
path = '/content/drive/MyDrive/Dataset/Fashion/'

from ultralytics import YOLO

# loading the model
detection_model = YOLO("/content/yolov8m.pt")

# choose random image
img = random.choice(os.listdir(images_path))

i=detection_model.predict(source='https://i.stack.imgur.com/GRdCC.jpg', conf=0.5, save=True, line_width=2, show_labels=False)

im = plt.imread('/content/runs/detect/predict/GRdCC.jpg')
plt.figure(figsize=(20,10))
plt.axis('off')
plt.imshow(im)

def convert(size,x,y,w,h):
    box = np.zeros(4)
    dw = 1./size[0]
    dh = 1./size[1]
    x = x/dw
    w = w/dw
    y = y/dh
    h = h/dh
    box[0] = x-(w/2.0)
    box[1] = x+(w/2.0)
    box[2] = y-(h/2.0)
    box[3] = y+(h/2.0)

    return (box)

def plot_annotations(img, filename):
    with open(annotations_path+filename, 'r') as f:
        for line in f:
            value = line.split()
            cls = int(value[0])
            x = float(value[1])
            y = float(value[2])
            w = float(value[3])
            h = float(value[4])

            img_h, img_w = img.shape[:2]
            bb = convert((img_w, img_h), x,y,w,h)
            cv2.rectangle(img, (int(round(bb[0])),int(round(bb[2]))),(int(round(bb[1])),int(round(bb[3]))),(255,0,0),2)
            plt.axis('off')
            plt.imshow(img)

import os
import random
import matplotlib.pyplot as plt
import cv2
import numpy as np

plt.figure(figsize=(20,12))
ls = os.listdir('/content/drive/MyDrive/Dataset/Fashion/JPEGImages')
c = 1

for i in random.sample(ls, 10):
    img = plt.imread ('/content/drive/MyDrive/Dataset/Fashion/JPEGImages/'+i)
    i = i.rstrip('.jpg') + '.txt'
    plt.subplot(2,5, c)
    plot_annotations(img, i)
    c+=1

train = []
with open(path+'ImageSets/Main/trainval.txt', 'r') as f:
    for line in f.readlines():
        if line[-1]=='\n':
            line = line[:-1]
        train.append(line)

test = []
with open(path+'ImageSets/Main/test.txt', 'r') as f:
    for line in f.readlines():
        if line[-1]=='\n':
            line = line[:-1]
        test.append(line)

len(train), len(test)

os.mkdir('/content/drive/MyDrive/Dataset/Fashion/working')
os.mkdir('/content/drive/MyDrive/Dataset/Fashion/working/train')
os.mkdir('/content/drive/MyDrive/Dataset/Fashion/working/train/images')
os.mkdir('/content/drive/MyDrive/Dataset/Fashion/working/train/labels')

os.mkdir('/content/drive/MyDrive/Dataset/Fashion/working/test')
os.mkdir('/content/drive/MyDrive/Dataset/Fashion/working/test/images')
os.mkdir('/content/drive/MyDrive/Dataset/Fashion/working/test/labels')

train_path = '/content/drive/MyDrive/Dataset/Fashion/working/train/'
test_path = '/content/drive/MyDrive/Dataset/Fashion/working/test/'

print('Copying Train Data..!!')
print(images_path)
print(train_path)

for i in tqdm.tqdm(train):
    a = shutil.copyfile(images_path+i+'.jpg', train_path+'images/'+i+'.jpg')
    a = shutil.copyfile(annotations_path+i+'.txt', train_path+'labels/'+i+'.txt')

print('Copying Test Data..!!')
for i in tqdm.tqdm(test):
    a = shutil.copyfile(images_path+i+'.jpg', test_path+'images/'+i+'.jpg')
    a = shutil.copyfile(annotations_path+i+'.txt', test_path+'labels/'+i+'.txt')

text = """
train: /content/drive/MyDrive/Dataset/Fashion/working/train/
val: /content/drive/MyDrive/Dataset/Fashion/working/test/

# number of classes
nc: 10

# class names
names: ['sunglass','hat','jacket','shirt','pants','shorts','skirt','dress','bag','shoe']
"""
with open("/content/data.yaml", 'w') as file:
    file.write(text)

model = YOLO("/content/yolov8m.pt")

model.train(data='/content/data.yaml', epochs=5)

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt

# %matplotlib inline
model_path = '/content/runs/detect/train/'

def plot(ls, size):
    c=1
    plt.figure(figsize=(15,10))
    for im in ls:
        plt.subplot(size[0],size[1],c)
        im = plt.imread(model_path+im)
        plt.imshow(im)
        c+=1
    plt.show()

plot(['P_curve.png','R_curve.png'], (1,2))
plot(['F1_curve.png','PR_curve.png'], (1,2))
plot(['confusion_matrix.png','labels.jpg'], (1,2))
plot(['results.png'],(1,1))

# choose random image from dataset

plt.figure(figsize=(20,20))
imgs = random.sample(os.listdir(images_path), 6)
c=1
print(os.getcwd())
for img in imgs:
    i=model.predict(source=images_path+img, exist_ok = True, conf=0.4, save=True, line_width=2, project="/content/runs/detect/", name = 'predict2')
    im = plt.imread('/content/runs/detect/predict2/'+img)
    plt.subplot(2,3,c)
    plt.axis('off')
    plt.imshow(im)
    c+=1

from google.colab import files
from IPython.display import Image

# Upload an image file
uploaded = files.upload()

# Get the filename of the uploaded image
uploaded_file = list(uploaded.keys())[0]

# Display the uploaded image with a specific width and height
Image(filename=uploaded_file,height=400)

plt.figure(figsize=(20,20))
c=1
print(os.getcwd())
i=model.predict(source=uploaded_file, exist_ok = True, conf=0.4, save=True, line_width=2, project="/content/runs/detect/", name = 'predict2')
im = plt.imread('/content/runs/detect/predict2/'+uploaded_file)
plt.subplot(2,3,c)
plt.axis('off')
plt.imshow(im)
c+=1

import pickle

def find_unpicklable_objects(obj):
    """
    Recursively finds unpicklable objects within a nested structure.

    Args:
        obj: The object to inspect.

    Returns:
        A list of unpicklable objects.
    """

    unpicklable_objects = []

    def check_picklable(o):
        try:
            pickle.dumps(o)
        except Exception as e:
            if isinstance(e, pickle.PickleError):
                unpicklable_objects.append(o)

    if isinstance(obj, dict):
        for value in obj.values():
            check_picklable(value)
    elif isinstance(obj, list):
        for item in obj:
            check_picklable(item)
    else:
        check_picklable(obj)

    return unpicklable_objects

unpicklable_objects = find_unpicklable_objects(model)

for obj in unpicklable_objects:
    print(f"Unpicklable object: {obj}")