# enable_lsl.py
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from mne_lsl.lsl import StreamInfo, StreamOutlet, local_clock
import threading
import json

# ---------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------
LSL_STREAM_NAME = "jsPsychMarkers"
LSL_STREAM_TYPE = "Markers"
LSL_SOURCE_ID = "jspsych-lsl-bridge"
SERVER_HOST = "localhost"
SERVER_PORT = 5000
# ---------------------------------------------------------------------

# Create an LSL outlet for event markers
info = StreamInfo(
    name=LSL_STREAM_NAME,
    stype=LSL_STREAM_TYPE,
    n_channels=1,
    sfreq=0,
    dtype="string",
    source_id=LSL_SOURCE_ID,
)
outlet = StreamOutlet(info)

# ---------------------------------------------------------------------
# HTTP Request Handler
# ---------------------------------------------------------------------
class MarkerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Accepts GET requests like:
        http://localhost:5000/marker?value=stim_onset
        or http://localhost:5000/marker?value=2
        """
        parsed = urlparse(self.path)
        if parsed.path == "/marker":
            params = parse_qs(parsed.query)
            value = params.get("value", ["1"])[0]  # default marker = "1"
            ts = local_clock()

            # Allow for richer JSON-style payloads if you ever need it
            try:
                value_str = json.dumps(json.loads(value))
            except json.JSONDecodeError:
                value_str = str(value)

            print(f"→ Marker {value_str} @ {ts:.6f}")
            outlet.push_sample([value_str], ts)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

        else:
            self.send_response(404)
            self.end_headers()

# ---------------------------------------------------------------------
def run_server():
    server_address = (SERVER_HOST, SERVER_PORT)
    httpd = HTTPServer(server_address, MarkerHandler)
    print(f"\n[LSL Bridge] Serving on http://{SERVER_HOST}:{SERVER_PORT}")
    print(f"[LSL Bridge] Stream '{LSL_STREAM_NAME}' ready for LabRecorder.\n")
    httpd.serve_forever()

# ---------------------------------------------------------------------
if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server)
    server_thread.start()