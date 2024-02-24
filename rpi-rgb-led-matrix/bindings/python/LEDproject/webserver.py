from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib

class SpotifyCallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Authorization successful. You can close this window.")
        
        # Parse the query string to get the code
        query_string = urllib.parse.urlparse(self.path).query
        query_components = urllib.parse.parse_qs(query_string)
        if 'code' in query_components:
            print("Authorization code:", query_components['code'][0])
        else:
            print("No code found in the callback URL.")

def run(server_class=HTTPServer, handler_class=SpotifyCallbackHandler, port=8888):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()