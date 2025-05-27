import cv2
import mediapipe as mp
import os
import threading
import sys
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw

# === Inicialización ===
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)

detener_evento = threading.Event()
mostrar_ventana = threading.Event()
mostrar_ventana.set()  # Visible por defecto

estado_camara = {'visible': True}

# === Conteo de dedos ===
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

# === Acciones por gesto ===
def ejecutar_comando_por_gesto(dedos):
    if dedos == [0, 0, 1, 0, 0]:
        os.system("shutdown /s /t 1")
    elif dedos == [1, 1, 1, 1, 1]:
        os.system("shutdown /a")
    elif dedos == [0, 1, 1, 0, 0]:
        os.system("rundll32 user32.dll,LockWorkStation")

# === Reconocimiento de gestos ===
def reconocimiento_gestos():
    cap = cv2.VideoCapture(0)
    ventana_abierta = False

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
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        if mostrar_ventana.is_set():
            cv2.imshow("Reconocimiento de gestos", frame)
            ventana_abierta = True
            if cv2.waitKey(10) & 0xFF == 27:
                detener_evento.set()
                break
        else:
            if ventana_abierta:
                cv2.destroyWindow("Reconocimiento de gestos")
                ventana_abierta = False
            cv2.waitKey(10)

    cap.release()
    cv2.destroyAllWindows()

# === Bandeja del sistema ===
def crear_icono():
    imagen = Image.new('RGB', (64, 64), color=(0, 123, 255))
    d = ImageDraw.Draw(imagen)
    d.rectangle([16, 16, 48, 48], fill=(255, 255, 255))
    return imagen

def texto_toggle():
    return "Ocultar cámara" if estado_camara['visible'] else "Mostrar cámara"

def toggle_ventana(icon, item):
    if estado_camara['visible']:
        mostrar_ventana.clear()
        estado_camara['visible'] = False
    else:
        mostrar_ventana.set()
        estado_camara['visible'] = True

def salir(icon, item):
    detener_evento.set()
    icon.stop()
    sys.exit()

# === Arranque del sistema ===
menu = Menu(
    MenuItem(lambda item: texto_toggle(), toggle_ventana),
    MenuItem('Salir', salir)
)

icono = Icon("GestosWindows", icon=crear_icono(), menu=menu)

hilo_gestos = threading.Thread(target=reconocimiento_gestos)
hilo_gestos.daemon = True
hilo_gestos.start()

icono.run()
