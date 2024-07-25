import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os

def generar_codigo_de_barras(nombre, ruta_guardado, formato, fondo_transparente):
    try:
        code128 = barcode.get_barcode_class('code128')
        codigo = code128(nombre, writer=ImageWriter())
        codigo.save("temp_image")  # Guardar imagen temporalmente

        imagen = Image.open("temp_image.png")
        if formato == 'jpeg':
            imagen = imagen.convert("RGB")  # Convertir a RGB para JPEG
            imagen.save(ruta_guardado, format='JPEG')
        else:
            if fondo_transparente:
                imagen = imagen.convert("RGBA")  # Convertir a RGBA para fondo transparente
                datas = imagen.getdata()
                new_data = []
                for item in datas:
                    if item[0] in list(range(220, 256)):
                        new_data.append((255, 255, 255, 0))  # Fondo blanco transparente
                    else:
                        new_data.append(item)
                imagen.putdata(new_data)
            imagen.save(ruta_guardado, format='PNG')
        os.remove("temp_image.png")  # Eliminar imagen temporal
        return ruta_guardado
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar el código de barras: {e}")

def mostrar_codigo_de_barras(nombre_archivo):
    try:
        imagen = Image.open(nombre_archivo)
        imagen = imagen.resize((300, 150), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(imagen)
        panel.config(image=img)
        panel.image = img
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo mostrar la imagen: {e}")

def generar_y_mostrar():
    nombre = entry.get().strip()
    formato = formato_var.get()
    fondo_transparente = fondo_transparente_var.get()

    if nombre:
        ruta_guardado = filedialog.asksaveasfilename(
            defaultextension=f".{formato}",
            filetypes=[("Archivos PNG", "*.png"), ("Archivos JPEG", "*.jpeg")],
            initialfile=f"{nombre}.{formato}",
            title="Guardar código de barras como..."
        )
        if ruta_guardado:
            if not os.path.splitext(ruta_guardado)[1]:  # Si no tiene extensión, añadir la extensión seleccionada
                ruta_guardado += f".{formato}"
            nombre_archivo = generar_codigo_de_barras(nombre, ruta_guardado, formato, fondo_transparente)
            if nombre_archivo:
                mostrar_codigo_de_barras(nombre_archivo)
                messagebox.showinfo("Éxito", f"Código de barras generado y guardado como {nombre_archivo}")
        else:
            messagebox.showwarning("Advertencia", "No se seleccionó ninguna ubicación para guardar el archivo")
    else:
        messagebox.showwarning("Advertencia", "Por favor, introduce un nombre")

# Crear la ventana principal
root = tk.Tk()
root.title("Generador de Código de Barras")
root.geometry("450x500")
root.resizable(False, False)

# Estilos personalizados
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 12), padding=10)
style.configure('TLabel', font=('Helvetica', 12))
style.configure('TEntry', font=('Helvetica', 12), padding=5)
style.configure('TCombobox', font=('Helvetica', 12))

# Crear y posicionar widgets
frame = ttk.Frame(root, padding="20")
frame.pack(expand=True, fill=tk.BOTH)

title_label = ttk.Label(frame, text="Generador de Código de Barras", font=('Helvetica', 16, 'bold'))
title_label.pack(pady=10)

entry_label = ttk.Label(frame, text="Introduce el nombre:")
entry_label.pack(pady=5)
entry = ttk.Entry(frame, width=30)
entry.pack(pady=5)

formato_label = ttk.Label(frame, text="Selecciona el formato:")
formato_label.pack(pady=5)
formato_var = tk.StringVar(value='png')
formato_combobox = ttk.Combobox(frame, textvariable=formato_var, values=['png', 'jpeg'], state='readonly')
formato_combobox.pack(pady=5)

fondo_transparente_var = tk.BooleanVar(value=True)
fondo_transparente_check = ttk.Checkbutton(frame, text="Fondo Transparente (solo PNG)", variable=fondo_transparente_var)
fondo_transparente_check.pack(pady=5)

generate_button = ttk.Button(frame, text="Generar Código de Barras", command=generar_y_mostrar)
generate_button.pack(pady=20)

panel = ttk.Label(frame)
panel.pack(pady=10)

# Ejecutar el bucle principal
root.mainloop()
