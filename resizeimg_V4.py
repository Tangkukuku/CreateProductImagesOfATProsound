import cv2
import os
import numpy as np
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#path = os.path.dirname(__file__)
#path1 = os.path.join(path,'img') #เข้าไปที่โฟเดอร์ img

def cv2_imread_win(img_filepath, np):
    stream = open(img_filepath, "rb")
    bytes = bytearray(stream.read())
    numpyarray = np.asarray(bytes, dtype=np.uint8)
    return cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)

def cropimg(img,color) :
    #shapeimgtest = white.shape
    shapelogoATProsound = img.shape
    #หา roi_height_first_on
    roi_height_first_on = shapelogoATProsound[0]
    #หา roi_weight_end_under
    roi_weight_end_under = 0
    #หา roi_height_first_left
    roi_height_first_left = shapelogoATProsound[1]
    #หา roi_weight_end_right
    roi_weight_end_right = 0

    logoATProsoundcrop = img
    for y in range(len(img)) :# h
        for x in range(len(img[y])):
            if list(img[y][x]) != list([color,color,color]) :
                if y < roi_height_first_on :
                    roi_height_first_on = y

                if y > roi_weight_end_under :
                    roi_weight_end_under = y
        
                if x < roi_height_first_left :
                    roi_height_first_left = x
                    
                if x > roi_weight_end_right :
                    roi_weight_end_right = x
    
    logoATProsoundcrop=img[roi_height_first_on:roi_weight_end_under,roi_height_first_left:roi_weight_end_right]
    return logoATProsoundcrop

def getcropimg(img) :
    i = 255
    while i > 245 :
        if list(img[0][0]) == [i,i,i] :
            img = cropimg(img,i)
        i = i - 1
    return img

def resizeimg(img,scale_percent) :
    height = int(img.shape[0] * scale_percent / 100)
    weight = int(img.shape[1] * scale_percent / 100)
    resize = cv2.resize(img,(weight,height), interpolation = cv2.INTER_AREA)
    return resize

def resizeimg_auto(logo,fixheight,fixweight) :
    #logo = resizeimg(logo,50)
    nlogo = logo.shape
    scale_percent_logo = 100
    hlogo = nlogo[0]
    wlogo = nlogo[1]
    if hlogo < fixheight and wlogo < fixweight :
        while hlogo < fixheight and wlogo < fixweight : # ขยายภาพ
            scale_percent_logo = scale_percent_logo + 1
            hlogo = (nlogo[0]/100)*scale_percent_logo
            wlogo = (nlogo[1]/100)*scale_percent_logo
        scale_percent_logo = scale_percent_logo - 1
    else :
        while hlogo > fixheight or wlogo > fixweight : #ย่อภาพ
            scale_percent_logo = scale_percent_logo - 1
            hlogo = (nlogo[0]/100)*scale_percent_logo
            wlogo = (nlogo[1]/100)*scale_percent_logo
    logo = resizeimg(logo,scale_percent_logo)
    return logo

def insert_img(img_main,insert_img,y,x):
    len_img = insert_img.shape

    height = 0
    for H in range(y, len_img[0]+y):
        weight = 0
        for W in range(x, len_img[1]+x):
            #print(white[H][W],H,W)
            img_main[H][W] = insert_img[height][weight]
            #img_main[H][W] = [0,0,255]
            weight = weight + 1
        height = height + 1
    return img_main

def add_ATProsound(dirs):
    x = 1
    for i in dirs :
        if "-ATProsound" in i :
            continue
        else :
            ii = i.split(".")
            os.rename(string+"\\"+i, string+"\\"+ii[0]+"-ATProsound."+ii[len(ii)-1])
            x = x + 1  

def bg_white(bg):
    HH = 0
    nbg = bg.shape
    for H in range(nbg[0]):
        WW = 0
        for W in range(nbg[1]):
            #print(white[H][W],H,W)
            bg[H][W] = [255,255,255]
            WW = WW + 1
        HH = HH + 1
    return bg

def center(len_white_img,len_img2):
    outputH = int((len_white_img[0]-len_img2[0])/2)
    outputW = int((len_img2[1]-len_white_img[1])/2)
    if outputH < 0 :
        outputH = outputH *-1
    if outputW < 0 :
        outputW = outputW *-1
    return outputH,outputW

def check_last_name(dirs):
    s = []
    for i in dirs :
        n = len(i)
        if i[n-4] == "." and i[n-3] == "j" and i[n-2] == "p" and i[n-1] == "g" :
            s.append(i)
        elif i[n-4] == "." and i[n-3] == "p" and i[n-2] == "n" and i[n-1] == "g" :
            s.append(i)
        elif i[n-4] == "." and i[n-3] == "J" and i[n-2] == "P" and i[n-1] == "G" :
            s.append(i)
        elif i[n-4] == "." and i[n-3] == "P" and i[n-2] == "N" and i[n-1] == "G" :
            s.append(i)
        elif i[n-5] == "." and i[n-4] == "่j" and i[n-3] == "p" and i[n-2] == "e" and i[n-1] == "g" :
            s.append(i)
    dirs = s
    return dirs

