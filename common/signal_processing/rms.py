import numpy as np

_BUF_LEN = int(np.ceil(0.1 * 512))


class RMS:
    def __init__(self, amplifier):
        self._amp = amplifier

    def get_rms(self, samples=_BUF_LEN):
        sig = np.array(self._amp.get_signal(samples))
        norm_sig = sig - sig.mean()
        rms = np.sqrt(np.sum(norm_sig * norm_sig))
        return rms
