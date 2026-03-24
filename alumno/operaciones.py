import os
from datetime import datetime
import subprocess 
from db import Alumnos, Grupos
from tkinter import filedialog, messagebox
import tkinter as tk

##Método para todos
def generarNombreArchivo(extension):
    carpeta = r"C:\Backup_Mongo"
    os.makedirs(carpeta, exist_ok=True)  # crea la carpeta si no existe
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(carpeta, f"alumnos_{timestamp}.{extension}")

# Función para validar que el grupo exista
def validarGrupo(cveGru):
    return Grupos.find_one({"cveGru": cveGru}) is not None

# Función para agregar alumno
def Agregar(ent_cveAlu, ent_nomAlu, ent_edaAlu, ent_cveGru):
    if not ent_cveAlu.get():
        messagebox.showerror("Error", "Por favor, ingresa la clave del alumno")
        return
    
    if not ent_nomAlu.get():
        messagebox.showerror("Error", "Por favor, ingresa el nombre del alumno")
        return
    
    if not ent_edaAlu.get():
        messagebox.showerror("Error", "Por favor, ingresa la edad del alumno")
        return
    
    if not ent_cveGru.get():
        messagebox.showerror("Error", "Por favor, ingresa la clave del grupo")
        return
    
    # Validar que la clave del alumno sea única
    try:
        cveAlu_int = int(ent_cveAlu.get())
        edaAlu_int = int(ent_edaAlu.get())
    except ValueError:
        messagebox.showerror("Error", "La clave y edad deben ser números")
        return
    
    if Alumnos.find_one({"cveAlu": cveAlu_int}) is not None:
        messagebox.showerror("Error", "Ya existe un alumno con la clave proporcionada")
        return
    
    # Validar que el grupo exista
    if not validarGrupo(ent_cveGru.get()):
        messagebox.showerror("Error", "El grupo ingresado no existe")
        return
    
    Alumnos.insert_one({
        "cveAlu": cveAlu_int, 
        "nomAlu": ent_nomAlu.get(), 
        "edaAlu": edaAlu_int,
        "cveGru": ent_cveGru.get()
    })
    messagebox.showinfo("Éxito", "Alumno agregado correctamente")
    ent_cveAlu.delete(0, tk.END)
    ent_nomAlu.delete(0, tk.END)
    ent_edaAlu.delete(0, tk.END)
    ent_cveGru.delete(0, tk.END)

# Función para actualizar alumno
def Actualizar(ent_cveAlu, ent_nomAlu, ent_edaAlu, ent_cveGru):
    if not ent_cveAlu.get():
        messagebox.showerror("Error", "Por favor, ingresa la clave del alumno a actualizar")
        return
    if not ent_nomAlu.get():
        messagebox.showerror("Error", "Por favor, ingresa el nuevo nombre del alumno")
        return
    if not ent_edaAlu.get():
        messagebox.showerror("Error", "Por favor, ingresa la nueva edad del alumno")
        return
    if not ent_cveGru.get():
        messagebox.showerror("Error", "Por favor, ingresa la clave del grupo")
        return
    
    try:
        cveAlu_int = int(ent_cveAlu.get())
        edaAlu_int = int(ent_edaAlu.get())
    except ValueError:
        messagebox.showerror("Error", "La clave y edad deben ser números")
        return
    
    # Validar que el grupo exista
    if not validarGrupo(ent_cveGru.get()):
        messagebox.showerror("Error", "El grupo ingresado no existe")
        return
    
    if Alumnos.find_one({"cveAlu": cveAlu_int}) is None:
        messagebox.showerror("Error", "No se encontró un alumno con la clave proporcionada")
        return
    
    Alumnos.update_one(
        {"cveAlu": cveAlu_int}, 
        {"$set": {
            "nomAlu": ent_nomAlu.get(),
            "edaAlu": edaAlu_int,
            "cveGru": ent_cveGru.get()
        }}
    )
    messagebox.showinfo("Éxito", "Alumno actualizado correctamente")
    ent_cveAlu.delete(0, tk.END)
    ent_nomAlu.delete(0, tk.END)
    ent_edaAlu.delete(0, tk.END)
    ent_cveGru.delete(0, tk.END)

#Función para ver alumno
def VerUnAlumno(ent_cveAlu):
    clave = ent_cveAlu.get().strip()
    
    if clave:
        try:
            cveAlu_int = int(clave)
            Alumno_Existente = Alumnos.find_one({"cveAlu": cveAlu_int})
            
            if not Alumno_Existente:
                messagebox.showerror("Error", "No existe un alumno con esa clave.")
                ent_cveAlu.delete(0, tk.END)
            else:
                resumen = f"Clave: {Alumno_Existente['cveAlu']}\nNombre: {Alumno_Existente['nomAlu']}\nEdad: {Alumno_Existente['edaAlu']}\nGrupo: {Alumno_Existente['cveGru']}"
                messagebox.showinfo("Datos del Alumno", resumen)
        except ValueError:
            messagebox.showerror("Error", "La clave debe ser un número")
    else:
        lista_alumnos = list(Alumnos.find())
        if not lista_alumnos:
            messagebox.showinfo("Alumnos", "No hay alumnos registrados")
            return
        
        listado = "--Listado de todos los alumnos --\n\n"
        for alumno in lista_alumnos:
            listado += f"Clave: {alumno['cveAlu']} | Nombre: {alumno['nomAlu']} | Edad: {alumno['edaAlu']} | Grupo: {alumno['cveGru']}\n"
        messagebox.showinfo("Todos los alumnos", listado)

