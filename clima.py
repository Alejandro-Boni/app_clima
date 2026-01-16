import customtkinter as ctk
import requests
from PIL import Image
import urllib.request
import io

def obtener_clima():
    ciudad = entrada_ciudad.get()
    # Tu API Key verificada
    api_key = "143da49a9f6c12559efd16c1f73a1c61"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units=metric&lang=es"
    
    try:
        respuesta = requests.get(url)
        data = respuesta.json()
        
        # Extracción de datos
        temp = data['main']['temp']
        humedad = data['main']['humidity']
        viento = data['wind']['speed']
        desc = data['weather'][0]['description']
        icon_code = data['weather'][0]['icon']
        
        # 1. Lógica de color de fondo según temperatura
        if temp > 28:
            color_fondo = "#FF4500" # Cálido
        elif temp < 15:
            color_fondo = "#1E90FF" # Frío
        else:
            color_fondo = "#2E8B57" # Templado
            
        ventana.configure(fg_color=color_fondo)
        
        # 2. Manejo del Icono
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@4x.png"
        with urllib.request.urlopen(icon_url) as u:
            raw_data = u.read()
            
        img = Image.open(io.BytesIO(raw_data))
        foto = ctk.CTkImage(light_image=img, dark_image=img, size=(160, 160))
        
        etiqueta_icono.configure(image=foto)
        etiqueta_icono.image = foto 
        
        # 3. Actualización de todas las etiquetas
        etiqueta_temp.configure(text=f"{int(temp)}°C")
        etiqueta_desc.configure(text=desc.capitalize())
        etiqueta_detalles.configure(text=f"💧 Humedad: {humedad}%  |  💨 Viento: {viento} m/s")
        
    except Exception as e:
        etiqueta_desc.configure(text="Ciudad no encontrada")
        etiqueta_temp.configure(text="--")
        etiqueta_detalles.configure(text="")
        etiqueta_icono.configure(image=None)

# --- Configuración de la Ventana ---
ctk.set_appearance_mode("dark")
ventana = ctk.CTk()
ventana.title("Estación Meteorológica Pro")
ventana.geometry("450x650")

# --- Elementos de la Interfaz ---
entrada_ciudad = ctk.CTkEntry(ventana, placeholder_text="Escribe una ciudad...", 
                              width=300, height=45, font=("Helvetica", 16))
entrada_ciudad.pack(pady=30)

boton = ctk.CTkButton(ventana, text="CONSULTAR CLIMA", command=obtener_clima, 
                      fg_color="#ffffff", text_color="#000000", 
                      hover_color="#dddddd", font=("Helvetica", 14, "bold"))
boton.pack(pady=10)

etiqueta_icono = ctk.CTkLabel(ventana, text="")
etiqueta_icono.pack(pady=10)

etiqueta_temp = ctk.CTkLabel(ventana, text="--°C", font=("Helvetica", 60, "bold"))
etiqueta_temp.pack(pady=5)

etiqueta_desc = ctk.CTkLabel(ventana, text="Esperando ciudad...", font=("Helvetica", 22))
etiqueta_desc.pack(pady=5)

# Etiqueta para Humedad y Viento
etiqueta_detalles = ctk.CTkLabel(ventana, text="", font=("Helvetica", 15, "italic"))
etiqueta_detalles.pack(pady=25)

ventana.mainloop()