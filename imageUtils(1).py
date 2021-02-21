import numpy as np
import math

def wrapImageData(imageDate, top=1, bottom=1, left=1, right=1):
    shape = imageDate.shape

    newHeight = shape[0] + top + bottom
    newWidth = shape[1] + left + right

    newShape = (newHeight, newWidth)

    newImageData = np.zeros(newShape)

    newImageData[top:newHeight - bottom, left:newWidth - right] = np.copy(imageDate)

    return newImageData


def dilate(imageData, structureElement, structureElementOrigin):
    structureElementShape = structureElement.shape

    top = structureElementOrigin[0]

    bottom = structureElementShape[0] - top - 1

    left = structureElementOrigin[1]

    right = structureElementShape[1] - left - 1

    wrappedImageData = wrapImageData(imageData, top, bottom, left, right)

    wrappedImageDataShape = wrappedImageData.shape

    newImageData = np.zeros(wrappedImageData.shape)

    for i in range(top, wrappedImageDataShape[0] - bottom):
        for t in range(left, wrappedImageDataShape[1] - right):
            if wrappedImageData[i, t] == 1:
                c1 = i - structureElementOrigin[0]
                c2 = t - structureElementOrigin[1]

                d = wrappedImageData[c1: c1 + structureElementShape[0], c2:c2 + structureElementShape[1]]

                c = d + structureElement

                c[c > 0] = 1

                newImageData[c1: c1 + structureElementShape[0], c2:c2 + structureElementShape[1]] = c

    result = newImageData[top:wrappedImageDataShape[0] - bottom, left:wrappedImageDataShape[1] - right]

    result = result.astype(int)

    return result

def erode(imageData, structureElement, structureElementOrigin):
    structureElementShape = structureElement.shape

    top = structureElementOrigin[0]

    bottom = structureElementShape[0] - top - 1

    left = structureElementOrigin[1]

    right = structureElementShape[1] - left - 1

    wrappedImageData = wrapImageData(imageData, top, bottom, left, right)

    wrappedImageDataShape = wrappedImageData.shape

    newImageData = np.zeros(wrappedImageData.shape)

    for i in range(top, wrappedImageDataShape[0] - bottom):
        for t in range(left, wrappedImageDataShape[1] - right):
            c1 = i - structureElementOrigin[0]
            c2 = t - structureElementOrigin[1]

            d = wrappedImageData[c1: c1 + structureElementShape[0], c2:c2 + structureElementShape[1]]

            check = (d == structureElement).all()

            if check:
                newImageData[i, t] = 1

    result = newImageData[top:wrappedImageDataShape[0] - bottom, left:wrappedImageDataShape[1] - right]

    return result

def close(imageData, structureElement, structureElementOrigin):
    dilatedImageData = dilate(imageData, structureElement, structureElementOrigin)

    erodedImageData = erode(dilatedImageData, structureElement, structureElementOrigin)

    return erodedImageData

def open(imageData, structureElement, structureElementOrigin):
    erodedImageData = erode(imageData, structureElement, structureElementOrigin)

    dilatedImageData = dilate(erodedImageData, structureElement, structureElementOrigin)

    return dilatedImageData

def calAreaAndCentroid(imageData, index):
    area = len(imageData[imageData == index])

    shape = imageData.shape

    x = 0
    y = 0

    for i in range(shape[0]):
        row = imageData[i, :]

        size = len(row[row == index])

        x = x + size * i

    x = x / area

    x = round(x, 2)

    for i in range(shape[1]):
        col = imageData[:, i]

        size = len(col[col == index])

        y = y + size * i

    y = y / area

    y = round(y, 2)

    centroid = [x, y]

    return area, centroid

