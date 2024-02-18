import numpy as np
import cv2
import imutils

def display(title,img):
    cv2.imshow(title,img)
    cv2.waitKey(0)

def print_shape(img):
    rows,cols = img.shape
    print(f'Image shape: ({rows},{cols})')

def create_point_source_image(imsize):
    img = np.zeros([imsize,imsize],dtype=np.uint8)
    for i in np.arange(imsize):
        for j in np.arange(imsize):
            if i == 100 and j == 100:
                img[i,j] = 255
                img[i-1,j-1] = 255
                img[i-1,j] = 255
                img[i,j-1] = 255
                img[i+1,j] = 255
                img[i+1,j+1] = 255
                img[i,j+1] = 255
                img[i-1,j+1] = 255
                img[i+1,j-1]= 255
    return img

def radon(img,theta):

    rows,cols = img.shape

    R = np.zeros([rows,len(theta)],dtype=np.double)
    
    for angle in np.arange(len(theta)):
        img_rot = imutils.rotate(img,theta[angle])
        for column in np.arange(cols):
            R[column,angle] = np.sum(img_rot[:,column])

    return R

def backproject(img,theta):

    rows,cols = img.shape

    B = np.zeros([rows,rows],dtype=np.double)

    for angle in np.arange(len(theta)):
        img_rot = imutils.rotate(img,theta[angle])

        B[:,angle] = img_rot[]
    


def main():
    N = 400
    theta = np.linspace(0,2*np.pi,400)*180/np.pi

    img = create_point_source_image(N)

    R = radon(img,theta)

    print_shape(R)
    display("sinogram",R)

if __name__ == "__main__":
    main()