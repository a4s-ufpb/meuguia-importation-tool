from dataclasses import dataclass
from . import Segmentation, AttractionType, MoreInfoLink

@dataclass
class Attraction:
    name: str
    city: str
    site: str
    state: str
    description: str
    image_url: str
    image_legend: str
    map_link: str
    segmentations: list[Segmentation]
    attraction_type: AttractionType
    more_info_links: list[MoreInfoLink]
    geo_latitude: str
    geo_longitude: str
    imported: bool
    import_status: str 