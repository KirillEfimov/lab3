from base_client import *
import requests
import json
import datetime

class VkUser(BaseClient):
    def __init__(self, username):
        self.name = username

    BASE_URL = 'https://api.vk.com/method/'
    method = 'users.get'
    http_method = 'GET'

    # Отправка запроса к VK API
    def _get_data(self, method, http_method):
        url=self.generate_url(method)
        response = requests.get(url=url+'?user_ids='+self.name)
        return self.response_handler(response)

    def response_handler(self, response):
        js = json.loads(response.text)
        try:
            return js['response'][0]['uid']
        except:
            raise Exception('There\'s no such user')


class VkFriends(BaseClient):
    def __init__(self, user_id):
        self.id = user_id

    BASE_URL = 'https://api.vk.com/method/'
    method = 'friends.get'
    http_method = 'GET'

    # Отправка запроса к VK API
    def _get_data(self, method, http_method):
        url=self.generate_url(method)
        response = requests.get(url=url+'?user_id='+str(self.id)+'&fields=bdate')
        return self.response_handler(response)

    def response_handler(self, response):
        js = json.loads(response.text)
        dates = []
        for friend in js['response']:
            try:
                dates.append(datetime.datetime.strptime(friend['bdate'],"%d.%m.%Y").date())
            except:
                pass
        ages = [int((datetime.date.today()-date).days/365.2425) for date in dates]
        return ages




