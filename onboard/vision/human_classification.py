import numpy as np
import cv2


class Human_Classify:
    measured_distance = 20
    real_width = 6
    ref_image = "ref_ped.jpg"

    def __init__(self, cap, out, hog):
        self.hog = hog
        self.distance = 0
        self.center_point = 0
        while True:

            self.ret, self.frame = cap.read()

            # resizing for faster detection
            frame = cv2.resize(self.frame, (640, 480))

            boxes, weights, human_width = self.find_human_data(self.hog, frame)
            boxes_array = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

            if human_width !=0 and boxes_array.size !=0:
                
                self.distance = self.distance_finder(self.Focal_Length_Finder(), human_width)
                self.center_point = self.find_box_center(boxes_array)
                print(self.distance)
                print(self.center_point)

                self.draw_boxes(boxes)
                

                # Write the output video 
            out.write(frame.astype('uint8'))
            # Display the resulting frame
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def find_box_center(self, boxes):
        box = boxes[0]
        xA, yA, xB, yB = box[0], box[1], box[2], box[3]
        center_coords = [0,0]
        
        center_x = (xA+xB)/2
        center_y = (yA+yB)/2
        center_coords[0], center_coords[1] = int(center_x), int(center_y)

        return center_coords
    
    def find_human_data(self, hog, image):
        human_width = 0

        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        # detect people in the image
        # returns the bounding boxes for the detected objects
        boxes, weights = hog.detectMultiScale(gray, winStride=(8,8))
        for (x, y, h, w) in boxes:

            
  
        # getting face width in the pixels
            human_width = w
  
    # return the face width in pixel
        print(len(boxes))
        print(boxes)

        return boxes, weights, human_width
    
    def draw_boxes(self, boxes):
        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
        if boxes.size !=0:
            center_point = self.find_box_center(boxes)
            print(center_point)

            for (xA, yA, xB, yB) in boxes:
                # display the detected boxes in the colour picture
                cv2.rectangle(self.frame, (xA, yA), (xB, yB),
                                (0, 255, 0), 2)
                cv2.circle(self.frame, (center_point[0],center_point[1]), radius=1, color=(0, 0, 255), thickness=-1)

    def Focal_Length_Finder(self):
        ref_image = cv2.imread(self.ref_image)
  
        
        ref_image_face_width = self.find_human_data(self.hog, ref_image)
    
        # finding the focal length
        focal_length = (ref_image_face_width * self.measured_distance) / self.real_width
        return focal_length
    
    def distance_finder(self, Focal_Length, face_width_in_frame):
        distance = (self.real_width * Focal_Length)/face_width_in_frame
        return distance
