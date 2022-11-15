from PIL import Image
import cv2
import numpy as np

# 读取图像
im = Image.open("../pic/Lena(marked).tif")
# im.show()

# 原图像缩放为128x128
im_resized = im.resize((128, 128))
# im_resized.show()
im_resized.save("../pic/Lena(resized).tif")

# 指定逆时针旋转的角度
im_rotate = im.rotate(10)
# im_rotate.show()
im_rotate.save("../pic/Lena(rotate).tif")

img = cv2.imread("../pic/Lena(marked).tif")
# print(img.shape)
cropped = img[0:200, 0:512]  # 裁剪坐标为[y0:y1, x0:x1]
cv2.imwrite("../pic/Lena(cropped).tif", cropped)

# 将图片灰度标准化
img = img / 255
# 产生高斯 noise
noise = np.random.normal(0, 0.3, img.shape)
# 将噪声和图片叠加
gaussian_out = img + noise
# 将超过 1 的置 1，低于 0 的置 0
gaussian_out = np.clip(gaussian_out, 0, 1)
# 将图片灰度范围的恢复为 0-255
gaussian_out = np.uint8(gaussian_out * 255)
# 将噪声范围搞为 0-255
# noise = np.uint8(noise*255)
cv2.imwrite("../pic/Lena(noise).tif", gaussian_out)
