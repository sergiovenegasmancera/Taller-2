import numpy as np
import cv2
import random
import os
from imageShape import * # Clase creada

if __name__ == '__main__':
    print('Ingrese las dimensiones de la imagen')
    print('Width = ')
    Width = input()
    print('Height =')
    Height = input()
    Image = imageShape(int(Width), int(Height))
    Image.generateShape()
    Image.showShape()
    string_shape, shape = Image.getShape()
    detector_shape = Image.whatShape(shape)
    print('The shape is a',detector_shape)
    if string_shape == detector_shape:
        print('Correct')
    else:
        print('Incorrect')



