import tkinter as tk
import ble_triangulate

def main():
    # Function to update label values
    def update_values():
        ble_triangulate.recv_update()
        yd_line = str(int(ble_triangulate.loc.y)) + "-yard line"
        possession.set("Team A")
        line_of_scrimmage.set("50-yard line")
        current_yard_line.set(yd_line)
        first_down_marker.set("55-yard line")
        yards_to_gain.set("10 yards")
        score.set("Home: 14 - Away: 7")
        play_clock.set("25")
        game_clock.set("12:35")
        quarter.set("2nd")
        print("ble_triangulate.loc.y: {}".format(ble_triangulate.loc.y))
    

    # Create the main window
    root = tk.Tk()
    root.title("GatorBall")
    root.geometry("900x600")
    root.configure(bg="lightblue")

    # Create a canvas to represent the field
    canvas = tk.Canvas(root, width=700, height=250, bg="lightgreen", highlightthickness=0)
    canvas.place(x=50, y=50)

    # End zones
    canvas.create_rectangle(0, 0, 70, 250, fill="orange")
    canvas.create_rectangle(630, 0, 700, 250, fill="orange")

    # Add text to end zones
    canvas.create_text(35, 125, text="END ZONE", angle=90, font=("Helvetica", 8), fill="black")
    canvas.create_text(665, 125, text="END ZONE", angle=90, font=("Helvetica", 8), fill="black")

    # Lines: scrimmage (yellow), first down marker (red), and a yard line (blue)
    canvas.create_line(350, 0, 350, 250, fill="yellow", width=3)  # line of scrimmage
    canvas.create_line(450, 0, 450, 250, fill="red", width=3)     # first down marker
    canvas.create_line(400, 0, 400, 250, fill="blue", width=3)    # current yard line

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

    LOC_TKINTER = tk.StringVar()
    

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
    }

    print(type(line_of_scrimmage))

    for label_text, position in labels.items():
        label = tk.Label(root, text=label_text, font=("Helvetica", 12), bg="lightblue")
        label.place(x=position[0], y=position[1])
        
        # Dynamic value labels
        value_label = tk.Label(root, textvariable=position[2], font=("Helvetica", 12), bg="lightblue")
        value_label.place(x=position[0] + 200, y=position[1])

    # Button to simulate updating values (in a real game, this could be hooked to a live data feed)
    update_button = tk.Button(root, text="Update Values", command=update_values)
    update_button.place(x=350, y=450)

    # Run the main loop
    root.mainloop()

ble_triangulate.init()
if __name__ == "__main__":
    main()