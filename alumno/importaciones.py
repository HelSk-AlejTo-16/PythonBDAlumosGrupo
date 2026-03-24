import csv
import json
import xml.etree.ElementTree as ET
from tkinter import filedialog, messagebox
# Asegúrate de importar Alumnos desde tu db.py
from db import Alumnos 

# Importar CSV de Alumnos (Estructura Real)
def importarCsvAlumnos():
    ruta_archivo = filedialog.askopenfilename(
        title="Seleccionar archivo CSV de Alumnos",
        filetypes=(("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*"))
    )
    
    if not ruta_archivo:
        return 

    try:
        agregados = 0
        errores = 0
        
        with open(ruta_archivo, mode="r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            
            for fila in lector:
                # Verificamos que las columnas necesarias existan en el CSV
                if "cveAlu" in fila and "nomAlu" in fila and "edaAlu" in fila and "cveGru" in fila:
                    
                    try:
                        # --- CONVERSIÓN DE DATOS Crucial ---
                        # Convertimos a entero las claves numéricas y la edad
                        cveAlu_int = int(fila["cveAlu"])
                        edaAlu_int = int(fila["edaAlu"])
                        nomAlu_str = fila["nomAlu"].strip() # quitamos espacios extra
                        cveGru_str = fila["cveGru"].strip()

                        # Validamos que no exista un alumno con esa cveAlu (duplicados)
                        if not Alumnos.find_one({"cveAlu": cveAlu_int}):
                            
                            # Insertamos respetando los tipos de datos
                            Alumnos.insert_one({
                                "cveAlu": cveAlu_int,
                                "nomAlu": nomAlu_str,
                                "edaAlu": edaAlu_int,
                                "cveGru": cveGru_str
                            })
                            agregados += 1
                        else:
                            # Ya existe un alumno con esa clave, lo saltamos
                            pass
                            
                    except ValueError:
                        # Si cveAlu o edaAlu no eran números válidos en el CSV
                        errores += 1
                        continue
                        
        final_msg = f"Importación finalizada.\n\n Agregados: {agregados}"
        if errores > 0:
            final_msg += f"\n Saltados por datos inválidos (no numéricos): {errores}"
            
        messagebox.showinfo("Resultado", final_msg)
        
    except Exception as e:
        messagebox.showerror("Error Critico", f"Ocurrió un error al procesar el CSV:\n{e}")


# Importar JSON de Alumnos (Estructura Real)
def importarJsonAlumnos():
    ruta_archivo = filedialog.askopenfilename(
        title="Seleccionar archivo JSON de Alumnos",
        filetypes=(("Archivos JSON", "*.json"), ("Todos los archivos", "*.*"))
    )
    
    if not ruta_archivo:
        return

    try:
        agregados = 0
        
        with open(ruta_archivo, mode="r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            
            for alumno in datos:
                # Extraemos los datos del JSON
                cve = alumno.get("cveAlu")
                nom = alumno.get("nomAlu")
                eda = alumno.get("edaAlu")
                gru = alumno.get("cveGru")
                
                # Verificamos que no falten datos esenciales
                if cve is not None and nom and eda is not None and gru:
                    
                    # Validar clave numérica y duplicados
                    try:
                        cve_int = int(cve)
                        
                        if not Alumnos.find_one({"cveAlu": cve_int}):
                            # JSON suele conservar los tipos, pero forzamos int por seguridad
                            Alumnos.insert_one({
                                "cveAlu": cve_int,
                                "nomAlu": nom,
                                "edaAlu": int(eda), 
                                "cveGru": gru
                            })
                            agregados += 1
                    except ValueError:
                        continue # Clave no numérica en JSON

        messagebox.showinfo("Importación Exitosa", f"Se importaron {agregados} alumnos desde el JSON.")
        
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al importar el JSON: {e}")


# Importar XML de Alumnos (Estructura Real)
def importarXmlAlumnos():
    ruta_archivo = filedialog.askopenfilename(
        title="Seleccionar archivo XML de Alumnos",
        filetypes=(("Archivos XML", "*.xml"), ("Todos los archivos", "*.*"))
    )
    
    if not ruta_archivo:
        return

    try:
        agregados = 0
        errores = 0
        
        arbol = ET.parse(ruta_archivo)
        raiz = arbol.getroot()

        # Buscamos nodos <Alumno> (la capitalización importa)
        for nodo_alumno in raiz.findall("Alumno"):
            nodo_cve = nodo_alumno.find("cveAlu")
            nodo_nom = nodo_alumno.find("nomAlu")
            nodo_eda = nodo_alumno.find("edaAlu")
            nodo_gru = nodo_alumno.find("cveGru")

            if all(v is not None for v in [nodo_cve, nodo_nom, nodo_eda, nodo_gru]):
                try:
                    # --- CONVERSIÓN DE DATOS Crucial ---
                    # XML lee todo como texto, necesitamos convertir a int
                    cve_int = int(nodo_cve.text)
                    eda_int = int(nodo_eda.text)
                    
                    if not Alumnos.find_one({"cveAlu": cve_int}):
                        Alumnos.insert_one({
                            "cveAlu": cve_int,
                            "nomAlu": nodo_nom.text.strip(),
                            "edaAlu": eda_int,
                            "cveGru": nodo_gru.text.strip()
                        })
                        agregados += 1
                except ValueError:
                    # Si la clave o edad no eran números válidos en el XML
                    errores += 1
                    continue

        final_msg = f"Importación XML finalizada.\n\n Agregados: {agregados}"
        if errores > 0:
            final_msg += f"\nSaltados por datos inválidos: {errores}"

        messagebox.showinfo("Resultado", final_msg)
        
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error critico al procesar el XML: {e}")