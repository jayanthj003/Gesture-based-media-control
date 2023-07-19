#GESTURE BASED MEDIA CONTROL

#import libraries
import cv2
import mediapipe as mp
import pyautogui
import time

#drawing hand landmarks and performing hand detection
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# For webcam input:
cap = cv2.VideoCapture(0)
#keep track starting point of a finger count
start_init = False 

#stores previous finger count 
prev = -1

#for hand detection and tracking
#Hands     --  object   
# mp_hands --  module
with mp_hands.Hands(              
    model_complexity=0,            
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7) as hands:
  
  #start a loop that will continue until webcam is available
  while cap.isOpened():
    end_time = time.time()
    success, image = cap.read()     #captures current frame from webcam
    image=cv2.flip(image,1)         #image is flipped horizontally to match mirror reflection of hand movements
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Initially set finger count to 0 for each cap
    fingerCount = 0

    if results.multi_hand_landmarks:
      

      for hand_landmarks in results.multi_hand_landmarks:
        # Get hand index to check label (left or right)
        handIndex = results.multi_hand_landmarks.index(hand_landmarks)
        handLabel = results.multi_handedness[handIndex].classification[0].label

        # Set variable to keep landmarks positions (x and y)
        handLandmarks = []

        # Fill list with x and y positions of each landmark
        for landmarks in hand_landmarks.landmark:
          handLandmarks.append([landmarks.x, landmarks.y])

        # Test conditions for each finger: Count is increased if finger is 
        #   considered raised.
        # Thumb: TIP x position must be greater or lower than IP x position, 
        #   deppeding on hand label.
        if handLabel == "Left" and handLandmarks[4][0] > handLandmarks[3][0]:
          fingerCount = fingerCount+1
        elif handLabel == "Right" and handLandmarks[4][0] < handLandmarks[3][0]:
          fingerCount = fingerCount+1

        # Other fingers: TIP y position must be lower than PIP y position, 
        #   as image origin is in the upper left corner.
        if handLandmarks[8][1] < handLandmarks[6][1]:       #Index finger
          fingerCount = fingerCount+1
        if handLandmarks[12][1] < handLandmarks[10][1]:     #Middle finger
          fingerCount = fingerCount+1
        if handLandmarks[16][1] < handLandmarks[14][1]:     #Ring finger
          fingerCount = fingerCount+1
        if handLandmarks[20][1] < handLandmarks[18][1]:     #Pinky
          fingerCount = fingerCount+1
        cnt=fingerCount
        if not(prev==cnt):
            if not(start_init):
                start_time = time.time()
                start_init = True

            elif (end_time-start_time) > 0.5:
                if (cnt == 1):
                    pyautogui.press("right")
                
                elif (cnt == 2):
                    pyautogui.press("left")

                elif (cnt == 3):
                    pyautogui.press("up")

                elif (cnt == 4):
                    pyautogui.press("down")

                elif (cnt == 5):
                    pyautogui.press("space") 

                elif(cnt==6):
                   pyautogui.hotkey("ctrl","b")

                elif(cnt==7):
                   pyautogui.hotkey("shift","p")

                elif(cnt==8):
                   pyautogui.hotkey("ctrl","f")

                elif(cnt==9):
                   pyautogui.hotkey("shift","n")

                elif(cnt==10):
                   pyautogui.hotkey("ctrl","right")
                   

                prev = cnt
                start_init = False

        # Draw hand landmarks 
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())

    # Display finger count
    cv2.putText(image, str(fingerCount), (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 10)

    # Display image
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
    
cap.release()