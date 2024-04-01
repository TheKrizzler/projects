import math
import time
import os

# The following variables can be modified to get different results. Code might break if you do though lmao
CAMERA = (0, 0, 0)
DISTANCE = 50
RESOLUTION = (50, 50)
PIXEL = ("@", "w", "*", "-", ".")

X_EDGE = (int((RESOLUTION[0] - (RESOLUTION[0]/2)) * -1), int(RESOLUTION[0] - (RESOLUTION[0]/2)))
Y_EDGE = (int((RESOLUTION[1] - (RESOLUTION[1]/2)) * -1), int(RESOLUTION[1] - (RESOLUTION[1]/2)))

def pointInFrame(point): # Takes a point in the 3D space, and places it on a 2D grid based on distance from camera.
    updatedPoint = [0,0,0]
    if point[2] >= DISTANCE:
        for i in range(2):
            if point[i] != 0 and point[2] != 0:
                updatedPoint[i] = DISTANCE / (point[2] / point[i])
            else:
                updatedPoint[i] = 0
        updatedPoint[2] = point[2]
    return updatedPoint

def isInFrame(points): # Not in use at the moment, but could come in handy later on
    x, y = round(pointInFrame(points)[0]), round(pointInFrame(points)[1])
    return X_EDGE[0] <= x <= X_EDGE[1] and Y_EDGE[0] <= y <= Y_EDGE[1]

def pointListToFrame(points): # Applies pointInFrame() to all points in a list
    newPoints = []
    for point in points:
        newPoints.append(pointInFrame(point))
    return newPoints

# The next three functions may or may not be in use. Still might come in handy x)

def findHighestInList(list):
    max = 0
    ind = 0
    for i in range(len(list)):
        if abs(list[i]) > max:
            max = list[i]
            ind = i
    return ind

def returnHighest(a,b):
    return a if a >= b else b

def returnLowest(a,b):
    return a if a <= b else b

def convertGridToRender(points):     # Converts points on the initial grid to renderable points.
    newPoints = []                   # Renderable points start at 0 and increase from there.
    for point in range(len(points)):
        newPoints.append([0,0,0])
        newPoints[point][0] = points[point][0] + (RESOLUTION[0] / 2)
        newPoints[point][1] = points[point][1] + (RESOLUTION[1] / 2)
        newPoints[point][2] = points[point][2]
    for point in newPoints:
        for i in point:
            i = int(i)
    return newPoints

def pointListToInt(points): # Rounds all numbers in a pointlist to intergers
    newPoints = []
    for i in points:
        newPoints.append([round(i[0]),round(i[1]),round(i[2])])
    return newPoints

def removeZFromSinglePoint(point): # [x, y, z] -> [x, y]
    newPoint = [point[0], point[1]]
    return newPoint

def removeZFromPoints(points): # [[x, y, z], [a, b, c]] -> [[x, y], [a, b]]
    newPoints = []
    for i in points:
        newPoints.append([i[0], i[1]])
    return newPoints

def sortByZ(points): # Takes a list of points and sorts them by their Z coordinates (index 2)
    arr = points     # I wanted this list to return largest to smallest, but that didn't work with the renderer, and now for some reason the opposite is working.
    n = len(arr)     # If it ain't broke, don't fix it.
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j][2] > arr[j+1][2]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# This function takes a list of points where all numbers are already converted to INTEGERS on a 2d grid 
def renderFrame(points):
    finalString = ""
    for y in range(RESOLUTION[1]):      # Turns everything upside down btw
        for x in range(RESOLUTION[0]):
            saveindex = []
            for i in points:
                if [round(x),round(y)] == removeZFromSinglePoint(i):
                    distanceRating = ((i[2]-DISTANCE if 0 < i[2]-DISTANCE <= 40 else 40) / 10) if i[2] - DISTANCE != 0 else 0
                    finalString += PIXEL[round(distanceRating)] * 2
                    saveindex = [x,y]
                    break
            if [x,y] == saveindex:
                continue
            finalString += "  "
        finalString += "\n"
    return finalString

def AddOrSubtract(x,y,bool): # (x + y) if bool==True else (x - y). Saves space in drawLine() function.
    if bool == True:
        return x + y
    else:
        return x - y

