from hiwonder_servo_control.lewansoul_servo_bus import ServoBus
import time
from typing import List, Dict, Union

servo_bus = ServoBus('/dev/ttyUSB0', baudrate=115200, discard_echo=True)
def test_servo_individual() -> None:
    """
    Test servo individually.
    """
    print("Starting Test: Testing servo individually")
    servo_1 = servo_bus.get_servo(1)
    servo_2 = servo_bus.get_servo(2)

    servo_1.move_time_write(0, 0)
    servo_2.move_time_write(0, 0)

    servo_1.move_time_write(180, 0)
    servo_2.move_time_write(90, 0)

    servo_1.move_time_write(0, 0)
    servo_2.move_time_write(0, 0)
    print("Finished Test: Testing servo individually")

def test_servo_simultaneous() -> None:
    """
    Test servo simultaneously.
    """
    print("Starting Test: Testing servo simultaneously")
    # Setting back to 0 point
    servo_bus.move_time_wait_write(1, 0, 0)
    servo_bus.move_time_wait_write(2, 0, 0)
    servo_bus.move_start(254)

    # Moving to separate positions
    servo_bus.move_time_wait_write(1, 90, 0)    # Set servo 1 to move to 45 degrees, but wait for the start command
    servo_bus.move_time_wait_write(2, 120, 0)   # Set servo 2 to move to 90 degrees, but wait for the start command
    servo_bus.move_start(254)                   # Send move_start command to both servos simultaneously (broadcast ID 254)

    # Setting back to 0 point
    servo_bus.move_time_wait_write(1, 0, 0)
    servo_bus.move_time_wait_write(2, 0, 0)
    servo_bus.move_start(254)

    print("Finished Test: Testing servo simultaneously")

if __name__ == '__main__':
    test_servo_individual()
    time.sleep(1)
    test_servo_simultaneous()