from fastapi import FastAPI, Query
from amadeus import Client

app = FastAPI(title="Buscador de Vuelos Económicos")

amadeus = Client(client_id="U0156VAr98TAIDHoHD3m49C7XKtmg36R", client_secret="OOoUAAFl4WRXwn6e")

@app.get("/buscar_vuelos")
def buscar_vuelos(origen: str, destino: str, fecha_ida: str, fecha_vuelta: str):
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origen,
            destinationLocationCode=destino,
            departureDate=fecha_ida,
            returnDate=fecha_vuelta,
            adults=1
        )
        return response.data
    except Exception as e:
        return {"error": str(e)}
