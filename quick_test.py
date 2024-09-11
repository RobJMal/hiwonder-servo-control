from hiwonder_servo_control.lewansoul_servo_bus import ServoBus
import time

servo_bus = ServoBus('/dev/ttyUSB0')

# Move servo with ID 1 to 90 degrees in 1.0 seconds
servo_1 = servo_bus.get_servo(1)
servo_2 = servo_bus.get_servo(2)

servo_1.move_time_write(0, 0)
servo_2.move_time_write(0, 0)
# time.sleep(1)
servo_1.move_time_write(180, 0)
servo_2.move_time_write(90, 0)
# time.sleep(1)
servo_1.move_time_write(0, 0)
servo_2.move_time_write(0, 0)

# time.sleep(2)

# # Move servo with ID 2 to 180 degrees in 2.0 seconds
# servo_2.move_time_write(0, 0)
# # time.sleep(2)
# servo_2.move_time_write(90, 0)
# # time.sleep(2)
# servo_2.move_time_write(0, 0)