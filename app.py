from pymongo import MongoClient
from flask import Flask, render_template, url_for, request, flash, redirect, jsonify, send_file, session, Response
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt
from Helpers import text2gest as tg
from Helpers import gest2text as gt
from Helpers import cartoonize as ct
import intervention as it
import os
import sys
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize
from moviepy.editor import *
import cv2
import webbrowser
from tensorflow import keras
from csv import writer
import csv

global flag, text, check
flag = 0
clip=[]
sep = ['.', '!']

app = Flask(__name__)
bcrypt = Bcrypt(app)
client = MongoClient('localhost', 27017)
db = client.cnt_db
majusers = db.majusers

cors = CORS(app, resources={r"/foo": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = '14ec258c169f5c19f78385bcc83a51df7444624b2ff90449b4a9832e6fe706a1'


@app.route('/')
def index():
    global letters_img
    check = 0
    return render_template('index.html', letters_img=letters_img, check=check)



@app.route("/text_gest", methods=['GET', 'POST'])
def text_gest():
    global text, check , data , fdata
    check=0
    text = request.form['text'] 
    if len(text)!=0:
        print(text)
        text = text.title()
        print(text)
        word_Lemmatized = WordNetLemmatizer()
        text = word_Lemmatized.lemmatize(text)
        print(text) 
        ls = tg.datalist()
        print(ls)
        word = it.similarWords(text)
        tex=sent_tokenize(text)
        print(tex)
        print(len(tex))
        print("word = ", word)
        if('.' not in text and len(word)!=0):   
            video = '../static/text_to_sign_videos/'+word[0]+'.mp4'
            return render_template('index.html', scroll='text2sign', check=check,  letters_img=letters_img, video=video)
    
        elif(len(tex)>1):
            print(tex)
            for i in range(0,len(tex)):
                clip.append(VideoFileClip('C:/Users/Dell/SC FINAL/static/text_to_sign_videos/'+word_Lemmatized.lemmatize(tex[i])+'mp4',target_resolution=(1080,1920)))
            final = concatenate_videoclips(clip)
            final.write_videofile("out.mp4")
            video = VideoFileClip("out.mp4")
            video.preview()
            return render_template('index.html', scroll='text2sign', check=check,letters_img=letters_img,video=video.preview())
        else:
            with open('data.csv', 'a', newline='') as fp:
                writer_object = writer(fp)
                lt = []
                lt.append(text)
                writer_object.writerow(lt)
                fp.close()
            return render_template('index.html', check=check, letters_img=letters_img, alertt='Video not Found !')
    
    else:
        file = request.files['textfile']
        file.save("./static/uploaded/file.txt")
        data=open('./static/uploaded/file.txt',"r")
        text = data.read() 
        print(text)
        text = text.title()
        print(text)
        word_Lemmatized = WordNetLemmatizer()
        text = word_Lemmatized.lemmatize(text)
        print(text) 
        ls = tg.datalist()
        #print(ls)
        word = it.similarWords(text)
        tex=sent_tokenize(text)
        #print(tg.splitter(text, sep))
        print(tex)
        print(len(tex))
        print("word = ", word)
        if('.' not in text and len(word)!=0):   
            video = '../static/text_to_sign_videos/'+word[0]+'.mp4'
            return render_template('index.html', scroll='text2sign', check=check, letters_img=letters_img, video=video)
    
        elif(len(tex)>1):
            print(tex)
            for i in range(0,len(tex)):
                clip.append(VideoFileClip('C:/Users/Dell/SC FINAL/static/text_to_sign_videos/'+word_Lemmatized.lemmatize(tex[i])+'mp4',target_resolution=(1080,1920)))
            final = concatenate_videoclips(clip)
            final.write_videofile("out.mp4")
            video = VideoFileClip("out.mp4")
            #video.preview()
            return render_template('index.html', scroll='text2sign', check=check, letters_img=letters_img,video=video.preview())
        else:
            with open('data.csv', 'a', newline='') as fp:
                writer_object = writer(fp)
                lt = []
                lt.append(text)
                writer_object.writerow(lt)
                fp.close()
            return render_template('index.html', check=check, letters_img=letters_img, alertt='Video not Found !')
    


@app.route("/uploadvideo/<file_name>", methods=['GET', 'POST'])
def download(file_name):
    global flag
    check=0
    rows = []
    # print('debuggggg')
    # print(file_name)
    temp = []
    temp.append(file_name)
    with open('data.csv', 'r') as fp:
        csvreader = csv.reader(fp)
        for row in csvreader:
            rows.append(row)
    # print(rows)
    rows.remove(temp)
    with open('data.csv', 'w', newline='') as fw:
        writerobj = writer(fw)
        writerobj.writerows(rows)
        fw.close()
    if(request.method == 'POST'):
        file = request.files['f1']
        file.save("./static/dataset/" + str(file_name) + ".mp4")
    inf = str(file_name) + '.mp4'
    outf = 'cart' + str(file_name) + '.mp4'
    ct.cartoonize(inf, outf, 0, 10)
    flag = 1
    return redirect('/inter')



@app.route('/video_feed1')
def video_feed1():
    return Response(gt.convert(1), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/gest_text_upload", methods=['GET', 'POST'])
def gest_text_upload():
    check=0
    file = request.files['f2']
    file.save("./static/uploaded/video.mp4")
    gt.convert(1)
    # os.remove("./static/uploaded/video.mp4")
    return render_template('index.html',scroll='sign2text', upload=1,  check=check, letters_img=letters_img)


@app.route('/video_feed')
def video_feed():
    return Response(gt.convert(0), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/gest_text_cam", methods=['GET', 'POST'])
def gest_text_cam():
    check=0
    gt.convert(0)
    return render_template('index.html',scroll='sign2text', webcam=1, check=check, letters_img=letters_img)


if __name__ == "__main__":
    global letters_img
    letters_img = []
    for i in "abcdefghijklmnopqrstuvwxyz":
        url = "../static/assets/img/letters/" + i + ".jpg"
        letters_img.append(url)

    print('Server Started !!')
    app.run(debug=True, use_reloader=False,port=80, host='0.0.0.0')
