import cv2
import numpy as np
import pyautogui
from time import sleep
from PIL import Image
import os

#location of opencv haarcascade <change according to your file location>
face_cascade = cv2.CascadeClassifier("C:/Users/Vineet/Desktop/faceRecognition-project/project/haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0)   # 0 = main camera , 1 = extra connected webcam and so on.
rec = cv2.face.LBPHFaceRecognizer_create()

#the path where the code is saved
pathz = "C:\\Users\\Vineet\\Desktop\\faceRecognition-project\\project" 


#recogizer module
def recog():
    """ Recognizes people from the pretrained .yml file """
    #print("Starting")
    rec.read(f"C:\\Users\\Vineet\\Desktop\\faceRecognition-project\\project\\chikoneye.yml") 
    id = 0  #set id variable to zero

    font = cv2.FONT_HERSHEY_COMPLEX 
    col = (255, 0, 0)
    strk = 2 

    while True:  #This is a forever loop
        ret, frame = cap.read() #Capture frame by frame 
    
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #change color from BGR to Gray
        faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5)

        #print(faces)
        for(x, y, w, h) in faces:
            #print(x, y, w, h)
            roi_gray = gray[y: y+h, x: x+w]  #region of interest is face

            #*** Drawing Rectangle ***
            color = (255, 0, 0)
            stroke = 2
            end_cord_x = x+w
            end_cord_y = y+h
            cv2.rectangle(frame, (x,y), (end_cord_x, end_cord_y), color, stroke)

            #***detect
            id, conf = rec.predict(roi_gray)
            #cv2.putText(np.array(roi_gray), str(id), font, 1, col, strk)
            print(id) #prints the id's
        
            #if sees unauthorized person
            if id != 1: 
                #execute lock command
                pyautogui.hotkey('win', 'r')   #win + run key combo
                pyautogui.typewrite("cmd\n")   # type cmd and 'Enter'= '\n'
                sleep(0.500)       #a bit delay <needed!>
                #windows lock code to command prompt and hit 'Enter'
                pyautogui.typewrite("rundll32.exe user32.dll, LockWorkStation\n") 

            elif id == 1:      #if authorized person
                print("Authorized Person\n") #do nothing

        
    
        cv2.imshow('ChikonEye', frame)

        #check if user wants to quit the program (pressing 'q')
        if cv2.waitKey(10) == ord('q'):
            op = pyautogui.confirm("Close the Program 'ChikonEye'?") 
            if op == 'OK':
                print("Out")
                break
            
                

    cap.release()
    cv2.destroyAllWindows() #remove all windows we have created




#create dataset and train the model
def data_Train():
    sampleNum = 0
    #print("Starting training")
    id = pyautogui.prompt(text="""Enter User ID.\n\nnote: numeric data only.""", title='ChikonEye', default='none')
    #check for user input
    
    """
    if id >  :
        print(id)
        pyautogui.alert(text='WRONG INPUT',title='ChikonEye',button='Back')
        recog()
    """

    #if user input is 1 2 or 3  max 5 here <you can change that.>
    if id != '1' and id != '2' and id != '3' and id != '4' and id != '5':
        pyautogui.alert(text='WRONG INPUT',title='ChikonEye',button='Back')
        recog()

    else:
        #let, the input is okay
        while True:
            
            
            ret, img = cap.read()  
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for(x, y, w, h) in faces: #find faces
                sampleNum = sampleNum + 1  #increment sample num till 21
                cv2.imwrite(f'{pathz}\\dataSet\\User.{id}.{sampleNum}.jpg', gray[y: y+h, x: x+w])
                cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 4)
                cv2.waitKey(100)

            cv2.imshow('faces', img)  #show image while capturing
            cv2.waitKey(1)
            if(sampleNum > 20): #21 sample is collected
                break   
            
    trainer()  #Train the model based on new images

    recog() #start recognizing
            


#Trainer 
def trainer():
    faces = []   #empty list for faces
    Ids = [] #empty list for IDs

    path = (f'{pathz}\\dataSet')

    #gets image id with path
    def getImageWithID(path):
        imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
        #print(f"{imagePaths}\n")
    
        for imagePath in imagePaths:
            faceImg = Image.open(imagePath).convert('L')
            #cv2.imshow('faceImg', faceImg)
            faceNp = np.array(faceImg, 'uint8')
            ID = int(os.path.split(imagePath)[-1].split('.')[1])
            #print(ID)
            faces.append(faceNp)
            Ids.append(ID)

            cv2.waitKey(10)

        return Ids, faces


    ids, faces = getImageWithID(path)

    print(ids, faces)
    rec.train(faces, np.array(ids))
    #create a yml file at the folder. WIll be created automatically.
    rec.save(f'{pathz}\\chikoneye.yml')   
    pyautogui.alert("Done Saving.\nPress OK to continue")
    cv2.destroyAllWindows()
    



#Options checking
opt =pyautogui.confirm(text= 'Chose an option', title='ChikonEye', buttons=['START', 'Train', 'Exit'])
if opt == 'START':
    #print("Starting the app")
    recog()
    
if opt == 'Train':
    opt = pyautogui.confirm(text="""
    Please look at the Webcam.\nTurn your head a little while capturing.\nPlease add just one face at a time.
    \nClick 'Ready' when you're ready.""", title='ChikonEye', buttons=['Ready', 'Cancel'])
        
    if opt == 'Ready':
            #print("Starting image capture + Training")
            data_Train()
    if opt == 'Cancel':
        print("Cancelled")
        recog()
        

if opt == 'Exit':
    print("Quit the app")
