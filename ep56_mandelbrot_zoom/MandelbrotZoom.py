import array
import numpy
from PIL import Image

#Width and height of the window
WIDTH = 800
HEIGHT = 800
NUM_FRAMES = 100

#Mandlebrot variables.
maxIteration = 1000
threshold = 10

#Starting MIN AND MAX VALUES. They start from -2 to 2.
sMinX = numpy.complex128(-2)
sMinY = numpy.complex128(-2)
sMaxX = numpy.complex128(2)
sMaxY = numpy.complex128(2)

#Ending MIN AND MAX VALUES.
#eMinX = numpy.complex128(-0.6002735730728121
#eMinY = numpy.complex128(-0.6646192892692977
#eMaxX = numpy.complex128(-0.6002735278513613
#eMaxY = numpy.complex128(-0.6646192440478469
eMinX = numpy.complex128(-1.2576470439078538)
eMinY = numpy.complex128(0.3780652779236957)
eMaxX = numpy.complex128(-1.2576470439074896)
eMaxY = numpy.complex128(0.3780652779240597)

minXIncr = 0
minYIncr = 0
maxXIncr = 0
maxYIncr = 0

#Color Variables
#colorMap = array.array('q')
colorMap = []
black = []

# Maps a number of a given input range to a number of the output range.
def map(inputNum, minInput, maxInput, minOutput, maxOutput) :
    return (inputNum - minInput) * (maxOutput - minOutput) / (maxInput - minInput) + minOutput

def initVars() :
    global sMinX, sMinY, sMaxX, sMaxY, eMinX, eMinY, eMaxX, eMaxY, minXIncr, minYIncr, maxXIncr, maxYIncr
    minXIncr = (eMinX - sMinX) / NUM_FRAMES
    minYIncr = (eMinY - sMinY) / NUM_FRAMES
    maxXIncr = (eMaxX - sMaxX) / NUM_FRAMES
    maxYIncr = (eMaxY - sMaxY) / NUM_FRAMES
    print(minXIncr, minYIncr, maxXIncr, maxYIncr)
    print("-------------------------");


# Initialize the color map.
def initializeColors() :
    global colorMap, black

    colorMap.append( [66, 30, 15] )
    colorMap.append( [25, 7, 26] )
    colorMap.append( [9, 1, 47] )
    colorMap.append( [4, 4, 73] )
    colorMap.append( [0, 7, 100] )
    colorMap.append( [12, 44, 138] )
    colorMap.append( [24, 82, 177] )
    colorMap.append( [57, 125, 209] )
    colorMap.append( [134, 181, 229] )
    colorMap.append( [211, 236, 248] )
    colorMap.append( [241, 233, 191] )
    colorMap.append( [248, 201, 95] )
    colorMap.append( [255, 170, 0] )
    colorMap.append( [204, 128, 0] )
    colorMap.append( [153, 87, 0] )
    colorMap.append( [106, 52, 3] )

    black.append(0)
    black.append(0)
    black.append(0)

# Taken from https://stackoverflow.com/questions/16500656/which-color-gradient-is-used-to-color-mandelbrot-in-wikipedia
def getColor(n) :
    global maxIteration, colorMap, black
    if n < maxIteration and n > 0 :
        i = n % 16
        return colorMap[i]

    return black

# This is where the Mandlebrot set is calculated.
def generateFrames() :
    global maxIteration, colorMap, black, sMinX, sMinY, sMaxX, sMaxY, eMinX, eMinY, eMaxX, eMaxY, minXIncr, minYIncr, maxXIncr, maxYIncr
    frameCount = 0
    newImageFrame = Image.new('RGB', [WIDTH, HEIGHT])
    pixels = newImageFrame.load()
    while sMinX < eMinX and sMinY < eMinY and sMaxX > eMaxX and sMaxY > eMaxY :
        for x in range(WIDTH) :
            for y in range(HEIGHT) :
                    a = map(x, 0, WIDTH, sMinX, sMaxX)
                    b = map(y, 0, HEIGHT, sMinY, sMaxY)
                    origA = a
                    origB = b

                    n = 0

                    while n < maxIteration :
                        aa = a*a - b*b
                        bb = 2 * a * b

                        if abs(aa+bb) > threshold :
                            break

                        a = aa + origA
                        b = bb + origB

                        n = n + 1

                    aColor = getColor(n)
                    pixels[x, y] = (aColor[0], aColor[1], aColor[2])

        #Done drawing. Save it
        fileName = "images\\image_frame_" + str(frameCount) + ".png"
        newImageFrame.save(fileName)
        print("Saved Frame", frameCount, " to file ", fileName)

        sMinX = sMinX + minXIncr
        sMinY = sMinY + minYIncr
        sMaxX = sMaxX + maxXIncr
        sMaxY = sMaxY + maxYIncr

        print(sMinX, ",", sMinY, "-", sMaxX, ",", sMaxY)

        minXIncr = minXIncr * 0.9
        minYIncr = minYIncr * 0.9
        maxXIncr = maxXIncr * 0.9
        maxYIncr = maxYIncr * 0.9

        frameCount = frameCount + 1

initVars()

initializeColors()

generateFrames()
