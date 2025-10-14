# enable_lsl.py
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from mne_lsl import StreamInfo, StreamOutlet
import threading

# Create an LSL outlet for markers
info = StreamInfo(name="jsPsychMarkers", stype="Markers", n_channels=1, sfreq=0, dtype="string")
outlet = StreamOutlet(info)

# Simple HTTP request handler
class MarkerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/marker":
            params = parse_qs(parsed.query)
            value = params.get("value", [""])[0]
            if value:
                print(f"Received marker: {value}")
                outlet.push_sample([value])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    server_address = ("localhost", 5000)
    httpd = HTTPServer(server_address, MarkerHandler)
    print("LSL bridge running on http://localhost:5000 ...")
    print("Waiting for markers from jsPsych...")
    httpd.serve_forever()

if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server)
    server_thread.start()