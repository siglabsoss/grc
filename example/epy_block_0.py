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
    def __init__(self, filename_base=''):  # only default arguments here
        gr.sync_block.__init__(
            self,
            name='Optional File Sync',
            in_sig=[np.complex64,np.complex64],
            out_sig=[np.complex64]
        )
        self.enable = False
        self.state = 0
        self.base = filename_base
        self.tail = '.raw'
        self.files_written = 0
        self.write_name = ''
        self.samples_written = 0

    def get_fname(self):
        if self.base is '':
            raise ValueError('\n\n\n    Optional File Sync filename must not be empty!!!!!\n\n\n')
        name = self.base + '_' + str(self.files_written) + self.tail
        self.files_written += 1
        return name
        

    def work(self, input_items, output_items):


        if len(input_items[1]) and (np.real(input_items[1][0]) > 0.1):
            next_enable = True
        else:
            next_enable = False

        if not self.enable and next_enable:
            name = self.get_fname()
            self.write_name = name
            print 'opening ' + self.write_name
            self.dumpfile = open(self.write_name, 'w')

        if self.enable and not next_enable:
            print 'closing ' + self.write_name + ', wrote ' + str(self.samples_written) + ' samples'
            self.dumpfile.close()
            self.write_name = ''


        self.enable = next_enable

        if self.enable:
            for s in input_items[0]:
                self.dumpfile.write(complex_to_raw(s))
            self.samples_written += len(input_items[0]) 

                # print np.real(input_items[1][0])
        # print len(input_items[1])
        return len(input_items[0])

