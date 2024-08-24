## CALIDAD DE ENERGÍA ELÉCTRICA 2023-B
## *******FENÓMENOS PERTURBADORES DE LA ONDA DE VOLTAJE**********
## ELABAORADOR POR: GUAMANI KEVIN

import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from PIL import Image, ImageTk 

def generar_onda():
    opcion_seleccionada = radio_var.get()
    amplitud = float(amp_edit.get())
    frecuencia = float(freq_edit.get())
    disminucion_amplitud = float(amp_dec_edit.get())
    tiempo_inicio = float(start_edit.get())
    tiempo_final = float(end_edit.get())
    duracion = float(dur_edit.get())

#Validación de datos (evita que los valores tanto de amplitud o tiempos sean negativos)
    if amplitud <= 0:
        tk.messagebox.showerror("Error", "La amplitud debe ser un número positivo.")
        return

    if disminucion_amplitud < 0 or disminucion_amplitud > 100:
        tk.messagebox.showerror("Error", "La disminución de amplitud debe estar entre 0% y 100%.")
        return

    if tiempo_inicio < 0 or tiempo_final <= tiempo_inicio or duracion <= 0:
        tk.messagebox.showerror("Error", "Por favor, ingrese tiempos válidos.")
        return

#Restricción de voltaje
    if opcion_seleccionada == 'SAG de Voltaje' and (disminucion_amplitud < 10 or disminucion_amplitud > 90):
        tk.messagebox.showerror("Error", "La disminución de amplitud para SAG de Voltaje debe estar entre 10% y 90%.")
        return

    if opcion_seleccionada == 'Bajo Voltaje' and (disminucion_amplitud < 10 or disminucion_amplitud > 20):
        tk.messagebox.showerror("Error", "La disminución de amplitud para Bajo Voltaje debe estar entre 10% y 20%.")
        return

    if opcion_seleccionada == 'Interrupción Breve' and (disminucion_amplitud < 90 or disminucion_amplitud > 100):
        tk.messagebox.showerror("Error", "La disminución de amplitud para Interrupción Breve debe estar entre 90% y 100%.")
        return
    
    if opcion_seleccionada == 'Interrupción Sostenida' and (disminucion_amplitud != 100):
        tk.messagebox.showerror("Error", "La disminución de amplitud para Interrupción Sostenida debe ser el 100%.")
        return
    
#Restricción de Tiempo
  
    if opcion_seleccionada == 'SAG de Voltaje':
        periodo = 1 / frecuencia
        if tiempo_final - tiempo_inicio < 0.5*periodo / frecuencia or tiempo_final - tiempo_inicio > 60:
            tk.messagebox.showerror("Error", "La duración para SAG de Voltaje debe estar entre 1/2 ciclo y 1 minuto.")
            return
    elif opcion_seleccionada == 'Bajo Voltaje':
        if tiempo_final - tiempo_inicio <= 60:
            tk.messagebox.showerror("Error", "La duración para Bajo Voltaje debe ser mayor a 1 minuto.")
            return
    elif opcion_seleccionada == 'Interrupción Breve':
        periodo = 1 / frecuencia
        if tiempo_final - tiempo_inicio < 0.5*periodo or tiempo_final - tiempo_inicio > 60:
            tk.messagebox.showerror("Error", "La duración para Interrupción Breve debe estar entre 1/2 ciclo y 1 minuto.")
            return
    elif opcion_seleccionada == 'Interrupción Sostenida':
        periodo = 1 / frecuencia
        if tiempo_final - tiempo_inicio <= 60:
            tk.messagebox.showerror("Error", "La duración para Interrupción Sostenida debe ser mayor a 1 minuto.")
            return
   
    if opcion_seleccionada in ('SAG de Voltaje', 'Bajo Voltaje', 'Interrupción Breve', 'Interrupción Sostenida'):
        titulo = opcion_seleccionada
    else:
        titulo = 'Onda Sinusoidal' 
   
  # Gráfico  
    t = np.arange(0, duracion, 0.00001)
    y = amplitud * np.sin(2 * np.pi * frecuencia * t)
    intervalo_idx = np.where((t >= tiempo_inicio) & (t <= tiempo_final))
    y[intervalo_idx] *= (1 - disminucion_amplitud / 100)
    
    fig=plt.figure(figsize=(10, 4))
    plt.plot(t, y)
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Voltaje [V]')
    plt.title(titulo)
    plt.grid(True)
    plt.show()
            

    
    # Mostrar el gráfico en la interfaz
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=3, column=3, columnspan=2, rowspan=10, padx=10, pady=5, sticky="nsew")

    # Añadir barra de herramientas de navegación
    toolbar_frame = ttk.Frame(root)
    toolbar_frame.grid(row=13, column=3, columnspan=2)
    toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
    toolbar.update()


