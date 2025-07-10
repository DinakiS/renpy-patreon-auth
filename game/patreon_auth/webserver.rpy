init python in webserver:
    PORT = 6167

    KEEP_RUNNING = False

    import http.server
    import threading
    from functools import partial

    class WebHandler(http.server.BaseHTTPRequestHandler):
        def __init__(self, *args, strategy=None, **kwargs):
            self.strategy = strategy
            super().__init__(*args, **kwargs)

        def do_GET(self):
            if self.strategy and self.path.startswith(self.strategy.callback_url):
                self.strategy.handle_auth(self)
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'Hello, World!')

    def run(strategy):
        global PORT, KEEP_RUNNING

        handler_class = partial(WebHandler, strategy=strategy)
        server = http.server.HTTPServer(('127.0.0.1', PORT), handler_class)

        while KEEP_RUNNING:
            server.handle_request()

    def stop():
        global KEEP_RUNNING

        KEEP_RUNNING = False

    def start(strategy):
        global KEEP_RUNNING

        if KEEP_RUNNING is False:
            KEEP_RUNNING = True
            
            thread = threading.Thread(target=run, kwargs={"strategy": strategy})
            thread.daemon = True
            thread.start()
