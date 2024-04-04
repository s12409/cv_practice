import cv2  # 載入opencv套件
import numpy as np  # 匯入 NumPy 套件


face_counter = 0
# 設定PUTTEXT()文字相關參數
textP = 'B10832014'
org = (181, 200)
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
color = (0, 255, 255)  # yellow
thickness = 2
lineType = cv2.LINE_AA
# 在圖像左上角繪製 "Wake Up!" 字樣
textw = 'Wake Up!'
orgw = (10, 30)
fontw = cv2.FONT_HERSHEY_SIMPLEX
fontScalew = 1
colorw = (0, 255, 255)  # yellow
thicknessw = 2
lineTypew = cv2.LINE_AA
color2 = (255, 0, 255)

# 解析 FourCC 視訊編解碼器四字元識別碼


def decode_fourcc(v):
    v = int(v)
    codec = "".join([chr((v >> 8 * i) & 0xFF) for i in range(4)])
    return codec  # 將32位元的 v, 分四段分別轉換為ASCII字元


# 載入人臉/人眼偵測訓練集
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
# 建立視訊或相機物件
img = cv2.VideoCapture("sleepy.mp4")

# 讀取視訊參數
height = img.get(cv2.CAP_PROP_FRAME_HEIGHT)  # 視訊畫面高
width = img.get(cv2.CAP_PROP_FRAME_WIDTH)  # 視訊畫面寬
fps = img.get(cv2.CAP_PROP_FPS)  # 視訊幀率
total_count = img.get(cv2.CAP_PROP_FRAME_COUNT)  # 視訊總幀數
print("影像高,寬: %d x %d" % (height, width))
print("視訊幀率(FPS, Frame Per Second): %.2f" % fps)
print("視訊總幀數: %d" % total_count)

# 取得 Codec 名稱
fourcc = img.get(cv2.CAP_PROP_FOURCC)
codec = decode_fourcc(fourcc)
print("視訊編解碼器四字元識別碼 (FourCC Codec): " + codec)

while True:  # 用無窮迴圈讀取影片中每個畫格(幀)
    ret, frame = img.read()  # 讀取影片中的畫格
    if ret == True:  # 若有讀取到影片中的畫格

        ###### 偵測膚色 #######
        # ROI是高寬25%:75%範圍
        # 將ROI從 BGR 轉換至 HSV 色空間(用 cvtColor())
        # 定義 HSV (hue, saturation, value) 空間的膚色上下界範圍(下界約 (0,50,50), 上界約 (80,180,220))
        # 註：HSV的範圍上限 [180, 256, 256]
        # 取HSV色空間下，ROI範圍內的膚色遮罩(用inRange())
        # 算出膚色面積率，也就膚色遮罩非零數值佔遮罩面積的比率(用np.count_nonzero()，可用mask[:]忽略維度，用round(,精度)四捨五入)
        # 如果膚色面積率高於0.07，代表「有膚色」，否則代表「無膚色」
        # 將膚色遮罩轉換為彩色格式(用cvtColor)
        # 在遮罩上加面積率數值(用putText())
        # 建立跟輸入影像一樣大，一樣格式的背景影像(用np.zeros())
        # 將背景影像設成灰色
        # 把膚色遮罩貼入背景影像
        frame1 = cv2.resize(frame, (0, 0), fx=0.75, fy=0.25)  # 影像縮小

        # 從 BGR 轉換至 HSV 色空間
        hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)

        # 定義 HSV (hue, saturation, value) 空間的色彩範圍
        lower_skin = np.array([0, 50, 50])
        upper_skin = np.array([80, 180, 220])  # maximum [180, 256, 256]

        # 取得色彩範圍內影像區域遮罩
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        # 計算遮罩的總像素數量
        total_pixels = mask.size

        # 計算非零元素的個數
        nonzero_pixels = np.count_nonzero(mask)

        # 計算膚色面積率
        skin_area_ratio = nonzero_pixels / total_pixels

        # 四捨五入到指定精度
        skin_area_ratio_rounded = round(skin_area_ratio, 2)  # 精度為 2

        # 輸出結果
        # print(f"膚色面積率: {skin_area_ratio_rounded}")
        if skin_area_ratio_rounded > 0.07:       # 計算膚色面積率高於0.07，視為「有膚色」
            countskin = 1
        elif skin_area_ratio_rounded < 0.07:    # 計算膚色面積率高於0.07，視為「no膚色」
            countskin = 2

        # 將膚色遮罩轉換為彩色格式(用cvtColor)
        color_mask2 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        cv2.putText(color_mask2, str(skin_area_ratio), orgw, fontw, fontScalew,
                    color2, thicknessw, lineTypew)  # 設定PUTTEXT()文字相關參數

        # 中值濾波 (除脈衝雜訊)
        # mask = cv2.medianBlur(mask, 7)

        # 根據遮罩複製影像
        # res= cv2.bitwise_and(frame, frame, mask= mask)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 影像轉灰階
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)  # 偵測人臉

        if len(faces) == 0 and countskin == 1:     # 偵測人臉「有膚色」但「無正臉」
            if face_counter == 10:  # 用face_counter來當文字顯示設定
                face_counter = face_counter-1
            elif 0 < face_counter < 10:
                face_counter -= 1
                cv2.putText(frame, textw, orgw, fontw, fontScalew,
                            colorw, thicknessw, lineTypew)  # 設定PUTTEXT()文字相關參數
        elif len(faces) == 0 and countskin == 2:     # 偵測人臉「no膚色」、「無正臉」
            if face_counter == 10:  # 用face_counter來當文字顯示設定
                face_counter = face_counter-1
            elif 0 < face_counter < 10:
                face_counter -= 1
                cv2.putText(frame, "Nobody", orgw, fontw, fontScalew,
                            color2, thicknessw, lineTypew)  # 設定PUTTEXT()文字相關參數
        else:
            face_counter = 10

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h),
                              (255, 0, 0), 2)  # 繪製人臉矩形框

                cv2.putText(frame, textP, org, font, fontScale, color,
                            thickness, lineType)    # 設定PUTTEXT()文字相關參數

        cv2.imshow("Video", color_mask2)  # 顯示該畫格
        cv2.imshow("Mask", frame)  # 顯示該畫格
        # 停每800/fps毫秒讀取鍵盤的按鍵
        key = cv2.waitKey(round(800/fps)) & 0xFF
        if key == 27:  # 當按鍵為ESC(ASCII碼為27)時跳出迴圈
            break
    else:  # 當沒讀到影片中的Frame時，跳出迴圈
        break

img.release()  # 釋放記憶體
cv2.destroyAllWindows()
