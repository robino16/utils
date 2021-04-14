import time

BAR_LENGTH = 30
FILL_CHAR = '-'
PAD_CHAR = ' '
CURRENT_CHAR = '>'
BRACKET_LEFT = ':'
BRACKET_RIGHT = ':'


def safely_divide(a, b):
    # avoid division by zero
    if b == 0:
        return 0
    return a / b


class ProgressBar:
    def __init__(self, total_nr_of_chunks=0, title="Progress", bar_length=BAR_LENGTH, fill_char=FILL_CHAR,
                 pad_char=PAD_CHAR, current_char=CURRENT_CHAR, resolution=0, step_size=1, show_time_remaining=True):
        self.title = title
        self.current_chunk = 0  # chunk, aka. iteration / epoch
        self.bar_length = bar_length
        self.fill_char = fill_char
        self.pad_char = pad_char
        self.current_char = current_char
        self.step_size = step_size
        self.resolution = resolution
        self.division_factor = 0
        self.started = False
        self.finished = False
        self.total_nr_of_chunks = 0
        self.start_time = None
        self.show_time_remaining = show_time_remaining
        self.info = ''
        if total_nr_of_chunks > 0:
            self._start(total_nr_of_chunks)

    def set(self, current_chunk, info='', total_nr_of_chunks=None):
        # set a specific current chunk (usually the _i_ variable in for-loops)
        if total_nr_of_chunks is not None and not self.started:
            self._start(total_nr_of_chunks)
        self.current_chunk = current_chunk + 1
        if info != '':
            self.info = info
        self._show_bar()

    def jump(self, chunks_to_add=1, info=''):
        # skip ahead a certain number of chunks
        self.info = info
        self.current_chunk += chunks_to_add
        self._show_bar()

    def next(self, info=''):
        # go to next chunk
        self.info = info
        self.jump()

    def finish(self):
        if self.finished:
            return
        self.current_chunk = self.total_nr_of_chunks
        self._draw_bar()
        self.finished = True
        print("")

    def _start(self, total_nr_of_chunks):
        self.total_nr_of_chunks = total_nr_of_chunks
        self.division_factor = self.total_nr_of_chunks / self.bar_length
        self.step_size = int(self.total_nr_of_chunks / self.resolution) if self.resolution != 0 else self.step_size
        self.start_time = time.time()
        self.started = True
        self._show_bar()

    def _all_is_good(self):
        if self.finished:
            return False
        elif not self.started:
            print("Failed to show progress bar. Please specify parameter: 'total_nr_of_chunks'.")
            self.finished = True
            return False
        elif self.current_chunk % self.step_size != 0:
            return False
        if self.current_chunk >= self.total_nr_of_chunks:
            self.finish()
            return False
        return True

    def _draw_bar(self):
        nr_of_fill_chars = int(safely_divide(self.current_chunk, self.division_factor))
        nr_of_pad_chars = int(self.bar_length - nr_of_fill_chars)
        progress_percentage = safely_divide(self.current_chunk * 100, self.total_nr_of_chunks)
        bar = self._get_bar_as_string(nr_of_fill_chars, nr_of_pad_chars, progress_percentage)
        print('\r{0} {1}'.format(bar, self.info), end="")

    def _show_bar(self):
        if self._all_is_good():
            self._draw_bar()

    def _get_bar_as_string(self, nr_of_fill_chars, nr_of_pad_chars, percentage):
        # specify bar format here
        bar = "{0}: {1}".format(self.title, BRACKET_LEFT)
        for i in range(nr_of_fill_chars):
            bar += self.fill_char
        bar += self.current_char
        for i in range(nr_of_pad_chars):
            bar += self.pad_char
        bar += "{0} {1}/{2} ({3}%)".format(BRACKET_RIGHT,
                                           self.current_chunk,
                                           self.total_nr_of_chunks,
                                           int(percentage))
        if self.show_time_remaining:
            if self.finished:
                bar += "Finished"
            else:
                bar += " ETA: {0}s".format(self._time_remaining())
        return bar

    def _time_remaining(self):
        elapsed_time = time.time() - self.start_time
        remaining_chunks = self.total_nr_of_chunks - self.current_chunk
        remaining_time = remaining_chunks * (elapsed_time / max(self.current_chunk, 1))
        return round(remaining_time, 2) if remaining_time < 1 else int(remaining_time)
