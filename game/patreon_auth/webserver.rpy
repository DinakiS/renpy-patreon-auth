init python in webserver:
    PORT = 6167

    KEEP_RUNNING = False

    import http.server
    import threading

    strategy = None

    class WebHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            global strategy

            if self.path.startswith(strategy.callback_url):
                strategy.handle_auth(self)
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'Hello, World!')

    def run(strat):
        global strategy, PORT, KEEP_RUNNING

        strategy = strat
        server = http.server.HTTPServer(('127.0.0.1', PORT), WebHandler)

        while KEEP_RUNNING:
            server.handle_request()

    def stop():
        global KEEP_RUNNING

        KEEP_RUNNING = False

    def start(strategy):
        global KEEP_RUNNING

        if KEEP_RUNNING is False:
            KEEP_RUNNING = True
            
            thread = threading.Thread(target=run, kwargs={"strat": strategy})
            thread.daemon = True
            thread.start()
