'''cv41: 滑鼠事件'''
import numpy as np
import cv2 as cv

buttonDown = False  # 滑鼠左鍵是否按下(全域面數)
buttonDownr = 1  # 滑鼠右鍵是否按下(全域面數)
ix, iy = -1, -1
blended = res1 = res2 = -1
# mouse callback function


def onmouse(event, x, y, flags, param):
    global ix, ix, buttonDown, buttonDownr
    if event == cv.EVENT_LBUTTONDOWN:  # 按下滑鼠左鍵
        buttonDown = True  # 繪畫狀態
        ix, iy = x, y
        # cv.destroyWindow('roi')  # 刪除 roi 視窗
    elif event == cv.EVENT_MOUSEMOVE:  # 滑鼠移動中
        if buttonDown == True:  # 繪畫狀態
            cv.circle(img1, (x, y), 6, (0, 255, 255), -1)  # 在游標位置繪製黃色圓形
    elif event == cv.EVENT_LBUTTONUP:  # 滑鼠左鍵彈起
        buttonDown = False  # 非繪畫狀態
    elif event == cv.EVENT_RBUTTONDOWN:
        buttonDownr = 0
        # cv.destroyWindow('draw')  # 刪除 draw 視窗

 # 讀取滑桿數值並處理之function


def onTrackbar(x):
    global blended, res1, res2
    slider1 = cv.getTrackbarPos('weight', 'fusion')  # 讀取滑桿數值
    slider2 = cv.getTrackbarPos('size', 'fusion')  # 讀取滑桿數值
    slider3 = cv.getTrackbarPos('negative', 'fusion')  # 讀取滑桿數值
    # 定义融合的权重
    alphaw = slider1/100
    betaw = 1-alphaw
    alphas = slider2/100
    betas = alphas
    # 获取两张图像的大小
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]

    fx = 0.5+alphas
    fy = 0.5+betas
    # 将im1的大小调整为im2的大小
    img3 = cv.resize(img1, (int(w2), int(h2)))

    # 将两个图像加权融合
    img_mix = cv.addWeighted(img3, alphaw, img2, betaw,  0)
    blended = img_mix.copy()
    # 計算負片效果
    blended[:, :slider3] = 255 - blended[:, :slider3]

    # ret, thresh = cv.threshold(
    #    blended, slider1, 255, cv.THRESH_BINARY)  # 根據 t 值做影像二值化
    # cv.imshow('fusion', blended)  # 显示融合后的图像
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    # 讀取sliders的資料
    # 注意slider2不得等於0
    # 算出im2的寬高
    # 讓im1縮小成im2的寬高，縮小後稱為im3
    # 建立跟im2一樣大的黑影像im4
    # 將縮小的im3貼入im4的中央
    # 根據slider1的數值,用cv2.addWeighted對im2與im4加權混合
    # .....
    # 顯示影像


# part1
print('press esc to exit:')
print('press r to reset 滑桿 in part2:')
print('click left button')
# Create a black image, a window and bind the function to window
img1 = np.zeros((400, 400, 3), np.uint8)
print('shape of img1:')
print(np.shape(img1))  # 顯示影像尺寸
cv.namedWindow('draw')
cv.setMouseCallback('draw', onmouse)  # 建立滑鼠反應函式

while (1):  # 永久迴圈
    cv.imshow('draw', img1)  # 顯示影像
    k1 = cv.waitKey(1) & 0xFF
    if k1 == 27:  # 按 Esc 離開
        break
    elif buttonDownr == 0:
        break


cv.destroyWindow('draw')  # 關閉視窗
# part2
# img2 = cv.imread('./data/ntust.jpg')  # 將影像開啟
img2 = cv.imread('F:/ntust_image_process/Example-Part6/Example-Part6/data/ntust.jpg')  # 將影像開啟
"F:\ntust_image_process\Example-Part6\Example-Part6\data\ntust.jpg"
print('shape of img2:')
print(np.shape(img2))  # 顯示影像尺寸
slider3_max = img2.shape[1]
print('shape of slider3_max:')
print(slider3_max)  # 顯示影像尺寸
cv.namedWindow('fusion')  # 視窗命名
# cv.imshow('fusion', img2)  # 顯示影像
cv.createTrackbar('weight', 'fusion', 50, 100, onTrackbar)  # 建立滑桿1
cv.createTrackbar('size', 'fusion', 50, 100, onTrackbar)  # 建立滑桿2
cv.createTrackbar('negative', 'fusion', 50, slider3_max, onTrackbar)  # 建立滑桿3
# cv.createTrackbar(滑桿名稱, 從屬視窗名稱, 調整值, 最大值, 反應函式)

while (1):  # 無限迴圈

    cv.imshow('fusion', blended)  # 显示融合后的图像
    k2 = cv.waitKey(10) & 0xFF  # 等待任意鍵輸入
    if k2 == 27:  # 如果是 Esc (ASCII 第27號)，脫離迴圈
        break
    elif k2 == 114:
        # press r to reset 滑桿
        cv.setTrackbarPos('weight', 'fusion', 50)
        cv.setTrackbarPos('size', 'fusion', 50)
        cv.setTrackbarPos('negative', 'fusion', 50)


cv.destroyAllWindows()  # 關閉所有視窗
