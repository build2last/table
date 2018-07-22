"""图片获取模块

1. 选择拍摄时机；
2. 响应其他模块获取图片的需求
"""

import math
import cv2
import time

def get_image(latest=True, save_to=""):
    cap = cv2.VideoCapture(0)
    try:
        ret, frame = cap.read()
        cap.release()
        cv2.destroyAllWindows()
        # Our operations on the frame come here
        filename = save_to
        if latest:
            cv2.imwrite(filename, frame)            
    except Exception as e:
        print(e)
    finally:
        cap.release()
        cv2.destroyAllWindows()
    return filename


if __name__ == '__main__':
    get_image()