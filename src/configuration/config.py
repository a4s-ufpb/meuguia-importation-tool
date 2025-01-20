from dataclasses import dataclass
import os
import configparser

@dataclass
class ENDPOINTS:
    api_url: str
    auth: str
    create_attraction: str
    segmentations: str
    more_info_links: str
    attraction_type: str

class ConfigReader:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigReader, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.cwd = os.getcwd()
        self.config_path = os.path.join(self.cwd, 'settings', 'config.ini')

        self.endpoints = None
        self.load()
    
    def load(self):
        if not os.path.exists(self.config_path):
            print('Config file not found', self.config_path)
            self.create_config()
        
        self.config_parser = configparser.ConfigParser()
        self.config_parser.read(self.config_path)

        self.validate_config_file(self.config_parser)

        self.endpoints = ENDPOINTS(
            self.config_parser['endpoints']['api'],
            self.config_parser['endpoints']['auth'],
            self.config_parser['endpoints']['create_attraction'],
            self.config_parser['endpoints']['segmentations'],
            self.config_parser['endpoints']['more_info_links'],
            self.config_parser['endpoints']['attraction_type']
        )
        
    def _base_config(self) -> configparser.ConfigParser:
        base_config = configparser.ConfigParser()
        base_config['endpoints'] = {
            'api': '',
            'auth': '/auth/authenticate',
            'create_attraction': '/tourists/create',
            'segmentations': '/segmentations',
            'more_info_links': '/more-info',
            'attraction_type': '/types'
        }
        return base_config

    def create_config(self):
        base_config = self._base_config()
        with open(self.config_path, 'w') as configfile:
            base_config.write(configfile)
        print("created")
    
    def validate_config_file(self, config_parser: configparser.ConfigParser):
        pass


if __name__ == "__main__":
    config = ConfigReader()
    print(config.endpoints)
