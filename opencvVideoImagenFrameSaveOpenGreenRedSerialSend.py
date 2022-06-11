# -*- coding: utf-8 -*-
"""
Created on Thu May 12 01:47:03 2022

@author: CAUDILLO
"""

import numpy as np
import cv2 as cv
import sys
import serial
import time
ser = serial.Serial('COM14', 9600, timeout = 1)
time.sleep(1)
cap = cv.VideoCapture(0, cv.CAP_DSHOW)
if not cap.isOpened():
    print("No se puede abrir la cámara")
    exit()  
while True:
    ret, frame = cap.read()      
    if not ret:
        print("No se puede recibir el marco. Saliendo ...")
        break
    '''
    Entrada externa. Esta 'a' debería de ser enviada por el puerto
    seria cuando se interrumpa la señal infraroja y la banda se detenga.
    '''
    print("presione 'a' para capturar fotografia")
    captura = input()
    if captura == ('a'):
            
        #Guardamos la imagen
        cv.imwrite("imagenFrame.jpg", frame)
        #Abrimos la imagen
        img = cv.imread("imagenFrame.jpg", flags = cv.IMREAD_COLOR)
        if img is None:
            sys.exit("No se pudo leer la imagen.")
            #Se le hace el tratamiento a la imagen
        rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        hsv = cv.cvtColor(rgb, cv.COLOR_RGB2HSV)
        lower_red1 = np.array([0, 100, 100], np.uint8)
        upper_red1 = np.array([8, 255, 255], np.uint8)
        lower_red2 = np.array([175, 100, 100], np.uint8)
        upper_red2 = np.array([179, 255, 255], np.uint8)
        lower_green = np.array([50, 100, 100], np.uint8)
        upper_green = np.array([85, 255, 255], np.uint8)
        maskRed1 = cv.inRange(hsv, lower_red1, upper_red1)
        maskRed2 = cv.inRange(hsv, lower_red2, upper_red2)
        maskRed = cv.add(maskRed1, maskRed2)
        maskGreen = cv.inRange(hsv, lower_green, upper_green)
        maskRG = cv.add(maskGreen, maskRed)      
        maskRGvis = cv.bitwise_and(img, img, mask = maskRG)
        #Se muestra la imagen tratada
        cv.imshow("imagenMask", maskRGvis)
        #Preguntamos por la exixtencia de los colores verde o rojo 
        Green = 255 in maskGreen
        if Green:
            print("True Green" )
            ser.write(b'v')    
        Red = 255 in maskRed
        if Red:
            print("True Red" )
            ser.write(b'r')
        cv.imwrite("imagenMask.jpg", maskRGvis)
        #Esperamos la tecla q para salir        
        k = cv.waitKey(0)    
        if k == ord('q'):
            break
    
cap.release()
cv.destroyAllWindows()
ser.close()