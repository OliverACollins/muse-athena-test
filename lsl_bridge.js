let lslBaseTime = null;

export async function syncLSL() {
  try {
    const startPerf = performance.now();
    const resp = await fetch("http://localhost:5000/sync");
    const lslTime = parseFloat(await resp.text());
    const endPerf = performance.now();
    const perfMid = (startPerf + endPerf) / 2;
    lslBaseTime = lslTime - perfMid / 1000;
    console.log("LSL sync done:", lslBaseTime);
  } catch (e) {
    console.error("LSL sync failed:", e);
  }
}

export function sendMarker(value = "1") {
  if (lslBaseTime === null) {
    console.warn("LSL not synced yet");
    return;
  }
  const ts = lslBaseTime + performance.now() / 1000;
  fetch(`http://localhost:5000/marker?value=${encodeURIComponent(value)}&ts=${ts}`)
    .then(() => console.log("sent marker", value))
    .catch(err => console.error("Marker send error:", err));
}
