
from fastapi import FastAPI, Query, HTTPException
from typing import Optional
from datetime import datetime

app = FastAPI(
    title="Buscador de Vuelos Económicos",
    description="Prototipo para encontrar los destinos más baratos en fechas específicas",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "status": "FastAPI está funcionando",
        "documentación": "/docs",
        "endpoint_buscar_vuelos": "/buscar_vuelos"
    }

vuelos_simulados = [
    {"destino": "Cancún", "precio": 320},
    {"destino": "Madrid", "precio": 700},
    {"destino": "Bogotá", "precio": 150},
    {"destino": "Buenos Aires", "precio": 430},
    {"destino": "Miami", "precio": 380},
    {"destino": "Ciudad de México", "precio": 300},
    {"destino": "Santiago", "precio": 400},
    {"destino": "Lima", "precio": 280},
    {"destino": "Nueva York", "precio": 600}
]

@app.get("/buscar_vuelos")
def buscar_vuelos(
    origen: str = Query(..., description="Aeropuerto de origen"),
    fecha_ida: str = Query(..., description="Fecha de ida (YYYY-MM-DD)"),
    fecha_vuelta: str = Query(..., description="Fecha de vuelta (YYYY-MM-DD)"),
    destino: Optional[str] = Query(None, description="Filtrar por destino"),
    precio_max: Optional[int] = Query(None, description="Filtrar por precio máximo")
):
    try:
        fecha_ida_dt = datetime.strptime(fecha_ida, "%Y-%m-%d")
        fecha_vuelta_dt = datetime.strptime(fecha_vuelta, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use YYYY-MM-DD")

    if fecha_ida_dt >= fecha_vuelta_dt:
        raise HTTPException(status_code=400, detail="La fecha de ida debe ser anterior a la fecha de vuelta")

    resultados = vuelos_simulados

    if destino:
        resultados = [v for v in resultados if v["destino"].lower() == destino.lower()]

    if precio_max is not None:
        if precio_max <= 0:
            raise HTTPException(status_code=400, detail="precio_max debe ser mayor a 0")
        resultados = [v for v in resultados if v["precio"] <= precio_max]

    resultados = sorted(resultados, key=lambda x: x["precio"])[:10]

    if not resultados:
        return {"mensaje": "No se encontraron vuelos con los filtros aplicados"}

    return {
        "origen": origen,
        "fecha_ida": fecha_ida,
        "fecha_vuelta": fecha_vuelta,
        "resultados": resultados
    }
