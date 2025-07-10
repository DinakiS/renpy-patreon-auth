init python:
    from urllib.parse import urlencode
    from urllib.request import urlopen, Request
    import json
    import ssl
    import certifi

    class PatreonClient:
        def __init__(self, access_token):
            self.access_token = access_token

        @property
        def headers(self):
            return {
                "Authorization": "Bearer " + self.access_token
            }

        @property
        def base_url(self):
            return "https://www.patreon.com/api/oauth2/v2"

        def get_user_data(self, query_params):
            query = urlencode(query_params)
            url = self.base_url + "/identity?{query}".format(query=query)
            req = Request(url, headers=self.headers)

            return self.do_request(req)

        def do_request(self, request):
            ctx = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile=certifi.where())

            response = urlopen(request, context=ctx)
            data = response.read().decode("utf-8")
            data = json.loads(data)
            return data
