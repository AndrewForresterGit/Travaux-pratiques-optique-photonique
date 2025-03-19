import cv2
##from PIL import Image
##from sklearn.preprocessing import normalize
from scipy.fft import fftfreq
import numpy as np
import matplotlib.pyplot as plt


def rgb2grey(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

def compress(image):
    shape = image.shape
    center_x = shape[0] // 2
    center_y = shape[1] // 2
    return image[center_x-16:center_x+16, center_y-16:center_y+16]

def save_bytes(image):
    byte_arr = []
    for row in image:
        for pix in row:
            print(bin(int(round(pix, -3)/100)))

def norm_im(image):
    return np.diag(image.sum(1)**-1) @ image

def main() -> None:
    fichier_im = "emoji.jpg"
    im_data = fichier_im.partition('.')
    save_file = f"{im_data[0]}_compressed.{im_data[2]}"

    im = cv2.imread(fichier_im)
    im_grey = rgb2grey(im)

    f = np.fft.fft2(im_grey)
    fshift = np.fft.fftshift(f)
##    magnitude_spectrum = 20*np.log(np.abs(fshift))
    im_compressed = np.abs(np.fft.ifft2(compress(fshift)))
    
    fig = plt.figure()
    ax1 = fig.add_subplot(121)
    ax1.imshow(im_grey, cmap='Greys_r')
    
    ax2 = fig.add_subplot(122)
    ax2.imshow(im_compressed, cmap='Greys_r')

##    save_bytes(im_compressed)

    plt.show()

if __name__ == "__main__":
    main()
