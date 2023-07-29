#!/usr/bin/env python3

'''
Copyright 2023 David Dovrat

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import ParameterDescriptor

from ros_nemala import NodeManager as nm
from ros_nemala_interfaces.msg import Terminate

"""
###################################################################################
class NeMALA_Tools - a facade class for NeMALA tools.
###################################################################################
"""

class NeMALA_Tools(Node):
    def __init__(self):

        super().__init__('nemala_node_manager')

        # declare ROS paramters
        self._parameter_endpoint = self.declare_parameter(name='proxy_endpoint_publishers',
                               value="ipc:///tmp/publishers",
                               descriptor=ParameterDescriptor(description='Where to publish the service messages.')
        )

        self._manager = nm.NodeManager()

        self.terminate_subscription = self.create_subscription(
            Terminate,
            'nemala_input_terminate_dispatcher',
            self.terminate_callback,
            10)
        self.terminate_subscription  # prevent unused variable warning

    def terminate_callback(self, msg):
        self.get_logger().info('Sending a termination request to dispatcher %d.' % msg.node_id)
        argv = ["NodeManager", "terminate", '[%d]' % msg.node_id, self._parameter_endpoint.value]
        self._manager.execute(argv)

def main(args=None):
    # ros2 initialization
    rclpy.init(args=args)
    tools = NeMALA_Tools()
    # Do
    try:
        rclpy.spin(tools)
    except KeyboardInterrupt:
        pass
    # Die
    tools.destroy_node()

###################################################################################
# Run the main function
###################################################################################
if __name__ == '__main__':
    main()
