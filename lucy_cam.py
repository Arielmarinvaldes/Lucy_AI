import cv2
import numpy as np

def draw(mask, color, frame):
    # Encontrar los contornos de la máscara
    contornos,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Dibujar los contornos en el marco original
    for c in contornos:
        area = cv2.contourArea(c)
        if area > 1000:
            new_contour = cv2.convexHull(c)
            cv2.drawContours(frame, [new_contour], 0, color, 3)

def capture():
    cap = cv2.VideoCapture(0)

    # Definir los rangos de colores para cada máscara
    low_yellow = np.array([24, 190, 20], np.uint8)
    high_yellow = np.array([30, 255, 255], np.uint8)
    low_blue = np.array([85, 200, 20], np.uint8)
    high_blue = np.array([125, 255, 255], np.uint8)
    low_green = np.array([45, 100, 20], np.uint8)
    high_green = np.array([75, 255, 255], np.uint8)
    low_red1 = np.array([0, 100, 20], np.uint8)
    high_red1 = np.array([5, 255, 255], np.uint8)
    low_red2 = np.array([175, 100, 20], np.uint8)
    high_red2 = np.array([180, 255, 255], np.uint8)

    while True:
        # Leer un fotograma de la cámara
        comp, frame = cap.read()
        if comp == True:
            # Convertir el fotograma a formato HSV
            frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # Crear las máscaras para cada color
            yellow_mask = cv2.inRange(frame_HSV, low_yellow, high_yellow)
            blue_mask = cv2.inRange(frame_HSV, low_blue, high_blue)
            green_mask = cv2.inRange(frame_HSV, low_green, high_green)
            
            red_mask1 = cv2.inRange(frame_HSV, low_red1, high_red1)
            red_mask2 = cv2.inRange(frame_HSV, low_red2, high_red2)
            red_mask = cv2.add(red_mask1, red_mask2)
            # Dibujar los contornos de cada color en el fotograma original
            draw(yellow_mask, [0, 255, 255], frame)
            draw(blue_mask, [255, 0, 0], frame)
            
            draw(green_mask, [0, 255, 0], frame)
            draw(red_mask, [0, 0, 255], frame)
            # Mostrar el fotograma en una ventana
            cv2.imshow('Webcam', frame)
        # Si se presiona la tecla 's', salir del bucle
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break

    # Liberar la cámara y cerrar todas las ventanas
    cap.release()
    cv2.destroyAllWindows()

