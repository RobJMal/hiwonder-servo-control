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
        
        # Default deltas
        self.relative_servo1_delta = 5  # Default delta for servo 1
        self.relative_servo2_delta = 5  # Default delta for servo 2
        
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

        # Sliders to adjust delta for each servo
        self.relative_servo1_label = tk.Label(self.root, text="Set Delta for Servo 1")
        self.relative_servo1_label.pack()

        self.relative_servo1_slider = tk.Scale(self.root, 
                                               from_=1,  # Positive delta only
                                               to=20, 
                                               orient="horizontal", 
                                               command=self.update_deltas)
        self.relative_servo1_slider.pack()

        self.relative_servo2_label = tk.Label(self.root, text="Set Delta for Servo 2")
        self.relative_servo2_label.pack()

        self.relative_servo2_slider = tk.Scale(self.root, 
                                               from_=1,  # Positive delta only
                                               to=20, 
                                               orient="horizontal", 
                                               command=self.update_deltas)
        self.relative_servo2_slider.pack()

        # Buttons to move servos
        self.positive_button = tk.Button(self.root, text="Move Positive", command=self.move_positive)
        self.positive_button.pack()

        self.negative_button = tk.Button(self.root, text="Move Negative", command=self.move_negative)
        self.negative_button.pack()

        self.servo1_positive_servo2_negative_button = tk.Button(self.root, text="Servo 1 Positive, Servo 2 Negative", command=self.move_servo1_positive_servo2_negative)
        self.servo1_positive_servo2_negative_button.pack()

        self.servo1_negative_servo2_positive_button = tk.Button(self.root, text="Servo 1 Negative, Servo 2 Positive", command=self.move_servo1_negative_servo2_positive)
        self.servo1_negative_servo2_positive_button.pack()

    def initialize_servos(self):
        # Set both servos to 0 degrees initially
        self.servo_bus.move_time_wait_write(1, 0, 0)
        self.servo_bus.move_time_wait_write(2, 0, 0)
        self.servo_bus.move_start(254)
        self.servo1_position = 0
        self.servo2_position = 0

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

    def update_deltas(self, _=None):
        """Update the deltas based on sliders for servo1 and servo2."""
        # Update deltas for both servos
        self.relative_servo1_delta = int(self.relative_servo1_slider.get())
        self.relative_servo2_delta = int(self.relative_servo2_slider.get())

    def move_positive(self):
        """Move both servos in the positive direction."""
        # Calculate new positions by adding the delta
        new_servo1_position = self.servo1_position + self.relative_servo1_delta
        new_servo2_position = self.servo2_position + self.relative_servo2_delta

        # Constrain the positions within the servo's angle limits
        new_servo1_position = max(self.servo_angle_limit_min, min(self.servo_angle_limit_max, new_servo1_position))
        new_servo2_position = max(self.servo_angle_limit_min, min(self.servo_angle_limit_max, new_servo2_position))

        # Move both servos
        self.servo_bus.move_time_write(1, new_servo1_position, 0.2)
        self.servo_bus.move_time_write(2, new_servo2_position, 0.2)

        # Update positions
        self.servo1_position = new_servo1_position
        self.servo2_position = new_servo2_position

    def move_negative(self):
        """Move both servos in the negative direction."""
        # Calculate new positions by subtracting the delta
        new_servo1_position = self.servo1_position - self.relative_servo1_delta
        new_servo2_position = self.servo2_position - self.relative_servo2_delta

        # Constrain the positions within the servo's angle limits
        new_servo1_position = max(self.servo_angle_limit_min, min(self.servo_angle_limit_max, new_servo1_position))
        new_servo2_position = max(self.servo_angle_limit_min, min(self.servo_angle_limit_max, new_servo2_position))

        # Move both servos
        self.servo_bus.move_time_write(1, new_servo1_position, 0.2)
        self.servo_bus.move_time_write(2, new_servo2_position, 0.2)

        # Update positions
        self.servo1_position = new_servo1_position
        self.servo2_position = new_servo2_position

    def move_servo1_positive_servo2_negative(self):
        """Move Servo 1 in the positive direction and Servo 2 in the negative direction."""
        # Calculate new positions
        new_servo1_position = self.servo1_position + self.relative_servo1_delta
        new_servo2_position = self.servo2_position - self.relative_servo2_delta

        # Constrain the positions within the servo's angle limits
        new_servo1_position = max(self.servo_angle_limit_min, min(self.servo_angle_limit_max, new_servo1_position))
        new_servo2_position = max(self.servo_angle_limit_min, min(self.servo_angle_limit_max, new_servo2_position))

        # Move both servos
        self.servo_bus.move_time_write(1, new_servo1_position, 0.2)
        self.servo_bus.move_time_write(2, new_servo2_position, 0.2)

        # Update positions
        self.servo1_position = new_servo1_position
        self.servo2_position = new_servo2_position

    def move_servo1_negative_servo2_positive(self):
        """Move Servo 1 in the negative direction and Servo 2 in the positive direction."""
        # Calculate new positions
        new_servo1_position = self.servo1_position - self.relative_servo1_delta
        new_servo2_position = self.servo2_position + self.relative_servo2_delta

        # Constrain the positions within the servo's angle limits
        new_servo1_position = max(self.servo_angle_limit_min, min(self.servo_angle_limit_max, new_servo1_position))
        new_servo2_position = max(self.servo_angle_limit_min, min(self.servo_angle_limit_max, new_servo2_position))

        # Move both servos
        self.servo_bus.move_time_write(1, new_servo1_position, 0.2)
        self.servo_bus.move_time_write(2, new_servo2_position, 0.2)

        # Update positions
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
