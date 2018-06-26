"""
© 2018 Jakob Rieke
"""


class Observable(object):
    def __init__(self, value, listener=None):
        if listener is None:
            listener = []
        self.value = value
        self.listener = listener

    def set(self, value):
        for listener in self.listener:
            listener(self.value, value)

        self.value = value

    def listen(self, listener):
        self.listener.append(listener)


class ObservableBool(Observable):
    def toggle(self):
        self.set(not self.value)


class ObservableString(Observable):
    pass


class ObservableNumber(Observable):
    pass
