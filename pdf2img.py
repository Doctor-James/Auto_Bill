import skimage.io as io
from skimage import data_dir
import os
import sys
import fitz
from PIL import Image

def pdf2img(filename):
	#  打开PDF文件，生成一个对象
	doc = fitz.open(filename)
	#print("共",doc.pageCount,"页")
	for pg in range(doc.pageCount):
		#print("\r转换为图片",pg+1,"/",doc.pageCount,end="")
		page = doc[pg]
		rotate = int(0)
		# 每个尺寸的缩放系数为8，这将为我们生成分辨率提高64倍的图像。
		zoom_x = 8.0
		zoom_y = 8.0
		trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
		pm = page.getPixmap(matrix=trans, alpha=False)
		imgname = './imgs/'+ filename[6:-4]+'.png'
		pm.writePNG(imgname.format(pg))

def get_filename(path,filetype):
	name=[]
	for root, dirs, files in os.walk(path):
		for i in files:
			if filetype in i:
				name.append(i.replace(filetype,''))
	return name

str='./pdf/*.pdf'
filenames = get_filename('./pdf/','')
for i in range(len(filenames)):
	filenames[i] = './pdf/' + filenames[i]
	pdf2img(filenames[i])
print('Done')