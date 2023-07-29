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

import sys
import re
from xml.etree.ElementTree import Element, SubElement, tostring
import zmq
import time
import datetime

"""
###################################################################################
class NodeManager - a facade class for NeMALA node management procedures.
###################################################################################
"""
class NodeManager:
    
    def __init__(self):
        self._result = 0
    
    def execute(self,argv):
        nodes = []
        topics = []
    
        # Check input for validity
        if (len(argv) < 4):
            print('Command too short')
            self._result = 1
        elif (len(argv) > 5):
            print('Command too long')
            self._result = 1
        else:
            op = argv[1]
            if (not self.checkOperation(op)):
                print('Unrecognized command')
                self._result = 1
            else:
                if (('terminate' == op) or ('timesync' == op)):
                    if (5 == len(argv)):
                        serviceProxyFrontEnd = argv[4]
                    else:
                        serviceProxyFrontEnd = argv[3]
                    topics = ['*']
                else:
                    serviceProxyFrontEnd = argv[4]
                    topics = re.findall(r'\b\d+\b', argv[3])
                    if not topics:
                        if argv[3] == '[*]':
                            topics = ['*']
                        else:
                            self._result = 1
    
        if (0 == self._result):
            nodes = re.findall(r'\b\d+\b', argv[2])
            if not nodes:
                if argv[2] == '[*]':
                    nodes = ['*']
                else:
                    self._result = 1
                    print('Bad node list')
    
        if (0 == self._result):
            msg = self.xmlBuilder(argv[1], nodes, topics, len(argv))
            ctx = zmq.Context()
            publisher = ctx.socket(zmq.PUB)
            publisher.connect(serviceProxyFrontEnd)
            time.sleep(1)
            publisher.send(msg)
            time.sleep(1)
            publisher.close()
            ctx.term()
        else:
            self.usage(argv[0])
            
        return self._result     

    def usage(self, executableName):
        print("usage: " + executableName + " <command> <nodes> <topics> <endpoint>")
        print("command              Either terminate, pause, resume or timesync")
        print("nodes                A list in brackets [] of all nodes affected by the command.")
        print("                     An asterisk (*) results in all nodes being affected.")
        print("topics               A list in brackets [] of all topics affected by the command.")
        print("                     An asterisk (*) results in all topics being affected.")
        print("                     The terminate and timesync commands ignore the topic list argument.")
        print("service endpoint     A string - the endpoint of service proxy front end to publish to.")
        print("Example: " + executableName + " timesync [1] ipc:///tmp/sproxy_in.ipc")

    
    def checkOperation(self, op):
        result = True
        if (op != 'pause') and (op != 'resume') and (op != 'terminate') and (op != 'timesync'):
            result = False
        return result
    
    
    def xmlBuilder(self, op, nodes, topics, len):
        root = Element('Message')
        header = SubElement(root, 'Header')
        topic = SubElement(header, 'Topic')
        topic.text = "0"
        content = SubElement(root, 'Body')
        operation = SubElement(content, 'Operation', attrib={'type':'text'})
        operation.text = op
        nodesLable = SubElement(content, 'nodes')
        for node in nodes:
            itemChild = SubElement(nodesLable, 'node')
            itemChild.text = node
        topicLable = SubElement(content, 'topics')
        for topic in topics:
            itemChild = SubElement(topicLable, 'topic')
            itemChild.text = topic
 
        timeString = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%b-%d %H:%M:%S.%f')  
        timeSt = SubElement(header, 'TimeStamp')
        timeSt.text = timeString 
        if op == 'timesync':
            timeLable = SubElement(content, 'time', attrib={'type':'text'})
            timeLable.text = timeString
        xmlString = tostring(root)
        return xmlString

###################################################################################
# Run the main function 
###################################################################################
if __name__ == '__main__':
    manager = NodeManager()
    sys.exit(manager.execute(sys.argv))
    
