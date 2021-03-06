import logging
import os

from collections import deque, namedtuple

LOGLEVEL = os.getenv('LOGLEVEL', default='CRITICAL')
logging.basicConfig(level=LOGLEVEL.upper())

Report = namedtuple('Report', ['number', 'data'])


def noop(*args, **kwargs):
    return None


class MockHidapiDevice:
    def __init__(self, vendor_id=None, product_id=None, release_number=None,
                 serial_number=None, bus=None, address=None):
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.release_numer = release_number
        self.serial_number = serial_number
        self.bus = bus
        self.address = address
        self.port = None

        self.open = noop
        self.claim = noop
        self.release = noop
        self.close = noop
        self.clear_enqueued_reports = noop

        self._read = deque()
        self.sent = list()

    def preload_read(self, report):
        self._read.append(report)

    def read(self, length):
        if self._read:
            number, data = self._read.popleft()
            if number:
                return [number] + list(data)[:length]
            else:
                return list(data)[:length]
        return None

    def write(self, data):
        data = bytes(data)  # ensure data is convertible to bytes
        self.sent.append(Report(data[0], list(data[1:])))
        return len(data) - 1
