import cv2
import mediapipe

def draw_points(image):

    drawingModule = mediapipe.solutions.drawing_utils
    handsModule = mediapipe.solutions.hands

    with handsModule.Hands(static_image_mode=True) as hands: #True/False

        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            
        try:
            if results.multi_hand_landmarks != None:
                for handLandmarks in results.multi_hand_landmarks:
                    for point in handsModule.HandLandmark:
        
                        drawingModule.draw_landmarks(image, handLandmarks, handsModule.HAND_CONNECTIONS)
                        #self.frame_q.put(image)

            #Camera().frame_q.put(image)

            return image
        except:
            print("No hand detected")

cap = cv2.VideoCapture(0)

while True:

    success, img = cap.read()

    img = cv2.rectangle(img, (100,100), (300,300), (0,255,0), 2) #image, start_point, end_point, color, thickness
    crop_img = img[100:300, 100:300]

    crop_img = draw_points(crop_img)
   
    cv2.imshow("Image", img)
    cv2.imshow("Cropped Image", crop_img)

    key = cv2.waitKey(1)