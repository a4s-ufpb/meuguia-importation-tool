from .model import Segmentation, AttractionType, MoreInfoLink

class CsvObjectMapper:

    @staticmethod
    def map_segmentations(segmentations_str:str, divider:str=",") -> list[Segmentation]:
        segmentations = []
        for segmentation_str in segmentations_str.split(divider):
            segmentations.append(Segmentation(
                id=None,
                name=segmentation_str.strip(),
                description=""
            ))
        return segmentations

    @staticmethod
    def map_info_links(row:dict) -> list[MoreInfoLink]:
        info_links = []
        info_links.append(MoreInfoLink(
            id=None,
            link=row["Link Fonte 1"],
            description=row["Fonte 1 de Informações"]
        ))
        info_links.append(MoreInfoLink(
            id=None,
            link=row["Link Fonte 2"],
            description=row["Fonte 2"]
        ))
        info_links.append(MoreInfoLink(
            id=None,
            link=row["Link Fonte 3"],
            description=row["Fonte 4"]
        ))
        info_links.append(MoreInfoLink(
            id=None,
            link=row["Link fonte 4"],
            description=row["Fonte 4"]
        ))
        info_links.append(MoreInfoLink(
            id=None,
            link=row["Link 1 para mais informações:"],
            description=row["Para mais informações 1 acesse:"]
        ))
        info_links.append(MoreInfoLink(
            id=None,
            link=row["Link 2 para mais informações:"],
            description=row["Para mais informações 2 acesse:"]
        ))
        info_links.append(MoreInfoLink(
            id=None,
            link=row["Link 3 para mais informações:"],
            description=row["Para mais informações 3 acesse:"]
        ))

        return [info_link for info_link in info_links if info_link.link != ""]

    @staticmethod
    def map_attraction_type(attraction_type_str:str) -> AttractionType:
        return AttractionType(
            id=None,
            name=attraction_type_str,
            description=""
        )