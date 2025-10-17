import pyxdf
import matplotlib.pyplot as plt
import numpy as np


data, header = pyxdf.load_xdf("sub-pilot_ses-S001_task-Muse_run-001_eeg.xdf") # replace file name in brackets with LabRecorder output file

for stream in data:
    y = stream['time_series']

    if isinstance(y, list):
        #list of strings, draw one vertical line for each marker
        for timestamp, marker in zip(stream['time_stamps'], y):
            plt.axvline(x=timestamp)
            print(f'Marker "{marker[0]}" @ {timestamp:.2f}s')
    elif isinstance(y, np.ndarray):
        #numeric data, draw as lines
        plt.plot(stream['time_stamps'], y)
    else:
        raise RuntimeError('Unknown stream format')

plt.show()


#================

# for stream in data:
#     name = stream['info']['name'][0]
#     y = stream['time_series']
#     t = stream['time_stamps']

#     if isinstance(y, np.ndarray):
#         t = t - t[0]  # Normalize time to start at 0
#         print(f"Plotting stream: {name}, shape: {y.shape}")

#         for i in range(y.shape[1]):  # one line per channel
#             plt.plot(t, y[:, i], label=f'Ch {i}')
#     else:
#         raise RuntimeError('Unknown stream format')

# plt.xlabel("Time (s)")
# plt.ylabel("Signal Amplitude (a.u. or µV)")
# plt.title("Numeric Stream(s) from XDF File")
# plt.legend()
# plt.tight_layout()
# plt.show()