def calPerimeter(imageData, index, useEightConnectivity=False):
    wrappedImageData = wrapImageData(imageData)

    shape = wrappedImageData.shape

    perimeterData = np.zeros(shape)

    for i in range(1, shape[0] - 1):
        for t in range(1, shape[1] - 1):
            d = wrappedImageData[i, t]

            if d == index:
                up = wrappedImageData[i - 1, t]
                down = wrappedImageData[i + 1, t]
                left = wrappedImageData[i, t - 1]
                right = wrappedImageData[i, t + 1]

                checkFourConnectivity = (up == 0) or (down == 0) or (left == 0) or (right == 0)

                check = checkFourConnectivity

                if useEightConnectivity:
                    upLeft = wrappedImageData[i - 1, t - 1]
                    upRight = wrappedImageData[i - 1, t + 1]
                    downLeft = wrappedImageData[i + 1, t - 1]
                    downRight = wrappedImageData[i + 1, t + 1]

                    checkEightConnectivity = upLeft == 0 or upRight == 0 or downLeft == 0 or downRight == 0

                    check = checkFourConnectivity or checkEightConnectivity

                if check:
                    perimeterData[i, t] = 1
    length = 0

    if useEightConnectivity:
        length = calPerimeterLengthForEightConnectivity(perimeterData)
    else:
        length = calPerimeterLengthForFourConnectivity(perimeterData)

    length = round(length, 2)

    result = perimeterData[1: shape[0] - 1, 1: shape[1] - 1]

    return result, length

def calPerimeterLengthForFourConnectivity(perimeterData):
    shape = perimeterData.shape

    length = 0

    perimeterDataCopy = perimeterData.copy()

    startPoint = ()

    found = False

    for i in range(1, shape[0] - 1):
        for t in range(1, shape[1] - 1):
            if perimeterDataCopy[i, t] == 1:
                startPoint = (i, t)

                found = True

                break

        if found:
            break

    currentPoint = startPoint

    while True:
        nextPoint = ()

        upPoint = (currentPoint[0] - 1, currentPoint[1])
        upRightPoint = (currentPoint[0] - 1, currentPoint[1] + 1)
        rightPoint = (currentPoint[0], currentPoint[1] + 1)
        downRightPoint = (currentPoint[0] + 1, currentPoint[1] + 1)
        downPoint = (currentPoint[0] + 1, currentPoint[1])
        downLeftPoint = (currentPoint[0] + 1, currentPoint[1] - 1)
        leftPoint = (currentPoint[0], currentPoint[1] - 1)
        upLeftPoint = (currentPoint[0] - 1, currentPoint[1] - 1)

        slope = False

        if (perimeterDataCopy[upPoint] == 1 or perimeterDataCopy[upRightPoint] == 1 or perimeterDataCopy[rightPoint] == 1) and (perimeterDataCopy[leftPoint] != 1 and perimeterDataCopy[upLeftPoint] != 1):
            if perimeterDataCopy[upPoint] == 1:
                nextPoint = upPoint
            elif perimeterDataCopy[upRightPoint] == 1:
                nextPoint = upRightPoint

                slope = True
            else:
                nextPoint = rightPoint
        elif (perimeterDataCopy[rightPoint] == 1 or perimeterDataCopy[downRightPoint] == 1 or perimeterDataCopy[downPoint] == 1) and (perimeterDataCopy[upPoint] != 1 and perimeterDataCopy[upRightPoint] != 1):
            if perimeterDataCopy[rightPoint] == 1:
                nextPoint = rightPoint
            elif perimeterDataCopy[downRightPoint] == 1:
                nextPoint = downRightPoint

                slope = True
            else:
                nextPoint = downPoint
        elif (perimeterDataCopy[downPoint] == 1 or perimeterDataCopy[downLeftPoint] == 1 or perimeterDataCopy[leftPoint] == 1) and (perimeterDataCopy[rightPoint] != 1 and perimeterDataCopy[downRightPoint] != 1):
            if perimeterDataCopy[downPoint] == 1:
                nextPoint = downPoint
            elif perimeterDataCopy[downLeftPoint] == 1:
                nextPoint = downLeftPoint

                slope = True
            else:
                nextPoint = leftPoint
        elif (perimeterDataCopy[leftPoint] == 1 or perimeterDataCopy[upLeftPoint] == 1 or perimeterDataCopy[upPoint] == 1) and (perimeterDataCopy[downPoint] != 1 and perimeterDataCopy[downLeftPoint] != 1):
            if perimeterDataCopy[leftPoint] == 1:
                nextPoint = leftPoint
            elif perimeterDataCopy[upLeftPoint] == 1:
                nextPoint = upLeftPoint

                slope = True
            else:
                nextPoint = upPoint

        if slope:
            length = length + math.sqrt(2)
        else:
            length = length + 1

        if nextPoint == startPoint or nextPoint == ():
            break

        perimeterDataCopy[currentPoint] = 2

        currentPoint = nextPoint

    return length