# Crear la ventana principal
root = tk.Tk()
root.title('Fenómenos Pertubadores de la Onda de Voltaje')
root.configure(bg='lightblue') 

# Importación de logos
image_path = "epn.png"
image1= Image.open(image_path)
image2=image1.resize((150,150))
photo1 = ImageTk.PhotoImage(image2)
image1_label = ttk.Label(root, image=photo1)
image1_label.grid(row=0, column=0, padx=10, pady=10)

image2_path = "electricidad.png"
image3= Image.open(image2_path)
image4=image3.resize((150,150))
photo2 = ImageTk.PhotoImage(image4)
image2_label = ttk.Label(root, image=photo2)
image2_label.grid(row=0, column=4, padx=10, pady=10)



# Encabezado
bold_font = ('Helvetica', 12, 'bold')
label = ttk.Label(root, text='CALIDAD DE ENERGÍA ELÉCTRICA 2023-B', font=bold_font)
label.grid(row=0, column=1, padx=5, pady=5)

label = ttk.Label(root, text='ESCUELA POLITECNICA NACIONAL', font=bold_font)
label.grid(row=1, column=1, padx=5, pady=5)

label = ttk.Label(root, text='Guamaní Kevin', font=bold_font)
label.grid(row=2, column=1, padx=5, pady=5)

# Selección del tipo de Onda por el usuario

ttk.Label(root, text='Tipo de Fenómeno Perturbador:').grid(row=3, column=0, padx=5, pady=5)
radio_var = tk.StringVar(value='SAG de Voltaje')
ttk.Combobox(root, textvariable=radio_var, values=['SAG de Voltaje', 'Bajo Voltaje', 'Interrupción Breve',
                  'Interrupción Sostenida']).grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky='w')

#Cuadros para los valores de entrada 
ttk.Label(root, text='Amplitud [V]:').grid(row=4, column=0, padx=5, pady=5)
amp_edit = ttk.Entry(root)
amp_edit.grid(row=4, column=1, padx=5, pady=5)

ttk.Label(root, text='Frecuencia [Hz]:').grid(row=5, column=0, padx=5, pady=5)
freq_edit = ttk.Entry(root)
freq_edit.grid(row=5, column=1, padx=5, pady=5)

ttk.Label(root, text='Disminución de Amplitud ΔV [%]:').grid(row=6, column=0, padx=5, pady=5)
amp_dec_edit = ttk.Entry(root)
amp_dec_edit.grid(row=6, column=1, padx=5, pady=5)

ttk.Label(root, text='Tiempo de Inicio del Fenómeno To [s]:').grid(row=7, column=0, padx=5, pady=5)
start_edit = ttk.Entry(root)
start_edit.grid(row=7, column=1, padx=5, pady=5)

ttk.Label(root, text='Tiempo Final del Fenómeno Tf [s]:').grid(row=8, column=0, padx=5, pady=5)
end_edit = ttk.Entry(root)
end_edit.grid(row=8, column=1, padx=5, pady=5)

ttk.Label(root, text='Tiempo de Simulación [s]:').grid(row=9, column=0, padx=5, pady=5)
dur_edit = ttk.Entry(root)
dur_edit.grid(row=9, column=1, padx=5, pady=5)


#Graficar la Onda
generate_button = ttk.Button(root, text='Graficar', command=generar_onda)
generate_button.grid(row=11, column=0, columnspan=2, padx=5, pady=5)

# Ejecutar la aplicación
root.mainloop()
