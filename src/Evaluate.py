import cv2 as cv
import math
from scipy.signal import convolve2d
import numpy as np
from PIL import Image


# def sum_img(img):
#     s = 0
#     for i in range(img.shape[0]):
#         for j in range(img.shape[1]):
#             s += img[i, j][0]
#     return s
#
#
# def mean_img(img):
#     return sum_img(img) / (img.shape[0] * img.shape[1])
#
#
# def deviation_img(img):
#     u = mean_img(img)
#     s = 0
#     for i in range(img.shape[0]):
#         for j in range(img.shape[1]):
#             s += math.pow(img[i, j][0] - u, 2)
#     return s / (img.shape[0] * img.shape[1])

def compute_mse(img1, img2):
    if img1.shape[0] == img2.shape[0] and img1.shape[1] == img2.shape[1]:
        d = 0
        for i in range(img1.shape[0]):
            for j in range(img1.shape[1]):
                d += math.pow(int(img1[i, j][0]) - int(img2[i, j][0]), 2)
        return d / (img1.shape[0] * img1.shape[1])
    else:
        print("error, pictures are not the same size!")
        return


def compute_psnr(img1, img2):
    a = compute_mse(img1, img2)
    if a == 0:
        return 'inf'
    else:
        return 10 * math.log10(math.pow(255, 2) / compute_mse(img1, img2))


def matlab_style_gauss2D(shape=(3, 3), sigma=0.5):
    m, n = [(ss - 1.) / 2. for ss in shape]
    y, x = np.ogrid[-m:m + 1, -n:n + 1]
    h = np.exp(-(x * x + y * y) / (2. * sigma * sigma))
    h[h < np.finfo(h.dtype).eps * h.max()] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh
    return h


def filter2(x, kernel, mode='same'):
    return convolve2d(x, np.rot90(kernel, 2), mode=mode)


def compute_ssim(im1, im2, k1=0.01, k2=0.03, win_size=11, L=255):
    # M, N = im1.shape
    c1 = (k1 * L) ** 2
    c2 = (k2 * L) ** 2
    window = matlab_style_gauss2D(shape=(win_size, win_size), sigma=1.5)
    window = window / np.sum(np.sum(window))
    if im1.dtype == np.uint8:
        im1 = np.double(im1)
    if im2.dtype == np.uint8:
        im2 = np.double(im2)
    mu1 = filter2(im1, window, 'valid')
    mu2 = filter2(im2, window, 'valid')
    mu1_sq = mu1 * mu1
    mu2_sq = mu2 * mu2
    mu1_mu2 = mu1 * mu2
    sigma1_sq = filter2(im1 * im1, window, 'valid') - mu1_sq
    sigma2_sq = filter2(im2 * im2, window, 'valid') - mu2_sq
    sigmal2 = filter2(im1 * im2, window, 'valid') - mu1_mu2
    ssim_map = ((2 * mu1_mu2 + c1) * (2 * sigmal2 + c2)) / ((mu1_sq + mu2_sq + c1) * (sigma1_sq + sigma2_sq + c2))
    return np.mean(ssim_map)


img_ori = cv.imread('../pic/Lena.tif')
img_embed = cv.imread('../pic/Lena.tif')
hist = cv.calcHist([img_ori], [0], None, [256], [0, 256])

peak_point_count = 0
for i in range(256):
    if peak_point_count < hist[i]:
        peak_point_count = hist[i][0]
EC = peak_point_count
ER = peak_point_count / (img_ori.shape[0] * img_ori.shape[1])

MSE = compute_mse(img_ori, img_embed)
PSNR = compute_psnr(img_ori, img_embed)

img_ori = Image.open('../pic/Lena.tif')
img_embed = Image.open('../pic/Lena.tif')

SSIM = compute_ssim(np.array(img_ori.resize((8, 8), Image.ANTIALIAS).convert('L'), 'f'),
                    np.array(img_embed.resize((8, 8), Image.ANTIALIAS).convert('L'), 'f'))

with open("../evaluate.txt", 'w') as file:
    file.write("MSE = {}\nPSNR = {}\nSSIM = {}\n\nEC = {}\nER = {}".format(MSE, PSNR, SSIM, EC, ER))
    file.close()
