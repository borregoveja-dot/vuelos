from fastapi import FastAPI
from amadeus import Client, ResponseError
from datetime import datetime

app = FastAPI(title="Buscador de Vuelos Económicos")

# Configura el cliente Amadeus con tus credenciales
amadeus = Client(
    client_id="U0156VAr98TAIDHoHD3m49C7XKtmg36R",  # Reemplaza con tu client_id
    client_secret="OOoUAAFl4WRXwn6e"  # Reemplaza con tu client_secret
)

# Diccionario para convertir códigos de aerolíneas a nombres
aerolineas = {
    "AA": "American Airlines",
    "UA": "United Airlines",
    "DL": "Delta Airlines",
    "IB": "Iberia",
    "AF": "Air France",
    "LH": "Lufthansa"
}

def formatear_fecha(fecha_iso):
    fecha = datetime.fromisoformat(fecha_iso)
    return fecha.strftime("%d de %B de %Y, %I:%M %p")

def formatear_duracion(duracion_iso):
    horas = duracion_iso.split("H")[0].replace("PT", "")
    minutos = duracion_iso.split("H")[1].replace("M", "") if "H" in duracion_iso else "0"
    return f"{horas} horas {minutos} minutos"

@app.get("/buscar_mejores_ofertas")
def buscar_mejores_ofertas(origen: str, fecha_ida: str, fecha_vuelta: str, adultos: int = 1, umbral_precio: float = 500):
    # Lista Top 50 destinos globales
    destinos = [
        "MIA"
    ]
    mejores_ofertas = []

    try:
        for destino in destinos:
            response = amadeus.shopping.flight_offers_search.get(
                originLocationCode=origen,
                destinationLocationCode=destino,
                departureDate=fecha_ida,
                returnDate=fecha_vuelta,
                adults=adultos
            )

            for oferta in response.data:
                precio_total = float(oferta['price']['total'])
                if precio_total <= umbral_precio:
                    itinerario = oferta['itineraries'][0]['segments'][0]
                    salida = formatear_fecha(itinerario['departure']['at'])
                    llegada = formatear_fecha(itinerario['arrival']['at'])
                    aerolinea = aerolineas.get(itinerario['carrierCode'], itinerario['carrierCode'])
                    duracion = formatear_duracion(itinerario['duration'])

                    mejores_ofertas.append({
                        "destino": destino,
                        "precio": f"{precio_total} USD",
                        "aerolinea": aerolinea,
                        "salida": salida,
                        "llegada": llegada,
                        "duracion": duracion
                    })

        # Ordenar por precio y devolver solo las 10 mejores
        mejores_ofertas.sort(key=lambda x: float(x["precio"].replace("USD", "").strip()))
        return {"mejores_ofertas": mejores_ofertas[:10] if mejores_ofertas else "No se encontraron ofertas por debajo del umbral"}

    except ResponseError as error:
        return {"error": str(error)}

