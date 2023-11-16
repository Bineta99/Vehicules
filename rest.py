# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 09:54:00 2023

@author: user
"""

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import requests
from config import *

app = Flask(__name__)
api = Api(app)

class Cartographie(Resource):
    def get(self, start, end):
        url = f"https://api.openrouteservice.org/v2/directions/driving-car?start={start}&end={end}"
        headers = {"Authorization": OPEN_ROUTE_API_KEY}
        response = requests.get(url, headers=headers)
        data = response.json()
        distance = data["features"][0]["properties"]["segments"][0]["distance"]
        return {"distance": distance}

class BornesRecharge(Resource):
    def get(self, lat, lon):
        url = BORNES_API_URL + f"{lat},{lon},10000"  # Cherche les bornes dans un rayon de 10 km
        response = requests.get(url)
        data = response.json()
        bornes = [{"nom": record["fields"]["n_station"], 
                   "adresse": record["fields"]["ad_station"], 
                   "lat": record["fields"]["geom"]["coordinates"][1], 
                   "lon": record["fields"]["geom"]["coordinates"][0]} 
                  for record in data["records"]]
        return bornes
    # def get(self, lat, lon):
    #     try:
    #         # Vérifiez si la latitude et la longitude sont valides
    #         if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
    #             return {"error": "Invalid latitude or longitude"}, 400

    #         url = BORNES_API_URL + f"{lat},{lon},10000"  # Cherche les bornes dans un rayon de 10 km
    #         response = requests.get(url)

    #         # Vérifiez si la requête a réussi
    #         if response.status_code == 200:
    #             data = response.json()
    #             records = data.get('records', [])  # obtenir la liste des enregistrements

    #             bornes = [
    #                 {
    #                     "nom": record.get("fields", {}).get("n_station", "N/A"), 
    #                     "adresse": record.get("fields", {}).get("ad_station", "N/A"), 
    #                     "lat": record.get("fields", {}).get("geom", {}).get("coordinates", [None, None])[1], 
    #                     "lon": record.get("fields", {}).get("geom", {}).get("coordinates", [None, None])[0]
    #                 } for record in records
    #             ]

    #             return bornes, 200  # le code de statut HTTP pour une réponse réussie
    #         else:
    #             return {"error": "API request failed with status code " + str(response.status_code)}, 500

    #     except Exception as e:
    #         return {"error": f"An unexpected error occurred: {str(e)}"}, 500

api.add_resource(Cartographie, '/cartographie/<string:start>/<string:end>')
api.add_resource(BornesRecharge, '/bornes/<float:lat>/<float:lon>')


if __name__ == "__main__":
    app.run(debug=True, port=5001)
