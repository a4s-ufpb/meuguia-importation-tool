from tkinter import filedialog
import customtkinter as ctk

from csvimporter import MGDataImporter
from csvimporter.model import Attraction
from gui import PADDING_MEDIUM, PADDING_SMALL, PADDING_EXTRA_LARGE, PADDING_LARGE
from gui.widgets import AttractionDetailsFrame
from gui.widgets import MenuFrame

class CsvImporterGUI(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.title('CSV Importer')
        self.geometry('400x200')
        self.resizable(False, False)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.csv_importer = MGDataImporter()
        self.auth_token = None
        self.attraction_details_frame = None

        self.display_authentication()

    def display_authentication(self):

        self.auth_frame = ctk.CTkFrame(self, fg_color='transparent')

        user_label = ctk.CTkLabel(self.auth_frame, text='Email:')
        user_label.grid(row=1, column=0, pady=PADDING_SMALL, padx=PADDING_SMALL, sticky='e')

        user_entry = ctk.CTkEntry(self.auth_frame)
        user_entry.grid(row=1, column=1, columnspan=2, pady=PADDING_SMALL, padx=PADDING_SMALL, sticky='ew')

        password_label = ctk.CTkLabel(self.auth_frame, text='Senha:')
        password_label.grid(row=2, column=0, pady=PADDING_SMALL, padx=PADDING_SMALL, sticky='e')

        password_entry = ctk.CTkEntry(self.auth_frame, show='*')
        password_entry.grid(row=2, column=1, columnspan=2, pady=PADDING_SMALL, padx=PADDING_SMALL, sticky='ew')

        submit_button = ctk.CTkButton(self.auth_frame, text='login', command=lambda: self._login(user_entry.get(), password_entry.get()))
        submit_button.grid(row=3, column=2, pady=PADDING_SMALL, padx=PADDING_SMALL, sticky='e')

        self.auth_frame.columnconfigure(1, weight=2) 
        self.auth_frame.columnconfigure(0, weight=0) 
        self.auth_frame.rowconfigure(0, weight=0)
        self.auth_frame.rowconfigure((1,2,3), weight=1)
        self.auth_frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)

    def display_select_file(self):
        if hasattr(self, 'auth_frame'):
            for widget in self.auth_frame.winfo_children():
                widget.destroy()
            self.auth_frame.destroy()

        self.select_file_frame = ctk.CTkFrame(self, fg_color='transparent')
        import_button = ctk.CTkButton(self.select_file_frame, text='selecione um arquivo', command=self._select_file)
        self.select_file_frame.rowconfigure(0, weight=1)
        self.select_file_frame.columnconfigure(0, weight=1)
        import_button.grid(row=0, column=0, pady=PADDING_LARGE, padx=PADDING_LARGE)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.select_file_frame.grid(row=0, column=0, sticky='nsew')
    
    def display_attractions(self):
        self.resizable(True, True)
        if hasattr(self, 'select_file_frame'):
            for widget in self.select_file_frame.winfo_children():
                widget.destroy()
            self.select_file_frame.destroy()

        self.geometry('900x600')

        self.menu_frame = MenuFrame(self, self.attractions, fg_color='transparent')
        self.menu_frame.grid(row=0, column=0, sticky='nsew')

        self.import_button = ctk.CTkButton(self, text='importar', command=self._import_attractions)
        self.import_button.grid(row=1, column=0, pady=(PADDING_SMALL, PADDING_MEDIUM), padx=PADDING_EXTRA_LARGE, stick='nsew')

    def display_attraction_details(self, attraction: Attraction) -> None:
        if self.attraction_details_frame is not None:
            self.attraction_details_frame.destroy()
        
        self.attraction_details_frame = AttractionDetailsFrame(self, attraction)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=0, minsize=340)
        self.attraction_details_frame.grid(row=0, column=1, rowspan=2, padx=20, pady=20, stick='nsew')

    def _import_attractions(self):
        self.import_button.configure(text='importando...')
        for i, attraction in enumerate(self.attractions):
            self.attractions[i] = self.csv_importer.post_attraction(attraction, self.auth_token)

        self.import_button.configure(text='finalizado')
        self.menu_frame.update_attraction_list()

    def _select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[('CSV', '*.csv')])

        if file_path != '':
            self._load_attractions(file_path)
            self.display_attractions()

    def _login(self, email, password):
        try:
            self.auth_token = self.csv_importer.login(email, password)
            self.display_select_file()
        except KeyError:
            error_label = ctk.CTkLabel(self.auth_frame, text='Credenciais Invalidas', text_color='red')
            error_label.grid(row=0, column=0, columnspan=3, sticky='new')

    def _load_attractions(self, file_path):
        self.attractions: list[Attraction] = self.csv_importer.map_csv_to_objects(file_path)
        self.current_page = 0