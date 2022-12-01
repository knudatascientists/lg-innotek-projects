import pandas as pd 
import numpy as np
import cv2

empty_mat = np.empty((500,500), np.float32)
zeros_mat = np.zeros((500,500))
ones_mat = np.ones((500,500))
ones_mat_int = np.ones((500,500), np.uint8)

cv2.imshow("empty_mat", empty_mat)
cv2.imshow("zeros_mat", zeros_mat)
cv2.imshow("ones_mat", ones_mat)
cv2.imshow("ones_mat_int", ones_mat_int)
cv2.waitKey(0)
cv2.destroyAllWindows()

zeros_mat.fill(10.)
ones_mat_int.fill(128)
cv2.imshow("zeros_mat_10", zeros_mat)
cv2.imshow("ones_mat_int_128", ones_mat_int)
cv2.waitKey(0)
cv2.destroyAllWindows()

my_mat = np.array([[255,255,0,0,255,255], [255,255,0,0,255,255]])
my_mat2 = np.array([[1.,1.,0.,0.,1.,1.], [1.,1.,0.,0.,1.,1.]])

print("img dtype", my_mat.dtype)
print("img ndim", my_mat.ndim)
print("img shape", my_mat.shape)