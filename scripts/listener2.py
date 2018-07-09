#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist, Vector3

class Drive():

	def __init__(self):
		rospy.init_node('robot')
		self.sub = rospy.Subscriber('/joy', Joy, self.callback)
		self.pub = rospy.Publisher('/RosAria/cmd_vel', Twist, queue_size=10)

		self.joy_x = .0
		self.joy_y = .0

	def callback(self, data):
		rospy.loginfo("got joy stick data")
		self.joy_x = data.axes[0]
		self.joy_y = data.axes[1]


	def set_direction(self, joy_x, joy_y):
		'''calculate robot's direction (twist)'''
		trans = joy_y*5
		ang = joy_x*5

		return Twist(Vector3(trans, 0, 0),Vector3(0, 0, ang))


	def run(self):
		r = rospy.Rate(50)
		while not rospy.is_shutdown():
			robot_direction = self.set_direction(self.joy_x, self.joy_y)
			self.pub.publish(robot_direction)
			r.sleep()

if __name__ == '__main__':
	d = Drive()
	try:
		d.run()
	except rospy.ROSInterruptException: pass
