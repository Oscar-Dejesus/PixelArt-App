import sys
import objc
from Cocoa import NSEvent, NSApplication, NSApp
import tkinter as tk

# Your zoom functions
def zoom_in():
    print("Zoom IN")

def zoom_out():
    print("Zoom OUT")

# Handler for scroll events
def handle_scroll(event):
    dy = event.scrollingDeltaY()
    if dy > 0:
        zoom_in()
    elif dy < 0:
        zoom_out()
    return event

# Create Tkinter window
root = tk.Tk()
root.geometry("600x400")
root.title("Trackpad Zoom Test")

# Bind Cocoa scroll events
mask = 1 << 22  # NSScrollWheelMask
NSEvent.addLocalMonitorForEventsMatchingMask_handler_(mask, handle_scroll)

# Run Tkinter
root.mainloop()
