import cv2
import numpy as np
# PATH = r"C:\Users\USER\Documents\GitHub\python_exer\221027\scatter_plot.png"
img = cv2.imread("./Lenna.png")

cv2.imshow("scatter",img)
cv2.waitKey(0)

# img = cv2.imread(".\scatter_plot.png")

# cv2.destroyAllWindows()
# python select interpretor
# ctrl + f5
# uint8
# cv2.imwrite("./Lenna.png", "scatter", [cv2.IMWRITE_JPEG_QUALITY, 95])

