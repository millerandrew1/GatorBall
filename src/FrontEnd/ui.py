import tkinter as tk
from threading import Thread
import queue
import serial
from PIL import Image, ImageTk
from tkinter import messagebox  
import math
import time
import traceback
import sys
import csv
import time
from datetime import datetime

# WebSocket Imports
import asyncio
import nest_asyncio
import uvicorn 
import threading
from threading import Lock
from fastapi import FastAPI, WebSocket
import json
from pathlib import Path

# Create a queue to safely pass data between threads
q = queue.Queue()

global distance
distance = 0

global started
started = False

global scrim_is_left
global fdm_is_left

global ytg_scrim_val
global ytg_fdm_val

global current_ball_x
global current_ball_y
current_ball_x = 0
current_ball_y = 0

global position_history
position_history = []

global current_time
current_time = 0
app = FastAPI()
clients = set()

file = Path("gameStates.json")

if not file.exists():
    file.write_text("[]")

file_lock = Lock()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    try: 
        while True:
            data = {"time": current_time, "yardX": current_ball_x, "yardY": current_ball_y}
            await websocket.send_json(data)
            await asyncio.sleep(0.1)
            try:
                with file_lock:
                    # Read current content of the file
                    with file.open("r") as f:
                        try:
                            existing_data = json.load(f)
                            if not isinstance(existing_data, list):
                                existing_data = []  # Reset if the file content is not a list
                        except json.JSONDecodeError:
                            existing_data = []  # If JSON is corrupted, reset it

                    # Append new data to the list
                    existing_data.append(data)

                    # Write the updated data back to the file
                    with file.open("w") as f:
                        json.dump(existing_data, f, indent=2)

            except Exception as e:
                print(f"Error writing to JSON file: {e}")
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        clients.discard(websocket)

def start_websocket_server():
    nest_asyncio.apply()
    uvicorn.run(app, host="0.0.0.0", port=8000)
# WebSocket Imports ^^^

