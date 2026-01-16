import customtkinter as ctk
import requests
from PIL import Image
import urllib.request
import io

def obtener_clima():
    ciudad = entrada_ciudad.get()
    # Tu API Key que ya comprobamos que funciona
    api_key = "143da49a9f6c12559efd16c1f73a1c61"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units=metric&lang=es"
    
    try:
        data = requests.get(url).json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        icon_code = data['weather'][0]['icon']
        
        # --- MEJORA 1: Colores según temperatura ---
        if temp > 28:
            color_fondo = "#FF4500" # Rojo/Naranja para calor intenso
        elif temp < 15:
            color_fondo = "#1E90FF" # Azul para frío
        else:
            color_fondo = "#2E8B57" # Verde mar para clima templado
            
        ventana.configure(fg_color=color_fondo)
        
        # --- MEJORA 2: Descarga de Icono en HD ---
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@4x.png"
        with urllib.request.urlopen(icon_url) as u:
            raw_data = u.read()
            
        img = Image.open(io.BytesIO(raw_data))
        foto = ctk.CTkImage(light_image=img, dark_image=img, size=(160, 160))
        
        etiqueta_icono.configure(image=foto)
        etiqueta_icono.image = foto 
        
        # --- MEJORA 3: Formato de texto ---
        etiqueta_resultado.configure(text=f"{int(temp)}°C\n{desc.capitalize()}")
        
    except Exception as e:
        etiqueta_resultado.configure(text="¡Ciudad no encontrada!")
        etiqueta_icono.configure(image=None)

# --- Interfaz Estética ---
ctk.set_appearance_mode("dark")
ventana = ctk.CTk()
ventana.title("Dashboard Meteorológico Pro")
ventana.geometry("400x600")

entrada_ciudad = ctk.CTkEntry(ventana, placeholder_text="Busca una ciudad...", width=280, height=45, font=("Helvetica", 16))
entrada_ciudad.pack(pady=40)

boton = ctk.CTkButton(ventana, text="Consultar", command=obtener_clima, 
                      fg_color="#ffffff", text_color="#000000", hover_color="#cccccc", font=("Helvetica", 14, "bold"))
boton.pack(pady=10)

etiqueta_icono = ctk.CTkLabel(ventana, text="")
etiqueta_icono.pack(pady=20)

etiqueta_resultado = ctk.CTkLabel(ventana, text="---", font=("Helvetica", 35, "bold"))
etiqueta_resultado.pack(pady=20)

ventana.mainloop()