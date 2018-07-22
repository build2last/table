from cv import imageCls
from cv import motionDetect

def test_img_cls_local():
    content = """[{'score': 0.836916, 'root': '商品-容器', 'keyword': '烧杯'}, {'score': 0.798096, 'root': 'Logo', 'keyword': '上好佳'}, {'score': 0.42774, 'root': '商品-容器', 'keyword': '杯子'}, {'score': 0.227892, 'root': '商品-容器', 'keyword': '玻璃杯'}, {'score': 0.02766, 'root': '商品-电脑办公', 'keyword': '回形针'}]"""#imageCls.shoot_now()
    print(content)


def test_img_cls():
    img = "cv/motion.jpg"
    prob, tag = imageCls.what_is_img(img)
    print(content)


if __name__ == '__main__':
    motionDetect.exe()