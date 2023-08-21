import time

import numpy as np
from scipy.signal import butter, iirnotch, lfilter, lfilter_zi

from amplifiers.drivers.debug.debug_amplifier import DummyAmplfier


class MainAmp:
    _SAMPLING_RATE = 512
    _HIGHPASS = 2
    _BANDPASS = 50

    def __init__(self, driver=None):
        driver = driver or DummyAmplfier
        self.amp = driver()
        self.update_time = time.time()

        # Filtering properties
        highpass = self._HIGHPASS / (self._SAMPLING_RATE / 2)
        self._high_b, self._high_a = butter(5, highpass, "highpass")

        Q = 30
        Fs = self._SAMPLING_RATE
        # self._notch_b, self._notch_a = iirnotch(50, Q, fs=Fs)
        self._notch_b, self._notch_a = iirnotch(50 / (Fs / 2), Q)  # gdy stary scipy

        self._high1_zl = lfilter_zi(self._high_b, self._high_a)
        self._high2_zl = lfilter_zi(self._high_b, self._high_a)
        self._notch1_zl = lfilter_zi(self._notch_b, self._notch_a)
        self._notch2_zl = lfilter_zi(self._notch_b, self._notch_a)

    def get_signal(self, n=256):
        current_update_time = time.time()
        signal = self.amp.get_data(n)
        pulled_n = len(signal)

        timestamps = np.linspace(self.update_time, current_update_time, pulled_n)
        self.update_time = current_update_time

        chan1 = [s[0] for s in signal]
        chan2 = [s[1] for s in signal]
        # Filtering
        if not isinstance(self.amp, DummyAmplfier):
            # Highpass
            chan1, self._high1_zl = lfilter(
                self._high_b, self._high_a, chan1, zi=self._high1_zl
            )
            # Notch
            chan1, self._notch1_zl = lfilter(
                self._notch_b, self._notch_a, chan1, zi=self._notch1_zl
            )

            # Highpass
            chan2, self._high2_zl = lfilter(
                self._high_b, self._high_a, chan2, zi=self._high2_zl
            )
            # Notch
            chan2, self._notch2_zl = lfilter(
                self._notch_b, self._notch_a, chan2, zi=self._notch2_zl
            )

        signal = [(t, s1 - s2) for t, s1, s2 in zip(timestamps, chan1, chan2)]

        return [s[1] for s in signal]  # zwróć tylko sample, bez czasów

    def destroy(self):
        self.amp.destroy()
