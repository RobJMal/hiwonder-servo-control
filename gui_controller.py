import tkinter as tk
from hiwonder_servo_control.lewansoul_servo_bus import ServoBus

class ServoControllerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Servo Controller")
        
        # Initialize the ServoBus
        self.servo_bus = ServoBus('/dev/ttyUSB0', baudrate=115200, discard_echo=False)
        
        # GUI Elements
        self.create_widgets()
        
        # Initialize servos to 0 degrees
        self.initialize_servos()

    def create_widgets(self):
        # Slider for Servo 1
        self.servo1_label = tk.Label(self.root, text="Servo 1 Position")
        self.servo1_label.pack()
        
        self.servo1_slider = tk.Scale(self.root, from_=0, to=180, orient="horizontal", command=self.move_servo_1)
        self.servo1_slider.pack()

        # Slider for Servo 2
        self.servo2_label = tk.Label(self.root, text="Servo 2 Position")
        self.servo2_label.pack()

        self.servo2_slider = tk.Scale(self.root, from_=0, to=180, orient="horizontal", command=self.move_servo_2)
        self.servo2_slider.pack()

    def initialize_servos(self):
        # Set both servos to 0 degrees initially
        self.servo_bus.move_time_wait_write(1, 0, 0)
        self.servo_bus.move_time_wait_write(2, 0, 0)
        self.servo_bus.move_start(254)

    def move_servo_1(self, position):
        """Move Servo 1 based on slider value."""
        position = int(position)
        self.servo_bus.move_time_write(1, position, 0.2)  # Move servo 1 to the slider's position

    def move_servo_2(self, position):
        """Move Servo 2 based on slider value."""
        position = int(position)
        self.servo_bus.move_time_write(2, position, 0.2)  # Move servo 2 to the slider's position

def main():
    # Initialize the tkinter root window
    root = tk.Tk()
    
    # Create the ServoControllerApp instance
    app = ServoControllerApp(root)
    
    # Start the tkinter main loop
    root.mainloop()

if __name__ == '__main__':
    main()
