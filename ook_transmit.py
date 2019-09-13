#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Ook Transmit
# Generated: Thu Aug 29 16:10:49 2019
##################################################

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt5 import Qt, QtCore
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import osmosdr
import sys
import time
from gnuradio import qtgui


class ook_transmit(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Ook Transmit")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Ook Transmit")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "ook_transmit")

        if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
            self.restoreGeometry(self.settings.value("geometry").toByteArray())
        else:
            self.restoreGeometry(self.settings.value("geometry", type=QtCore.QByteArray))

        ##################################################
        # Variables
        ##################################################
        self.symbol_rate = symbol_rate = int (4e3)
        self.samp_rate = samp_rate = 2e6
        self.packet = packet = "0101010101222222201010101101101000101011011101111000110111101100110100011111110010110011101111000222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222010101010122222220101010110110100010101101110111100011011110110011010001111111001011001110111100022222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222201010101012222222010101011011010001010110111011110001101111011001101000111111100101100111011110002222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222220101010101222222201010101101101000101011011101111000110111101100110100011111110010110011101111000222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222"
        self.carrier_freq = carrier_freq = 433.937e6
        self.bits_per_pack = bits_per_pack = 2

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=int(samp_rate / symbol_rate),
                decimation=1,
                taps=(1, ),
                fractional_bw=None,
        )
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + '' )
        self.osmosdr_sink_0.set_sample_rate(samp_rate)
        self.osmosdr_sink_0.set_center_freq(carrier_freq, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(10, 0)
        self.osmosdr_sink_0.set_if_gain(20, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna('', 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)

        self.digital_map_bb_0 = digital.map_bb(([0x2, 0x1, 0x0]))
        self.blocks_vector_source_x_0 = blocks.vector_source_b([ int (x) for x in packet ], False, 1, [])
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(bits_per_pack)
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(int(samp_rate / symbol_rate), 1, 4000)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_float_to_complex_0, 0), (self.osmosdr_sink_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.digital_map_bb_0, 0))
        self.connect((self.digital_map_bb_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_moving_average_xx_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ook_transmit")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate
        self.blocks_moving_average_xx_0.set_length_and_scale(int(self.samp_rate / self.symbol_rate), 1)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate)
        self.blocks_moving_average_xx_0.set_length_and_scale(int(self.samp_rate / self.symbol_rate), 1)

    def get_packet(self):
        return self.packet

    def set_packet(self, packet):
        self.packet = packet
        self.blocks_vector_source_x_0.set_data([ int (x) for x in self.packet ], [])

    def get_carrier_freq(self):
        return self.carrier_freq

    def set_carrier_freq(self, carrier_freq):
        self.carrier_freq = carrier_freq
        self.osmosdr_sink_0.set_center_freq(self.carrier_freq, 0)

    def get_bits_per_pack(self):
        return self.bits_per_pack

    def set_bits_per_pack(self, bits_per_pack):
        self.bits_per_pack = bits_per_pack


def main(top_block_cls=ook_transmit, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
