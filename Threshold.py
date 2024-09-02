from pynq import Overlay
from pynq import allocate
from pynq.lib.video import *
import numpy as np
from PIL import Image
import cv2

# Load the overlay
overlay = Overlay('/home/xilinx/overlay/image_filter1/image_filter.bit')

#Insanciate IP DMA          
dma = overlay.axi_dma_0

#load the image
im = cv2.imread("car_3072.pgm")
im_int = np.array(im, dtype = np.uint32)
size = im_int.size

#Convert the image into an array of 32 bits
im_array = list(im.ravel())
im_int32 = im_array[:(size)]
im_int32 = np.array(im_int32, dtype = 'int32')


#Allocate buffers for the DMA transaction
in_buffer = allocate(shape=(size,), dtype=np.int32)
out_buffer = allocate(shape=(size,), dtype=np.int32)

#Copy the Array Image into the buffer
np.copyto(in_buffer,im_int32)

#Transaction to/from DMA
dma.sendchannel.start()
dma.recvchannel.start()
dma.sendchannel.transfer(in_buffer)
dma.recvchannel.transfer(out_buffer)

#Convert the array into an Image and save it
out_buffer = np.reshape(out_buffer, im_int.shape)
img = Image.fromarray(np.uint8(out_buffer))
img.save('filtered_image.png')
