#analyse the cropped Images

import cv2
from RomanNumberDetector import roi_number

def countConnectedComponents(img):
    # You need to choose 4 or 8 for connectivity type
    connectivity = 8
    # Perform the operation
    output = cv2.connectedComponentsWithStats(img, connectivity, cv2.CV_32S)
    # Get the results
    # The first cell is the number of labels
    num_labels = output[0]

    #also counts the background, so -1
    count = num_labels -1
    countedComponents.append(count)

countedComponents = []

def analyseNumber(image):
    countedComponents.clear()

    ###roi
    crop_Array = []
    crop_Array = roi_number.cropNumber(image)

    try:
        countConnectedComponents(crop_Array[0])
        countConnectedComponents(crop_Array[1])
        countConnectedComponents(crop_Array[2])
        countConnectedComponents(crop_Array[3])

        print(countedComponents)

        if (countedComponents[1] == 3 and countedComponents[3] == 2):
            #print(4)
            return 4
        elif (countedComponents[1] == 3 and countedComponents[2] == 3):
            #print(3)
            return 3
        elif (countedComponents[0] == 2 and countedComponents[1] == 2 and countedComponents[3] == 1):
            #print(5)
            return 5
        elif (countedComponents[1] == 2 and countedComponents[2] == 2):
            #print(2)
            return 2
        elif (countedComponents[1] == 1 and countedComponents[2] == 1):
            #print(1)
            return 1
        else:
            return 0

    except:
        return 0