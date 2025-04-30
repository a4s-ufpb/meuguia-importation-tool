import csv
import requests
import unicodedata
import re

from .model import Segmentation, AttractionType, Attraction
from .mapper import CsvObjectMapper

from configuration import ENDPOINTS

def normalize_string(string:str) -> str:
    # Remove acentos
    texto = unicodedata.normalize('NFD', string)
    texto = texto.encode('ascii', 'ignore').decode('utf-8')

    # Remove tudo que não for letra (a-z ou A-Z)
    texto = re.sub(r'[^a-zA-Z]', '', texto)

    # Converte para minúsculas (opcional)
    return texto.lower()


class MGDataImporter:
    def __init__(self):
        self.cities = self.get_citites() 
        print(self.cities)

    def login(self, email:str, password:str) -> str:
        url = ENDPOINTS.api_url + ENDPOINTS.auth
        headers = {"Content-Type": "application/json"}
        body = {
            "email": email,
            "password": password
        }

        response = requests.post(url, json=body, headers=headers)
        return response.json()["token"]

    def map_csv_to_objects(self, file_path: str) -> list[Attraction]:
        attractions = []
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if not row["Nome do Atrativo"]:
                    continue

                segmentations = CsvObjectMapper.map_segmentations(row["Segmentação"])
                more_info_links = CsvObjectMapper.map_info_links(row)
                attraction_type = CsvObjectMapper.map_attraction_type(row["Tipo de Atrativo"])

                attraction = Attraction(
                    name=row["Nome do Atrativo"],
                    city=row["Município"],
                    state="Paraíba - PB",
                    site=row["Site"],
                    description=row["Descrição"],
                    image_url=row["Foto"],
                    image_legend=row["Legenda da foto"],
                    map_link=row["Link do Mapa"],
                    geo_latitude=row["Latitude"],
                    geo_longitude=row["Longitude"],
                    segmentations=segmentations,
                    more_info_links=more_info_links,
                    attraction_type=attraction_type,
                    imported=False,
                    import_status="Não importado"
                )

                attractions.append(attraction)

        return attractions

    def post_attraction(self, attraction:Attraction, jwt:str) -> Attraction:
        url = ENDPOINTS.api_url + ENDPOINTS.create_attraction
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {jwt}"
        }
        
        for segmentation in attraction.segmentations:
            segmentation.id = self._post_segmentation(segmentation, jwt)
        
        attraction.attraction_type.id = self._post_attraction_type(attraction.attraction_type, jwt)
        
        city_id = self.cities.get(normalize_string(attraction.city))
        
        body = {
            "name": attraction.name,
            "description": attraction.description,
            "map_link": attraction.map_link,
            "city_id": city_id,
            "image_link": attraction.image_url,
            "info_source": attraction.site,
            "segmentations": [
                segmentation.id for segmentation in attraction.segmentations
            ],
            "attraction_type": attraction.attraction_type.id,
            "more_info_links": [
                {"link": info_link.link, "description":info_link.description} for info_link in attraction.more_info_links
            ]
        }

        print("Body:", body)

        response = requests.post(url, json=body, headers=headers)

        attraction.imported = True if response.status_code == 201 else False
        attraction.import_status = "Importado" if response.status_code == 201 else str(response.json())
        return attraction

    def _post_segmentation(self, segmentation:Segmentation, jwt:str) -> str:
        if self._exist(segmentation):
            id:str = requests.get(f"{ENDPOINTS.api_url}{ENDPOINTS.segmentations}/search?name={segmentation.name}",
                                  headers={"Authorization": "Bearer " + jwt}).json()[0]["id"]
            return id

        url = ENDPOINTS.api_url + ENDPOINTS.segmentations
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {jwt}"
        }

        body = {
            "name": segmentation.name,
            "description": segmentation.description
        }

        response = requests.post(url, json=body, headers=headers)
        return response.json()["id"]

    def _post_attraction_type(self, attraction_type:AttractionType, jwt:str) -> str:
        if self._exist(attraction_type):
            id:str = requests.get(f"{ENDPOINTS.api_url}{ENDPOINTS.attraction_type}/search?name={attraction_type.name}",
                                  headers={"Authorization": "Bearer " + jwt}).json()[0]["id"]
            return id

        url = ENDPOINTS.api_url + ENDPOINTS.attraction_type
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {jwt}"
        }

        body = {
            "name": attraction_type.name,
            "description": attraction_type.description
        }

        response = requests.post(url, json=body, headers=headers)
        return response.json()["id"]
    
    def get_citites(self) -> dict[str, id]:
        cities = []
        page = 0
        page_size = 100

        while True:
            url = f"{ENDPOINTS.api_url}{ENDPOINTS.cities}?page={page}&size={page_size}"
            response = requests.get(url)
            data = response.json()
            cities.extend(data["content"])

            if data.get("last"):
                break

            for city in cities:
                 city["name"], city["id"]

            page += 1

        return {normalize_string(city["name"]): city["id"] for city in cities}

    def _exist(self, resource:any) -> bool:
        if isinstance(resource, Segmentation):
            url = f"{ENDPOINTS.api_url}{ENDPOINTS.segmentations}/search?name={resource.name}"
        elif isinstance(resource, AttractionType):
            url = f"{ENDPOINTS.api_url}{ENDPOINTS.attraction_type}/search?name={resource.name}"
        else:
            return False
        
        response = requests.get(url)
        print("Response status code:", response.status_code)
        return len(response.json()) > 0
