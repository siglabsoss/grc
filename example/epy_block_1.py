"""
Embedded Python Blocks:

Each this file is saved, GRC will instantiate the first class it finds to get
ports and parameters of your block. The arguments to __init__  will be the
parameters. All of them are required to have default values!
"""
import numpy as np
from gnuradio import gr
import struct

def complex_to_raw(n):

    s1 = struct.pack('%df' % 1, np.real(n))
    s2 = struct.pack('%df' % 1, np.imag(n))

    return s1 + s2

class blk(gr.sync_block):
    def __init__(self, filename=''):  # only default arguments here
        gr.sync_block.__init__(
            self,
            name='Optional File Sync',
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        self.state = 0

    def work(self, input_items, output_items):
        # output_items[0][:] = input_items[0] * self.factor

        if self.state is 2:
            self.dumpfile.close()
            self.state = 3

        if self.state is 1:
            for s in output_items[0]:
                self.dumpfile.write(complex_to_raw(s))
            self.state = 2

        if self.state is 0:
            self.dumpfile = open('/mnt/overflow/work/grc/example/foo.raw', 'w')
            self.state = 1


        return len(input_items[0])
