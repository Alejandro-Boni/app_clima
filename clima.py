import customtkinter as ctk
import requests
from PIL import Image
import urllib.request
import io
from datetime import datetime, timedelta

def obtener_clima():
    ciudad = entrada_ciudad.get()
    api_key = "143da49a9f6c12559efd16c1f73a1c61"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units=metric&lang=es"
    
    try:
        data = requests.get(url).json()
        
        # Datos meteorológicos
        temp = data['main']['temp']
        humedad = data['main']['humidity']
        viento = data['wind']['speed']
        desc = data['weather'][0]['description']
        icon_code = data['weather'][0]['icon']
        
        # Cálculo de Hora Local
        desplazamiento = data['timezone'] 
        hora_utc = datetime.utcnow()
        hora_local = hora_utc + timedelta(seconds=desplazamiento)
        hora_formateada = hora_local.strftime("%H:%M")
        
        # Colores dinámicos
        if temp > 28: color_fondo = "#E67E22" 
        elif temp < 15: color_fondo = "#2980B9" 
        else: color_fondo = "#27AE60" 
        
        ventana.configure(fg_color=color_fondo)
        # El frame debe tener un color que resalte pero sin 'alpha'
        frame_detalles.configure(fg_color="#1a1a1a") 
        
        # Icono HD
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@4x.png"
        with urllib.request.urlopen(icon_url) as u:
            raw_data = u.read()
        img = Image.open(io.BytesIO(raw_data))
        foto = ctk.CTkImage(light_image=img, dark_image=img, size=(180, 180))
        
        etiqueta_icono.configure(image=foto)
        etiqueta_icono.image = foto 
        
        # Actualización de Textos
        etiqueta_temp.configure(text=f"{int(temp)}°C")
        etiqueta_desc.configure(text=desc.upper())
        etiqueta_hora.configure(text=f"Hora Local: {hora_formateada}")
        etiqueta_humedad.configure(text=f"💧 {humedad}%")
        etiqueta_viento.configure(text=f"💨 {viento} m/s")
        
    except Exception as e:
        etiqueta_desc.configure(text="CIUDAD NO ENCONTRADA")
        etiqueta_temp.configure(text="--")

# --- Interfaz Corregida ---
ctk.set_appearance_mode("dark")
ventana = ctk.CTk()
ventana.title("Weather Pro Dashboard")
ventana.geometry("450x750")

entrada_ciudad = ctk.CTkEntry(ventana, placeholder_text="Buscar ciudad...", 
                              width=320, height=50, corner_radius=25)
entrada_ciudad.pack(pady=(40, 10))

boton = ctk.CTkButton(ventana, text="BUSCAR", command=obtener_clima, 
                      corner_radius=25, fg_color="white", text_color="black")
boton.pack(pady=10)

etiqueta_icono = ctk.CTkLabel(ventana, text="")
etiqueta_icono.pack(pady=0)

etiqueta_temp = ctk.CTkLabel(ventana, text="--°C", font=("Helvetica", 80, "bold"))
etiqueta_temp.pack(pady=0)

etiqueta_desc = ctk.CTkLabel(ventana, text="DESCUBRE EL CLIMA", font=("Helvetica", 18, "bold"))
etiqueta_desc.pack(pady=5)

etiqueta_hora = ctk.CTkLabel(ventana, text="--:--", font=("Helvetica", 16))
etiqueta_hora.pack(pady=10)

# --- Frame de Detalles (Corregido sin alpha) ---
frame_detalles = ctk.CTkFrame(ventana, fg_color="transparent", corner_radius=20)
frame_detalles.pack(pady=30, padx=40, fill="x")

etiqueta_humedad = ctk.CTkLabel(frame_detalles, text="💧 --%", font=("Helvetica", 16, "bold"))
etiqueta_humedad.pack(side="left", expand=True, pady=20)

etiqueta_viento = ctk.CTkLabel(frame_detalles, text="💨 -- m/s", font=("Helvetica", 16, "bold"))
etiqueta_viento.pack(side="left", expand=True, pady=20)

ventana.mainloop()