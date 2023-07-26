# import the necessary packages
import numpy as np
import cv2
 
# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cv2.startWindowThread()

# open webcam video stream
cap = cv2.VideoCapture(0)

# the output will be written to output.avi
out = cv2.VideoWriter(
    'output.avi',
    cv2.VideoWriter_fourcc(*'MJPG'),
    15.,
    (640,480))

def find_box_center(boxes):
        box = boxes[0]
        xA, yA, xB, yB = box[0], box[1], box[2], box[3]
        center_coords = [0,0]
        
        center_x = (xA+xB)/2
        center_y = (yA+yB)/2
        center_coords[0], center_coords[1] = int(center_x), int(center_y)

        return center_coords

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # resizing for faster detection
    frame = cv2.resize(frame, (640, 480))
    # using a greyscale picture, also for faster detection
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # detect people in the image
    # returns the bounding boxes for the detected objects
    boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )
    print(len(boxes))
    print(boxes)

    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
    if boxes.size !=0:
        center_point = find_box_center(boxes)
        print(center_point)

        for (xA, yA, xB, yB) in boxes:
            # display the detected boxes in the colour picture
            cv2.rectangle(frame, (xA, yA), (xB, yB),
                            (0, 255, 0), 2)
            cv2.circle(frame, (center_point[0],center_point[1]), radius=1, color=(0, 0, 255), thickness=-1)
        
    # Write the output video 
    out.write(frame.astype('uint8'))
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    


# When everything done, release the capture
cap.release()
# and release the output
out.release()
# finally, close the window
cv2.destroyAllWindows()
cv2.waitKey(1)

