import cv2
from skimage.metrics import peak_signal_noise_ratio
from skimage.metrics import structural_similarity

def evaluate(original, stego):
    img1 = cv2.imread(original)
    img2 = cv2.imread(stego)

    psnr = peak_signal_noise_ratio(img1, img2)

    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    ssim = structural_similarity(gray1, gray2)

    return psnr, ssim