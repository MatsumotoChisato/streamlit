# Striamlit を用いたWeb画像処理アプリ
import streamlit as st

import numpy as np
from PIL import Image
import cv2


def pil2cv(image):
    ''' PIL型 -> OpenCV型 '''
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image

with st.sidebar:
    th = st.slider('Threshold value', 0, 255, 125)
    st.write("Threshold value", th)

with st.sidebar:
    radio = st.radio(
        "Choose a binary method",
        ("Threshold", "Adaptive threshold mean","Adaptive threshold Gaussian",
        "Otsu' thresholding", "Otsu's thresholding + Gaussian fileter")
    )
    erosion=st.button("Erosion",key=1)
    dilation=st.button("Dilation",key=2)

st.title('最初のページ')
'''
### 画像処理プログラム
'''
uploaded_image=st.file_uploader("ファイルアップロード", type='jpg')
col1, col2= st.columns(2)
image_loc = st.empty()

col1.header("Original image")
col2.header("Binary image")
with col1:
    # st.header("A cat")
    if uploaded_image is not None:
        image=Image.open(uploaded_image,)
        img_array = np.array(image)
        st.image(img_array,caption = '元画像',use_column_width = None)
        img=pil2cv(image) 

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret,th1 = cv2.threshold(gray,th,255,cv2.THRESH_BINARY)
        th2 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
        cv2.THRESH_BINARY,11,2)
        th3 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
        cv2.THRESH_BINARY,11,2)
        # image2 = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        ret2,th4 = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        blur = cv2.GaussianBlur(gray,(5,5),0)
        ret3,th5 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)   

if radio=="Threshold" and uploaded_image is not None:
    col2.image(th1)
elif radio=="Adaptive threshold mean" and uploaded_image is not None:
    col2.image(th2)
elif radio=="Adaptive threshold Gaussian" and uploaded_image is not None:
    col2.image(th3)
elif radio=="Otsu' thresholding" and uploaded_image is not None:
    col2.image(th4)
elif radio=="Otsu's thresholding + Gaussian fileter" and uploaded_image is not None:
    col2.image(th5)

if erosion:
    kernel = np.ones((5,5),np.uint8)
    erodedimage = cv2.erode(th5,kernel,iterations = 1)
    
    
    
    col1.image(erodedimage)