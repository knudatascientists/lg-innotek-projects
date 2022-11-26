#%%
import cv2
import ft_model
import ft_preprocess
import setting
import silence_tensorflow
import tensorflow as tf

silence_tensorflow.silence_tensorflow()
tf.random.set_seed(42)


ng = "../image/module/true_ng/GSY827AN7C2253_AAO17363K_PKT04_CM1EQSUA0011_20220712204613_DirectLight_NG.jpg"
ok = "../image/module/true_ok/GSY827AN7A1705_AAO18599K_PKT06_CM1EQSUA0012_20220711200838_DirectLight_OK.jpg"
overkill = "../image/module/overkill/GSY848CN8B2764_AAO31299K_PKT03_CM1EQSUA0022_20220811204734_DirectLight_NG.jpg"

img_ng = cv2.imread(ng)
img_ok = cv2.imread(ok)
img_overkill = cv2.imread(overkill)

test = ft_preprocess.get_preprocess_img(img_ng)

cv2.imshow("33", test)
cv2.waitKey(0)
cv2.destroyAllWindows()

img_ng = ft_preprocess.cvt_pred_img(img_ng)
img_ok = ft_preprocess.cvt_pred_img(img_ok)
img_overkill = ft_preprocess.cvt_pred_img(img_overkill)

# %%

model = ft_model.Model(setting.IMG_SIZE)
model.load_weights(setting.TOP_WEIGHT)

pred_ng = model.predict(img_ng)
pred_ok = model.predict(img_ok)
pred_overkill = model.predict(img_overkill)

print(f"pred ng : {pred_ng}")
print(f"pred ok : {pred_ok}")
print(f"pred overkill : {pred_overkill}")

# %%
