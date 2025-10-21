# enable_lsl.py
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from mne_lsl.lsl import StreamInfo, StreamOutlet, local_clock
import threading

# ---------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------
LSL_STREAM_NAME = "jsPsychMarkers"
LSL_STREAM_TYPE = "Markers"
LSL_SOURCE_ID = "jspsych-lsl-bridge"
SERVER_HOST = "0.0.0.0"
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

desc = info.desc()
desc.append_child_value("manufacturer", "jsPsych")
channels = desc.append_child("channels")
ch = channels.append_child("channel")
ch.append_child_value("label", "JsPsychMarker")
ch.append_child_value("unit", "string")

outlet = StreamOutlet(info)

# ---------------------------------------------------------------------
# HTTP Request Handler
# ---------------------------------------------------------------------
class MarkerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        path = parsed.path

        if path == "/sync":
            # Return current LSL clock to JS
            ts = local_clock()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(str(ts).encode())

        elif path == "/marker":
            value = params.get("value", ["1"])[0]
            ts_js = params.get("ts", [None])[0]

            if ts_js is not None:
                ts = float(ts_js)
            else:
                ts = local_clock()

            outlet.push_sample([value], ts)
            print(f"→ Marker {value} @ {ts:.6f}")

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
