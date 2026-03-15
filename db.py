from pymongo import MongoClient as MC

# Conexión a MongoDB
client = MC("mongodb://localhost:27017/")
db = client["BD_GrupoAlumno"]
Grupos = db["Grupo"]