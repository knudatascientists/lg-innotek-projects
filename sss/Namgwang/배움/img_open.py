import pandas as pd 
import numpy as np
import cv2
PATH = r"C:\Users\USER\Documents\GitHub\python_exer\221027\scatter_plot.png"
img = cv2.imread(PATH)

img2 = cv2.copyTo(img, None)
img2[50:100,:,:] = 0

cv2.imshow("scatter", img)
cv2.imshow("scatter_new", img2)