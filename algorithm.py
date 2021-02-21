import numpy
import math
import matplotlib
from matplotlib import pyplot
from PIL import Image

def imBinary(grayImage, threshold=80):
    binaryImage = numpy.zeros(shape=(grayImage.shape[0], grayImage.shape[1]), dtype=numpy.uint8)
    for i in range(grayImage.shape[0]):
        for j in range(grayImage.shape[1]):
            if grayImage[i][j] > threshold:
                binaryImage[i][j] = 1
            else:
                binaryImage[i][j] = 0
    return binaryImage

def surround(imageOrigin, top, bottom, left, right):
    shape = imageOrigin.shape
    newHeight = shape[0] + 2
    newWidth = shape[1] + 2
    newShape = (newHeight, newWidth)
    newImageData = numpy.zeros(newShape)
    newImageData[top+1: bottom-1, left-1: right+1] = numpy.copy(imageOrigin)
    return newImageData

def dilate(imageData, structuringElementOrigin, structuringElement):
    structuringElementHeight = structuringElement.shape[0]
    structuringElementWidth = structuringElement.shape[1]
    dilateImage = numpy.zeros(shape=imageData.shape)
    for i in range(structuringElementOrigin[0], imageData.shape[0]-structuringElementHeight+structuringElementOrigin[0]+1):
        for j in range(structuringElementOrigin[1], imageData.shape[1]-structuringElementWidth+structuringElementOrigin[1]+1):
            a = imageData[i-structuringElementOrigin[0] : i-structuringElementOrigin[0]+structuringElementHeight,
                j-structuringElementOrigin[1] : j-structuringElementOrigin[1]+structuringElementWidth]
            dilateImage[i, j] = numpy.max(a * structuringElement)
    return dilateImage

def erode(imageData, structuringElementOrigin, structuringElement):
    structuringElementHeight = structuringElement.shape[0]
    structuringElementWidth = structuringElement.shape[1]
    erodeImage = numpy.zeros(shape=imageData.shape)
    for i in range(structuringElementOrigin[0], imageData.shape[0]-structuringElementHeight+structuringElementOrigin[0]+1):
        for j in range(structuringElementOrigin[1], imageData.shape[1]-structuringElementWidth+structuringElementOrigin[1]+1):
            a = imageData[i-structuringElementOrigin[0] : i-structuringElementOrigin[0]+structuringElementHeight,
                j-structuringElementOrigin[1] : j-structuringElementOrigin[1]+structuringElementWidth]
            if numpy.sum(a * structuringElement) == numpy.sum(structuringElement):  #Determine whether overlap
                erodeImage[i, j] = 1
    return erodeImage

def open(imageData, structuringElementOrigin, structuringElement):
    erodeImageData = erode(imageData, structuringElementOrigin, structuringElement)
    dilateImageData = dilate(erodeImageData, structuringElementOrigin, structuringElement)
    return dilateImageData

def close(imageData, structuringElementOrigin, structuringElement):
    dilateImageData = dilate(imageData, structuringElementOrigin, structuringElement)
    erodeImageData = erode(dilateImageData, structuringElementOrigin, structuringElement)
    return erodeImageData

def areaCentroid(imageData, index):
    area = len(imageData[imageData == index])
    shape = imageData.shape
    x = 0
    y = 0
    for i in range(shape[0]):
        row = imageData[i, :]
        numberOfOne = len(row[row == index])
    x = (x + numberOfOne * i) / area
    x = round(x, 2)

    for j in range(shape[1]):
        column = imageData[:, j]
        numberOfOne = len(column[column == index])
    y = (y + numberOfOne * j) / area
    y =round (y, 2)

    centroid = [x, y]

    return area
    return centroid


def perimeter():
    pass

def perimeterFour():
    pass

def perimeterEight():
    pass

# def circularity1(imageData, index, ):
#     areaSize = areaCentroid(imageData, index)
#     area = areaSize[0]
#     perimeterData = perimeter()
#     perimeterLength = perimeterData[0]
#     perimeterLengthSquare = numpy.square(perimeterLength)
#     c1 = perimeterLengthSquare / area
#     c1 = round(c1, 2)
#     return c1

# def circularity2(imageData, index, ):
#     centroidSize = areaCentroid(imageData, index)
#     centroid = centroidSize[1]
#     perimeterData = perimeter()
#     perimeterCollection = perimeterData[1]
#     perimeterShape = perimeterCollection.shape
#     k = 0
#     muR = 0
#     for i in range(perimeterShape[0]):
#         for j in range(perimeterShape[1]):
#             x = i - centroid[0]
#             y = j - centroid[1]
#             xSquare = numpy.square(x)
#             ySquare = numpy.square(y)
#             averageCoordinate = numpy.sqrt(xSquare + ySquare)
#             muR = muR +averageCoordinate
#             k = k + 1
#     muR = muR / k

#     sigmaRSquare = 0
#     for i in range(perimeterShape[0]):
#         for j in range(perimeterShape[1]):
#             x = i - centroid[0]
#             y = j - centroid[1]
#             xSquare = numpy.square(x)
#             ySquare = numpy.square(y)
#             rangeSqrt = numpy.sqrt(xSquare + ySquare)
#             rangeCoordinate = numpy.square(rangeSqrt - muR)
#             sigmaRSquare = sigmaRSquare + rangeCoordinate
#     sigmaRSquare = sigmaRSquare / k
#     sigmaR = numpy.sqrt(sigmaRSquare)

#     c2 = muR / sigmaR
#     c2 = round(c2, 2)
#     return c2


