import streamlit as st
import cv2
from PIL import Image, ImageEnhance
import numpy as np
import os

face_cascade =cv2.CascadeClassifier("Haarcascade_Path")
eye_cascade = cv2.CascadeClassifier("Haarcascade_Path")

def detect_faces(our_image):
    new_img = np.array(our_image.convert("RGB"))
    faces = face_cascade.detectMultiScale(new_img, 1.1, 2)
    for(x, y, w, h) in faces:
        cv2.rectangle(new_img,(x, y),(x+w, y+h),(255, 0, 0),2)
    return new_img, faces
def detect_eyes(our_image):
    new_img=np.array(our_image.convert("RGB"))
    eyes=eye_cascade.detectMultiScale(new_img, 1.3, 5)
    for(x,y, w,h) in eyes:
        cv2.rectangle(new_img, (x,y), (x+w, y+h), (0,255,0),2)
    return new_img
def cartoonize_image(our_image):
     new_img = np.array(our_image.convert("RGB"))
     gray=cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
     gray=cv2.medianBlur(gray, 5)
     edges=cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 9, 9)
     color=cv2.bilateralFilter(new_img, 9, 300, 300)
     cartoon=cv2.bitwise_and(color, color, mask = edges)
     return cartoon
def cannize_image(our_image):
    new_img=np.array(our_image.convert("RGB"))
    img=cv2.GaussianBlur(new_img, (13,13), 0)
    canny=cv2.Canny(img, 100, 150)
    return canny
    
def main():
    st.title("Image Editing App")
    st.text("Edits your images in a fast and simple way")
    
    activities= ['Detection', 'About']
    choice=st.sidebar.selectbox('Select Activity',activities)
    if choice == 'Detection':
        st.subheader('Face Detection')
        image_file =  st.file_uploader('Upload Image',type=['jpg','png','jpeg'])

        if image_file is not None:
           our_image = Image.open(image_file)
           st.text("Original Image")
           st.image(our_image)
           enhance_type =  st.sidebar.radio("Enhance type",["Original","Gray-scale","Contrast","Brightness","Blurring","Sharpness"])
           if enhance_type == "Gray-scale":
               img =np.array(our_image.convert('RGB'))
               gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
               st.image(gray)
           elif enhance_type == "Contrast":
                rate = st.sidebar.slider("Contrast",0.5,6.0)
                enhancer = ImageEnhance.Contrast(our_image)
                enhanced_img =   enhancer.enhance(rate)
                st.image(enhanced_img)
           elif enhance_type == "Brightness":
                rate = st.sidebar.slider("Brightness",0.0,8.0)
                enhancer = ImageEnhance.Brightness(our_image)
                enhanced_img =   enhancer.enhance(rate)
                st.image(enhanced_img) 
           elif enhance_type == "Blurring":
               rate = st.sidebar.slider("Blurring",0.0,7.0)
               blurred_img = cv2.GaussianBlur(np.array(our_image),(15,15), rate)
               st.image(blurred_img)
           elif enhance_type == "Sharpness":
               rate = st.sidebar.slider("Sharpness",0.0,14.0)
               enhancer = ImageEnhance.Sharpness(our_image)
               enhanced_img = enhancer.enhance(rate)
               st.image(enhanced_img)
           elif enhance_type == "Original":
               st.image(our_image,width = 300)
           else:
               st.image(our_image, width = 300)
        tasks =["Faces", "Eyes", "Cartoonize", "Cannize"]
        feature_choice = st.sidebar.selectbox("Find Features",tasks)
        if st.button("Process"):
            if feature_choice == "Faces":
                result_img, result_faces = detect_faces(our_image)
                st.image(result_img)
                st.success("Found {} faces".format(len(result_faces)))
            elif feature_choice == "Eyes":
                result_img = detect_eyes(our_image)
                st.image(result_img)
            elif feature_choice == "Cartoonize":
                result_img = cartoonize_image(our_image)
                st.image(result_img)
            elif feature_choice == "Cannize":
                result_img = cannize_image(our_image)
                st.image(result_img)


    elif choice == 'About':
        st.subheader("About the developer")
        st.markdown("Built with streamlit by [ S.Venkata SaiShashank](https://youtube.com//@venomousclaw5325)")
        st.text("Iam S.Venkata Sai Shashank I have good knowledge in C,Python,Java,SQL,HTML,CSS,JAVA SCRIPT")



if __name__ == '__main__':
    main()
    
