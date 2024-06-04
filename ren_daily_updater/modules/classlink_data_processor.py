import json
import pandas as pd
from modules.oneroster import OneRoster

class ClasslinkDataProcessor:
    def __init__(self, api_key, api_secret):
        self.oneroster_connection = OneRoster(api_key, api_secret)
    def _get_data(self, url):
        result = self.oneroster_connection.make_roster_request(url)
        return json.loads(result['response'])

    def get_user_data(self, data_urls):
        user_data_frames = []
        for url in data_urls:
            user_data_json = self._get_data(url)
            user_data_frames.append(pd.DataFrame(user_data_json['users']))
        df_data = pd.concat(user_data_frames)
        df_data.reset_index(drop=True, inplace=True)
        try:
            df_data = df_data.join(pd.json_normalize(df_data['metadata']).add_prefix('metadata.'))
            df_data = df_data.join(pd.json_normalize(df_data['orgs']).drop(\
                [1,2,3,4,5,6], axis='columns'))
            df_data = df_data.join(pd.json_normalize(df_data[0]).add_prefix('org.'))
            return df_data
        except KeyError:
            return df_data
    
    def get_demographic_data(self, data_urls):
        demographic_data_frames = []
        for url in data_urls:
            demographic_data_json = self._get_data(url)
            demographic_data_frames.append(pd.DataFrame(demographic_data_json['demographics']))
        df_data = pd.concat(demographic_data_frames)
        df_data.reset_index(drop=True, inplace=True)
        try:
            df_data = df_data.join(pd.json_normalize(df_data['metadata']))
            return df_data
        except KeyError:
            return df_data
    
    def get_class_data(self, data_urls):
        class_data_frames = []
        for url in data_urls:
            class_data_json = self._get_data(url)
            class_data_frames.append(pd.DataFrame(class_data_json['classes']))
        df_data = pd.concat(class_data_frames)
        df_data.reset_index(drop=True, inplace=True)
        try:
            df_data = df_data.join(pd.json_normalize(df_data['school']).add_prefix('school.'))
            df_data = df_data.join(pd.json_normalize(df_data['course']).add_prefix('course.'))
            return df_data
        except KeyError:
            return df_data
    
    def get_enrollment_data(self, data_urls):
        enrollment_data_frames = []
        for url in data_urls:
            enrollment_data_json = self._get_data(url)
            enrollment_data_frames.append(pd.DataFrame(enrollment_data_json['enrollments']))
        df_data = pd.concat(enrollment_data_frames)
        df_data.reset_index(drop=True, inplace=True)
        try:
            df_data = df_data.join(pd.json_normalize(df_data['user']).add_prefix('user.'))
            df_data = df_data.join(pd.json_normalize(df_data['school']).add_prefix('school.'))
            df_data = df_data.join(pd.json_normalize(df_data['class']).add_prefix('class.'))
            return df_data
        except KeyError:
            return df_data
        
    def generate_api_url_list(self, base_url, total_records=10000, limit=10000):
        num_of_urls = -(-total_records // limit)
        api_url_list = []
        for url_count in range(num_of_urls):
            offset = url_count * limit
            api_url = f"{base_url}limit={limit}&offset={offset}"
            api_url_list.append(api_url)
        return api_url_list