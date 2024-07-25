import cv2
from pyzbar.pyzbar import decode
import numpy as np
import datetime
import winsound  # Solo para Windows
from tkinter import Tk, Label, Button, messagebox
from PIL import Image, ImageTk

# Diccionario que asigna costos a códigos específicos
costos = {
    "6965821830868": 5.00,
    "mathias": 4.00
}

# Crear la ventana principal de la interfaz gráfica
root = Tk()
root.title("Escáner de Código de Barras")
root.geometry("800x600")

# Crear un panel para mostrar el video en vivo
video_panel = Label(root)
video_panel.pack()

# Etiqueta para mostrar el costo
costo_label = Label(root, text="Costo: $0.00", font=('Helvetica', 16))
costo_label.pack(pady=20)

def emitir_pitido():
    """
    Emite un pitido usando winsound en Windows.
    """
    frecuencia = 1000  # Frecuencia en Hertz
    duracion = 500     # Duración en milisegundos
    winsound.Beep(frecuencia, duracion)

def guardar_en_factura(codigo, costo):
    """
    Guarda el código de barras y su costo en un archivo de factura.
    """
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('factura.txt', 'a') as archivo:
        archivo.write(f"{fecha} - Código: {codigo} - Costo: ${costo:.2f}\n")

def escanear_codigo_de_barras():
    """
    Escanea códigos de barras desde la cámara y maneja la interfaz gráfica.
    """
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("No se puede acceder a la cámara.")
            break
        
        # Preprocesar la imagen
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Decodificar códigos de barras
        decoded_objects = decode(binary)
        
        for obj in decoded_objects:
            codigo = obj.data.decode('utf-8')
            
            if codigo in costos:
                costo = costos[codigo]
                
                # Dibujar un rectángulo alrededor del código de barras
                points = obj.polygon
                if len(points) == 4:
                    pts = np.array([point for point in points], dtype=np.int32)
                    pts = pts.reshape((-1, 1, 2))
                    cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
                    
                    # Mostrar el texto del código de barras y el costo
                    cv2.putText(frame, f"{codigo} - ${costo:.2f}", (pts[0][0][0], pts[0][0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    
                    # Actualizar la etiqueta de costo en la interfaz gráfica
                    costo_label.config(text=f"Costo: ${costo:.2f}")
                    
                    # Guardar el código y el costo en el archivo de factura
                    guardar_en_factura(codigo, costo)
                    
                    # Emitir un pitido
                    emitir_pitido()
        
        # Convertir la imagen de OpenCV a formato que tkinter puede manejar
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        imagen = Image.fromarray(frame_rgb)
        imagen_tk = ImageTk.PhotoImage(imagen)
        video_panel.config(image=imagen_tk)
        video_panel.image = imagen_tk
        
        # Actualizar la interfaz gráfica
        root.update_idletasks()
        root.update()

        # Salir si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    escanear_codigo_de_barras()
