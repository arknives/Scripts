import tkinter as tk

# Create the window
root = tk.Tk()
root.geometry("400x400")
root.title("Workout Checklist")

# function to add a new row
def add_new_row():
    # get the last row number
    last_row = int(root.grid_size()[1])
    
    # create new widgets for the new row
    workout_entry = tk.Entry(root)
    quantity_entry = tk.Entry(root)
    complete_checkbutton = tk.Checkbutton(root, variable=tk.BooleanVar(), onvalue=True, offvalue=False)
    
    # add the widgets to the new row
    workout_entry.grid(row=last_row, column=0, sticky="EW")
    quantity_entry.grid(row=last_row, column=1, sticky="EW")
    complete_checkbutton.grid(row=last_row, column=2, sticky="EW")

# create labels for the first row
row0_column1_label = tk.Label(root, text="Workout")
row0_column1_label.grid(row=0, column=0)

row0_column2_label = tk.Label(root, text="Quantity")
row0_column2_label.grid(row=0, column=1)

row0_column3_label = tk.Label(root, text="Complete")
row0_column3_label.grid(row=0, column=2)

workout_entry = tk.Entry(root)
quantity_entry = tk.Entry(root)
complete_checkbutton = tk.Checkbutton(root, variable=tk.BooleanVar(), onvalue=True, offvalue=False)

# create a frame to hold the "Add New Row" button
button_frame = tk.Frame(root)
button_frame.grid(row=2, column=1, sticky="S")

# create "Add New Row" button inside the frame
add_button = tk.Button(button_frame, text="Add New Row", command=add_new_row)
add_button.grid(row=3, column=0, sticky="EW")

root.mainloop()
