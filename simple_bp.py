import numpy as np
import cv2
import sys
import imutils
import argparse
from matplotlib import pyplot as plt
from phantominator import shepp_logan

def display_result(src,R,B,theta,N):

    fig,axs = plt.subplots(nrows=1,ncols=3,figsize=(12,4))

    axs[0].set_title("Source Image")
    axs[0].imshow(src)

    axs[1].set_title("Sinogram")
    axs[1].imshow(R,extent=[theta[0],theta[len(theta)-1],N,0])
    axs[1].set_aspect(0.8)

    axs[2].set_title("Back-projected Image")
    axs[2].imshow(B,interpolation='none')

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
                img[i-size:i+size,j-size:j+size] = 255
    return img

def radon(img,theta,sl):

    if sl == True:
        rows,cols,x = img.shape
    else:
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

def fourier_1D(R,theta):

    Rfft = np.fft.fft(R,axis=0)

    rows,cols = Rfft.shape



    plt.figure(1)
    plt.imshow(np.imag(Rfft),extent=[theta[0],theta[len(theta)-1],rows,0])
    plt.show()

    return Rfft

def shepp_logan_radon(sl):
    N = 256
    steps = 100
    theta = np.linspace(0,2*np.pi,steps)*180/np.pi

    M0 = shepp_logan((N,N,1),MR=False, zlims=(-.25,.25))
    R = radon(M0,theta,sl)
    #Rfft = fourier_1D(R,theta)
    B = backproject(R,theta)
    display_result(M0,R,B,theta,N)

def main(arg1,sl):

    if sl == True:
        # Run shepp logan example
        shepp_logan_radon(sl)
    else:
        # Define number of rotations
        steps = 500
        theta = np.linspace(0,2*np.pi,steps)*180/np.pi
        # Unpack user arguments
        N = arg1['image_size']
        loc = []
        loc.append(arg1['source'][0])
        loc.append(arg1['source'][1])
        diameter = arg1['source'][2]

        # Source image creation
        img = create_point_source_image(N,loc,diameter)
        # Radon transform of image
        R = radon(img,theta,sl)
        # Backprojection of image
        B = backproject(R,theta)
        # Display results
        display_result(img,R,B,theta,N)
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Demonstrate simple backprojection on a point source created from the user.")
    parser.add_argument('-i','--image_size', type=int, default=0, required=False)
    parser.add_argument('-s','--source', type=int, nargs='*', default = 0, required=False)

    args = parser.parse_args()

    if args.image_size == 0 or args.source == 0:
        sl = True
    else:
        sl = False
    
    main(vars(args),sl)