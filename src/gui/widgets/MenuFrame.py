import customtkinter as ctk

from csvimporter.mgDataImporter import Attraction
from gui import PADDING_EXTRA_LARGE, PADDING_MEDIUM, PADDING_SMALL
from . import AttractionFrame

class MenuFrame(ctk.CTkFrame):
    def __init__(self, master, attractions:list[Attraction], **kwargs):
        self.current_page = 0
        self.page_size = 10
        self.attractions= attractions
        self.master = master

        super().__init__(master, **kwargs)

        text = ctk.CTkLabel(self, text='Atrações')
        text.grid(row=0, column=0, pady=(PADDING_SMALL, PADDING_MEDIUM), padx=PADDING_EXTRA_LARGE, stick='nswe')

        self.attractions_frame = ctk.CTkScrollableFrame(self, fg_color='transparent')
        self.attractions_frame.columnconfigure(0, weight=1)
        self.attractions_frame.grid(row=1, column=0, padx=PADDING_EXTRA_LARGE, pady=PADDING_MEDIUM, stick='nsew')

        nav_frame = ctk.CTkFrame(self, fg_color='transparent')
        nav_frame.columnconfigure((0, 1), weight=1)

        self.page_info_label = ctk.CTkLabel(nav_frame, text="")
        self.page_info_label.grid(row=0, column=0, columnspan=2, pady=PADDING_SMALL)

        prev_button = ctk.CTkButton(nav_frame, text='Anterior', command=self.prev_page)
        prev_button.grid(row=1, column=0, padx=PADDING_SMALL, pady=PADDING_SMALL, stick='e')
        next_button = ctk.CTkButton(nav_frame, text='Próximo', command=self.next_page)
        next_button.grid(row=1, column=1, padx=PADDING_SMALL, pady=PADDING_SMALL, stick='w')

        nav_frame.grid(row=2, column=0, pady=PADDING_SMALL, padx=PADDING_EXTRA_LARGE, stick='ns')

        self.rowconfigure((0, 2, 3), weight=0)
        self.rowconfigure(1, weight=4)
        self.columnconfigure(0, weight=1)

        self.update_attraction_list()

    def update_attraction_list(self):
        for widget in self.attractions_frame.winfo_children():
            widget.destroy()

        start_index = self.current_page * self.page_size
        end_index = start_index + self.page_size
        for i, attraction in enumerate(self.attractions[start_index:end_index]):
            attraction_index = start_index + i + 1
            attraction_frame = AttractionFrame(self.attractions_frame, attraction_index, attraction, status='✅' if attraction.imported else '❌')
            attraction_frame.grid(row=i, column=0, pady=PADDING_SMALL, padx=PADDING_SMALL, sticky='nsew')

            attraction_frame.bind("<Button-1>", lambda e, attraction=attraction: self.master.display_attraction_details(attraction))

        total_pages = (len(self.attractions) + self.page_size - 1) // self.page_size
        self.page_info_label.configure(text=f"Página {self.current_page + 1} de {total_pages}")

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_attraction_list()

    def next_page(self):
        if (self.current_page + 1) * self.page_size < len(self.attractions):
            self.current_page += 1
            self.update_attraction_list()
    
    def import_attractions(self):
        self.import_button.configure(text='importando...')
        for i, attraction in enumerate(self.attractions):
            self.attractions[i] = self.csv_importer.post_attraction(attraction, self.auth_token)

        self.import_button.configure(text='finalizado')
        self.update_attraction_list()