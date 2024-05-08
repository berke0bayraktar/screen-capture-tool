import sys
from pynput import mouse, keyboard
from PIL import ImageGrab
import os

class ScreenCaptureTool:
    def __init__(self):
        self.top_left = None
        self.bottom_right = None
        self.listener = None
        self.setting_points = False

    def start(self):
        # Listen to keyboard inputs in a separate thread
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

    def on_press(self, key):
        try:
            if key.char == 'p':
                # Reset points and start setting them again
                self.top_left = None
                self.bottom_right = None
                self.setting_points = True
                print("Click two corners of the region to capture...")
                self.capture_points()
            elif key.char == 'x':
                # Take screenshot if points are set and Enter is pressed
                if self.top_left and self.bottom_right:
                    self.take_screenshot()
                else:
                    print("Please set the points first by pressing 'p'.")
        except AttributeError:
            pass

    def capture_points(self):
        # Use a mouse listener to capture two points
        def on_click(x, y, button, pressed):
            if pressed:
                if not self.top_left:
                    self.top_left = (x, y)
                    print(f"Top-left corner set at: {self.top_left}")
                else:
                    self.bottom_right = (x, y)
                    print(f"Bottom-right corner set at: {self.bottom_right}")
                    return False  # Stop listener
        
        with mouse.Listener(on_click=on_click) as listener:
            listener.join()
        self.setting_points = False

    def take_screenshot(self):
        # Take a screenshot of the specified region
        img = ImageGrab.grab(bbox=(self.top_left[0], self.top_left[1], self.bottom_right[0], self.bottom_right[1]))
        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')
        file_path = f'screenshots/screenshot_{len(os.listdir("screenshots")) + 1}.png'
        img.save(file_path)
        print(f"Screenshot saved as {file_path}")

if __name__ == '__main__':
    tool = ScreenCaptureTool()
    tool.start()
