import cv2
import numpy as np
import skimage.io as io
from skimage import data_dir
import os
import sys
import fitz
# from reportlab.lib.pagesizes import portrait
# from reportlab.pdfgen import canvas
from PIL import Image

def pdf2img(filename=r'./HDMI.pdf'):
	#  打开PDF文件，生成一个对象
	doc = fitz.open(filename)
	print("共",doc.pageCount,"页")
	for pg in range(doc.pageCount):
		print("\r转换为图片",pg+1,"/",doc.pageCount,end="")
		page = doc[pg]
		rotate = int(0)
		# 每个尺寸的缩放系数为8，这将为我们生成分辨率提高64倍的图像。
		zoom_x = 8.0
		zoom_y = 8.0
		trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
		pm = page.getPixmap(matrix=trans, alpha=False)
		pm.writePNG(r'./tu'+'{:02}.png' .format(pg))
	print()

def img_reshape(img_ori):
    GrayImage = cv2.cvtColor(img_ori, cv2.COLOR_BGR2GRAY)
    ret, img_thresh = cv2.threshold(GrayImage, 250, 255, cv2.THRESH_BINARY)
    coords = np.column_stack(np.where(img_thresh < 255))
    coords = coords[:, ::-1]  # x, y互换
    min_rect = cv2.minAreaRect(coords)
    box = cv2.boxPoints(min_rect)
    box = np.int0(box)
    cv2.drawContours(img_thresh, [box], 0, [0, 255, 0], 1)
    box_x = [i[0] for i in box]
    box_y = [i[1] for i in box]
    area1 = img_ori[min(box_y):max(box_y), min(box_x):max(box_x)]  # y,x
    img = cv2.resize(area1, (1400, 900))
    return img

def img_div(img_ori):
    img = img_reshape(img_ori)
    # area1 = img[328:522,0:380] #名称
    # area2 = img[328:522,486:568] #单位
    # area3 = img[328:522,568:731] #数量
    area1 = img[328:578, :]
    area2 = img[:170, 980:]
    img_vector = []
    img_vector.append(area1)
    img_vector.append(area2)
    return img_vector
    # cv2.imshow('ss', img)
    # cv2.imshow('area1', area1)
    # cv2.imshow('area2', area2)
    # cv2.waitKey(0)

# str='./bills/*.png'
# coll = io.ImageCollection(str)
# for i in range(len(coll)):
#     img_vector = img_div(coll[i])
#     cv2.imshow('area1', img_vector[0])
#     cv2.imshow('area2', img_vector[1])
#     cv2.waitKey(0)
pdf2img()
