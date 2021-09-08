import cv2
import numpy as np

class Kordinat:
    def __init__(self,first_x=0,first_y=0,sec_x=0,sec_y=0,bolgeAdi="",sayac=0,girenler=0,cikanlar=0,tempSayac=0):
        self.fX = first_x
        self.fY = first_y
        self.sX = sec_x
        self.sY = sec_y
        self.bolgeAdi = bolgeAdi
        self.sayac = sayac
        self.girenler = girenler
        self.cikanlar = cikanlar
        self.tempSayac= tempSayac
#http://velospeer.spdns.org/mjpg/video.mjpg

cap = cv2.VideoCapture("http://velospeer.spdns.org/mjpg/video.mjpg")
fgbg = cv2.createBackgroundSubtractorMOG2()
fgbg.setShadowValue(0)
line = 300
peopleout,peoplein = 0,0
contours_previous = []
contours_now = []
sayac = 0
tempKordinat = Kordinat()
kordinatlar = []
maskelenmisler = []
extract = False
selected_ROI = False
drawing = False
ix = -1
iy = -1
def extract_coordinates(event, x, y, flags, parameters):
    global drawing,tempKordinat
    if event == cv2.EVENT_LBUTTONDOWN:
        tempKordinat.fX = x
        tempKordinat.fY = y
    elif event == cv2.EVENT_LBUTTONUP:
        tempKordinat.sX = x
        tempKordinat.sY = y
        tempKordinat.bolgeAdi = input("Bölgenin adını giriniz :")
        kordinatlar.append(tempKordinat)
        cv2.rectangle(frame,(100,200), (200,400), (0, 255, 0), 2)
        tempKordinat = Kordinat(0,0,0,0,"")
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", extract_coordinates)
while(cap.isOpened()):
    ret, frame = cap.read()
    for kordinat in kordinatlar:
        maske = fgbg.apply(frame).copy()[kordinat.fY:kordinat.sY, kordinat.fX:kordinat.sX]
        try:
            thresh = cv2.dilate(maske,None,iterations=1)
        except:
            continue
        contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        f = frame[kordinat.fY:kordinat.sY, kordinat.fX:kordinat.sX]
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < 1000:
                continue
            (x,y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(f, (x, y), (x + w,y + h), (0, 255, 0), 2)
            cv2.drawContours(f, [contour], -1, (0, 0, 255), 2)
            kordinat.sayac+=1
        if kordinat.sayac > kordinat.tempSayac:
            kordinat.girenler += kordinat.sayac-kordinat.tempSayac
        elif kordinat.sayac < kordinat.tempSayac:
            kordinat.cikanlar += kordinat.tempSayac - kordinat.sayac
        cv2.putText(frame, "Mevcut: " + str(kordinat.sayac) ,(kordinat.fX+10,kordinat.fY-10),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,2)
        cv2.putText(frame, "Toplam: "+ str(kordinat.girenler),(kordinat.fX+10,kordinat.sY+30),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,2)
        cv2.rectangle(frame, (kordinat.fX, kordinat.fY), (kordinat.sX, kordinat.sY), (102, 0, 153), 4)
        cv2.putText(frame, "{}".format(kordinat.bolgeAdi), (int(((kordinat.sX-kordinat.fX)/2)+kordinat.fX)-30,int(((kordinat.sY-kordinat.fY)/2)+kordinat.fY)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        kordinat.tempSayac = kordinat.sayac
        kordinat.sayac=0
        
    cv2.imshow("Frame",frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
