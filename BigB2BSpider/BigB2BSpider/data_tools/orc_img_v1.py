# import re
# import time
#
# import pytesseract
# import requests
# from PIL import Image
#
# # with open("a.jpg" ,"ab")as f:
# #     f.write(res.content)
#
# # pytesseract.pytesseract.tesseract_cmd = 'D://tesseract_w64//tesseract.exe'
# # tessdata_dir_config = '--tessdata-dir "D://tesseract_w64//tessdata"'
#
# def recognition_image(path):
#     img = Image.open(path)
#     img = img.convert('RGBA')  # 转换为RGBA
#     pix = img.load()  # 读取为像素
#     for x in range(img.size[0]):  # 处理上下黑边框
#         pix[x, 0] = pix[x, img.size[1] - 1] = (255, 255, 255, 255)
#     for y in range(img.size[1]):  # 处理左右黑边框
#         pix[0, y] = pix[img.size[0] - 1, y] = (255, 255, 255, 255)
#     for y in range(img.size[1]):  # 二值化处理，这个阈值为R=95，G=95，B=95
#         for x in range(img.size[0]):
#             if pix[x, y][0] < 95 or pix[x, y][1] < 95 or pix[x, y][2] < 95:
#                 pix[x, y] = (0, 0, 0, 255)
#             else:
#                 pix[x, y] = (255, 255, 255, 255)
#     str = pytesseract.image_to_string(img, lang='chi_sim')
#     # str = pytesseract.image_to_string(img, lang='eng')
#     # image_to_string(image, lang='eng', config=tessdata_dir_config)
#
#     print(str)
#     # return str
# # recognition_image()
#
# if __name__ == '__main__':
#     # recognition_image()
#     print(recognition_image("image.png"))
#
#
# # import requests
# #
# # session = requests.Session()
# #
# # api_url = "https://api-cn.faceplusplus.com/imagepp/v1/recognizetext"
# # headers = {
# #     "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
# #     "user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36",
# # }
# #
# # image_url = 'http://www.cntrades.com/extend/image.php?auth=b5b7l4-S-xkHmJwCCHGw-S-pQ6GQ6pvELDxAdDGZVkFDZjaBtrd9y5kE4UA3hw'
# # api_key = 'gd8LgteLrzNwhjj57n81QGYIYHlLAdMX'
# # api_secret = 'rm0RXBA6KQ2yx-MJSYzhYaGkxi1usRoZ'
# # data = {
# #     'url': image_url
# # }
# # res = session.post(url=api_url,data=data,headers=headers,timeout=10)
# # print(res.text)
#
