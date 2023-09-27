#importing dependencies 
import cv2                  #importing computer vision 
import pyttsx3              #importing Text-to-speech library for audio feedback

import mediapipe as mp              #importing Mediapipe which gives us all the pose estimation libraries and all the different media pipe solutions (solutions basically means different components within mediapipe library)
import numpy as np                  #importing mediapipe which later in the code is used in trigonometry thing



#creating variables
prev=None
curr=None

mp_drawing=mp.solutions.drawing_utils     #mp_drawing variable is used to access the drawing utilites                                      #drawing utilites are within mediapipe solutions and helps inorder to visualize the pose of a person 
mp_pose=mp.solutions.pose                 #mp_pose variable is used to access the pose models availabe                                     # in mediapipe there is whole lot of solutions or we can say models such as hand pose model which is helpful in finding the joints of the hand from an image or set of video frames and mp_pose vaiable helps to access any of the available models
voice=pyttsx3.init()



#function to calculate angle
def calculate_angle(a,b,c=0):
    a=np.array(a)#first point                           # all the angles passed is stored as numpy array and it helps is in making calculating angles easier
    b=np.array(b)#mid point
    c=np.array(c)#last point

    radians=np.arctan2(a[1]-b[1],a[0]-b[0])
    angle=np.abs(radians*180.0/np.pi)

  
    return angle



# READING VEDIO FEED 
cap=cv2.VideoCapture('warrior.mp4')      #accessing our webcam                                                                           #created an instance of VedioCapture class and pass the camera number or recorded vedio path inside the VedioCapture()

ret,frame=cap.read()                     #reading from the webcam feed                                                                   #cap.read() will basically return two things , one is image caught that is recieved with the help of frame variable and other thing it returns is the reading from the resource specified is successful or not (using True or False) so that gets stored in ret
cv2.imshow('frame',frame)                #visualizing how our computer is seeing through webcam


with mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as pose:       #creating a mediapipe instance and accessing it with the help of pose variable 
    while cap.isOpened():                                                                  #while the image feed is open we will be reading from the vedio feed
     ret,frame=cap.read()                                                                  #frame by frame we will be reading from the vedio feed 

    #RECOLORING OUR IMAGE 
     image=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)                                           #opencv feed by default reads images in BGR format , but in order to do operations on this image using Mediapipe it must be in RGB format
     image.flags.writeable=False

    #makes detection using mediapipe
     results=pose.process(image)

    #restoring back to bgr format in order to process the image further using computer vision ,and computer vision requires image to be in BGR format
     image.flags.writeable=True
     image=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    #extract landmarks
     try:
         landmarks=results.pose_landmarks.landmark
        #get coordinates of shoulder,elbow and wrist
         Lshoulder=[landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
         Lelbow=[landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
         Lwrist=[landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
         Lhip=[landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
         Lknee=[landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
         Lankle=[landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

        
        
       
        #get coordinates of shoulder,elbow and wrist
         Rshoulder=[landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
         Relbow=[landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
         Rwrist=[landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
         Rhip=[landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
         Rknee=[landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
         Rankle=[landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

        #calculate angle between sholer,elbow and wrist
         angle1=(180-calculate_angle(Lshoulder,Lelbow).astype(int))
         print('angle1-',angle1)
        
        #print the angle on the screen using putText() provided by computer vision 
         cv2.putText(image,str(angle1),
                     tuple(np.multiply(Lshoulder,[850,480]).astype(int)),
                     cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA
                     )
        #calculate angle between shouler,elbow and wrist
         angle2=calculate_angle(Rshoulder,Relbow).astype(int)
         print('angle2-',angle2)
        #print the angle on the screen
         cv2.putText(image,str(angle2),
                     tuple(np.multiply(Rshoulder,[850,480]).astype(int)),
                     cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA
                     )
        

         angle3=calculate_angle(Lhip,Lknee).astype(int)
         print('angle3-',angle3)
        #print the angle on the screen
         cv2.putText(image,str(angle3),
                     tuple(np.multiply(Lankle,[850,480]).astype(int)),
                     cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA
                     )
         
         
         angle4=90+calculate_angle(Rhip,Rknee).astype(int)
         print('angle4-',angle4)
        #print the angle on the screen
         cv2.putText(image,str(angle4),
                     tuple(np.multiply(Rknee,[850,480]).astype(int)),
                     cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA
                     )
         
         if angle1>20 or angle2>20 :
             
             alert='please ,raise your both hands upwards '
             prev=alert
             cv2.putText(image,alert,(24,25),cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255),1,cv2.LINE_AA)
            #---
             if prev!=curr:
                voice.say(alert)
                voice.runAndWait()
                curr=prev
            
            

         elif angle4>120 :
             curr=alert
             alert='please,bend your knee.'
             prev=alert
             cv2.putText(image,alert,(24,25),cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255),1,cv2.LINE_AA)
             if prev!=curr:
                voice.say(alert)
                voice.runAndWait()
                curr=prev
            


         else :
             alert='perfect,you are doing great.'
             prev=alert
             if prev!=curr:
                voice.say(alert)
                voice.runAndWait()
                curr=prev
            
    
             cv2.putText(image,alert,(24,25),cv2.FONT_HERSHEY_COMPLEX,1,(0, 0, 255),1,cv2.LINE_AA)
      
       
     except:
         pass

    #main logic
    

             
    #render detections
     mp_drawing.draw_landmarks(image,results.pose_landmarks,mp_pose.POSE_CONNECTIONS,
                               mp_drawing.DrawingSpec(color=(245,117,66),thickness=2,circle_radius=2),
                               mp_drawing.DrawingSpec(color=(255,255,255),thickness=4,circle_radius=3))

    
    #visualize the feed
     cv2.imshow('frame',image)
     
     # Exit the loop when the 'q' key is pressed
     if cv2.waitKey(30) & 0xff == ord('q'):              #the window created gets closed only when 'q' is entered , basically it is like getch() in C language                                # waitkey(30) means the window created will be held and will not disappearing till 30 seconds , another thing is the mask 0xff which basically a mask bit and if the entered key is equal to the ascii value of the key which is being compared with mask bit then obly the window will be closed by exiting the while loop
            break
   


#to release all the resource held(like camera)
cap.release()
#after the vedio feed is closed the window in which it is shown should also be destroyed
cv2.destroyAllWindows()