#Limpiar Alumno
def Limpiar(ent_cveAlu, ent_nomAlu, ent_edaAlu, ent_cveGru):
    clave = ent_cveAlu.get()
    nombre = ent_nomAlu.get()
    edad = ent_edaAlu.get()
    grupo = ent_cveGru.get()
    
    if not clave and not nombre and not edad and not grupo:
        messagebox.showerror("Atención", "No hay nada para limpiar")
    else:
        ent_cveAlu.delete(0, tk.END)
        ent_nomAlu.delete(0, tk.END)
        ent_edaAlu.delete(0, tk.END)
        ent_cveGru.delete(0, tk.END)

#Eliminar Alumno
def EliminarAlumno(ent_cveAlu, ent_nomAlu, ent_edaAlu, ent_cveGru): 
    clave = ent_cveAlu.get().strip()
    
    if clave:
        try:
            cveAlu_int = int(clave)
            Alumno_Existente = Alumnos.find_one({"cveAlu": cveAlu_int})
            
            if not Alumno_Existente:
                messagebox.showerror("Error", "No existe un alumno con esa clave.")
                ent_cveAlu.delete(0, tk.END)
            else:
                Alumnos.delete_one({"cveAlu": cveAlu_int})
                messagebox.showinfo("Éxito", "Alumno eliminado exitosamente")
                ent_cveAlu.delete(0, tk.END)
                ent_nomAlu.delete(0, tk.END)
                ent_edaAlu.delete(0, tk.END)
                ent_cveGru.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "La clave debe ser un número")
    else:
        messagebox.showerror("Error", "Por favor ingresa la clave del alumno a eliminar")
        
# 1. Eliminar todos los alumnos
def eliminarTodosLosAlumnos():
    # Siempre es buena práctica pedir confirmación antes de vaciar una colección
    respuesta = messagebox.askyesno(
        "Confirmar Eliminación", 
        "¿Estás seguro de que deseas eliminar TODOS los alumnos?\n\nEsta acción no se puede deshacer."
    )
    
    if respuesta:
        try:
            # Un filtro vacío {} borra todos los documentos de la colección
            resultado = Alumnos.delete_many({})
            messagebox.showinfo("Éxito", f"Se han eliminado {resultado.deleted_count} alumnos de la base de datos.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al vaciar la colección: {e}")


# 2. Ejecutar Backup de Alumnos (mongodump)
def ejecutarBackupAlumnos():
    # Seleccionar dónde guardar la carpeta de respaldo
    carpeta_destino = filedialog.askdirectory(
        title="Selecciona la carpeta para guardar el Backup de Alumnos"
    )
    
    if not carpeta_destino:
        return 
        
    # Crear nombre de carpeta con fecha y hora
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta_backup = os.path.join(carpeta_destino, f"backup_alumnos_{timestamp}")
    
    try:
        # Usamos --collection=Alumno para no mezclar con la colección Grupos
        comando = [
            "mongodump",
            "--db=BD_GrupoAlumno",
            "--collection=Alumno",
            f"--out={ruta_backup}"
        ]
        
        resultado = subprocess.run(comando, capture_output=True, text=True)
        
        if resultado.returncode == 0:
            messagebox.showinfo("Backup Exitoso", f"Respaldo de Alumnos generado correctamente en:\n{ruta_backup}")
        else:
            messagebox.showerror("Error en Backup", f"Hubo un problema al generar el backup:\n{resultado.stderr}")
            
    except FileNotFoundError:
        messagebox.showerror("Error", "No se encontró el comando 'mongodump'. Asegúrate de tener las MongoDB Database Tools instaladas y en el PATH.")
    except Exception as e:
        messagebox.showerror("Error Inesperado", f"Ocurrió un error: {e}")


# 3. Restaurar todos los Alumnos (mongorestore)
def restaurarTodosLosAlumnos():
    # Para restaurar una sola colección, el usuario debe seleccionar el archivo .bson generado
    ruta_archivo_bson = filedialog.askopenfilename(
        title="Selecciona el archivo Alumno.bson para restaurar",
        filetypes=(("Archivos BSON de MongoDB", "*.bson"), ("Todos los archivos", "*.*"))
    )
    
    if not ruta_archivo_bson:
        return 

    respuesta = messagebox.askyesno(
        "Confirmar Restauración", 
        f"¿Deseas restaurar la colección de Alumnos desde este archivo?\n\n{ruta_archivo_bson}"
    )

    if respuesta:
        try:
            comando = [
                "mongorestore",
                "--db=BD_GrupoAlumno",
                "--collection=Alumno",
                ruta_archivo_bson
            ]

            resultado = subprocess.run(comando, capture_output=True, text=True)

            if resultado.returncode == 0:
                messagebox.showinfo("Restauración Exitosa", "El backup de alumnos se ha restaurado correctamente.")
            else:
                messagebox.showerror("Error de Restauración", f"Hubo un problema:\n{resultado.stderr}")

        except FileNotFoundError:
            messagebox.showerror("Herramienta no encontrada", "No se encontró el comando 'mongorestore'.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")
