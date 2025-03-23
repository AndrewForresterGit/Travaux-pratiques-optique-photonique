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
    size = 9
    return image[center_x-size//2:center_x+size//2+1,
                 center_y-size//2:center_y+size//2+1]

def save_bytes(image):
    byte_arr = []
    string = ""
    for row in image:
        string += f'{row}'

def norm_im(image):
    normed = cv2.normalize(image, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    return np.abs(np.rint(256*normed))


def main() -> None:
    fichier_im = "locked_in.jpg"
    im_data = fichier_im.partition('.')
    save_file = f"{im_data[0]}_compressed.{im_data[2]}"

    im = cv2.imread(fichier_im)
    im_grey = rgb2grey(im)

    f = np.fft.fft2(im_grey)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = compress(20*np.log(np.abs(fshift)))
    
    im_compressed = np.abs(np.fft.ifft2(compress(fshift)))
    
    fig = plt.figure()
    ax1 = fig.add_subplot(121)
    ax1.imshow(im_grey, cmap='Greys_r')
    
    ax2 = fig.add_subplot(122)
    ax2.imshow(magnitude_spectrum, cmap='Greys_r')

    for i in norm_im(magnitude_spectrum):
        string = ''
        for j in i:
            string += f'{int(j)}*'
        print(string[:-1] + '\\n')
    
##    save_bytes(im_compressed)
##    print(im_compressed)
    plt.show()

if __name__ == "__main__":
    main()
