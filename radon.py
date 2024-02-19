import numpy as np
import cv2
import imutils
from matplotlib import pyplot as plt

def display_result(src,R,B,theta,N):

    fig,axs = plt.subplots(nrows=1,ncols=3,figsize=(12,4))

    axs[0].set_title("Source Image")
    axs[0].imshow(src)

    axs[1].set_title("Sinogram")
    axs[1].imshow(R,extent=[theta[0],theta[len(theta)-1],N,0])
    axs[1].set_aspect(0.8)

    axs[2].set_title("Back-projected Image")
    axs[2].imshow(B)

    fig.suptitle("Radon Transform")
    plt.show()

def display(title,img,i):
    plt.figure(i)
    plt.imshow(img)
    plt.title(title)

def print_shape(img):
    rows,cols = img.shape
    print(f'Image shape: ({rows},{cols})')

def create_point_source_image(imsize,location,size):
    img = np.zeros([imsize,imsize],dtype=np.uint8)
    for i in np.arange(imsize):
        for j in np.arange(imsize):
            if i == location[0] and j == location[1]:
                #img[i,j] = 255
                #img[i-1,j-1] = 255
                #img[i-1,j] = 255
                #img[i,j-1] = 255
                #img[i+1,j] = 255
                #img[i+1,j+1] = 255
                #img[i,j+1] = 255
                #img[i-1,j+1] = 255
                #img[i+1,j-1]= 255

                img[i-size:i+size,j-size:j+size] = 255
    return img

def radon(img,theta):

    rows,cols = img.shape

    R = np.zeros([rows,len(theta)],dtype=np.double)
    
    for angle in np.arange(len(theta)):
        img_rot = imutils.rotate(img,theta[angle])
        for column in np.arange(cols):
            R[column,angle] = np.sum(img_rot[:,column])

    return R

def backproject(R,theta):

    rows,cols = R.shape

    B = np.zeros([rows,rows],dtype=np.double)
    B_rot = np.zeros([rows,rows],dtype=np.double)
    for angle in np.arange(len(theta)):
        for i in np.arange(rows):
            B_rot[i,:] = R[:,angle]
        
        B_rot = imutils.rotate(B_rot,-1*theta[angle])
        B += B_rot
    
    return B


def main():
    # Define point source and image properties
    N = 400
    loc = [280,165]
    diameter = 3
    steps = 100
    theta = np.linspace(0,2*np.pi,steps)*180/np.pi

    # Source image creation
    img = create_point_source_image(N,loc,diameter)
    # Radon transform of image
    R = radon(img,theta)
    # Backprojection of image
    B = backproject(R,theta)

    
    display_result(img,R,B,theta,N)


if __name__ == "__main__":
    main()