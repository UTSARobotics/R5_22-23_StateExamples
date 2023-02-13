#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.check_condition_state import CheckConditionState
from flexbe_states.log_state import LogState
from flexbe_states.subscriber_state import SubscriberState
from flexbe_states.wait_state import WaitState
from realsense_motions_flexbe_states.publisher_data_state import PublisherUInt16State
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri Feb 10 2023
@author: jc
'''
class move_by_qrSM(Behavior):
	'''
	example
	'''


	def __init__(self):
		super(move_by_qrSM, self).__init__()
		self.name = 'move_by_qr'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['failed'])
		_state_machine.userdata.home = 0
		_state_machine.userdata.down = 180

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:62 y:33
			OperatableStateMachine.add('qr_sub',
										SubscriberState(topic="/jcCam_barcode", blocking=False, clear=False),
										transitions={'received': 'is_A', 'unavailable': 'wait'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'qr_read'})

			# x:403 y:331
			OperatableStateMachine.add('console',
										LogState(text="QR Read but not A or B.", severity=Logger.REPORT_HINT),
										transitions={'done': 'qr_sub'},
										autonomy={'done': Autonomy.Off})

			# x:607 y:73
			OperatableStateMachine.add('down_pub',
										PublisherUInt16State(topic="/servo"),
										transitions={'done': 'servo_wait'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'down'})

			# x:610 y:214
			OperatableStateMachine.add('front_pub',
										PublisherUInt16State(topic="/servo"),
										transitions={'done': 'servo_wait'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'home'})

			# x:284 y:38
			OperatableStateMachine.add('is_A',
										CheckConditionState(predicate=lambda qr_read: qr_read.data == "A"),
										transitions={'true': 'down_pub', 'false': 'Is_B'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'qr_read'})

			# x:911 y:150
			OperatableStateMachine.add('servo_wait',
										WaitState(wait_time=1),
										transitions={'done': 'qr_sub'},
										autonomy={'done': Autonomy.Off})

			# x:83 y:217
			OperatableStateMachine.add('wait',
										WaitState(wait_time=10),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:286 y:192
			OperatableStateMachine.add('Is_B',
										CheckConditionState(predicate=lambda qr_read: qr_read.data == "B"),
										transitions={'true': 'front_pub', 'false': 'console'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'qr_read'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
