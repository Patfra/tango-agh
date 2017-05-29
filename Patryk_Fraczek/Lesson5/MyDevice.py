# -*- coding: utf-8 -*-
#
# This file is part of the MyDevice project
#
# 
#
# Distributed under the terms of the GPL license.
# See LICENSE.txt for more info.

""" 

"""

__all__ = ["MyDevice", "main"]

# PyTango imports
import PyTango
from PyTango import DebugIt
from PyTango.server import run
from PyTango.server import Device, DeviceMeta
from PyTango.server import attribute, command
from PyTango.server import class_property, device_property
from PyTango import AttrQuality, AttrWriteType, DispLevel, DevState
# Additional import
# PROTECTED REGION ID(MyDevice.additionnal_import) ENABLED START #
from time import time
from PyTango import AttributeProxy
from PyTango import AttrQuality
# PROTECTED REGION END #    //  MyDevice.additionnal_import


class MyDevice(Device):
    """
    """
    __metaclass__ = DeviceMeta
    # PROTECTED REGION ID(MyDevice.class_variable) ENABLED START #
    image_maximum = 0.0
    polled_ds = 0.0
    quality_counter = 0
    quality_list= [AttrQuality.ATTR_VALID,AttrQuality.ATTR_INVALID,AttrQuality.ATTR_ALARM,AttrQuality.ATTR_CHANGING,AttrQuality.ATTR_WARNING]
    # PROTECTED REGION END #    //  MyDevice.class_variable
    # ----------------
    # Class Properties
    # ----------------

    # -----------------
    # Device Properties
    # -----------------

    DeviceToRead = device_property(
        dtype='str', default_value="sys/tg_test/1"
    )

    # ----------
    # Attributes
    # ----------

    PolledDoubleScalar = attribute(
        dtype='double',
    )

    ImagineMaximum = attribute(
        dtype='double',
    )

    # ---------------
    # General methods
    # ---------------

    def init_device(self):
        Device.init_device(self)
        # PROTECTED REGION ID(MyDevice.init_device) ENABLED START #
        self.set_state(DevState.ON)
        # PROTECTED REGION END #    //  MyDevice.init_device

    def always_executed_hook(self):
        # PROTECTED REGION ID(MyDevice.always_executed_hook) ENABLED START #
        pass
        # PROTECTED REGION END #    //  MyDevice.always_executed_hook

    def delete_device(self):
        # PROTECTED REGION ID(MyDevice.delete_device) ENABLED START #
        pass
        # PROTECTED REGION END #    //  MyDevice.delete_device

    # ------------------
    # Attributes methods
    # ------------------

    def read_PolledDoubleScalar(self):
        # PROTECTED REGION ID(MyDevice.PolledDoubleScalar_read) ENABLED START #
        attr_proxy = PyTango.AttributeProxy(self.DeviceToRead+'/double_scalar')
        self.polled_ds = attr_proxy.read().value
        self.debug_stream(str(self.polled_ds))
        return self.polled_ds
        # PROTECTED REGION END #    //  MyDevice.PolledDoubleScalar_read

    def read_ImagineMaximum(self):
        # PROTECTED REGION ID(MyDevice.ImagineMaximum_read) ENABLED START #
        attr_proxy = PyTango.AttributeProxy(self.DeviceToRead+'/double_image_ro')
        value = attr_proxy.read().value
        maximums = []
        for row in value:
            maximums.append(max(row))
        self.image_maximum = max(maximums)
        attr_quality = AttrQuality.ATTR_VALID
        self.push_change_event("ImagineMaximum", self.image_maximum , time(), attr_quality)
        self.push_archive_event("ImagineMaximum", self.image_maximum , time(), attr_quality)
        if (self.image_maximum < 20):
            self.set_state(DevState.OFF)
        else:
            if (self.image_maximum < 30):
                self.set_state(DevState.WARNING)
            else:
                self.set_state(DevState.ON)

        return float(self.image_maximum), time(), attr_quality
        # PROTECTED REGION END #    //  MyDevice.ImagineMaximum_read

    # --------
    # Commands
    # --------

    @command
    @DebugIt()
    def ChangeDoubleScalarQuality(self):
        # PROTECTED REGION ID(MyDevice.ChangeDoubleScalarQuality) ENABLED START #
        self.quality_counter=(self.quality_counter+1)%5
        self.PolledDoubleScalar.set_quality(self.quality_list[self.quality_counter])
        # PROTECTED REGION END #    //  MyDevice.ChangeDoubleScalarQuality

# ----------
# Run server
# ----------


def main(args=None, **kwargs):
    from PyTango.server import run
    return run((MyDevice,), args=args, **kwargs)

if __name__ == '__main__':
    main()
