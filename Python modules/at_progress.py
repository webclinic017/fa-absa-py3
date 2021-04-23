import sys
from time import time

def start_stopwatch():
    start = time()
    return lambda: time() - start

class ProgressEndedError(IndexError):
    """Indicates that the progress was increased beyond the set-up size."""

class LineProgress(object):
    """A class for showing a progressbar in the log of PRIME."""
    _labels = map(str, list(range(10, 100, 10))) + ['DONE']
    _label_length = len("".join(_labels))
    _length = 80

    def __init__(self, count):
        self._count = count
        self._position = 0

        dash_count = self._length - self._label_length
        segment_dash_count = dash_count/10
        self._bar = ''

        for i in range(10):
            self._bar += '-' * segment_dash_count
            self._bar += self._labels[i]

        self._drawn_length = 0

    def inc(self):
        if self._position >= self._count:
            raise ProgressEndedError
        self._position += 1
        self.update_visual()

    def update_visual(self):
        completed = float(self._position) / self._count
        completed_length = completed * len(self._bar)
        if completed_length > self._drawn_length:
            to_draw = int(completed_length - self._drawn_length)
            target_drawn_length = self._drawn_length + to_draw

            for i in range(self._drawn_length, target_drawn_length):
                sys.stdout.write(self._bar[i])

            self._drawn_length = target_drawn_length

            if self._drawn_length == len(self._bar):
                sys.stdout.write('\n')