def calPerimeterLengthForEightConnectivity(perimeterData):
    shape = perimeterData.shape

    length = 0

    perimeterDataCopy = perimeterData.copy()

    startPoint = ()

    found = False

    for i in range(1, shape[0] - 1):
        for t in range(1, shape[1] - 1):
            if perimeterDataCopy[i, t] == 1:
                startPoint = (i, t)

                found = True

                break

        if found:
            break

    currentPoint = startPoint

    while True:
        nextPoint = ()

        upPoint = (currentPoint[0] - 1, currentPoint[1])
        rightPoint = (currentPoint[0], currentPoint[1] + 1)
        downPoint = (currentPoint[0] + 1, currentPoint[1])
        leftPoint = (currentPoint[0], currentPoint[1] - 1)

        if (perimeterDataCopy[upPoint] == 1 or perimeterDataCopy[rightPoint]) == 1 and perimeterDataCopy[
            leftPoint] != 1:
            if perimeterDataCopy[upPoint] == 1:
                nextPoint = upPoint
            else:
                nextPoint = rightPoint
        elif (perimeterDataCopy[rightPoint] == 1 or perimeterDataCopy[downPoint] == 1) and perimeterDataCopy[
            upPoint] != 1:
            if perimeterDataCopy[rightPoint] == 1:
                nextPoint = rightPoint
            else:
                nextPoint = downPoint
        elif (perimeterDataCopy[downPoint] == 1 or perimeterDataCopy[leftPoint] == 1) and perimeterDataCopy[
            rightPoint] != 1:
            if perimeterDataCopy[downPoint] == 1:
                nextPoint = downPoint
            else:
                nextPoint = leftPoint
        elif (perimeterDataCopy[leftPoint] == 1 or perimeterDataCopy[upPoint] == 1) and perimeterDataCopy[
            downPoint] != 1:
            if perimeterDataCopy[leftPoint] == 1:
                nextPoint = leftPoint
            else:
                nextPoint = upPoint

        if nextPoint == ():
            minDistanceToStartPointPoint = ()
            minDistanceToStartPoint = 0

            continueFind = True

            if perimeterDataCopy[upPoint] == 2:
                distanceToStartPoint = math.pow((upPoint[0] - startPoint[0]), 2) + math.pow(
                    (upPoint[1] - startPoint[1]), 2)

                if minDistanceToStartPoint == 0 or distanceToStartPoint < minDistanceToStartPoint:
                    minDistanceToStartPointPoint = upPoint
                    minDistanceToStartPoint = distanceToStartPoint

                    if distanceToStartPoint == 0:
                        continueFind = False

            if perimeterDataCopy[rightPoint] == 2:
                distanceToStartPoint = math.pow((rightPoint[0] - startPoint[0]), 2) + math.pow(
                    (rightPoint[1] - startPoint[1]), 2)

                if continueFind and minDistanceToStartPoint == 0 or distanceToStartPoint < minDistanceToStartPoint:
                    minDistanceToStartPointPoint = rightPoint
                    minDistanceToStartPoint = distanceToStartPoint

                    if distanceToStartPoint == 0:
                        continueFind = False

            if perimeterDataCopy[downPoint] == 2:
                distanceToStartPoint = math.pow((downPoint[0] - startPoint[0]), 2) + math.pow(
                    (downPoint[1] - startPoint[1]), 2)

                if continueFind and minDistanceToStartPoint == 0 or distanceToStartPoint < minDistanceToStartPoint:
                    minDistanceToStartPointPoint = downPoint
                    minDistanceToStartPoint = distanceToStartPoint

                    if distanceToStartPoint == 0:
                        continueFind = False

            if perimeterDataCopy[leftPoint] == 2:
                distanceToStartPoint = math.pow((leftPoint[0] - startPoint[0]), 2) + math.pow(
                    (leftPoint[1] - startPoint[1]), 2)

                if continueFind and minDistanceToStartPoint == 0 or distanceToStartPoint < minDistanceToStartPoint:
                    minDistanceToStartPointPoint = leftPoint
                    minDistanceToStartPoint = distanceToStartPoint

            nextPoint = minDistanceToStartPointPoint

        length = length + 1

        if nextPoint == startPoint:
            break

        perimeterDataCopy[currentPoint] = 2

        currentPoint = nextPoint

    return length

