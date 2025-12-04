from fastapi import FastAPI
from amadeus import Client, ResponseError
from datetime import datetime

app = FastAPI(title="Buscador de Vuelos Económicos")

# Configura el cliente Amadeus con tus credenciales del Sandbox

rom amadeus import Client

amadeus = Client(
    client_id="U0156VAr98TAIDHoHD3m49C7XKtmg36R",
    client_secret="OOoUAAFl4WRXwn6e"
)


# Diccionario para convertir códigos de aerolíneas a nombres
aerolineas = {
    "AA": "American Airlines",
    "UA": "United Airlines",
    "DL": "Delta Airlines"
}

def formatear_fecha(fecha_iso):
    fecha = datetime.fromisoformat(fecha_iso)
    return fecha.strftime("%d de %B de %Y, %I:%M %p")

def formatear_duracion(duracion_iso):
    horas = duracion_iso.split("H")[0].replace("PT", "")
    minutos = duracion_iso.split("H")[1].replace("M", "") if "H" in duracion_iso else "0"
    return f"{horas} horas {minutos} minutos"

@app.get("/buscar_vuelos")
def buscar_vuelos(origen: str, destino: str, fecha_ida: str, fecha_vuelta: str, adultos: int = 1):
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origen,
            destinationLocationCode=destino,
            departureDate=fecha_ida,
            returnDate=fecha_vuelta,
            adults=adultos
        )

        resultados = []
        for oferta in response.data:
            precio = oferta['price']['total'] + " USD"
            itinerario = oferta['itineraries'][0]['segments'][0]
            salida = formatear_fecha(itinerario['departure']['at'])
            llegada = formatear_fecha(itinerario['arrival']['at'])
            aerolinea = aerolineas.get(itinerario['carrierCode'], itinerario['carrierCode'])
            duracion = formatear_duracion(itinerario['duration'])

            resultados.append({
                "precio": precio,
                "aerolinea": aerolinea,
                "salida": salida,
                "llegada": llegada,
                "duracion": duracion
            })

        return {
            "origen": origen,
            "destino": destino,
            "fecha_ida": fecha_ida,
            "fecha_vuelta": fecha_vuelta,
            "resultados": resultados
        }

    except ResponseError as error:
        return {"error": str(error)}



