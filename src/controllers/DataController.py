from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseSignal
import re
import os


class DataController(BaseController):

    
    def __init__(self):
        super().__init__()


    def validate_uploaded_file(self, file: UploadFile):

        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value

        if file.size > self.app_settings.FILE_MAX_SIZE * 1024 * 1024:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value      

        return True, ResponseSignal.FILE_VALIDATION_SUCCESS.value 

    def generate_unique_file_name(self, original_file_name: str, project_id: str):

        random_key = self.generate_rand_strings()
        project_path = ProjectController().get_project_path(project_id=project_id)

        clean_file_name = self.generate_clean_file_name(original_file_name=original_file_name)

        new_file_path = os.path.join(project_path, random_key + "_" + clean_file_name)

        while os.path.exists(new_file_path):
            random_key = self.generate_rand_strings()
            new_file_path = os.path.join(project_path, random_key + "_" + clean_file_name)
        return new_file_path    

    def generate_clean_file_name(self, original_file_name: str):

        #remove special characters except for dot, dash and underscore
        clean_file_name = re.sub(r'[^\w\.-]', '_', original_file_name)

        #replace spaces with underscores
        clean_file_name = clean_file_name.replace(' ', '_')
        return clean_file_name      