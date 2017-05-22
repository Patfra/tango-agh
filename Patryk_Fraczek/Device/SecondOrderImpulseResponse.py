# -*- coding: utf-8 -*-
#
# This file is part of the SecondOrderImpulseResponse project
#
# 
#
# Distributed under the terms of the LGPL license.
# See LICENSE.txt for more info.

""" SecondOrder

This is a sample DS for simulating a impulse response of a second-order intertial object.
"""

__all__ = ["SecondOrderImpulseResponse", "main"]

# PyTango imports
import PyTango
from PyTango import DebugIt
from PyTango.server import run
from PyTango.server import Device, DeviceMeta
from PyTango.server import attribute, command
from PyTango.server import class_property, device_property
from PyTango import AttrQuality, AttrWriteType, DispLevel, DevState
# Additional import
# PROTECTED REGION ID(SecondOrderImpulseResponse.additionnal_import) ENABLED START #
from scipy import signal
from numpy import arange
# PROTECTED REGION END #    //  SecondOrderImpulseResponse.additionnal_import


class SecondOrderImpulseResponse(Device):
    """
    This is a sample DS for simulating a impulse response of a second-order intertial object.
    """
    __metaclass__ = DeviceMeta
    # PROTECTED REGION ID(SecondOrderImpulseResponse.class_variable) ENABLED START #
    amplification = 1.0
    time_constant_1 = 1.0
    time_constant_2 = 1.0
    output = [0.0]
    # PROTECTED REGION END #    //  SecondOrderImpulseResponse.class_variable
    # ----------------
    # Class Properties
    # ----------------

    # -----------------
    # Device Properties
    # -----------------

    TimeRange = device_property(
        dtype='str',
    )

    # ----------
    # Attributes
    # ----------

    TimeConstant_1 = attribute(
        dtype='double',
        access=AttrWriteType.READ_WRITE,
    )

    Amplification = attribute(
        dtype='double',
        access=AttrWriteType.READ_WRITE,
    )

    TimeConstant_2 = attribute(
        dtype='double',
        access=AttrWriteType.READ_WRITE,
    )

    Output = attribute(
        dtype=('double',),
        max_dim_x=10000,
    )

    # ---------------
    # General methods
    # ---------------

    def init_device(self):
        Device.init_device(self)
        # PROTECTED REGION ID(SecondOrderImpulseResponse.init_device) ENABLED START #
        self.set_state(DevState.ON)
        self.set_status("Second Order working!")
        # PROTECTED REGION END #    //  SecondOrderImpulseResponse.init_device

    def always_executed_hook(self):
        # PROTECTED REGION ID(SecondOrderImpulseResponse.always_executed_hook) ENABLED START #
        pass
        # PROTECTED REGION END #    //  SecondOrderImpulseResponse.always_executed_hook

    def delete_device(self):
        # PROTECTED REGION ID(SecondOrderImpulseResponse.delete_device) ENABLED START #
        pass
        # PROTECTED REGION END #    //  SecondOrderImpulseResponse.delete_device

    # ------------------
    # Attributes methods
    # ------------------

    def read_TimeConstant_1(self):
        # PROTECTED REGION ID(SecondOrderImpulseResponse.TimeConstant_1_read) ENABLED START #
        return self.time_constant_1
        # PROTECTED REGION END #    //  SecondOrderImpulseResponse.TimeConstant_1_read

    def write_TimeConstant_1(self, value):
        # PROTECTED REGION ID(SecondOrderImpulseResponse.TimeConstant_1_write) ENABLED START #
        self.time_constant_1=value
        # PROTECTED REGION END #    //  SecondOrderImpulseResponse.TimeConstant_1_write

    def read_Amplification(self):
        # PROTECTED REGION ID(SecondOrderImpulseResponse.Amplification_read) ENABLED START #
        return self.amplification
        # PROTECTED REGION END #    //  SecondOrderImpulseResponse.Amplification_read

    def write_Amplification(self, value):
        # PROTECTED REGION ID(SecondOrderImpulseResponse.Amplification_write) ENABLED START #
        self.amplification = value
        # PROTECTED REGION END #    //  SecondOrderImpulseResponse.Amplification_write

    def read_TimeConstant_2(self):
        # PROTECTED REGION ID(SecondOrderImpulseResponse.TimeConstant_2_read) ENABLED START #
        return self.time_constant_2
        # PROTECTED REGION END #    //  SecondOrderImpulseResponse.TimeConstant_2_read

    def write_TimeConstant_2(self, value):
        # PROTECTED REGION ID(SecondOrderImpulseResponse.TimeConstant_2_write) ENABLED START #
        self.time_constant_2 = value
        # PROTECTED REGION END #    //  SecondOrderImpulseResponse.TimeConstant_2_write

    def read_Output(self):
        # PROTECTED REGION ID(SecondOrderImpulseResponse.Output_read) ENABLED START #
        return self.output
        # PROTECTED REGION END #    //  SecondOrderImpulseResponse.Output_read

    # --------
    # Commands
    # --------

    @command
    @DebugIt()
    def CalculateResponse(self):
        # PROTECTED REGION ID(SecondOrderImpulseResponse.CalculateResponse) ENABLED START #
        try:
            h_times = arange(0.0, float(self.TimeRange), 1)
            sys = signal.lti(self.amplification, [1, self.time_constant_1, self.time_constant_2])
            impulse_response = sys.impulse(T=h_times)[1]
            self.output = impulse_response
        except Exception as e:
            self.set_state(DevState.FAULT)
            self.set_status("Exception caught in CalculateResponse:\n%s" % e)
        # PROTECTED REGION END #    //  SecondOrderImpulseResponse.CalculateResponse

# ----------
# Run server
# ----------


def main(args=None, **kwargs):
    from PyTango.server import run
    return run((SecondOrderImpulseResponse,), args=args, **kwargs)

if __name__ == '__main__':
    main()
