init python:
    import requests
    from urllib.parse import urlencode
    import json

    class PatreonClient:
        def __init__(self, access_token):
            self.access_token = access_token

        @property
        def headers(self):
            return {
                "Authorization": f"Bearer {self.access_token}",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            }

        @property
        def base_url(self):
            return "https://www.patreon.com/api/oauth2/v2"

        def get_user_data(self, query_params):
            query = urlencode(query_params)
            url = f"{self.base_url}/identity?{query}"
            return self.do_request(url)

        def do_request(self, url):
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                print("Patreon request error:", str(e))
                raise
