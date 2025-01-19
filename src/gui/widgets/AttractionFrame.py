import customtkinter as ctk

from csvimporter.mgDataImporter import Attraction
from gui import PADDING_SMALL, PADDING_MEDIUM

class AttractionFrame(ctk.CTkFrame):
    attraction_status_toplevel: ctk.CTkToplevel = None
    def __init__(self, master, index:int, attraction:Attraction, status:str='', **kwargs) -> None:
        super().__init__(master, **kwargs)

        self.columnconfigure((0, 3), weight=0)
        self.columnconfigure(1, weight=3)

        self.index_label = ctk.CTkLabel(self, text=index)
        self.index_label.grid(row=0, column=0, pady=PADDING_MEDIUM, padx=PADDING_MEDIUM, stick='w')

        self.name_label = ctk.CTkLabel(self, text=attraction.name)
        self.name_label.grid(row=0, column=1, pady=PADDING_MEDIUM, padx=PADDING_MEDIUM, stick='w')

        self.status_label = ctk.CTkLabel(self, text=status)
        self.status_label.bind("<Button-1>", lambda e: self.show_attraction_status(attraction))
        self.status_label.grid(row=0, column=2, pady=PADDING_MEDIUM, padx=PADDING_MEDIUM, stick='e')

    def show_attraction_status(self, attraction: Attraction):
        if self.attraction_status_toplevel is None or not self.attraction_status_toplevel.winfo_exists():
            self.attraction_status_toplevel = ctk.CTkToplevel(self)
            self.attraction_status_toplevel.title("Detalhes de importação")
            self.attraction_status_toplevel.geometry("400x400")

        for widget in self.attraction_status_toplevel.winfo_children():
            widget.destroy()

        self.attraction_status_toplevel.columnconfigure(0, weight=1)
        self.attraction_status_toplevel.rowconfigure(0, weight=0)
        self.attraction_status_toplevel.rowconfigure(1, weight=1)


        attraction_name_label = ctk.CTkLabel(self.attraction_status_toplevel, text=attraction.name, wraplength=30, justify='center', font=('Arial', 14, 'bold'))
        attraction_name_label.grid(row=0, column=0, pady=PADDING_SMALL, padx=PADDING_SMALL, stick='nsew')

        attraction_status_text = ctk.CTkLabel(self.attraction_status_toplevel, text=attraction.import_status, wraplength=360, justify='left')
        attraction_status_text.grid(row=1, column=0, pady=PADDING_SMALL, padx=PADDING_SMALL, stick='nsew')