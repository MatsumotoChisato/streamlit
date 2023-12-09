# Striamlit を用いたWeb画像処理アプリ
import streamlit as st
import numpy as np
import cv2
from PIL import Image
import io

with st.sidebar:
    th = st.slider('しきい値', 0, 50, 10)
    radio = st.radio(
        "2値化手法を選択してください",
        ("gray", "canny"))
    st.write("canny()エッジ検出機に渡される２つの閾値のうち、大きいほうの閾値0")
    par1 = st.slider('パラメータ1', 50, 150, 120)
    st.write("円の中心を検出する際の投票数の閾値．小さくなるほど、より誤検出が起こる可能性アリ")
    par2 = st.slider('パラメータ2', 5, 25, 13)

with st.sidebar:
    ratio = st.slider('隠れている粒の比率', 1, 10, 3)
    st.write("ratio value", ratio)
'''
### ブドウ粒数カウント
'''

col1, col2= st.columns(2)
image_loc = st.empty()

with col1:
    filename = "grape2.png"
    img = cv2.imread(filename)
    
    # バイナリから読み込み(python3なのでbinaryモードで読み込み)
    with open(filename, 'rb') as f:
        binary = f.read()
    # 一度ndarrayに変換してからdecodeします。reshapeだけしてると思われます.
    arr = np.asarray(bytearray(binary), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)  # 'load it as it is'
    
    
    # バイト列から画像をデコードする
    #img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    #1チャンネル（白黒画像に変換）
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    #######################################    
    if radio=="gray":
        canny_gray = blur
    elif radio=="canny":
        #Cannyにてエッジ検出処理（やらなくてもよい）
        canny_gray = cv2.Canny(blur,th,200)

    #houghで使う画像の指定、後で変えたりする際に変数してしておくと楽。
    cimg = canny_gray
    # 画像を表示する
    col1.subheader("Binary image")
    col1.image(cimg)

    j = 1
    
    #hough関数
    circles = cv2.HoughCircles(cimg,cv2.HOUGH_GRADIENT,1,20,param1=par1,param2=par2,minRadius=10,maxRadius=18)
        # param1 ; canny()エッジ検出機に渡される２つの閾値のうち、大きいほうの閾値0
        # param2 ; 円の中心を検出する際の投票数の閾値、小さくなるほど、より誤検出が起こる可能性がある。
        # minRadius ; 検出する円の大きさ最小値
        # maxRadius ; 検出する円の大きさ最大値

    #if circles is not None and len(circles) > 0:
    if circles is not None :
        #型をfloat32からunit16に変更：整数のタイプになるので、後々トラブルが減る。
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # 外側の円を描く
            cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
            # 中心の円を描く
            cv2.circle(img,(i[0],i[1]),2,(0,0,255),2)
            # 円の数を数える
            j = j + 1
        
        
    #円の合計数を表示
    col2.subheader("reselt 検出数　："+ str(j))       
    col2.image(img)


    #cv2.putText(img,'Count :'+str(j), (30,30), fontType, 1, (0, 0, 0), 1, cv2.LINE_AA)

    ratio = 1+(ratio/10)
    total = j * ratio

    col2.write(str(ratio))
    #st.write(type(cv2_img))
    #cv2.putText(img,'ratio :'+str(ratio), (30,60), fontType, 1, (0, 0, 0), 1, cv2.LINE_AA)
    col2.write("比率 : " + str(ratio))
    #cv2.putText(img,'Total :'+str(total), (30,90), fontType, 1, (0, 0, 0), 1, cv2.LINE_AA)
    col2.write("合計 : " + str(total))