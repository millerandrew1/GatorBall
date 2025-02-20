import tkinter as tk
from threading import Thread
import queue
import serial
from PIL import Image, ImageTk
from tkinter import messagebox  
# import ble_triangulate as triangulate
import localization as lx
import math

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

# Triangulation
global P
global loc
global x
global y

def main():
    def update_values_from_serial():
        """Update values dynamically from the queue."""
        while not q.empty():
            try:
                global distance
                global loc
                global x
                global y
                global started

                distance = q.get_nowait()
                print("EXECUTING JAIODHAIUKSGHDKJWB")
                distance *= 1.093

                print(f"DISTANCE: {distance}")

                yd_line = f"{distance:.3f} yards"

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
                print(f"THIS IS {ball_pos}")

            except Exception as e:
                print(f"Error updating values: {e}")

        root.after(100, update_values_from_serial) # FIXME change back to 100?

    # ESP32 -> COM5
    # ESP3212 -> COM6
    def read_in_serial(): 
        
        """Read data from the serial port in a background thread."""
        global P
        global loc
        global x
        global y
        try:
            ser1 = serial.Serial('COM5', 115200)  # CHANGE COM PORT as needed
            ser2 = serial.Serial('COM6', 115200)
            ser1.timeout = 5
            ser2.timeout = 5
            print('Serial port opened')

            P=lx.Project(mode='2D',solver='LSE') 
            # NOTE: CHANGE ANCHOR COORDINATES BEFORE USE IF NEEDED
            a_x = int(0)
            a_y = int(0)
            b_x = int(5) # b
            b_y = int(0)

            P.add_anchor('anchor_A',(a_x,a_y))
            P.add_anchor('anchor_B',(b_x,b_y))

            t,label=P.add_target()

            while True:
                if ser1.in_waiting > 0 and ser2.in_waiting > 0:
                        a = ser1.readline().decode('utf-8').strip() # a
                        c = ser2.readline().decode('utf-8').strip() # c
                        print(f"THIS IS a: {a}")
                        print(f"THIS IS c: {c}")

                        # if a and c:
                            # try:
                            #     fa = float(a)
                            #     fc = float(c)
                            #     print(fa)
                            #     print(fc)
                            # except: 
                            #     print("cant convert a or c to float")

                        try:
                                # if fa != 0.0 and fc != 0.0:
                                    # global distance
                                    # distance = float(data)
                                    # # Convert to yards
                                    # distance_yd = distance * 1.093
                                    # distance = distance_yd
                                    # print(f"DISTANCE IN YARDS: {distance}")
                                    # q.put(distance)
                                    # triangulate.updateLoc(a,c)

                                    # arccos( (c^2) - (a^2) - (b^2)) / (-2ab)

                                    # manually do the math
                                    # a = float(a)
                                    # b_x = float(b_x)
                                    # c = float(c)
                                    # ang_theta = math.acos( ((c*c) - (a*a) - (b_x*b_x))  / (-2*a*b_x) )
                                    # print(f"THIS IS ang_theta: {ang_theta}")

                                    # new_dist_x = a * math.cos(ang_theta) * 1.093
                                    # print(f"THIS IS new_dist: {new_dist_x}")

                                t.add_measure('anchor_A',a)
                                t.add_measure('anchor_B',c)

                                P.solve()
                                loc = t.loc
                                    # global x
                                    # global y
                                    # x = float(loc.x)
                                    # y = float(loc.y)
                                    # print(f"loc: {loc}")
                                    # print(f"x: {x}")
                                    # print(f"y: {y}")    

                                    # q.put(new_dist_x)
                                q.put(loc.x)
                                    # break
                                    # now we should have the values in the queue
                        except Exception as e:
                            print(f"HAPPENING HERE: {e}")
                        # else:
                        #     print("skipping b/c a and c are invalid")
                        #     break

        except Exception as e:
            print(f"Error reading serial: {e}")

    def update_screen():
        global distance
        
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

        # Place the football on the canvas FIXME change loc.x back to distance
        global vals
        canvas.create_image((distance + 110) * 4.5, 150, image=tk_ball_img,
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
        # update_first_down(marker_val)

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
        # update_first_down(marker_val)

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

        # update_scrim(scrim_val)
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

        # update_scrim(scrim_val)
        update_first_down(marker_val)

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

    # Serial reading thread
    serial_thread = Thread(target=read_in_serial, daemon=True)
    serial_thread.start()

    # Kick off periodic updates
    root.after(5, update_values_from_serial)
    root.mainloop()

if __name__ == "__main__":
    main()

# TODO:
# 2). Sample every 20 points to produce an averaged distance 
# 3). Save previous position data for the ball and display in some menu
# START/STOP functionality for each play
# Display a few of the previous positions of the ball on the interface
#   Export positions for each play to CSV?
