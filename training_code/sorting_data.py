# -*- coding: utf-8 -*-
"""Sorting_Data

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1L1fywClDcpYKGFvITnqIoCIleIWHS9Gw
"""

import numpy as np
import random
import PIL
import pandas as pd
from os import listdir
import IPython.display as IP
import matplotlib.pyplot as plt
from time import sleep
from collections import Counter
import pylab as barplt
from google.colab import drive, files
drive.mount('/content/drive')

#Determine which type a Pokemon will be when sorting into validation, training, testing
#Important for dual type Pokemon
def determinetype(Pokemon):
  return Pokemon[2]
  """
  rand = 0
  if(type(i[3]) != str): #Pokemon only has one type
    return i[2]
  else: #If dual type, 75% chance of returning first type, 25% of returning second
    rand = random.random()
    if rand >= .75:
      return i[3]
    else:
      return i[2]
      """

#Save images to Google Drive
def save_images(data_set, name):
  save = ""
  if name == "Training":
    save = "TrainingData"
  elif name == "Testing":
    save = "TestingData"
  elif name == "Validation":
    save = "ValidationData"
  else:
    save = "TrainingData"
  for PKMN in data_set:
    img = PIL.Image.open(path + PKMN[0])
    img.save('/content/drive/My Drive/' + save + '/' + PKMN[1] + '/' + PKMN[0])

#Generate distribution of Pokemon types in a data set
#dataSet is a list of tuples with each data point
#name is the name of the graph being saved
def generateStats(dataSet, name):
  #Smaller dictionary that stores the types of Pokemon, but only in a data set
  dataset_dict = {}
  for point in dataSet:
    if point[1] not in dataset_dict:
      dataset_dict[point[1]] = []
    temp = dataset_dict[point[1]]
    temp.append(point[0])
    dataset_dict[point[1]] = temp
  sortedlabels = sorted(dataset_dict)
  type_counts = []
  for Ptype in sortedlabels:
    type_counts.append(len(dataset_dict[Ptype]))
  fig, ax = plt.subplots()
  fig.clf()
  fig, ax = plt.subplots()
  plt.bar(list(np.arange(18)), type_counts)
  plt.xlabel("Types")
  plt.ylabel("Occurences")
  plt.title("Type Distribution, " + name + " Set")
  plt.xticks(list(np.arange(18)), sortedlabels, rotation = 90)
  plt.show()
  fig.tight_layout()
  fig.savefig('/content/drive/My Drive/DataStats/' + name + '.jpeg')

#Import spreadsheet
!git clone https://github.com/blucifer22/catchem-all.git
df = pd.read_excel('catchem-all/Pokemon_Classifications_2.xlsx')
matrix = df.values


#Import images from path
#Get list of image names
image_names = listdir('catchem-all/data/pokemon/base_pokemon/')
path = 'catchem-all/data/pokemon/base_pokemon/'

#Sort Pokemon by type. Create dictionary
#Get types

dictionary = {}
for i in matrix:
  if i[2] not in dictionary:
    dictionary[i[2]] = []
  if type(i[3]) == str and i[3] not in dictionary:
    dictionary[i[3]] = []
  PKMNtype = determinetype(i)
  myList = dictionary[PKMNtype]
  myList.append(str(i[0]) + '.jpg')
  dictionary[PKMNtype] = myList

#Sort Pokemon into training, validation, and testing lists
training = []
validation = []
testing = []

#Shuffle the order of the Pokemon in each type list.
#Start adding Pokemon to training, validation, and testing lists
#Then shuffle the training, validation, and testing data sets so they are in random order
dictionaryPokemon = {}
print(image_names)
for i in image_names:
  loc = i.find('.jpg')
  for typeP in dictionary:
    if i[0:loc+4] in dictionary[typeP]:
      if typeP not in dictionaryPokemon:
        dictionaryPokemon[typeP] = []
      myList = dictionaryPokemon[typeP]
      myList.append(i)
      dictionaryPokemon[typeP] = myList
      break #found where the Pokemon should go

for k in dictionaryPokemon:
  newList = dictionaryPokemon[k]
  np.random.shuffle(newList)
  dictionaryPokemon[k] = newList
  counter = 0
  for Poke in newList:
    if counter % 10 < 7:
      training.append((Poke, k))
    elif counter % 10 < 9:
      testing.append((Poke, k))
    else:
      validation.append((Poke, k))
    counter += 1

np.random.shuffle(training)
np.random.shuffle(validation)
np.random.shuffle(testing)

generateStats(training, "Training") 
generateStats(testing, "Testing")
generateStats(validation, "Validation")
generateStats(training + testing + validation, "Whole")
save_images(validation, "Validation")
save_images(training, "Training")
save_images(testing, "Testing")

  
"""

Verify that images are loaded into the program. Try some out
image = PIL.Image.open(path + image_names[250])
plt.imshow(image)
"""