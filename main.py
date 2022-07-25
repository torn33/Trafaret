import cv2
import easyocr
from matplotlib import pyplot as pl
from datetime import datetime
import glob
import openpyxl
import difflib
import os

def similarity(s1, s2):
  normalized1 = s1.lower()
  normalized2 = s2.lower()
  matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
  return matcher.ratio()
# подключаем камеру
#  video = cv2.VideoCapture("rtsp://admin:1994ok@192.168.1.9/user=admin_password=1994ok_channel=2_stream=0.sdp")
#  ret, frame = video.read()  # выделяем кадр
#  cv2.imwrite('img/cam.png', frame)  # сохраняем кадр
try:
    img = cv2.imread('img/g5.jpg')  # открываем кадр
except:
    print('Ошибка! Исходное изображениие не получено!')
    exit()

trafs = cv2.CascadeClassifier('tr.xml')   # подключаем навык нейросетки

results = trafs.detectMultiScale(img, scaleFactor=1.05, minNeighbors=15)  # ищем номер


for (x, y, w, h) in results:   # получаем из цикла координаты номера
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), thickness=3)  # обрамляем номер в прямоугольник
    x1 = x
    x2 = x+w
    y1 = y
    y2 = y + h
#  print(x1,y1,x2,y2)
try:
   cropped = img[y1:y2, x1:x2]
except:
    print('Ошибка! Исходное изображениие не обнаружено!')
    exit()
if os.path.isdir("arh/") == False:
    os.mkdir("arh/")
current_datetime = datetime.now()
path="arh/"+str(current_datetime)+".jpg"
path = path.replace(":", "-")

cv2.imwrite(path, img)
gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)  # делаем скриншот серым

# threshold the image
#img_filter = cv2.bilateralFilter(gray, 50, 50, 50)
#img_binary = cv2.threshold(img_filter, thresh, 255, cv2.THRESH_BINARY)[1]
ret, threshold = cv2.threshold(gray, 80, 255, 0)

text = easyocr.Reader(['en'], gpu=True)  # задаем язык распознавания
text = text.readtext(threshold, detail=0, paragraph=1, text_threshold=0.5, low_text=0.4, contrast_ths=0.3, allowlist = ['A', 'B', 'C', 'E', 'H', 'K','M', 'O', 'P', 'T', 'X', 'Y', '1', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'])   # распознаем текст с картинки
num_str = ""
for str_get in text:
    num_str += str_get
num_str = num_str.replace(" ", "")
print(num_str)

for file in glob.glob("*.xlsx"):  # ищем exel файл
    pass

try:
    book = openpyxl.open(file, read_only=True)
    sheet = book.active

except:
    print('Ошибка! Таблица номеров не обнаружена!')
    exit()
max_reliability=0
num_reliability=""
for row in range(2,sheet.max_row+1):

    #print(sheet[row][0].value)
    if max_reliability<similarity(sheet[row][0].value, num_str)*100:
        max_reliability = int(similarity(sheet[row][0].value, num_str)*100)
        num_reliability = sheet[row][0].value
if max_reliability<42:
    print("Недостаточное совпадение по Таблице ("+str(max_reliability)+"%)")
    print("Вероятный номер (" + num_reliability + ")")
else:
    print("Процент совпадения "+str(max_reliability)+"%")
    print("Вероятный номер ("+num_reliability+")")


#print("Вероятное совпадение"+num_reliability+"(Процент достоверности-"+str(max_reliability)+")")





pl.imshow(cv2.cvtColor(threshold, cv2.COLOR_BGR2RGB))  # выводим изображение


pl.show()

#print(upper_text)  # выводим распознанный текст







