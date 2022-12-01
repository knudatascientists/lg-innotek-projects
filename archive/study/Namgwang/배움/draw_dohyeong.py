import pandas as pd 
import numpy as np
import cv2

img = np.zeros([500,500,3], np.uint8)

cv2.rectangle(img, (10,10), (100,100), (0,0,225), thickness=1)

cv2.line(img, (10,300), (100,300), (0,255,0), thickness=3)

cv2.putText(img, "hello", (200,100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255))

cv2.circle(img, (300,300), 20, (0, 255,255))

pointsl = np.array([[350,350], [360,410], [370,420], [450,460] ], np.int32)

cv2.polylines(img, [pointsl], True, (255,0,0))

# cv2.ellipse(img, (300,150))
cv2.imshow("img", img)
cv2.waitKey(0)