def calC1(imageData, index, useEightConnectivity=False):
    areaAndCentroid = calAreaAndCentroid(imageData, index)

    area = areaAndCentroid[0]

    perimeterInfo = calPerimeter(imageData, index, useEightConnectivity)

    perimeterLength = perimeterInfo[1]

    c1 = math.pow(perimeterLength, 2) / area

    c1 = round(c1, 2)

    return c1

def calC2(imageData, index, useEightConnectivity=False):
    areaAndCentroid = calAreaAndCentroid(imageData, index)

    centroid = areaAndCentroid[1]

    perimeterInfo = calPerimeter(imageData, index, useEightConnectivity)

    perimeterData = perimeterInfo[0]

    shape = perimeterData.shape

    k = 0

    ur = 0

    for i in range(shape[0]):
        for t in range(shape[1]):
            if perimeterData[i, t] == 1:
                ur = ur + math.sqrt(math.pow(i - centroid[0], 2) + math.pow(t - centroid[1], 2))

                k = k + 1

    ur = ur / k

    theRSquare = 0

    for i in range(shape[0]):
        for t in range(shape[1]):
            if perimeterData[i, t] == 1:
                theRSquare = theRSquare + math.pow(math.sqrt(math.pow(i - centroid[0], 2) + math.pow(t - centroid[1], 2)) - ur, 2)

    theRSquare = theRSquare / k

    theR = math.sqrt(theRSquare)

    c2 = ur / theR

    c2 = round(c2, 2)

    return c2

