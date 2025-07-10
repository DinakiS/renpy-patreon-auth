init python in auth:
    from urllib.parse import urlencode, urlparse, parse_qs
    from urllib.request import urlopen, Request
    import ssl
    import certifi

    from store import webserver, OpenURL
    import json

    class OAuth2Strategy():
        def __init__(self, authorization_url, token_url, client_id, callback_url, scope):
            self.authorization_url = authorization_url
            self.token_url = token_url
            self.client_id = client_id
            self.callback_url = callback_url
            self.scope = scope

            self.on_success_callback = None
            self.on_fail_callback = None

        def run(self, on_success_callback = None, on_fail_callback = None):
            self.on_success_callback = on_success_callback
            self.on_fail_callback = on_fail_callback

            webserver.start(self)
            renpy.run(OpenURL(self.make_authorize_url()))

        def make_authorize_url(self):
            return self.authorization_url + "?client_id={client_id}&scope={scope}&redirect_uri={redirect_uri}&response_type=code".format(
                client_id=self.client_id,
                scope=self.scope,
                redirect_uri=self.redirect_uri,
            )
        
        @property
        def redirect_uri(self):
            return "http://localhost:" + str(webserver.PORT) + self.callback_url

        def handle_auth(self, request):
            parsed_path = urlparse(request.path)
            query = parse_qs(parsed_path.query)

            code = query.get("code")
            if not code:
                request.send_response(400)
                request.send_header('Content-type', 'text/html')
                request.end_headers()
                request.wfile.write(b'Failed to authenticate. You can now close this window.')

                webserver.stop()

                if self.on_fail_callback:
                    self.on_fail_callback()
                return

            code = code[0]

            tokens = self.get_tokens(code)

            request.send_response(200)
            request.send_header('Content-type', 'text/html')
            request.end_headers()
            request.wfile.write(b'Success! You can now close this window.')

            webserver.stop()

            if self.on_success_callback:
                self.on_success_callback(tokens)

        def get_tokens(self, code):
            ctx = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile=certifi.where())

            data = urlencode({
                "grant_type": "authorization_code",
                "code": code,
                "client_id": self.client_id,
                "redirect_uri": self.redirect_uri,
            }).encode("utf-8")
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            req = Request(self.token_url, data=data, headers=headers, method="POST")

            response = urlopen(req, context=ctx)

            data = response.read().decode("utf-8")
            data = json.loads(data)
            return data
