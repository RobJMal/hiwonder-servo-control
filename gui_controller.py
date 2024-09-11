import tkinter as tk
from hiwonder_servo_control.lewansoul_servo_bus import ServoBus

class ServoControllerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Servo Controller")
        
        # Initialize the ServoBus
        self.servo_bus = ServoBus('/dev/ttyUSB0', baudrate=115200, discard_echo=False)
        
        # Track the current positions of the servos
        self.servo1_position = 0
        self.servo2_position = 0
        self.servo_angle_limit_min = 0
        self.servo_angle_limit_max = 240
        
        # Track the previous value of the relative slider
        self.previous_relative_value = 0
        
        # GUI Elements
        self.create_widgets()
        
        # Initialize servos to 0 degrees
        self.initialize_servos()

    def create_widgets(self):
        # Slider for Servo 1
        self.servo1_label = tk.Label(self.root, text="Servo 1 Position")
        self.servo1_label.pack()
        
        self.servo1_slider = tk.Scale(self.root, 
                                      from_=self.servo_angle_limit_min, 
                                      to=self.servo_angle_limit_max, 
                                      orient="horizontal", 
                                      command=self.move_servo_1)
        self.servo1_slider.pack()

        # Slider for Servo 2
        self.servo2_label = tk.Label(self.root, text="Servo 2 Position")
        self.servo2_label.pack()

        self.servo2_slider = tk.Scale(self.root, 
                                      from_=self.servo_angle_limit_min, 
                                      to=self.servo_angle_limit_max, 
                                      orient="horizontal", 
                                      command=self.move_servo_2)
        self.servo2_slider.pack()

        # Slider to adjust both servos simultaneously
        self.relative_slider_label = tk.Label(self.root, text="Move Both Servos by (Relative Movement)")
        self.relative_slider_label.pack()

        self.relative_slider = tk.Scale(self.root, 
                                        from_=-90, 
                                        to=90, 
                                        orient="horizontal", 
                                        command=self.move_both_servos)
        self.relative_slider.pack()

    def initialize_servos(self):
        # Set both servos to 0 degrees initially
        self.servo_bus.move_time_wait_write(1, 0, 0)
        self.servo_bus.move_time_wait_write(2, 0, 0)
        self.servo_bus.move_start(254)
        self.servo1_position = 0
        self.servo2_position = 0
        self.previous_relative_value = 0  # Reset the relative slider's previous value

    def move_servo_1(self, position):
        """Move Servo 1 based on slider value."""
        position = int(position)
        self.servo_bus.move_time_write(1, position, 0.2)  # Move servo 1 to the slider's position
        self.servo1_position = position  # Update the current position

    def move_servo_2(self, position):
        """Move Servo 2 based on slider value."""
        position = int(position)
        self.servo_bus.move_time_write(2, position, 0.2)  # Move servo 2 to the slider's position
        self.servo2_position = position  # Update the current position

    def move_both_servos(self, new_relative_value):
        """Move both servos by a relative amount."""
        new_relative_value = int(new_relative_value)

        # Calculate the delta (difference) between the current and previous slider value
        delta_position = new_relative_value - self.previous_relative_value

        # Update the previous slider value
        self.previous_relative_value = new_relative_value
        
        # Calculate new positions for both servos
        new_servo1_position = self.servo1_position + delta_position
        new_servo2_position = self.servo2_position + delta_position
        
        # Constrain the positions within 0-180 degrees
        new_servo1_position = max(0, min(180, new_servo1_position))
        new_servo2_position = max(0, min(180, new_servo2_position))
        
        # Move both servos to the new positions
        self.servo_bus.move_time_write(1, new_servo1_position, 0.2)
        self.servo_bus.move_time_write(2, new_servo2_position, 0.2)
        
        # Update the positions
        self.servo1_position = new_servo1_position
        self.servo2_position = new_servo2_position

def main():
    # Initialize the tkinter root window
    root = tk.Tk()
    
    # Create the ServoControllerApp instance
    app = ServoControllerApp(root)
    
    # Start the tkinter main loop
    root.mainloop()

if __name__ == '__main__':
    main()
