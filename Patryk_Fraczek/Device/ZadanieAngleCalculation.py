# -*- coding: utf-8 -*-
#
# This file is part of the ZadanieAngleCalculation project
#
# 
#
# Distributed under the terms of the LGPL license.
# See LICENSE.txt for more info.

""" Calculate angle from double_scalar

double_scalar from Tango_test to angle
"""

__all__ = ["ZadanieAngleCalculation", "main"]

# PyTango imports
import PyTango
from PyTango import DebugIt
from PyTango.server import run
from PyTango.server import Device, DeviceMeta
from PyTango.server import attribute, command
from PyTango.server import class_property, device_property
from PyTango import AttrQuality, AttrWriteType, DispLevel, DevState
# Additional import
# PROTECTED REGION ID(ZadanieAngleCalculation.additionnal_import) ENABLED START #
from numpy import arcsin
# PROTECTED REGION END #    //  ZadanieAngleCalculation.additionnal_import


class ZadanieAngleCalculation(Device):
    """
    double_scalar from Tango_test to angle
    """
    __metaclass__ = DeviceMeta
    # PROTECTED REGION ID(ZadanieAngleCalculation.class_variable) ENABLED START #
    attr_proxy = PyTango.AttributeProxy('sys/tg_test/1/double_scalar')
    value = attr_proxy.read().value
    out = attr_proxy.read().value
    # PROTECTED REGION END #    //  ZadanieAngleCalculation.class_variable
    # ----------------
    # Class Properties
    # ----------------

    # -----------------
    # Device Properties
    # -----------------

    SecondDeviceName = device_property(
        dtype='str', default_value="sys/tg_test/1/double_scalar"
    )

    # ----------
    # Attributes
    # ----------

    output = attribute(
        dtype='double',
    )

    input = attribute(
        dtype='double',
    )

    # ---------------
    # General methods
    # ---------------

    def init_device(self):
        Device.init_device(self)
        # PROTECTED REGION ID(ZadanieAngleCalculation.init_device) ENABLED START #
        self.set_state(DevState.ON)
        self.set_status("Second Order working!")
        # PROTECTED REGION END #    //  ZadanieAngleCalculation.init_device

    def always_executed_hook(self):
        # PROTECTED REGION ID(ZadanieAngleCalculation.always_executed_hook) ENABLED START #
        pass
        # PROTECTED REGION END #    //  ZadanieAngleCalculation.always_executed_hook

    def delete_device(self):
        # PROTECTED REGION ID(ZadanieAngleCalculation.delete_device) ENABLED START #
        pass
        # PROTECTED REGION END #    //  ZadanieAngleCalculation.delete_device

    # ------------------
    # Attributes methods
    # ------------------

    def read_output(self):
        # PROTECTED REGION ID(ZadanieAngleCalculation.output_read) ENABLED START #
        return self.out
        # PROTECTED REGION END #    //  ZadanieAngleCalculation.output_read

    def read_input(self):
        # PROTECTED REGION ID(ZadanieAngleCalculation.input_read) ENABLED START #
        return self.value
        # PROTECTED REGION END #    //  ZadanieAngleCalculation.input_read

    # --------
    # Commands
    # --------

    @command
    @DebugIt()
    def CalculateAngle(self):
        # PROTECTED REGION ID(ZadanieAngleCalculation.CalculateAngle) ENABLED START #
        try:
            self.out = arcsin(self.value/360)
        except Exception as e:
            self.set_state(DevState.FAULT)
            self.set_status("Exception caught in CalculateAngle:\n%s" % e)
        # PROTECTED REGION END #    //  ZadanieAngleCalculation.CalculateAngle

    @command
    @DebugIt()
    def GetInput(self):
        # PROTECTED REGION ID(ZadanieAngleCalculation.GetInput) ENABLED START #
        try:
            self.attr_proxy = PyTango.AttributeProxy('sys/tg_test/1/double_scalar')
            self.value = self.attr_proxy.read().value  # metoda read() zwraca obiekt DeviceAttribute
        except Exception as e:
            self.set_state(DevState.FAULT)
            self.set_status("Exception caught in GetInput:\n%s" % e)
        # PROTECTED REGION END #    //  ZadanieAngleCalculation.GetInput

# ----------
# Run server
# ----------


def main(args=None, **kwargs):
    from PyTango.server import run
    return run((ZadanieAngleCalculation,), args=args, **kwargs)

if __name__ == '__main__':
    main()