def drawLine(a, b): # Takes two points and draws enough points to make a "line" in the final render. This function should work before and 
    line = []
    differences = []
    axSmaller = a[0] < b[0]
    aySmaller = a[1] < b[1]
    azSmaller = a[2] < b[2]
    for i in range(3):
        differences.append(abs(a[i] - b[i]))
    highestDifference = returnHighest(RESOLUTION[0], RESOLUTION[1])
    for i in range(highestDifference):
        line.append([AddOrSubtract(a[0], round((differences[0]/highestDifference)*i), axSmaller), AddOrSubtract(a[1], round((differences[1]/highestDifference)*i), aySmaller), AddOrSubtract(a[2], round((differences[2]/highestDifference)*i), azSmaller)])
    return line

# I have never used sin or cos before i started this project. Keep that in mind when reading the following function

def getCubeCorners(center, size, rotation): # Rotation given in degrees and converted to radians in the function
    halfSize = size/2
    radians = [rotation[0]*math.pi/180, rotation[1]*math.pi/180, rotation[2]*math.pi/180]
    offsets = [45*math.pi/180,135*math.pi/180,225*math.pi/180,315*math.pi/180]
    radius = math.sqrt(halfSize**2 + halfSize**2)
    a = [center[0] + math.sin(offsets[3] + radians[1])*radius,center[1]+halfSize,center[2] + math.cos(offsets[1] + radians[1])*radius]
    b = [center[0] + math.sin(offsets[0] + radians[1])*radius,center[1]+halfSize,center[2] + math.cos(offsets[2] + radians[1])*radius]
    c = [center[0] + math.sin(offsets[1] - radians[1])*radius,center[1]-halfSize,center[2] + math.cos(offsets[2] + radians[1])*radius]
    d = [center[0] + math.sin(offsets[2] - radians[1])*radius,center[1]-halfSize,center[2] + math.cos(offsets[1] + radians[1])*radius]
    e = [center[0] + math.sin(offsets[3] - radians[1])*radius,center[1]+halfSize,center[2] + math.cos(offsets[3] - radians[1])*radius]
    f = [center[0] + math.sin(offsets[0] - radians[1])*radius,center[1]+halfSize,center[2] + math.cos(offsets[0] - radians[1])*radius]
    g = [center[0] + math.sin(offsets[1] + radians[1])*radius,center[1]-halfSize,center[2] + math.cos(offsets[0] - radians[1])*radius]
    h = [center[0] + math.sin(offsets[2] + radians[1])*radius,center[1]-halfSize,center[2] + math.cos(offsets[3] - radians[1])*radius]
    return [a,b,c,d,e,f,g,h]

def drawCube(cornerList): # cornerList has to contain 8 points where line ABCDA connects the face opposing the face line EFGHE makes.
    line1=drawLine(cornerList[0], cornerList[1])
    line2=drawLine(cornerList[1], cornerList[2])
    line3=drawLine(cornerList[2], cornerList[3])
    line4=drawLine(cornerList[3], cornerList[0])
    line5=drawLine(cornerList[0], cornerList[4])
    line6=drawLine(cornerList[1], cornerList[5])
    line7=drawLine(cornerList[2], cornerList[6])
    line8=drawLine(cornerList[3], cornerList[7])
    line9=drawLine(cornerList[4], cornerList[5])
    line10=drawLine(cornerList[5], cornerList[6])
    line11=drawLine(cornerList[6], cornerList[7])
    line12=drawLine(cornerList[7], cornerList[4])
    return line1+line2+line3+line4+line5+line6+line7+line8+line9+line10+line11+line12

def cubeToRender(center, size, rotation): # I don't wanna type out the next line every time. To render your own points, use the functions below, but replace the drawCube() function with your own points.
    return renderFrame(sortByZ(convertGridToRender(pointListToInt(pointListToFrame(drawCube(getCubeCorners(center,size,rotation)))))))

def cubeSpinAnimation(fps,degreesPerFrame,center,size):             # This function is very slow as it has to render each frame.
    frequency = 1/fps                                               # It stores all the rendered frames before it displays them,
    animation = []                                                  # so once all the frames are rendered its smooth sailing
    print("Creating animation!")                                    #
    for i in range(0,360,degreesPerFrame):                          # Currently only rotation around the Y axis is supported.
        animation.append(cubeToRender(center,size,[0,i,0]))         
        print(f"{round(degreesPerFrame/360*100*(i/degreesPerFrame),2)}%")
    print("Done!")
    while True:
        for i in animation:
            os.system('cls') # CHANGE THIS IF YOU ARE NOT ON WINDOWS
            print(i)
            time.sleep(frequency)

cubeSpinAnimation(10,5,[0,0,75],30) # Example animation. Takes a while to render, but looks alright in my opinion.