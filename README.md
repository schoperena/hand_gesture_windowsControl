
# 🖐️ Control de Gestos para Windows con Python

Este proyecto permite controlar tu computadora con **gestos de la mano usando una webcam**. Por ejemplo, puedes apagar el sistema, bloquear la pantalla o cancelar un apagado mostrando ciertos gestos como ✊ (puño cerrado) o ✌️ (dos dedos). El programa se ejecuta en segundo plano y se puede cerrar fácilmente desde un **ícono en la bandeja del sistema (System Tray)**.

## ✅ Requisitos

- Python 3.10 o superior (recomendado Python 3.12)
- Sistema operativo: **Windows**
- Una webcam funcional

## 📦 Instalación de dependencias

Antes de ejecutar el programa, instala las librerías necesarias con pip:

```bash
pip install opencv-python mediapipe pystray pillow
```

## 🚀 Uso

1. Ejecuta `main.py` desde tu entorno virtual o como `.exe` compilado.
2. Muestra gestos frente a la cámara:
   - 😡 Dedo medio → Apagar sistema
   - ✌️ Dos dedos (índice y medio) → Bloquear pantalla
3. Para cerrar el programa, haz clic derecho en el **ícono azul** que aparece en la bandeja del sistema (cerca del reloj) y selecciona **Salir**.

## 💡 Compilar como .exe

Para crear un ejecutable standalone:

```bash
pyinstaller main.spec
```

Asegúrate de que tu `.spec` esté configurado con `--onefile` correctamente

---

🎯 Ideal para automatización, accesibilidad o como proyecto educativo de visión por computadora.
