import customtkinter as ctk

class AttractionDetailsFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, attraction, **kwargs):
        super().__init__(master, **kwargs)

        self.attraction_name_label = ctk.CTkLabel(self, text=f"Nome do atrativo: {attraction.name}", wraplength=260, justify='left')
        self.attraction_name_label.grid(row=0, column=0, pady=10, padx=(10, 20), sticky='w')

        self.attraction_city_label = ctk.CTkLabel(self, text=f"Cidade: {attraction.city}", wraplength=260, justify='left')
        self.attraction_city_label.grid(row=1, column=0, pady=10, padx=(10, 20), sticky='w')

        self.attraction_site_label = ctk.CTkLabel(self, text=f"Site: {attraction.site}", wraplength=260, justify='left')
        self.attraction_site_label.grid(row=2, column=0, pady=10, padx=(10, 20), sticky='w')

        self.attraction_state_label = ctk.CTkLabel(self, text=f"Estado: {attraction.state}", wraplength=260, justify='left')
        self.attraction_state_label.grid(row=3, column=0, pady=10, padx=(10, 20), sticky='w')

        self.attraction_description_label = ctk.CTkLabel(self, text=f"Descrição: {attraction.description}", wraplength=260, justify='left')
        self.attraction_description_label.grid(row=4, column=0, pady=10, padx=(10, 20), sticky='w')

        self.attraction_image_url_label = ctk.CTkLabel(self, text=f"URL da imagem: {attraction.image_url}", wraplength=260, justify='left')
        self.attraction_image_url_label.grid(row=5, column=0, pady=10, padx=(10,20), sticky='w')

        self.attraction_image_legend_label = ctk.CTkLabel(self, text=f"Legenda da imagem: {attraction.image_legend}", wraplength=260, justify='left')
        self.attraction_image_legend_label.grid(row=6, column=0, pady=10, padx=(10,20), sticky='w')

        self.attraction_map_link_label = ctk.CTkLabel(self, text=f"Link do mapa: {attraction.map_link}", wraplength=260, justify='left')
        self.attraction_map_link_label.grid(row=7, column=0, pady=10, padx=(10,20), sticky='w')

        self.attraction_segmentations_label = ctk.CTkLabel(
            self, 
            text=f"Segmentações: {', '.join(segmentation.name for segmentation in attraction.segmentations)}",
            wraplength=260,
            justify='left'
        )
        self.attraction_segmentations_label.grid(row=8, column=0, pady=10, padx=(10,20), sticky='w')

        self.attraction_type_label = ctk.CTkLabel(self, text=f"Tipo: {attraction.attraction_type.name}", wraplength=260, justify='left')
        self.attraction_type_label.grid(row=9, column=0, pady=10, padx=(10,20), sticky='w')

        self.attraction_more_info_links_label = ctk.CTkLabel(
            self, 
            text=f"Mais informações: {', '.join(link.link for link in attraction.more_info_links)}",
            wraplength=260,
            justify='left'
        )
        self.attraction_more_info_links_label.grid(row=10, column=0, pady=10, padx=(10,20), sticky='w')

        self.attraction_geo_latitude_label = ctk.CTkLabel(self, text=f"Latitude: {attraction.geo_latitude}", wraplength=260, justify='left')
        self.attraction_geo_latitude_label.grid(row=11, column=0, pady=10, padx=(10,20), sticky='w')

        self.attraction_geo_longitude_label = ctk.CTkLabel(self, text=f"Longitude: {attraction.geo_longitude}", wraplength=260, justify='left')
        self.attraction_geo_longitude_label.grid(row=12, column=0, pady=10, padx=(10,20), sticky='w')

