import tkinter as tk
from threading import Thread
import queue
import serial
from PIL import Image, ImageTk

# Create a queue to safely pass data between threads
q = queue.Queue()

global distance
distance = 0

global current_yd_line_val
current_yd_line_val = 530

def main():
    def update_values_from_serial():
        """Update values dynamically from the queue."""
        while not q.empty():
            try:
                global distance
                distance = q.get_nowait()  # Get the next float value
                # data = 50 + distance
                yd_line = f"{distance:.3f} yards"  # Format float to 1 decimal place
                possession.set("Team A")  # Example updates
                line_of_scrimmage.set("50-yard line")
                current_yard_line.set("50-yard line")  # Use the formatted float value
                first_down_marker.set("55-yard line")
                yards_to_gain.set("10 yards")
                score.set("Home: 14 - Away: 7")
                play_clock.set("25")
                game_clock.set("12:35")
                quarter.set("2nd")
                ball_pos.set(yd_line)
            except Exception as e:
                print(f"Error updating values: {e}")

        # Re-schedule the function to check again
        root.after(100, update_values_from_serial)  # Call itself every 100ms

    def read_in_serial():
        """Read data from the serial port in a background thread."""
        try:
            ser = serial.Serial('COM10', 115200) # NOTE: CHANGE THE COM PORT TO MATCH YOUR DEVICE
            ser.timeout = 5
            print('Serial port opened')

            while True:
                if ser.in_waiting > 0:
                    data = ser.readline().decode('utf-8').strip()
                    try:
                        if float(data):
                            global distance
                            distance = float(data)  # Convert to float
                            # Convert to yards
                            distance_yd = distance * 1.093
                            distance = distance_yd
                            print(f"DISTANCE IN YARDS: {distance}")
                            q.put(distance)  # Add the float value to the queue
                    except ValueError:
                        pass  # Silently handle any issues with padding
        except Exception as e:
            print(f"Error reading serial: {e}") 

    def update_screen():
        global distance, ball_img
        
        # Load the image and keep a reference to prevent garbage collection
        ball_img = Image.open("football.png")  
        ball_img = ball_img.resize((30, 30), Image.ANTIALIAS)
        ball_img = ImageTk.PhotoImage(ball_img)

        # Clear any existing objects with tag "ball"
        canvas.delete("ball")

        # Dynamically place the ball image based on `distance`
        canvas.create_image((distance + 110) * 4.5, 150, image=ball_img, anchor=tk.CENTER, tags="ball")

        # Call this function again after 50ms
        root.after(50, update_screen)

    # Create the main window
    root = tk.Tk()
    root.title("GatorBall")
    root.geometry("900x600")
    root.configure(bg="lightblue")

    # Create a canvas to represent the field
    canvas = tk.Canvas(root, width=700, height=250, bg="lightgreen", highlightthickness=0)
    canvas.place(x=50, y=50)

    update_screen()

    gator = Image.open("gator.png")  
    gator = gator.resize((200, 150), Image.ANTIALIAS)
    gator = ImageTk.PhotoImage(gator)
    canvas.create_image(350, 120, image=gator, anchor=tk.CENTER, tags="gator")

    # End zones
    canvas.create_rectangle(0, 0, 70, 250, fill="orange")
    canvas.create_rectangle(630, 0, 700, 250, fill="orange")

    # Add text to end zones
    canvas.create_text(35, 125, text="END ZONE", angle=90, font=("Helvetica", 8), fill="black")
    canvas.create_text(665, 125, text="END ZONE", angle=90, font=("Helvetica", 8), fill="black")

    # Lines: scrimmage (yellow), first down marker (red), and a yard line (blue)
    # update blue line to reflect distances being read in from bt, change to be a dot
    # yellow line updated upon button press @ beginning of every play -> where ball is at that pt
    # @ beginning of every play yellow line and dot are in same place
    # red line @ beginning of every set of downs, it is a set distance from line of scrimmage, it is 10 yards, will need to scale
    # canvas.create_line(350, 0, 350, 250, fill="yellow", width=3)  # line of scrimmage
    # canvas.create_rectangle(50, 150, distance, 150, fill="black", width=20)

    canvas.create_line(575, 0, 575, 250, fill="red", width=3)     # first down marker
    canvas.create_line(current_yd_line_val, 0, current_yd_line_val, 250, fill="blue", width=3)    # current yard line

    # Variables to hold dynamic label values
    possession = tk.StringVar()
    line_of_scrimmage = tk.StringVar()
    current_yard_line = tk.StringVar()
    first_down_marker = tk.StringVar()
    yards_to_gain = tk.StringVar()
    score = tk.StringVar()
    play_clock = tk.StringVar()
    game_clock = tk.StringVar()
    quarter = tk.StringVar()
    ball_pos = tk.StringVar()

    # Initial values for the variables
    possession.set("N/A")
    line_of_scrimmage.set("N/A")
    current_yard_line.set("N/A")
    first_down_marker.set("N/A")
    yards_to_gain.set("N/A")
    score.set("N/A")
    play_clock.set("N/A")
    game_clock.set("N/A")
    quarter.set("N/A")
    ball_pos.set("N/A")

    # Labels for game details with dynamic values
    labels = {
        "Possession:": (50, 350, possession),
        "Line of Scrimmage:": (50, 380, line_of_scrimmage),
        "Current Yard Line:": (50, 410, current_yard_line),
        "First Down Marker:": (400, 350, first_down_marker),
        "Yards To Gain:": (400, 380, yards_to_gain),
        "Score:": (400, 410, score),
        "Play Clock:": (750, 350, play_clock),
        "Game Clock:": (750, 380, game_clock),
        "Quarter:": (750, 410, quarter),
        "Distance from anchor point: ": (50, 440, ball_pos)
    }

    for label_text, position in labels.items():
        label = tk.Label(root, text=label_text, font=("Helvetica", 12), bg="lightblue")
        label.place(x=position[0], y=position[1])

        # Dynamic value labels
        value_label = tk.Label(root, textvariable=position[2], font=("Helvetica", 12), bg="lightblue")
        value_label.place(x=position[0] + 200, y=position[1])

    # Start the background thread for reading serial data
    serial_thread = Thread(target=read_in_serial, daemon=True)
    serial_thread.start()

    # Start the update function with a delay of 5ms
    root.after(5, update_values_from_serial)

    # Run the main loop
    root.mainloop()

if __name__ == "__main__":
    main()


# FEATURES TO IMPLEMENT:
# 1). Save max distance the ball has reached. ("Forward progress")
# 2). Reflecting distance of ball on UI (can be a black dot), want ball to start on line of scrimmage, move fwd/bkwd to show it moves
# 3). NEXT SEM: Align game clock with status of ball
# 4). Fix line of scrimmage thing
