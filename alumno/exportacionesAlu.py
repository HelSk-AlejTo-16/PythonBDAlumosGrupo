import csv
import json
import os
from operacionesAlu import generarNombreArchivo
from dbAlu import Alumnos
from tkinter import messagebox
import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom


# Exportar csv
def exportarCsv():
    alumnos = list(Alumnos.find())
 
    if not alumnos:
        messagebox.showwarning("Atención", "No hay alumnos para exportar.")
        return
 
    nombre_archivo = generarNombreArchivo("csv")
 
    with open(nombre_archivo, mode="w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        # Encabezado
        escritor.writerow(["cveAlu", "nomAlu", "edaAlu", "cveGru"])
        # Filas
        for alumno in alumnos:
            escritor.writerow([alumno["cveAlu"], alumno["nomAlu"], alumno["edaAlu"], alumno["cveGru"]])
 
    ruta = os.path.abspath(nombre_archivo)
    messagebox.showinfo("Exportado", f"Archivo CSV generado exitosamente:\n{ruta}")

# Exportar json
def exportarJson():
    alumnos = list(Alumnos.find())
 
    if not alumnos:
        messagebox.showwarning("Atención", "No hay alumnos para exportar.")
        return
 
    # Convertir ObjectId de MongoDB a string para que sea serializable
    for alumno in alumnos:
        alumno["_id"] = str(alumno["_id"])
 
    nombre_archivo = generarNombreArchivo("json")
 
    with open(nombre_archivo, mode="w", encoding="utf-8") as archivo:
        json.dump(alumnos, archivo, ensure_ascii=False, indent=4)
 
    ruta = os.path.abspath(nombre_archivo)
    messagebox.showinfo("Exportado", f"Archivo JSON generado exitosamente:\n{ruta}")


# Exportar xml
def exportarXml():
    alumnos = list(Alumnos.find())
 
    if not alumnos:
        messagebox.showwarning("Atención", "No hay alumnos para exportar.")
        return
 
    # Crear estructura XML
    raiz = ET.Element("Alumnos")
 
    for alumno in alumnos:
        nodo_alumno = ET.SubElement(raiz, "Alumno")
        nodo_cve = ET.SubElement(nodo_alumno, "cveAlu")
        nodo_cve.text = str(alumno["cveAlu"])
        nodo_nom = ET.SubElement(nodo_alumno, "nomAlu")
        nodo_nom.text = alumno["nomAlu"]
        nodo_edad = ET.SubElement(nodo_alumno, "edaAlu")
        nodo_edad.text = str(alumno["edaAlu"])
        nodo_gru = ET.SubElement(nodo_alumno, "cveGru")
        nodo_gru.text = alumno["cveGru"]
 
    # Formatear el XML con sangría para que sea legible
    xml_str = minidom.parseString(ET.tostring(raiz, encoding="unicode")).toprettyxml(indent="  ")
 
    # Eliminar la línea extra que agrega toprettyxml al inicio
    lineas = xml_str.split("\n")
    xml_formateado = "\n".join(lineas[1:])
 
    nombre_archivo = generarNombreArchivo("xml")
 
    with open(nombre_archivo, mode="w", encoding="utf-8") as archivo:
        archivo.write('<?xml version="1.0" encoding="utf-8"?>\n')
        archivo.write(xml_formateado)
 
    ruta = os.path.abspath(nombre_archivo)
    messagebox.showinfo("Exportado", f"Archivo XML generado exitosamente:\n{ruta}")


def ejecutarBackup():
    alumnos = list(Alumnos.find())
 
    if not alumnos:
        messagebox.showwarning("Atención", "No hay alumnos para respaldar.")
        return
 
    # Crear carpeta backups si no existe
    carpeta_backup = r"C:\Backup_Mongo\Backups_Alumnos"
    os.makedirs(carpeta_backup, exist_ok=True)
 
    # Subcarpeta con timestamp para este backup
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    subcarpeta = os.path.join(carpeta_backup, f"backup_{timestamp}")
    os.makedirs(subcarpeta)
 
    # Convertir ObjectId a string
    for alumno in alumnos:
        alumno["_id"] = str(alumno["_id"])
 
    # Guardar como JSON dentro de la subcarpeta
    ruta_archivo = os.path.join(subcarpeta, "alumnos.json")
    with open(ruta_archivo, mode="w", encoding="utf-8") as archivo:
        json.dump(alumnos, archivo, ensure_ascii=False, indent=4)
 
    ruta = os.path.abspath(subcarpeta)
    messagebox.showinfo("Backup exitoso", f"Backup realizado correctamente.\nUbicación:\n{ruta}")
