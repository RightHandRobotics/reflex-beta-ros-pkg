from math import sin, pi

import rospy

from reflex_msgs.msg import Hand


def spoof_rhr_data():
    pub = rospy.Publisher('/reflex_hand', Hand, queue_size=10)
    rospy.init_node('spoof_reflex_hand', anonymous=True)
    r = rospy.Rate(50)

    hand = Hand()
    counter = 0.0
    rate_of_cycle = 40.0

    while not rospy.is_shutdown():
        sine_signal = sin(counter/rate_of_cycle)
        finger_angle = (1.4*sine_signal) + 1.4
        preshape_angle = (-(pi/4)*sine_signal)+pi/4
        if (sine_signal > 0):
            contact = True
        else:
            contact = False
        scalar = (200*sine_signal) + 200

        for i in range(3):
            hand.finger[i].proximal = finger_angle  # Proximal joints
            hand.finger[i].distal = 0.5*finger_angle  # Distal joints
            for j in range(9):
                hand.finger[i].contact[j] = contact  # Finger tactile contact
                hand.finger[i].pressure[j] = scalar  # Finger pressure scalar
        hand.palm.preshape = preshape_angle
        for i in range(6):
            hand.palm.contact[i] = contact
            hand.palm.pressure[i] = scalar

        pub.publish(hand)
        counter += 1
        r.sleep()


if __name__ == '__main__':
    try:
        spoof_rhr_data()
    except rospy.ROSInterruptException:
        pass
