import pyautogui
import time
import pyscreeze
import cv2
import pyperclip

screenWidth, screenHeight = pyautogui.size()
screenScale = 1
msg_flag = 0


def search(img, x_Deviation, y_Deviation, mousebutton):
    global msg_flag
    time.sleep(1)
    target = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    # 先截图
    screenshot = pyscreeze.screenshot('.//my_screenshot.png')
    # 读取图片 灰色会快
    temp = cv2.imread(r'.//my_screenshot.png', cv2.IMREAD_GRAYSCALE)

    theight, twidth = target.shape[:2]
    tempheight, tempwidth = temp.shape[:2]
    print("目标图宽高：" + str(twidth) + "-" + str(theight))
    print("模板图宽高：" + str(tempwidth) + "-" + str(tempheight))
    # 先缩放屏幕截图 INTER_LINEAR INTER_AREA
    scaleTemp = cv2.resize(temp, (int(tempwidth / screenScale), int(tempheight / screenScale)))
    stempheight, stempwidth = scaleTemp.shape[:2]
    print("缩放后模板图宽高：" + str(stempwidth) + "-" + str(stempheight))
    # 匹配图片
    res = cv2.matchTemplate(scaleTemp, target, cv2.TM_CCOEFF_NORMED)
    mn_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print(max_val)
    if (max_val >= 0.9):
        # 计算出中心点
        top_left = max_loc
        bottom_right = (top_left[0] + twidth, top_left[1] + theight)
        tagHalfW = int(twidth / 2)
        tagHalfH = int(theight / 2)
        tagCenterX = top_left[0] + tagHalfW
        tagCenterY = top_left[1] + tagHalfH
        # 左键点击屏幕上的这个位置
        pyautogui.click(tagCenterX + x_Deviation, tagCenterY + y_Deviation, button=mousebutton)
    else:
        msg_flag = 1
        print("没找到")


search(r".//wechat_msg.png", 0, -90, 'right')
search(r".//wechat_copy.png", 0, 0, 'left')
if msg_flag == 1:
    search(r".//wechat_msg2.png", -150, -90, 'right')
    search(r".//wechat_copy.png", 0, 0, 'left')
    msg_flag = 0
wechat_msg = pyperclip.paste()
search(r".//qq_msg.png", 0, -90, 'right')
search(r".//qq_copy.png", 0, -15, 'left')
qq_msg = pyperclip.paste()

while True:
    search(r".//wechat_msg.png", 0, -90, 'right')
    search(r".//wechat_copy.png", 0, 0, 'left')
    if msg_flag == 1:
        search(r".//wechat_msg2.png", -110, -90, 'right')
        search(r".//wechat_copy.png", 0, 0, 'left')
        msg_flag = 0
    if str(pyperclip.paste()) != str(wechat_msg):
        wechat_msg = pyperclip.paste()
        if '#' in str(wechat_msg):
            search(r".//qq_msg.png", 0, 90, 'left')
            pyautogui.hotkey('ctrl', 'v')
            search(r".//qq_send.png", 0, 0, 'left')
            time.sleep(2) # 等待Yunzai回应

            search(r".//qq_msg.png", 0, -90, 'right')
            search(r".//qq_copy.png", 0, -15, 'left')
            while msg_flag == 1:
                time.sleep(2)
                msg_flag = 0
                search(r".//qq_msg.png", 0, -90, 'right')
                search(r".//qq_copy.png", 0, -15, 'left')
            qq_msg = pyperclip.paste()
            search(r".//wechat_msg.png", 0, 90, 'left')
            pyautogui.hotkey('ctrl', 'v')
            search(r".//wechat_send.png", 0, 0, 'left')

    search(r".//qq_msg.png", 0, -90, 'right')
    search(r".//qq_copy.png", 0, -15, 'left')
    if str(pyperclip.paste()) != str(qq_msg):
        qq_msg = pyperclip.paste()
        search(r".//wechat_msg.png", 0, 90, 'left')
        pyautogui.hotkey('ctrl', 'v')
        search(r".//wechat_send.png", 0, 0, 'left')

    print("wait next loop")
    time.sleep(5)

# pyautogui.moveTo(200,400,duration=0)