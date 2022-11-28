#%%
import os
import sys

import cv2
import ft_model
import silence_tensorflow
import tensorflow as tf

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import img_preprocess
import settings

silence_tensorflow.silence_tensorflow()
tf.random.set_seed(42)


ng = "../image/module/true_ng/GSY827AN870095_AAO10893K_PKT04_CM1EQSUA0011_20220807204205_DirectLight_NG.jpg"
ok = "../image/module/true_ok/GSY827AN7A1705_AAO18599K_PKT06_CM1EQSUA0012_20220711200838_DirectLight_OK.jpg"
overkill = "../image/module/overkill/GSY827AN7B0975_AAO04656K_PKT06_CM1EQSUA0012_20220711235545_DirectLight_NG.jpg"

img_ng = cv2.imread(ng)
img_ok = cv2.imread(ok)
img_overkill = cv2.imread(overkill)

#%%
img_ng = img_preprocess.get_preprocess_img(img_ng, image_size=settings.IMG_SIZE)
img_ok = img_preprocess.get_preprocess_img(img_ok, image_size=settings.IMG_SIZE)
img_overkill = img_preprocess.get_preprocess_img(img_overkill, image_size=settings.IMG_SIZE)

# print(img_ng.shape)

cv2.imshow("123", img_ng)
cv2.waitKey(0)
cv2.destroyAllWindows()

# %%
model = ft_model.Model(settings.IMG_SHAPE)
model.load_weights(settings.TOP_WEIGHT)

img_ng = img_preprocess.get_preprocess_img(img_ng, image_size=settings.IMG_SIZE, predict=True)
img_ok = img_preprocess.get_preprocess_img(img_ok, image_size=settings.IMG_SIZE, predict=True)
img_overkill = img_preprocess.get_preprocess_img(img_overkill, image_size=settings.IMG_SIZE, predict=True)

pred_ng = model.predict(img_ng)
pred_ok = model.predict(img_ok)
pred_overkill = model.predict(img_overkill)

print(f"pred ng : {pred_ng}")
print(f"pred ok : {pred_ok}")
print(f"pred overkill : {pred_overkill}")

# %%