def main():
    def update_values_from_serial():
        """Update values dynamically from the queue."""
        while not q.empty():
            try:
                global distance
                global started
                global current_ball_x
                global current_ball_y

                ball_x, ball_y = q.get_nowait()

                ball_x *= 1.093
                ball_y *= 1.093

                print(f"DISPLAY X={ball_x}, DISPLAY Y={ball_y}")

                current_ball_x = ball_x
                current_ball_y = ball_y
                now = datetime.now()
                current_time = time.strftime("%H:%M:%S") + f".{now.microsecond // 1000:03d}"
                print(f"current_time: {current_time}")

                position_history.append((current_ball_x, current_ball_y, current_time))
                if len(position_history) > 50:
                    position_history.pop(0)

                yd_line = f"{ball_x:.3f} yards"

                # Example updates
                if not started:
                    started = True
                    possession.set("Team A")
                    line_of_scrimmage.set("50")
                    first_down_marker.set("25")
                    yards_to_gain.set("10 yards")
                    score.set("Home: 14 - Away: 7")
                    play_clock.set("25")
                    game_clock.set("12:00")
                    quarter.set("2nd")

                ball_pos.set(yd_line)

            except Exception as e:
                print(f"Error updating values: {e}")

        root.after(100, update_values_from_serial) 

    # ESP32 -> COM5
    # ESP3212 -> COM6
    def read_in_serial(): 
        
        """Read data from the serial port in a background thread."""
        try:
            ser1 = serial.Serial('COM3', 115200)  # CHANGE COM PORT as needed
            ser2 = serial.Serial('COM4', 115200)
            ser1.timeout = 3
            ser2.timeout = 3
            print('Serial port opened')

            def try_parse_float(s: str):
                # Replace null bytes and strip whitespace
                s_clean = s.replace('\x00', '').strip()
                # If empty after cleaning, return None
                if not s_clean:
                    return None
                try:
                    return float(s_clean)
                except ValueError:
                    return None

            # NOTE: CHANGE ANCHOR COORDINATES BEFORE USE IF NEEDED
            a_x = 0
            a_y = 0
            b_x = 0 
            b_y = 5 # ANCHOR B POSITION

            anchor1_buf = []
            anchor2_buf = []

            # Create lists to compute a moving average of the inputs
            ROLLING_SIZE = 1
            rolling_a = []
            rolling_c = []

            while True:
                now = time.monotonic()

                # Read from anchor 1 (ser1) if data available
                if ser1.in_waiting > 0:
                    raw_a = ser1.readline().decode('utf-8').strip()
                    a = try_parse_float(raw_a)
                    if a is not None:
                        anchor1_buf.append((now, a))  
                        print(f"A: {a:.3f} at {now:.3f}")

                # Read from anchor 1 (ser2) if data available
                if ser2.in_waiting > 0:
                    raw_c = ser2.readline().decode('utf-8').strip()
                    c = try_parse_float(raw_c)
                    if c is not None:
                        anchor2_buf.append((now, c))  
                        print(f"C: {c:.3f} at {now:.3f}")

                # Try to sync the most recent value of anchor1 with the most relevant anchor 2 value
                if anchor1_buf and anchor2_buf:
                    t1, a_val = anchor1_buf[-1]

                    best_idx = None
                    best_dt = float('inf')
                    best_c = None

                    for i, (t2, c_val) in enumerate(anchor2_buf):
                        dt = abs(t2 - t1)
                        if dt < best_dt:
                            best_dt = dt
                            best_idx = i
                            best_c = c_val

                    if best_idx is not None and best_dt < 0.2:  # max 200ms mismatch allowed
                        print(f"SYNCED: a={a_val}, c={best_c}, dt={best_dt:.3f}")

                        # Smooth the values (moving average)
                        rolling_a.append(a_val)
                        rolling_c.append(best_c)
                        if len(rolling_a) > ROLLING_SIZE:
                            rolling_a.pop(0)
                        if len(rolling_c) > ROLLING_SIZE:
                            rolling_c.pop(0)

                        a_avg = sum(rolling_a) / len(rolling_a)
                        c_avg = sum(rolling_c) / len(rolling_c)

                        # Compute the angle
                        try:
                            numerator = a_avg*a_avg + b_y*b_y - c_avg*c_avg
                            denominator = 2 * a_avg * b_y
                            ang_theta_val = numerator / denominator
                            ang_theta_val = max(-1, min(1, ang_theta_val))  # clamp

                            ang_theta = math.acos(ang_theta_val)
                            print(f"ANG_THETA: {ang_theta}")
                            # SWAPPED X AND Y FOR NEW ANCHOR ORIENTATION: FIXME
                            new_dist_y = a_avg * math.cos(ang_theta)
                            new_dist_x = a_avg * math.sin(ang_theta)

                            print(f"CALCULATED X={new_dist_x:.3f}, CALCULATED Y={new_dist_y:.3f}")
                            q.put((new_dist_x, new_dist_y))
                        except Exception as e:
                            print(f"Math error: {e}")

                        # Cleanup used data
                        pop1 = anchor1_buf.pop()  # last one used
                        pop2 = anchor2_buf = anchor2_buf[best_idx + 1:]  # drop old ones
                        print(f"POPPED {pop1} AND {pop2}")
        except Exception as e:
            tb = sys.exc_info()[2]
            lineno = tb.tb_lineno
            print(f"Error reading serial: {e} on line {lineno}")

    def update_screen():
        # global distance
        global current_ball_x
        global current_ball_y
        
        # ----------------------------------------------------------
        # 1) Load and resize the football image, convert to RGBA
        # ----------------------------------------------------------
        ball_img = Image.open("football.png")
        ball_img = ball_img.resize((30, 30))
        ball_img = ball_img.convert("RGBA")

        # ----------------------------------------------------------
        # 2) Remove the "lightgreen" background (#90EE90) -> (144,238,144)
        # ----------------------------------------------------------
        datas = ball_img.getdata()
        new_data = []
        for item in datas:
            # item is (R, G, B, A)
            if item[0] == 144 and item[1] == 238 and item[2] == 144:
                # Make this pixel fully transparent
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        ball_img.putdata(new_data)

        # Convert to PhotoImage for tkinter

        tk_ball_img = ImageTk.PhotoImage(ball_img)

        # Clear old football
        canvas.delete("ball")

        x_coord = (current_ball_x + 110) * 4.5
        # x_coord = (current_ball_x + 50) * 10
        y_coord = 150 - (current_ball_y * 4.5) #FIXME

        canvas.create_image(x_coord, y_coord, image=tk_ball_img,
                            anchor=tk.CENTER, tags="ball") 
        
        # Keep a reference to avoid garbage collection
        canvas.tk_ball_img_ref = tk_ball_img

        root.after(50, update_screen)

    # ----------------------------------------------------------------
    # Helper functions
    # ----------------------------------------------------------------
    def enable_edit():
        entry_possession.config(state="normal")
        entry_line_of_scrimmage.config(state="normal")
        entry_first_down_marker.config(state="normal")
        entry_yards_to_gain.config(state="normal")
        entry_score.config(state="normal")

    def save_edit():
        entry_possession.config(state="disabled")
        entry_line_of_scrimmage.config(state="disabled")
        entry_first_down_marker.config(state="disabled")
        entry_yards_to_gain.config(state="disabled")
        entry_score.config(state="disabled")

        # Validate the blue line (line_of_scrimmage)
        scrim_raw = line_of_scrimmage.get()
        try:
            yard_scrim_val = int(scrim_raw)
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter an integer between 0 and 50 for the line of scrimmage."
            )
            return
        if yard_scrim_val < 0 or yard_scrim_val > 50:
            messagebox.showerror(
                "Invalid Input",
                "Please enter a number from 0 to 50 for the line of scrimmage."
            )
            return

        # Validate the red line (first_down_marker)
        marker_raw = first_down_marker.get()
        try:
            yard_fdm_val = int(marker_raw)
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter an integer between 0 and 50 for the first down marker."
            )
            return
        if yard_fdm_val < 0 or yard_fdm_val > 50:
            messagebox.showerror(
                "Invalid Input",
                "Please enter a number from 0 to 50 for the first down marker."
            )
            return

        # EDGE CASE: 
        # LEFT LEFT -> normal
        # RIGHT LEFT/LEFT RIGHT -> SUBRACT 50 FROM BOTH THEN SUM
        global ytg_scrim_val
        global ytg_fdm_val
        global scrim_is_left
        global fdm_is_left

        if (scrim_is_left and fdm_is_left) or (not scrim_is_left and not fdm_is_left): # both left or both right
            yards_to_gain_val = abs(yard_scrim_val - yard_fdm_val)
        else:
            yards_to_gain_val = abs(ytg_scrim_val + ytg_fdm_val)

        yards_to_gain.set(f"{yards_to_gain_val}")
        

    def update_scrim(yard_val):
        PIXELS_PER_YARD = 5.6
        LEFT_OFFSET = 70
        RIGHT_OFFSET = 630

        global ytg_scrim_val
        ytg_scrim_val = abs(50 - yard_val)

        if endzone_side == "left":
            new_x = LEFT_OFFSET + (yard_val * PIXELS_PER_YARD)
        else: # right offset
            new_x = RIGHT_OFFSET - (yard_val * PIXELS_PER_YARD)

        canvas.coords(scrimmage_line_id, new_x, 0, new_x, 250)
        print(f"Blue line updated to yard {yard_val} at x={new_x}")

    def update_first_down(yard_val):
        PIXELS_PER_YARD = 5.6
        LEFT_OFFSET = 70
        RIGHT_OFFSET = 630

        global ytg_fdm_val
        ytg_fdm_val = abs(50 - yard_val)

        if endzone_side == "left":
            new_x = LEFT_OFFSET + (yard_val * PIXELS_PER_YARD)
        else: # right offset
            new_x = RIGHT_OFFSET - (yard_val * PIXELS_PER_YARD)

        canvas.coords(first_down_line_id, new_x, 0, new_x, 250)
        print(f"Red line updated to yard {yard_val} at x={new_x}")

    def set_left_scrim():
        nonlocal endzone_side
        endzone_side = "left"

        global scrim_is_left
        scrim_is_left = True

        try:
            scrim_val = int(line_of_scrimmage.get())
            # marker_val = int(first_down_marker.get())
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter an integer from 0 to 50 for the line of scrimmage."
            )
            return  # If invalid, just ignore
        if (scrim_val < 0) or (scrim_val > 50):
            messagebox.showerror(
                "Invalid Input",
                "Please enter a number from 0 to 50 for the line of scrimmage."
            )
            return
        
        update_scrim(scrim_val)

    def set_right_scrim():
        nonlocal endzone_side
        endzone_side = "right"

        global scrim_is_left 
        scrim_is_left = False

        try:
            scrim_val = int(line_of_scrimmage.get())
            # marker_val = int(first_down_marker.get())
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter an integer from 0 to 50 for the line of scrimmage."
            )
            return  # If invalid, just ignore
        if (scrim_val < 0) or (scrim_val > 50):
            messagebox.showerror(
                "Invalid Input",
                "Please enter a number from 0 to 50 for the line of scrimmage."
            )
            return

        update_scrim(scrim_val)

    def set_left_fdm():
        nonlocal endzone_side
        endzone_side = "left"

        global fdm_is_left
        fdm_is_left = True

        try:
            # scrim_val = int(line_of_scrimmage.get())
            marker_val = int(first_down_marker.get())
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter an integer from 0 to 50 for the first down marker."
            )
            return  # If invalid, just ignore
        if (marker_val < 0) or (marker_val > 50):
            messagebox.showerror(
                "Invalid Input",
                "Please enter an integer from 0 to 50 for the first down marker."
            )
            return

        update_first_down(marker_val)

    def set_right_fdm():
        nonlocal endzone_side
        endzone_side = "right"

        global fdm_is_left
        fdm_is_left = False
        
        try:
            # scrim_val = int(line_of_scrimmage.get())
            marker_val = int(first_down_marker.get())
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter an integer from 0 to 50 for the first down marker."
            )
            return  # If invalid, just ignore
        if (marker_val < 0) or (marker_val > 50):
            messagebox.showerror(
                "Invalid Input",
                "Please enter an integer from 0 to 50 for the first down marker."
            )
            return

        update_first_down(marker_val)

    """Check if input_string can be converted to a float"""
    def is_float(input_string):
        try:
            float(input_string)
            return True
        except ValueError:
            return False
        
    def export_history():
        global position_history
        filename = "position_log.csv"
        try:
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                # Write a header row
                writer.writerow(["Timestamp", "X (yards)", "Y (yards)"])
                # Write each position
                for (px, py, tstamp) in position_history:
                    writer.writerow([tstamp, f"{px:.3f}", f"{py:.3f}"])
            messagebox.showinfo("Export complete", f"History exported to {filename}")
        except Exception as e:
            messagebox.showerror("Export error", f"Could not export CSV: {e}")

    # ----------------------------------
    # Main GUI setup
    # ----------------------------------
    root = tk.Tk()
    root.title("GatorBall")
    root.geometry("900x580")
    root.configure(bg="lightblue")

    canvas = tk.Canvas(root, width=700, height=250, bg="lightgreen", highlightthickness=0)
    canvas.place(x=50, y=50)

    endzone_side = "left" # Default to left

    update_screen()

    # Gator image
    gator = Image.open("gator.png")
    gator = gator.resize((200, 150))
    gator = ImageTk.PhotoImage(gator)
    canvas.create_image(350, 120, image=gator, anchor=tk.CENTER, tags="gator")

    # End zones
    canvas.create_rectangle(0, 0, 70, 250, fill="orange")
    canvas.create_rectangle(630, 0, 700, 250, fill="orange")
    canvas.create_text(35, 125, text="END ZONE", angle=90, font=("Helvetica", 8), fill="black")
    canvas.create_text(665, 125, text="END ZONE", angle=90, font=("Helvetica", 8), fill="black")

    # Red line
    first_down_line_id = canvas.create_line(575, 0, 575, 250, fill="red", width=3)

    # Blue line
    scrimmage_line_id = canvas.create_line(530, 0, 530, 250, fill="blue", width=3)

    # StringVars
    possession = tk.StringVar()
    line_of_scrimmage = tk.StringVar()
    first_down_marker = tk.StringVar()
    yards_to_gain = tk.StringVar()
    score = tk.StringVar()
    play_clock = tk.StringVar()
    game_clock = tk.StringVar()
    quarter = tk.StringVar()
    ball_pos = tk.StringVar()
    ball_x_new = tk.StringVar()

    # Initial
    possession.set("N/A")
    line_of_scrimmage.set("N/A")
    first_down_marker.set("N/A")
    yards_to_gain.set("N/A")
    score.set("N/A")
    play_clock.set("N/A")
    game_clock.set("N/A")
    quarter.set("N/A")
    ball_pos.set("N/A")

    # Labels/entries
    label_possession = tk.Label(root, text="Possession:", font=("Helvetica", 12), bg="lightblue")
    label_possession.place(x=50, y=350)
    entry_possession = tk.Entry(root, textvariable=possession, font=("Helvetica", 12), state="disabled")
    entry_possession.place(x=250, y=350)

    label_line_of_scrimmage = tk.Label(root, text="Line of Scrimmage:", font=("Helvetica", 12), bg="lightblue")
    label_line_of_scrimmage.place(x=50, y=410)
    entry_line_of_scrimmage = tk.Entry(root, textvariable=line_of_scrimmage, font=("Helvetica", 12), state="disabled")
    entry_line_of_scrimmage.place(x=250, y=410)

    label_distance_anchor = tk.Label(root, text="Distance from anchor point:", font=("Helvetica", 12), bg="lightblue")
    label_distance_anchor.place(x=50, y=380)
    entry_ball_pos = tk.Entry(root, textvariable=ball_pos, font=("Helvetica", 12), state="disabled")
    entry_ball_pos.place(x=250, y=380)

    label_first_down_marker = tk.Label(root, text="First Down Marker:", font=("Helvetica", 12), bg="lightblue")
    label_first_down_marker.place(x=450, y=410)
    entry_first_down_marker = tk.Entry(root, textvariable=first_down_marker, font=("Helvetica", 12), state="disabled")
    entry_first_down_marker.place(x=600, y=410)

    label_yards_to_gain = tk.Label(root, text="Yards To Gain:", font=("Helvetica", 12), bg="lightblue")
    label_yards_to_gain.place(x=450, y=380)
    entry_yards_to_gain = tk.Entry(root, textvariable=yards_to_gain, font=("Helvetica", 12), state="disabled")
    entry_yards_to_gain.place(x=600, y=380)

    label_score = tk.Label(root, text="Score:", font=("Helvetica", 12), bg="lightblue")
    label_score.place(x=450, y=350)
    entry_score = tk.Entry(root, textvariable=score, font=("Helvetica", 12), state="disabled")
    entry_score.place(x=600, y=350)

    # Buttons
    edit_button = tk.Button(root, text="Edit", command=enable_edit, font=("Helvetica", 20))
    edit_button.place(x=370, y=500)

    save_button = tk.Button(root, text="Save", command=save_edit, font=("Helvetica", 20))
    save_button.place(x=470, y=500)

    left_button_scrim = tk.Button(root, text="Left", command=set_left_scrim, font=("Helvetica", 14))
    left_button_scrim.place(x=290, y=440)

    right_button_scrim = tk.Button(root, text="Right", command=set_right_scrim, font=("Helvetica", 14))
    right_button_scrim.place(x=350, y=440)

    left_button_fdm = tk.Button(root, text="Left", command=set_left_fdm, font=("Helvetica", 14))
    left_button_fdm.place(x=650, y=440)

    right_button_fdm = tk.Button(root, text="Right", command=set_right_fdm, font=("Helvetica", 14))
    right_button_fdm.place(x=710, y=440)

    export_button = tk.Button(root, text="Export History", command=export_history, font=("Helvetica", 14))
    export_button.place(x=180, y=500)

    # Serial reading thread
    serial_thread = Thread(target=read_in_serial, daemon=True)
    serial_thread.start()

    # Kick off periodic updates
    root.after(5, update_values_from_serial)
    root.mainloop()

if __name__ == "__main__":
    ws_thread = threading.Thread(target=start_websocket_server, daemon=True)
    ws_thread.start()

    main()

# TODO:
# 2). Sample every 20 points to produce an averaged distance 
# 3). Save previous position data for the ball and display in some menu
# START/STOP functionality for each play
# Display a few of the previous positions of the ball on the interface
#   Export positions for each play to CSV?


# Features for RC:
# 1). accuracy/responsiveness (DONE)
# 2). vertical translation of ball to detect out of bounds (IP)
# 3). history of ball position (IP)
