from helpers.config import get_settings, Settings
import os
import random
import string

class BaseController:
    def __init__(self):
        self.app_settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.files_dir = os.path.join(self.base_dir, "assets/files")
        self.database_dir = os.path.join(self.base_dir, "assets/database")

    def generate_rand_strings(self, length=12):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))    
        
    def get_vectordb_path(self, vectordb_name):

        vectordb_path = os.path.join(self.database_dir, vectordb_name)

        if not os.path.exists(vectordb_path):

            os.makedirs(vectordb_path)

        return vectordb_path