import customtkinter as ctk
import requests

# Configuración de la ventana
ventana = ctk.CTk()
ventana.title("Mi Dashboard del Clima")
ventana.geometry("400x500")

def obtener_clima():
    ciudad = entrada_ciudad.get()
    api_key = "143da49a9f6c12559efd16c1f73a1c61" 
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units=metric&lang=es"
    
    try:
        respuesta = requests.get(url).json()
        temp = respuesta['main']['temp']
        desc = respuesta['weather'][0]['description']
        
        etiqueta_resultado.configure(text=f"{temp}°C\n{desc.capitalize()}")
    except:
        etiqueta_resultado.configure(text="Ciudad no encontrada")

# Elementos de la interfaz
entrada_ciudad = ctk.CTkEntry(ventana, placeholder_text="Escribe una ciudad...")
entrada_ciudad.pack(pady=20)

boton_buscar = ctk.CTkButton(ventana, text="Ver Clima", command=obtener_clima)
boton_buscar.pack(pady=10)

etiqueta_resultado = ctk.CTkLabel(ventana, text="", font=("Arial", 25))
etiqueta_resultado.pack(pady=30)

ventana.mainloop()