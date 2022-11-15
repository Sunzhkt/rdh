import cv2 as cv
import matplotlib.pyplot as plt
import str2code
import numpy as np

# plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 绘制原图像
img = cv.imread("../pic/Lena.tif")
plt.title('Original Lena')
plt.imshow(img)
plt.show()

# 绘制原图像灰度直方图
hist = cv.calcHist([img], [0], None, [256], [0, 256])

ax = plt.gca()    # 得到图像的Axes对象
ax.spines['right'].set_color('none')   # 将图像右边的轴设为透明
ax.spines['top'].set_color('none')     # 将图像上面的轴设为透明
ax.xaxis.set_ticks_position('bottom')    # 将x轴刻度设在下面的坐标轴上
ax.yaxis.set_ticks_position('left')         # 将y轴刻度设在左边的坐标轴上
ax.spines['bottom'].set_position(('data', 0))   # 将两个坐标轴的位置设在数据点原点
ax.spines['left'].set_position(('data', 0))
# index = 0
# _out = []
# out = np.array(_out)
# max = img.ravel().shape[0]/3
# i = 0
# while index<max:
#         out = np.append(out,(img.ravel()[3*index+1]))
#         index +=1


plt.title('Histogram of Original Lena')
plt.plot(hist)
plt.savefig('../pic/original hist.jpg')
plt.show()

# 进行整张图的遍历找到出现次数最多的点(同一灰度值最多的)
peak_point_pixel = 0
peak_point_count = 0
for i in range(256):
    if peak_point_count < hist[i]:
        peak_point_pixel = i
        peak_point_count = hist[i][0]
# print("peak point:", peak_point_pixel)
# print(peak_point_count)

# 找到最少的点
zero_point_pixel = 0
zero_point_count = [999999]
for i in range(peak_point_pixel, 256):
    if zero_point_count > hist[i]:
        zero_point_pixel = i
        zero_point_count = hist[i][0]
# print("zero point:": zero_point_pixel)


# 遍历图片将处于最小点和最大点之间的进行增减操作
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        if zero_point_pixel > img[i, j][0] > peak_point_pixel:
            img[i, j][0] = img[i, j][0] + 1
            img[i, j][1] = img[i, j][1] + 1
            img[i, j][2] = img[i, j][2] + 1

cv.imwrite('../pic/Lena(shifted).tif', img)
plt.title('shifted Lena')
plt.imshow(img)
plt.show()


hist_shift = cv.calcHist([img], [0], None, [256], [0, 256])
ax = plt.gca()    # 得到图像的Axes对象
ax.spines['right'].set_color('none')   # 将图像右边的轴设为透明
ax.spines['top'].set_color('none')     # 将图像上面的轴设为透明
ax.xaxis.set_ticks_position('bottom')    # 将x轴刻度设在下面的坐标轴上
ax.yaxis.set_ticks_position('left')         # 将y轴刻度设在左边的坐标轴上
ax.spines['bottom'].set_position(('data', 0))   # 将两个坐标轴的位置设在数据点原点
ax.spines['left'].set_position(('data', 0))
plt.title('Shifted Histogram')
plt.plot(hist_shift)
plt.savefig('../pic/shifted hist.jpg')
plt.show()

with open("../ciphertext.txt", 'r') as file:
    s_input = file.read()
    s_bit = str2code.str_encode(s_input)
    if len(s_bit) > peak_point_count:
        print("error, ciphertext too long, please rerun after changing the ciphertext!")
    else:
        message = s_bit.ljust(int(peak_point_count), '0')

        index = 0
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if img[i, j][0] == peak_point_pixel:
                    if message[index] == '1':
                        img[i, j][0] += 1
                        img[i, j][1] += 1
                        img[i, j][2] += 1
                    index += 1

        hist_embed = cv.calcHist([img], [0], None, [256], [0, 256])
        ax = plt.gca()  # 得到图像的Axes对象
        ax.spines['right'].set_color('none')  # 将图像右边的轴设为透明
        ax.spines['top'].set_color('none')  # 将图像上面的轴设为透明
        ax.xaxis.set_ticks_position('bottom')  # 将x轴刻度设在下面的坐标轴上
        ax.yaxis.set_ticks_position('left')  # 将y轴刻度设在左边的坐标轴上
        ax.spines['bottom'].set_position(('data', 0))  # 将两个坐标轴的位置设在数据点原点
        ax.spines['left'].set_position(('data', 0))
        plt.title('Histogram of the Marked Lena')
        plt.plot(hist_embed)
        plt.savefig('../pic/embedded hist.jpg')
        plt.show()

        cv.imwrite('../pic/Lena(marked).tif', img)
        plt.imshow(img)
        plt.title('Marked Lena')
        plt.show()
file.close()
