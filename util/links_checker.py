import requests


class LinkChecker:
    def __init__(self):
        self.valid_status_codes = range(200, 500)

    def check_link(self, link):
        response = requests.head(link)
        status_code = response.status_code
        return status_code in self.valid_status_codes
