#%%
import cv2
import ft_model
import img_preprocess
import setting
import silence_tensorflow
import tensorflow as tf

silence_tensorflow.silence_tensorflow()
tf.random.set_seed(42)

# model = ft_model.Model(setting.IMG_SIZE)
# model.load_weights(setting.BASE_WEIGHT)


def load_pred_img(path):
    img = cv2.imread(path)
    img = img_preprocess.find_contours(img, show=False)
    # img = img.reshape(-1, img.shape[0], img.shape[1], 3)

    return img


overkill = load_pred_img("../image/sample/overkill/overkill_0.jpg")
ng = load_pred_img("../image/sample/true_ng/c1-9.jpg")
ok = load_pred_img("../image/sample/true_ok/ok_1.jpg")

cv2.imshow("test", ng)
cv2.waitKey()
cv2.destroyAllWindows()


#%%
# pred_overkill = model.predict(overkill)
# pred_ok = model.predict(ok)
# pred_ng = model.predict(ng)

# print(f"overkill = {pred_overkill}")
# print(f"true ok = {pred_ok}")
# print(f"true ng = {pred_ng}")

# %%