def Remove_logo_upper_right(img):
    nimg = img.shape
    height = int((nimg[0]/100)*15)
    weight = int((nimg[1]/100)*85)
    for h in range(0,height):
            for w in range(weight,nimg[1]):
                img[h][w] = img[0][0]
                #img[h][w] = [0,255,255]
    return img

def text_size_auto(text,fontname):
    path = os.getcwd()
    white = np.zeros((250,700,3), np.uint8)
    white  = bg_white(white)

    color_coverted = cv2.cvtColor(white, cv2.COLOR_BGR2RGB)

    pil_image = Image.fromarray(color_coverted)

    I1 = ImageDraw.Draw(pil_image)

    font = ""
    if fontname == "BoldItalic" :
        font = ImageFont.truetype(path+"\\font\Kanit-BoldItalic.ttf", 48)
    elif fontname == "ExtraLight" :
        font = ImageFont.truetype(path+"\\font\Kanit-Regular.ttf", 35)

    I1.text((35, 35),text, font=font, fill =(0, 0, 0))

    white = np.array(pil_image) 
    white = white[:, :, ::-1].copy()

    white = getcropimg(white)

    return white

path = os.getcwd()
logoATProsound = cv2.imread(path+"\logoATProsound\logoATProsound.jpg")
OFFICIAL_STORE = cv2.imread(path+"\OFFICIAL_STORE\OFFICIAL_STORE.png")

OFFICIAL_STORE = cv2.resize(OFFICIAL_STORE,(512,100), interpolation = cv2.INTER_AREA)
logoATProsound = resizeimg(logoATProsound,25)


#logoAlesis = cv2.imread(r"E:\year4\project\project\logoAlesis.jpg")
while True :

    string = input("path folder :")
    dirs = os.listdir( str(string) )
    add_ATProsound(dirs)
    dirs = os.listdir( str(string) )
    dirs = check_last_name(dirs)
    for i in dirs :
        print(i)
    
    for i in dirs :
        check_remove_logo = -1
        t0 = time.time()
        logoTrue_False = True
        try : 
            logo = i.split(".")
            logo = logo[0].split("_")
            model = logo[1]
            text = logo[2].replace('-ATProsound', '')
            if len(logo) > 3 :
                check_remove_logo = logo[3].find("removelogo")
            logo = path+"\logo\\"+logo[0]+".jpg"
            logo = cv2.imread(logo)
            fixheightlogo,fixweightlogo = 100,274
            logo = resizeimg_auto(logo,fixheightlogo,fixweightlogo)
            nlogo = logo.shape
            
        except AttributeError :
            print("name pid")
            logoTrue_False = False

        string = string +"\\"
        img = cv2_imread_win(string+i,np)

        if check_remove_logo != -1 :
            #img = resizeimg(img,25)
            img = Remove_logo_upper_right(img)

        img = getcropimg(img)

        white = np.zeros((1024,1024,3), np.uint8)
        white  = bg_white(white)
        nwhite = white.shape
        #len_img = img.shape
        #len_img2 = ""
        #len_white_img = white.shape

        fixheightimg = 700
        fixweightimg = 700

        img = resizeimg_auto(img,fixheightimg,fixweightimg)
        nimg = img.shape
        white = insert_img(white,img,int((nwhite[0]-nimg[0])/2),int((nwhite[1]-nimg[1])/2))

        #white = Remove_logo_upper_right(white)

        #shapeimgtest = white.shape

        #logoATProsound = cropimg(logoATProsound)
        
        model = text_size_auto(model,"BoldItalic")
        nmodel = model.shape
        text = text_size_auto(text,"ExtraLight")
        ntext = text.shape
        
        white = insert_img(white,model,nwhite[0]-100-nmodel[0],nwhite[1]-35-nmodel[1])
        white = insert_img(white,text,nwhite[0]-80-ntext[0]+nmodel[0],nwhite[1]-35-ntext[1])


        white = insert_img(white,logoATProsound,35,35)
        white = insert_img(white,OFFICIAL_STORE,924,0)
        if logoTrue_False :
            white = insert_img(white,logo,int((150-nlogo[0])/2),nwhite[1]-35-nlogo[1])
        
        #font = cv2.FONT_HERSHEY_SIMPLEX

        #cv2.putText(white,'มิกเซอร์',(1024-35-35,1024-500), font, 2,(0,0,0),10)

        cutname = i.split('.')
        cutname2 = cutname[0].split("_")
        filename = string+"\\"+cutname2[0]+" "+cutname2[1]+" "+"-ATProsound.jpg" #+"-ATProsound.jpg"
        cv2.imwrite(filename, white)
        print(cutname[0]," done","(",int(time.time() - t0),"s",")")

        #cv2.imshow("img",img)
        #cv2.imshow("white",white)

    print("Success")
