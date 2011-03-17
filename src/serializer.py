class Serializer(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self.level = 0
        self.buffers = [[]]
        self.push_buffer()

    def push_buffer(self):
        self.buffers.append([])

    def pop_buffer(self, separator = ''):
        buffer = self.buffers.pop()
        self.buffers[-1].append(separator.join(buffer))

    def start_list(self):
        self.push_buffer()

    def start_item(self):
        self.push_buffer()

    def end_item(self):
        self.pop_buffer()

    def end_list(self, separator = ', '):
        self.pop_buffer(separator)

    def emit(self, s):
        self.buffers[-1].append(s)

    def dec(self):
        self.level -= 1

    def inc(self):
        self.level += 1

    def nl(self):
        self.emit('\n' + ('\t' * self.level))

    def start(self):
        self.reset()

    def end(self):
        self.pop_buffer()
        return self.buffers[0][0]

