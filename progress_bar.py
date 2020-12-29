# Progress Bar v1.0.0 by robino16
import time


# default values
# can be changed by the application before usage
BAR_LENGTH = 30
FILL_CHAR = '█'
PAD_CHAR = ' '
CURRENT_CHAR = ''


def safely_divide(a, b):
    # avoid division by zero
    if b == 0:
        return 0
    return a / b


class ProgressBar:

    # --- interface functions ---

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
        if total_nr_of_chunks > 0:
            self.start(total_nr_of_chunks)

    def set(self, current_chunk, total_nr_of_chunks=None):
        # set a specific current chunk (usually the _i_ variable in for-loops)
        if total_nr_of_chunks is not None and not self.started:
            self.start(total_nr_of_chunks)
        self.current_chunk = current_chunk + 1
        self.show_bar()

    def jump(self, chunks_to_add=1):
        # skip ahead a certain number of chunks
        self.current_chunk += chunks_to_add
        self.show_bar()

    def next(self):
        # go to next chunk
        self.jump()

    def finish(self):
        if self.finished:
            return
        self.current_chunk = self.total_nr_of_chunks
        self.draw_bar()
        self.finished = True
        print("")

    # --- internal functions ---

    def start(self, total_nr_of_chunks):
        self.total_nr_of_chunks = total_nr_of_chunks
        self.division_factor = self.total_nr_of_chunks / self.bar_length
        self.step_size = int(self.total_nr_of_chunks / self.resolution) if self.resolution != 0 else self.step_size
        self.start_time = time.time()
        self.started = True

    def all_is_good(self):
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

    def draw_bar(self):
        nr_of_fill_chars = int(safely_divide(self.current_chunk, self.division_factor))
        nr_of_pad_chars = int(self.bar_length - nr_of_fill_chars)
        progress_percentage = safely_divide(self.current_chunk * 100, self.total_nr_of_chunks)
        bar = self.get_bar_as_string(nr_of_fill_chars, nr_of_pad_chars, progress_percentage)
        print('{}\r'.format(bar), end="")

    def show_bar(self):
        if self.all_is_good():
            self.draw_bar()

    def get_bar_as_string(self, nr_of_fill_chars, nr_of_pad_chars, percentage):
        # specify bar format here
        bar = "{0}: |".format(self.title)
        for i in range(nr_of_fill_chars):
            bar += self.fill_char
        bar += self.current_char
        for i in range(nr_of_pad_chars):
            bar += self.pad_char
        bar += "| {0}/{1} ({2}%)".format(self.current_chunk,
                                         self.total_nr_of_chunks,
                                         int(percentage))
        if self.show_time_remaining:
            bar += " ETA: {0}s".format(self.time_remaining())
        return bar

    def time_remaining(self):
        elapsed_time = time.time() - self.start_time
        remaining_chunks = self.total_nr_of_chunks - self.current_chunk
        remaining_time = remaining_chunks * (elapsed_time / max(self.current_chunk, 1))
        return round(remaining_time, 2) if remaining_time < 1 else int(remaining_time)


def demo_a():
    print("Demo A - Simple Usage")
    total_iterations = 70
    bar = ProgressBar(total_iterations)
    for i in range(total_iterations):
        time.sleep(0.01)  # do tasks here
        bar.next()
    bar.finish()


def demo_b():
    n = 10000
    print("Demo B - Update on Every n={0}th Step:".format(n))
    total_iterations = 2000000
    bar = ProgressBar(title="Progress", step_size=n)
    for i in range(total_iterations):
        # do tasks here
        bar.set(i, total_iterations)
    bar.finish()


def demo_c():
    print("Demo C - Arrow:")
    total_iterations = 100
    arrow = ProgressBar(total_iterations, title="Arrow", bar_length=50, fill_char='-', pad_char=' ', current_char='>')
    for i in range(total_iterations):
        time.sleep(0.01)  # do tasks here
        arrow.next()
    arrow.finish()


if __name__ == "__main__":
    demo_a()
    demo_b()
    demo_c()
