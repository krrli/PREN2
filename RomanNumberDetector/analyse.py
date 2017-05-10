#analyse the cropped Images

import cv2
from RomanNumberDetector import roi_number

def countConnectedComponents(img):

    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Threshold it so it becomes binary
    ret, thresh = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    #cv2.imshow('test', thresh)

    # You need to choose 4 or 8 for connectivity type
    connectivity = 8
    # Perform the operation
    output = cv2.connectedComponentsWithStats(thresh, connectivity, cv2.CV_32S)
    # Get the results
    # The first cell is the number of labels
    num_labels = output[0]
    # The second cell is the label matrix
    labels = output[1]
    # The third cell is the stat matrix
    stats = output[2]
    # The fourth cell is the centroid matrix
    centroids = output[3]

    ###also counts the background, so -1
    #print(num_labels -1)

    count = num_labels -1
    countedComponents.append(count)


#####
countedComponents = []


def analyseNumber(image):
    countedComponents.clear()
    #image = cv2.imread(image)

    ###roi
    crop_Array = []
    crop_Array = roi_number.cropNumber(image)

    try:

        countConnectedComponents(crop_Array[0])
        countConnectedComponents(crop_Array[1])
        countConnectedComponents(crop_Array[2])
        countConnectedComponents(crop_Array[3])

        #cv2.imshow('test1', crop_Array[0])
        #cv2.imshow('test2', crop_Array[1])
        #cv2.imshow('test3', crop_Array[2])
        #cv2.imshow('test4', crop_Array[3])


        print(countedComponents)


        if (countedComponents[1] == 3 and countedComponents[2] == 3):
            #print(3)
            return 3
        elif (countedComponents[1] == 3 and countedComponents[3] == 2):
            # print(4)
            return 4
        elif (countedComponents[1] == 2 and countedComponents[2] == 1):
            #print(5)
            return 5
        elif (countedComponents[1] == 2 and countedComponents[2] == 2):
            #print(2)
            return 2
        elif (countedComponents[1] == 1 and countedComponents[2] == 1):
            #print(1)
            return 1
        else:
            #randomNumb = (str)(random.randint(1, 5))
            #print("random " + randomNumb)
            return 0

        #cv2.waitKey(0)

    except:
        return 0