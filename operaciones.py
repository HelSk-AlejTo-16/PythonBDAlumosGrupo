import os
from datetime import datetime 
from db import Grupos
from tkinter import messagebox
import tkinter as tk

##Método para todos
def generarNombreArchivo(extension):
    carpeta = r"C:\Backup_Mongo"
    os.makedirs(carpeta, exist_ok=True)  # crea la carpeta si no existe
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    
    return os.path.join(carpeta, f"grupos_{timestamp}.{extension}")

# Función para agregar grupo
def Agregar(ent_cveGru, ent_nomGru):
    if not ent_cveGru.get():
        messagebox.showerror("Error", "Por favor, ingresa la clave del grupo")
        return
    
    if not ent_nomGru.get():
        messagebox.showerror("Error", "Por favor, ingresa el nombre del grupo")
        return
    
    if Grupos.find_one({"cveGru": ent_cveGru.get()}) is not None:
        messagebox.showerror("Error", "Ya existe un grupo con la clave proporcionada")
        return
    else:
        Grupos.insert_one({"cveGru": ent_cveGru.get(), "nomGru": ent_nomGru.get()})
        messagebox.showinfo("Éxito", "Grupo agregado correctamente")
        ent_cveGru.delete(0, tk.END)
        ent_nomGru.delete(0, tk.END)

# Función para actualizar grupo
def Actualizar(ent_cveGru, ent_nomGru):
    if not ent_cveGru.get():
        messagebox.showerror("Error", "Por favor, ingresa la clave del grupo a actualizar")
        return
    if not ent_nomGru.get():
        messagebox.showerror("Error", "Por favor, ingresa el nuevo nombre del grupo")
        return
    
    if Grupos.find_one({"cveGru": ent_cveGru.get()}) is None:
        messagebox.showerror("Error", "No se encontró un grupo con la clave proporcionada")
        return
    else:
        Grupos.update_one({"cveGru": ent_cveGru.get()}, {"$set": {"nomGru": ent_nomGru.get()}})
        messagebox.showinfo("Éxito", "Grupo actualizado correctamente")
        ent_cveGru.delete(0, tk.END)
        ent_nomGru.delete(0, tk.END)

#Función para ver grupo
def VerUnGrupo(ent_cveGru, ent_nomGru):
    # .get().strip() elimina espacios accidentales al inicio o final
    clave = ent_cveGru.get().strip()
    nombre = ent_nomGru.get().strip()

    if clave and nombre:
        Grupo_Existente = Grupos.find_one({"cveGru": clave, "nomGru": nombre})
        
        if not Grupo_Existente:
            messagebox.showerror("Error", "No existe un grupo con esos datos.")
            ent_cveGru.delete(0, tk.END)
            ent_nomGru.delete(0, tk.END)
        else:
          
            resumen = f"Clave: {Grupo_Existente['cveGru']}\nNombre: {Grupo_Existente['nomGru']}"
            messagebox.showinfo("Éxito", resumen)
    elif clave or nombre:
        messagebox.showwarning("Atención", "Por favor llene ambos campos.")
    else:
      
        lista_grupos = Grupos.find()
        listado = "--Listado de todos los grupos --\n \n"

        for grupo in lista_grupos:
            listado += f"{grupo['cveGru']} - {grupo['nomGru']}\n"
        messagebox.showinfo("Todos los grupos", listado)

#Limpiar Grupo.
def Limpiar(ent_cveGru, ent_nomGru):
    clave = ent_cveGru.get()
    nombre = ent_nomGru.get()
    if not clave and not nombre:
       messagebox.showerror("Atención", "No hay nada para borrar")

    else:
        
        ent_nomGru.delete(0,tk.END)
        ent_cveGru.delete(0,tk.END)
#Eliminar Grupo 
def EliminarGrupo(ent_cveGru, ent_nomGru): 
    clave = ent_cveGru.get().strip()
    nombre = ent_nomGru.get().strip()

    if clave and nombre:
        Grupo_Existente = Grupos.find_one({"cveGru": clave, "nomGru": nombre})

        if not Grupo_Existente:
            messagebox.showerror("Error", "No existe un grupo con esos datos.")
            ent_cveGru.delete(0, tk.END)
            ent_nomGru.delete(0, tk.END)
        
        else:
            Grupos.delete_one({"cveGru":clave, "nomGru":nombre})
            messagebox.showinfo("Éxito", "Se borró exitosamente el grupo")
            ##Falta borrar los alumnos :p
    elif clave or nombre:
            messagebox.showerror("Atención", "Por favor llene ambos campos.")

    else:
        messagebox.showerror("Error", "Llene los dos apartados.")