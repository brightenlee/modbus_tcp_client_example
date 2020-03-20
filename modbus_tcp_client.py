#!/usr/bin/env python

"""
Software License Agreement (BSD License)

Authors : Brighten Lee <shlee@gaitech.kr / brighten0522@gmail.com>

Copyright (c) 2019, Gaitech Korea Co., Ltd.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

  1. Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.
    
  2. Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL
THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
THE POSSIBILITY OF SUCH DAMAGE.
"""

"""
pip install -U pymodbus
pip install -U pymodbus[twisted]
"""

import time
import logging
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

import rospy
import rosnode
from std_msgs.msg import Bool


class ModbusTcpNode:
    def __init__(self):
        rospy.init_node("modbus_tcp_client_node", anonymous=True)
        rospy.Subscriber("/vacuum_gripper", Bool, self.callback)

        self.UNIT = 0x01
        self.client = ModbusClient("192.168.0.150", port=502)
        self.client.connect()
        rq = self.client.write_coil(0, False)
        rospy.loginfo("Initialize Modbus Tcp Node")

    def __del__(self):
        self.client.close()

    def callback(self, data):
        if data.data == True:
            rq = self.client.write_coil(0, True)
            rr = self.client.read_coils(0, 1, unit=self.UNIT)
        else:
            rq = self.client.write_coil(0, False)
            rr = self.client.read_coils(0, 1, unit=self.UNIT)

        if not rr.bits[0] == data.data:
            rospy.logerr("Failed to send the command. Please try agian")
        else:
            rospy.loginfo("Vaccum gripper is " + ("activated" if data.data else "deactivated"))


if __name__ == "__main__":
    try:
        node = ModbusTcpNode()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
