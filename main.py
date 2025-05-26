import cv2
import mediapipe as mp
import os
import threading
import sys
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw

# === Inicialización de MediaPipe ===
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)

# === Función para contar dedos levantados ===
def contar_dedos(hand_landmarks):
    dedos = []
    if hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x < hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x:
        dedos.append(1)
    else:
        dedos.append(0)
    for id in [mp_hands.HandLandmark.INDEX_FINGER_TIP,
               mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
               mp_hands.HandLandmark.RING_FINGER_TIP,
               mp_hands.HandLandmark.PINKY_TIP]:
        if hand_landmarks.landmark[id].y < hand_landmarks.landmark[id - 2].y:
            dedos.append(1)
        else:
            dedos.append(0)
    return dedos

# === Ejecutar comandos según gesto ===
def ejecutar_comando_por_gesto(dedos):
    if dedos == [0, 0, 1, 0, 0]:
        os.system("shutdown /s /t 1")
    elif dedos == [0, 1, 1, 0, 0]:
        os.system("rundll32 user32.dll,LockWorkStation")

# === Función principal de visión artificial ===
def reconocimiento_gestos():
    cap = cv2.VideoCapture(0)
    while not detener_evento.is_set():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                dedos = contar_dedos(hand_landmarks)
                ejecutar_comando_por_gesto(dedos)
    cap.release()

# === Crear ícono de la bandeja ===
def crear_icono():
    imagen = Image.new('RGB', (64, 64), color=(70, 130, 180))
    d = ImageDraw.Draw(imagen)
    d.rectangle([16, 16, 48, 48], fill=(255, 255, 255))
    return imagen

# === Función para cerrar desde el menú ===
def salir(icon, item):
    detener_evento.set()
    icon.stop()
    sys.exit()

# === Hilo para procesamiento de gestos ===
detener_evento = threading.Event()
hilo_gestos = threading.Thread(target=reconocimiento_gestos)
hilo_gestos.daemon = True
hilo_gestos.start()

# === Menú e ícono de pystray ===
menu = Menu(MenuItem('Salir', salir))
icono = Icon("hand_ges_control", icon=crear_icono(), menu=menu)
icono.run()

