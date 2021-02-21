'''
    File name: CS563_Assignment_1.py
    Group member: ZeYu Wang, Kaili Yang, Hanru Huang
    Date created: 08/02/2020
    Python Version: 3.8.6
    IDE: VS Code
'''

import numpy as np
import matplotlib.pyplot as plt

# Task1: Give a brief greeting and announce its purpose
def init():
    print("Introduction: Welcome to use this image analysis program. Users input the name of the pgm file and the program will return processed data like detected objects and their features. The function is done through the command line.")
    print("Note: Please make sure that the image file and the script are in the same directory.")
    print("")
    
# Task2: Prompt the user for its input
def inputImage():
    imageName = input("Please input the name of the *.pgm image file: ")
    imageUrl = './{imageName}.pgm'.format(imageName=imageName)
    pgmData = readpgm(imageUrl)
    rowData = pgmData[0]
    size = pgmData[1]
    arrData = np.reshape(rowData,size)
    # print(arrData)
    # plt.imshow(arrData)
    # plt.show()
    # setThreshold(arrData, size)
    labelConnectedPixel(arrData)

def readpgm(name):
    with open(name) as f:
        lines = f.readlines()
    # Ignores commented lines
    for l in list(lines):
        if l[0] == '#':
            lines.remove(l)
    # Makes sure it is ASCII format (P2)
    assert lines[0].strip() == 'P2'
    # Converts data to a list of integers
    data = []
    for line in lines[1:]:
        data.extend([int(c) for c in line.split()])   # read the picture
    return (np.array(data[3:]),(data[1],data[0]),data[2])

# Task3: Give clean output of all objects detected and their features
def setThreshold(data, size):
    data_threshold = data
    threshold = int(input("Please input a threshold: "))
    for i in range(len(data)):
        for j in range(len(data[i])):
            data_threshold[i][j] = 255 if data[i][j] > threshold else 0
    plt.imshow(data_threshold)
    plt.show()
    
# Task4: Thresholding and cleaning using morphological filters
def targetObjectes(data):
    pass
    
# Task5: Detect object pixels and perform connected-components labeling of connected pixels
def labelConnectedPixel(data):
    parent = []
    data_negate = data
    for i in range(len(data)):
        for j in range(len(data[i])):
            data_negate[i][j] = -1 if data[i][j] >0 else 0
    print(data_negate)
    
    
    
    
init()
inputImage()

