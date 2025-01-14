import csv
import requests

from .model import Segmentation, AttractionType, MoreInfoLink, Attraction
from utils.mapper import CsvObjectMapper

class MGDataImporter:
    def __init__(self):
        pass

    def login(self, email:str, password:str) -> str:
        url = "http://localhost:8080/api/auth/authenticate"
        headers = {"Content-Type": "application/json"}
        body = {
            "email": email,
            "password": password
        }

        response = requests.post(url, json=body, headers=headers)
        print("Response status code:", response.status_code)
        print("Response body:", response.json())
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
        url = "http://localhost:8080/api/tourists/create"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {jwt}"
        }
        
        for info_link in attraction.more_info_links:
            info_link.id = self._post_info_link(info_link, jwt)
        
        for segmentation in attraction.segmentations:
            segmentation.id = self._post_segmentation(segmentation, jwt)
        
        attraction.attraction_type.id = self._post_attraction_type(attraction.attraction_type, jwt)
        
        body = {
            "name": attraction.name,
            "description": attraction.description,
            "map_link": attraction.map_link,
            "city": attraction.city,
            "state": attraction.state,
            "image_link": attraction.image_url,
            "info_source": attraction.site,
            "segmentations": [
                {"id": segmentation.id, "name": segmentation.name, "description": segmentation.description} for segmentation in attraction.segmentations
            ],
            "attraction_type": {"id": attraction.attraction_type.id, "name": attraction.attraction_type.name, "description": attraction.attraction_type.description},
            "more_info_links": [
                {"id": info_link.id, "link": info_link.link, "description": info_link.description} for info_link in attraction.more_info_links
            ]
        }

        response = requests.post(url, json=body, headers=headers)
        print("Response status code:", response.status_code)

        attraction.imported = True if response.status_code == 201 else False
        attraction.import_status = "Importado" if response.status_code == 201 else str(response.json())
        return attraction

    def _post_segmentation(self, segmentation:Segmentation, jwt:str) -> str:
        if self._exist(segmentation):
            id:str = requests.get("http://localhost:8080/api/segmentations/search?name=" + segmentation.name, headers={"Authorization": "Bearer " + jwt}).json()[0]["id"]
            return id

        url = "http://localhost:8080/api/segmentations"
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


    def _post_info_link(self, info_link:MoreInfoLink, jwt:str) -> str:
        url = "http://localhost:8080/api/more-info"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {jwt}"
        }

        body = {
            "link": info_link.link.strip(),
            "description": info_link.description.strip()
        }

        response = requests.post(url, json=body, headers=headers)
        return response.json()["id"]

    def _post_attraction_type(self, attraction_type:AttractionType, jwt:str) -> str:
        if self._exist(attraction_type):
            id:str = requests.get("http://localhost:8080/api/types/search?name=" + attraction_type.name, headers={"Authorization": "Bearer " + jwt}).json()[0]["id"]
            return id

        url = "http://localhost:8080/api/types"
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
    
    def _exist(self, resource:any) -> bool:
        if isinstance(resource, Segmentation):
            url = f"http://localhost:8080/api/segmentations/search?name={resource.name}"
        elif isinstance(resource, AttractionType):
            url = f"http://localhost:8080/api/types/search?name={resource.name}"
        
        response = requests.get(url)
        return len(response.json()) > 0
