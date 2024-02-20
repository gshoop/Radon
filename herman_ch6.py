import numpy as np
from matplotlib import pyplot as plt

def display(title,img,i):
    plt.figure(i)
    plt.imshow(img)
    plt.title(title)

def create_point_source_image(imsize,location,size):
    img = np.zeros([imsize,imsize],dtype=np.uint8)
    basis = np.zeros([imsize,imsize],dtype=np.float64)
    pixel_value = 255

    for i in np.arange(imsize):
        for j in np.arange(imsize):
            if i == location[0] and j == location[1]:
                img[i-size:i+size,j-size:j+size] = pixel_value
                basis[i-size:i+size,j-size:j+size] = 1.0
    return img,basis

def main():

    # Image properties
    N = 128
    J = N**2
    loc = [32,89]
    diameter = 3

    img,basis =create_point_source_image(N,loc,diameter)

    b = basis.flatten()

    display("Basis Image",basis,1)
    
    plt.show()



if __name__ == "__main__":
    main()