def calBoundingBoxAndExtremalPoints(imageData, index):
    imageDataCope = imageData.copy()

    shape = imageDataCope.shape

    boundingBox = np.zeros(shape)

    topmostLeft = ()

    found = False

    for i in range(shape[0]):
        for t in range(shape[1]):
            d = imageData[i, t]

            if d == index:
                topmostLeft = (i, t)

                boundingBox[topmostLeft] = 1

                found = True

                break
        if found:
            break

    topmostRight = ()

    found = False

    for i in range(shape[0]):
        for t in range(shape[1] - 1, -1, -1):
            d = imageData[i, t]

            if d == index:
                topmostRight = (i, t)

                boundingBox[topmostRight] = 1

                found = True

                break
        if found:
            break

    bottommostLeft = ()

    found = False

    for i in range(shape[0 - 1] - 1, -1, -1):
        for t in range(shape[1]):
            d = imageData[i, t]

            if d == index:
                bottommostLeft = (i, t)

                boundingBox[bottommostLeft] = 1

                found = True

                break
        if found:
            break

    bottommostRight = ()

    found = False

    for i in range(shape[0] - 1, -1, -1):
        for t in range(shape[1] - 1, -1, -1):
            d = imageData[i, t]

            if d == index:
                bottommostRight = (i, t)

                boundingBox[bottommostRight] = 1

                found = True

                break
        if found:
            break

    leftmostTop = ()

    found = False

    for t in range(shape[1]):
        for i in range(shape[0]):
            d = imageData[i, t]

            if d == index:
                leftmostTop = (i, t)

                boundingBox[leftmostTop] = 1

                found = True

                break
        if found:
            break

    leftmostBottom = ()

    found = False

    for t in range(shape[1]):
        for i in range(shape[0] - 1, -1, -1):
            d = imageData[i, t]

            if d == index:
                leftmostBottom = (i, t)

                boundingBox[leftmostBottom] = 1

                found = True

                break
        if found:
            break

    rightmostTop = ()

    found = False

    for t in range(shape[1] - 1, -1, -1):
        for i in range(shape[0]):
            d = imageData[i, t]

            if d == index:
                rightmostTop = (i, t)

                boundingBox[rightmostTop] = 1

                found = True

                break
        if found:
            break

    rightmostBottom = ()

    found = False

    for t in range(shape[1] - 1, -1, -1):
        for i in range(shape[0] - 1, -1, -1):
            d = imageData[i, t]

            if d == index:
                rightmostBottom = (i, t)

                boundingBox[rightmostBottom] = 1

                found = True

                break
        if found:
            break

    boundingBox[topmostLeft[0], leftmostTop[1]:rightmostTop[1] + 1] = 1

    boundingBox[bottommostLeft[0], leftmostBottom[1]:rightmostBottom[1] + 1] = 1

    boundingBox[topmostLeft[0]:bottommostLeft[0] + 1, leftmostTop[1]] = 1

    boundingBox[topmostRight[0]:bottommostRight[0] + 1, rightmostTop[1]] = 1

    mostPositionPoints = [
        topmostLeft, topmostRight,
        bottommostLeft, bottommostRight,
        leftmostTop, leftmostBottom,
        rightmostTop, rightmostBottom]

    distanceTopLeftToBottomRight = calTwoPointsDistance(topmostLeft, bottommostRight)
    distanceTopRightToBottomLeft = calTwoPointsDistance(topmostRight, bottommostLeft)
    distanceLeftTopToRightBottom = calTwoPointsDistance(leftmostTop, rightmostBottom)
    distanceLeftBottomToRightTop = calTwoPointsDistance(leftmostBottom, rightmostTop)

    extremalAxisLengths = [
        distanceTopLeftToBottomRight, distanceTopRightToBottomLeft, distanceLeftTopToRightBottom,
        distanceLeftBottomToRightTop]

    boundingBox = boundingBox.astype(int)

    return mostPositionPoints, extremalAxisLengths, boundingBox

def calTwoPointsDistance(firstPoint, secondPoint):
    distance = np.linalg.norm(np.array(firstPoint) - np.array(secondPoint))

    Q = 1

    if firstPoint[0] != secondPoint[0] and firstPoint[1] != secondPoint[1]:
        tan = abs(firstPoint[0] - secondPoint[0]) / abs(firstPoint[1] - secondPoint[1])

        angle = abs(math.atan(tan))

        if angle < (math.pi / 4):
            Q = 1 / abs(math.cos(angle))
        else:
            Q = 1 / abs(math.sin(angle))

    distance = distance + Q

    distance = round(distance, 2)

    return distance

def calSecondMoments(imageData, index):
    areaAndCentroid = calAreaAndCentroid(imageData, index)

    centroid = areaAndCentroid[1]

    shape = imageData.shape

    A = 0

    urr = 0
    urc = 0
    ucc = 0

    for i in range(shape[0]):
        for t in range(shape[1]):
            d = imageData[i, t]

            if d == index:
                A = A + 1

                r = i - centroid[0]
                c = t - centroid[1]

                urr = urr + math.pow(r, 2)
                urc = urc + r * c
                ucc = ucc + math.pow(c, 2)

    urr = round(urr / A, 2)
    urc = round(urc / A, 2)
    ucc = round(ucc / A, 2)

    return urr, urc, ucc

def calAxisOfLeastInertia(imageData, index):
    urr, urc, ucc = calSecondMoments(imageData, index)

    result = (2 * urc) / (urr - ucc)

    result = round(result, 2)

    return result
