import cv2 as cv
import matplotlib.pyplot as plt
import str2code

img_ori = cv.imread("../pic/Lena.tif")
hist_ori = cv.calcHist([img_ori], [0], None, [256], [0, 256])

# 进行整张图的遍历找到出现次数最多的点(同一灰度值最多的)
peak_point_pixel = 0
peak_point_count = 0
for i in range(256):
    if peak_point_count < hist_ori[i]:
        peak_point_pixel = i
        peak_point_count = hist_ori[i][0]
# print("peak point:", peak_point_pixel)
# print(peak_point_count)

# 找到最少的点
zero_point_pixel = 0
zero_point_count = [999999]
for i in range(peak_point_pixel, 256):
    if zero_point_count > hist_ori[i]:
        zero_point_pixel = i
        zero_point_count = hist_ori[i][0]


# print("zero point:": zero_point_pixel)

def extract_atk(name):
    img = cv.imread("../pic/Lena(" + name + ").tif")
    hist = cv.calcHist([img], [0], None, [256], [0, 256])

    text = ''
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i, j][0] == peak_point_pixel:
                text += '0'
            elif img[i, j][0] == (peak_point_pixel + 1):
                text += '1'
            else:
                continue
    text = text.rstrip('0')
    with open("../result(" + name + ").txt", 'w') as file:
        file.write(str2code.str_decode(text))
        # try:
        #     file.write(str2code.str_decode(text))
        # except:
        #     file.write(str2code.str_decode(text, flag=1))
        #     pass


extract_atk('resized')
extract_atk('rotate')
extract_atk('cropped')
extract_atk('noise')

# 将最大值旁边的个数赋值给最大值
# hist[peak_point_pixel] += hist[peak_point_pixel + 1]
# hist[peak_point_pixel + 1] = 0
# print(hist_embed[peak_point_pixel])

# plt.title('Shift-back Histogram')
# plt.plot(hist)
# plt.savefig('../pic/shift_back hist.jpg')
# plt.show()

# 将直方图恢复
# for i in range(img.shape[0]):
#     for j in range(img.shape[1]):
#         if zero_point_pixel >= img[i, j][0] > peak_point_pixel:
#             img[i, j][0] = img[i, j][0] - 1
#             img[i, j][1] = img[i, j][1] - 1
#             img[i, j][2] = img[i, j][2] - 1
# plt.title('Recovered Histogram')
# hist_recover = cv.calcHist([img], [0], None, [256], [0, 256])
# plt.plot(hist_recover)
# plt.savefig('../pic/recovered hist.jpg')
# plt.show()

# cv.imwrite('Lena(recovered).tif', img)
#
# plt.imshow(img)
# plt.title('Recovered Lena')
# plt.show()
