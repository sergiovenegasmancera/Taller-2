import numpy as np
import cv2
import random
import os

class imageShape:
    def __init__(self, width,  height):
        self.width = width
        self.height = height
        # Creating a black image with 3 channels
        # RGB and unsigned int datatype
        self.shape = np.zeros((self.height, self.width, 3), dtype="uint8")
        # Se genera un numero entre 0 y 3
        self.x = random.randint(0, 3)
        self.string_shape = ' '

    def generateShape (self):
        #triangle: equilátero, lado = min(width, height)/2
        if self.x == 0:
            # Se guarda el tipo de figura a generar
            self.string_shape = 'triangle'
            if self.width < self.height:
                min = self.width/2
            else:
                min = self.height/2
        # Se generan los tres puntos del triangulo
            point_a = (int(self.width/2), int((self.height/2)-(1.73205*(min/4))))
            point_b = (int((self.width/2)-min/2), int((self.height/2)+(1.73205*(min/4))))
            point_c = (int((self.width/2)+min/2), int((self.height/2)+(1.73205*(min/4))))

            # cv2.line(self.shape, point_a, point_b, (255, 255, 0), 3)
            # cv2.line(self.shape, point_a, point_c, (255, 255, 0), 3)
            # cv2.line(self.shape, point_b, point_c, (255, 255, 0), 3)

            # Se unen los puntos
            triangle_cnt = np.array([point_a, point_b, point_c])
            cv2.drawContours(self.shape, [triangle_cnt], 0, (255, 255, 0), -1)

        #square: lado = min(width, height)/2, rotado 45 grados
        if self.x == 1:
            # Se guarda el tipo de figura a generar
            self.string_shape = 'square'
            if self.width < self.height:
                min = self.width/2
            else:
                min = self.height/2

            #Se generan los 4 puntos del cuadrado
            point_a = (int(self.width / 2) , int((self.height/2)-min/1.41421))
            point_b = (int((self.width / 2)-min/1.41421) , int(self.height/2))
            point_c = (int(self.width / 2) , int((self.height/2)+min/1.41421))
            point_d = (int((self.width / 2)+min/1.41421) , int(self.height/2))

            # cv2.line(self.shape, point_a, point_b, (255, 255, 0), 3)
            # cv2.line(self.shape, point_b, point_c, (255, 255, 0), 3)
            # cv2.line(self.shape, point_c, point_d, (255, 255, 0), 3)
            # cv2.line(self.shape, point_a, point_d, (255, 255, 0), 3)

            #Se unen los 4 puntos
            square_cnt = np.array([point_a, point_b, point_c, point_d])
            cv2.drawContours(self.shape, [square_cnt], 0, (255, 255, 0), -1)

        #rectangle: lado_horizontal = width/2, lado_vertical = height/2
        if self.x ==2:
            # Se guarda el tipo de figura a generar
            self.string_shape = 'rectangle'
            #Se genera el rectangulo con el metodo rectangle()
            cv2.rectangle(self.shape, (int(self.width/4), int(self.height/4)), (int((self.width*3)/4), int((self.height*3)/4)), (255, 255, 0), -1)

        #circle: radio = min(width, height)/4
        if self.x == 3:
            # Se guarda el tipo de figura a generar
            self.string_shape = 'circle'
            if self.width < self.height:
                min = self.width
            else:
                min = self.height
            # Se genera el circulo con el metodo circle()
            cv2.circle(self.shape, (int(self.width/2), int(self.height/2)), int(min/4), (255, 255, 0), thickness = -1)

    def showShape(self):
        cv2.imshow('shape', self.shape)
        cv2.waitKey(5000)
        cv2.destroyAllWindows()

    def getShape(self):
        return self.string_shape, self.shape

    def whatShape(self, img):
        # Se genera la escala de grises de la imagen recibida
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        image_contour = img.copy()
        image_square = img.copy()
        image_rectangle = img.copy()
        image_circle = img.copy()
        image_triangle = img.copy()

        # Otsu's global threshold
        _, img_otsu = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # Find contour
        contour, _ = cv2.findContours(img_otsu, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contour_area = int(cv2.contourArea(contour[0]))

        #Find square contour
        rect = cv2.minAreaRect(contour[0])
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        #cv2.drawContours(image_square, [box], 0, (0, 255, 0), 5)
        #cv2.imshow('shape', image_square)
        #cv2.waitKey(0)
        # Se calcula el area del rectangulo minimo que encierra el contorno
        square_area = int(cv2.contourArea(box))

        # Find rectangle contour
        x,y,w,h = cv2.boundingRect(contour[0])
        #cv2.rectangle(image_rectangle, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #cv2.imshow('shape', image_rectangle)
        #cv2.waitKey(0)
        rect2 = ((x,y),(x+w,y+h), 0)
        box2 = cv2.boxPoints(rect2)
        box2 = np.int0(box2)
        # Se calcula el area del rectangulo horizontal que encierra el contorno
        rectangle_area = int(w*h)

        # Find circle contour
        (x, y), radius = cv2.minEnclosingCircle(contour[0])
        center = (int(x), int(y))
        radius = int(radius)
        #cv2.circle(image_circle, center, radius, (0, 255, 0), 2)
        #cv2.imshow('shape', image_circle)
        #cv2.waitKey(0)
        # Se calcula el area del circulo minimo que encierra el contorno
        circle_area = int(radius * radius * np.pi)

        # Find convex (triangle) contour
        hull = cv2.convexHull(contour[0])
        #cv2.drawContours(image_triangle, [hull], 0, (255, 0, 0), 2)
        #cv2.imshow('shape', image_triangle)
        #cv2.waitKey(0)
        # Se calcula el area del poligono convexo que encierra el contorno
        convex_area = int(cv2.contourArea(hull))

        # print('Area contorno = ',str(contour_area))
        # print('Area cuadrado = ', str(square_area))
        # print('Area rectangulo = ', str(rectangle_area))
        # print('Area circulo = ', str(circle_area))
        # print('Area triangulo = ', str(convex_area))

        # Se detecta que tipo de figura se encuentra en la imagen por medio de las diferentes
        # areas previamente calculadas
        min_error = contour_area*0.03
        # Triangle??????
        if (convex_area >= contour_area-min_error) and (convex_area <= contour_area+min_error):
            if (square_area > contour_area + min_error):
                if (rectangle_area > contour_area + min_error):
                    if (circle_area > contour_area + min_error):
                        shape_detector = 'triangle'
        # Square????????
        if (square_area >= contour_area-min_error) and (square_area <= contour_area+min_error):
            if (convex_area >= contour_area-min_error) and (convex_area <= contour_area+min_error):
                if rectangle_area > contour_area+min_error:
                    shape_detector = 'square'
        # Rectangle????????
        if (square_area >= contour_area - min_error) and (square_area <= contour_area + min_error):
            if (convex_area >= contour_area - min_error) and (convex_area <= contour_area + min_error):
                if (rectangle_area >= contour_area - min_error) and (rectangle_area <= contour_area + min_error):
                    shape_detector ='rectangle'
        # Circle????????
        if (circle_area >= contour_area - min_error) and (circle_area <= contour_area + min_error):
            if (convex_area >= contour_area - min_error) and (convex_area <= contour_area + min_error):
                if rectangle_area > contour_area + min_error:
                    if square_area > contour_area + min_error:
                        shape_detector ='circle'
        return shape_detector


