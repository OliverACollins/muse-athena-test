import * as lsl from "https://unpkg.com/lsl-web/dist/lsl.js";

console.log("Initialising LSL outlet...");
const outlet = await lsl.createOutlet("Markers", "Markers", 1, 0, lsl.channel_format_t.cf_string);

window.lslOutlet = outlet; // make it accessible globally
console.log("✅ LSL outlet ready");
