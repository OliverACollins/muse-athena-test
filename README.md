# Muse Athena Test
Using a simple experiment, testing the Muse S Athena in terms of ERPs and face processing, as well as the synchrony between a photosensor and automated triggers in detecting trial markers for stimulus onset/cessation.

[**Test the experiment**](https://oliveracollins.github.io/muse-athena-test/)

## Step-by-step guide on testing the experiment with physiological signals

### Hardware
#### Computers involved in the setup
- **The recording machine** (used by the experimenter, with dual-monitor setup)
- **The experiment machine** (used by the participant)

#### Signal processing
- **BITalino board**
- **Lux photosensor**: tape to top-left-hand corner of the experiment machine's monitor to detect trial markers
- **ECG**: 3 electrodes - follow instructions printed out
- Potentially **EDA** at a later point?
- **Muse S Athena headband**

<br>

### Software
- **VScode**: on both machines, with both Python and Jupyter extensions installed
- **Python (ideally 3.12)**: on both machines
- **OpenSignals**: on recording machine, created for the BITalino
- **Lab Recorder (LSL)**: on recording machine

<br>

### Setting up the BITalino
- Connect Lux photosensor and ECG to the BITalino (ports A3 and Ax, respectively)
- Turn BITalino on, and establish a Bluetooth connection with the recording machine. PIN is 1234
- Connect to the BITalino through OpenSignals
- Select/modify BITalino ports on OpenSignals accordingly (e.g., set port A3 as "LUX")
- Navigate to the control panel, and over to the "Integration" tab, to ensure that OpenSignals streams to the Lab Streaming Layer (rather than merely to a separate file). Ensure that the data will be saved to the correct folder (e.g., /muse-athena-test/data/)
- Start the data acquisiton (using the red "recording" button) to view signals, ensuring they are working as expected
- Adjust the panels for each signal to the "Automatic" viewer
- Stretch the panel at the bottom of the signals for better viewing

<br>

### Setting up the Muse Athena
- Open GitHub repo folder (muse-athena-test/)
- In the terminal, install the OpenMuse package (dev branch), uninstalling any previous versions (`pip uninstall OpenMuse`): `pip install https://github.com/DominiqueMakowski/OpenMuse/zipball/dev --upgrade`
- After installing the package, in a new terminal, write: `OpenMuse find`
- Following that, in a new terminal, stream the Muse data using: `OpenMuse stream --address <your-muse-address>`, pasting in the idiosyncratic MAC address as appropriate. Presets can also be set within this terminal (e.g., `--preset 4129`), with the default being `--preset 1041`
- You can now view the Muse LSL streams through typing `OpenMuse view` in a new terminal

You can find the OpenMuse GitHub repo here: [https://github.com/DominiqueMakowski/OpenMuse](https://github.com/DominiqueMakowski/OpenMuse)

<br>

### Running the LSL Python bridge + index.html for the experiment
- Ensure both machines are connected to the same WiFi network

#### The recording machine
- In VScode, on the recording machine, in a new terminal, write `ipconfig` and locate the device's **IPv4 address**
- Then, open lsl_bridge.py in VScode from the muse-athena-test/ folder
- In lsl_bridge.py, on line 13, ensure that the script says `SERVER_HOST = "0.0.0.0"`, allowing the server to locate all potential network connections (and not merely local networks)
- Turn off the Windows firewall on the recording machine (Windows Security > Firewall and network protection > Public network)
- Ensure mne-lsl is installed on the recording machine (`pip install mne-lsl`)
- Select all code within this file, and press shift+enter to run the script

#### The experiment machine
- Now, on the experiment machine, open the GitHub repo folder in VScode (muse-athena-test/)
- Locate the **three** instances of `localhost` in the lsl_bridge.py script, adapting them so that the web address corresponds to the IPv4 address of both machines (e.g., `fetch("http://localhost:5000/sync", ...)` -> `fetch("http://173.032.2.382:5000/sync", ...)`). It is **CRUCIAL** that you include the `:5000` port addres safter the IPv4 address
- After, in a new terminal for index.html, ensure the working directory corresponds to the index script using `cd` (e.g., `cd "C:\Users\path\index.html"`)
- In a new terminal, run `python -m http.server 8000`
- In the web browser, now find [http://localhost:8000/index.html](http://localhost:8000/index.html) to open up the experiment. Now, VScode will send our markers to the shared IPv4 address!

<br>

### Setting up LabRecorder / recording the experiment
- Ensure LabRecorder is downloaded on the recording machine
- Once all streams have been set up, after pressing "Update", they ***should*** all appear on LabRecorder. Select ALL relevant streams for data acquisition
- When all relevant streams are present, and that you have double-checked that such streams are recording as expected, begin the recording by pressing "Start"
