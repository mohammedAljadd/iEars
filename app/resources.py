from importlib.resources import path
from unicodedata import name
from urllib import response
from flask_restful import  Resource
from app.utils import *
from flask import request
import cv2
import pytesseract
import pathlib

class Facial_Recognition(Resource):
    def post(self):
        if request.files:
            
            from app import app
            imgs_path = app.config['IMAGE_FOLDER']

            # Face cascade xml file
            cascades = app.config['CASCADE_FOLDER']
            face_cascade = cv2.CascadeClassifier(os.path.join(cascades, 'haarcascade_frontalface_default.xml'))
            
            # Make upload folder empty first
            empty_folder(imgs_path)

            # Save the image
            image = request.files["image"]
            image_name = image.filename
            image_path = imgs_path+image_name
            image.save(image_path)
            
            # Grayscale
            gray_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

            
            # Detect the face with face_cascade
            faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.05, minNeighbors=5)
            for (x, y, w, h) in faces:
                face = gray_image[y:y+h, x:x+w]
                IMG_SIZE = 128 
                face_resized = cv2.resize(face, (IMG_SIZE, IMG_SIZE)) 
                face_expanded = np.expand_dims(face_resized, axis=0)

                # Rescale the image, the model was trained on scaled images
                face_input = face_expanded/255.0

                # Make prediction
                prediction = predict(face_input, threshold=0.6)
            
            return prediction

class Object_Detection(Resource):
    def post(self):
        return {"msg": "Object_Detection"}

class Text_recognition(Resource):
    def post(self):
        if request.files:
            from app import app
            image = request.files["image"]
            image_path = f"{app.config['IMAGE_FOLDER']}"+"/"+image.filename
            image.save(image_path)
           
            pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

            img = cv2.imread(image_path, cv2.COLOR_BGR2GRAY) 
            img = cv2.resize(img, (960, 540)) 

            

            predictions = pytesseract.image_to_string(img)
            result = predictions.replace('\n', ' ')
            if len(result)>=1:
                result = str(text_translation(result))
                return {"result": result}
            else:
                return {"result": "No text detected"}
            

    