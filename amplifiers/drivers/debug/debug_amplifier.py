import csv
import itertools
from pathlib import Path
from queue import Queue

import numpy as np

SAMPLES_PER_SECOND = 256


class DummyAmplfier:
    """To jest głupi wzmacniacz który nic nie robi.
    Jest tylko po to, żeby nie komplikować kodu.
    Dodatkowo nie działa z RMS"""

    def __init__(self, offset=10):
        self.strength = 8
        self.offset = offset
        self.data = Queue(maxsize=SAMPLES_PER_SECOND)
        self.signals = {}

    @staticmethod
    def _read_signal(file):
        signal = np.load(file)
        return signal

    def run(self):
        pass

    def set_strength(self, strength):
        self.strength = strength

    def get_data(self, n=SAMPLES_PER_SECOND):
        signal = []
        for _ in range(n):
            self.data.put(self.next_sample())
        for _ in range(n):
            signal.append(self.data.get())
        return signal

    def next_sample(self):
        sample = max(0, min(10, self.strength + np.random.random() - 0.5)) + self.offset
        return [sample, 0]

    def destroy(self):
        pass


class DummySignalsAmplfier:
    def __init__(self):
        self.strength = 5
        self.data = Queue(maxsize=SAMPLES_PER_SECOND)
        self.signals = {}
        self.load_signals()

    def load_signals(self):
        folder = Path(__file__).parent / "signals"
        self.signals[0] = DummySignalsAmplfier._read_signal(folder / "low.csv")
        self.signals[4.5] = DummySignalsAmplfier._read_signal(folder / "medium.csv")
        self.signals[9] = DummySignalsAmplfier._read_signal(folder / "max.csv")

    @staticmethod
    def _read_signal(file):
        signal = []
        with open(file) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                signal.append((float(row["ExG1"]), float(row["ExG2"])))
        return itertools.cycle(signal)

    def run(self):
        pass

    def set_strength(self, strength):
        self.strength = strength

    def get_data(self, n=SAMPLES_PER_SECOND):
        signal = []
        for _ in range(n):
            self.data.put(self.next_sample())
        for _ in range(n):
            signal.append(self.data.get())
        return signal

    def next_sample(self):
        idxs = np.array(list(self.signals.keys()))
        pos = np.abs(idxs - self.strength).argmin()
        return next(self.signals[idxs[pos]])

    def destroy(self):
        pass
