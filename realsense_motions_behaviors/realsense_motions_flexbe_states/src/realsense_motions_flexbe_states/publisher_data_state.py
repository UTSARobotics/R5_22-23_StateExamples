#!/usr/bin/env python3
from flexbe_core import EventState
from flexbe_core.proxy import ProxyPublisher
from std_msgs.msg import UInt16

class PublisherUInt16State(EventState):
    '''
    Publishes a float (std_msgs/UInt16) message on a given topic name.
    -- topic	string		The topic on which should be published.
    ># value 	float				Value of float.
    <= done 					Done publishing.
    '''

    def __init__(self, topic):
        super(PublisherUInt16State, self).__init__(outcomes=['done'], input_keys=['value'])
        self._topic = topic
        self._pub = ProxyPublisher({self._topic: UInt16})

    def execute(self, userdata):
        return 'done'

    def on_enter(self, userdata):
        val = UInt16()
        val.data = userdata.value
        self._pub.publish(self._topic, val)
