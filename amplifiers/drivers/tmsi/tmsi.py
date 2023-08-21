import ctypes
import multiprocessing
import time
import traceback
from multiprocessing import Lock, Process
from multiprocessing.sharedctypes import Array

import numpy as np

try:
    from obci_cpp_amplifiers.amplifiers import TmsiCppAmplifier
except ImportError:
    try:
        from braitech.amplifiers.tmsi.amplifiers import TmsiCppAmplifier
    except ImportError:
        TmsiCppAmplifier = None


class TMSI:
    def __init__(self, sampling_rate=512):
        if not TmsiCppAmplifier:
            raise ValueError("Nie ma sterowników do TMSI")

        amps = TmsiCppAmplifier.get_available_amplifiers("usb")

        self.channels = (
            0,
            1,
        )  # Zmienić, jeśli kanały są inne. UWAGA python liczy od zara, a kanały są od 1!

        try:
            self.__amp = TmsiCppAmplifier(amps[0])
        except IndexError:
            raise ValueError("Wzmacniacz niepodłączony")
        self.__amp.sampling_rate = sampling_rate

        self.__gains = np.array(self.__amp.current_description.channel_gains)
        self.__offsets = np.array(self.__amp.current_description.channel_offsets)

        self.__chan1 = Array("d", np.zeros(sampling_rate * 2))
        self.__chan2 = Array("d", np.zeros(sampling_rate * 2))

        self.__lock = Lock()

        self.should_sample = multiprocessing.Value(ctypes.c_bool, True)

        self.__process = Process(target=self.__run)
        self.__process.start()

        print("Wzmacniacz działa")

    @property
    def data(self):
        return [[s1, s2] for s1, s2 in zip(self.__chan1, self.__chan2)]

    @property
    def amplifier(self):
        return self.__amp

    def __run(self):
        self.__amp.start_sampling()
        time.sleep(0.05)
        while self.should_sample.value:
            self.__get_data()

    def __get_data(self):
        number_of_samples = 64  # TODO fix magic number
        try:  # TODO
            samples = self.amplifier.get_samples(number_of_samples).samples
        except Exception:
            traceback.print_exc()
            exit()
        samples = self.samples_to_microvolts(samples)
        chan1 = samples[:, self.channels[0]]
        chan2 = samples[:, self.channels[1]]
        with self.__lock:
            self.__chan1[:-number_of_samples] = self.__chan1[number_of_samples:]
            self.__chan1[-number_of_samples:] = Array("d", chan1)

            self.__chan2[:-number_of_samples] = self.__chan2[number_of_samples:]
            self.__chan2[-number_of_samples:] = Array("d", chan2)

    def samples_to_microvolts(self, samples):
        return samples * self.__gains + self.__offsets

    @property
    def amp(self):
        return self.__amp

    def get_data(self, sample_count=128):
        max_samples_count = len(self.data)
        if sample_count is None:
            sample_count = max_samples_count
        if not (1 <= sample_count <= max_samples_count):
            # TODO warning
            sample_count = min(1, max(sample_count, max_samples_count))
        with self.__lock:
            return self.data[-sample_count:]

    def terminate(self):
        print("Zabijam wzmacniacz")
        self.should_sample.value = False
        self.__amp.stop_sampling()

    @property
    def lock(self):
        return self.__lock

    def destroy(self):
        self.terminate()
