import tkinter as tk
from tkinter import filedialog

def open_file_dialog():
    # Access the file_path_string variable defined in the global scope
    global file_path_string
    file_path = filedialog.askopenfilename(initialdir="~/Desktop", title="Select a file", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    file_path_string = file_path  # Update the file_path_string variable with the selected file path
    file_path_entry.config(text=file_path_string)  # Update the file path entry widget with the selected file path
    # Enable the search button after file is chosen
    search_button.config(state="normal")

# Create a new tkinter window
root = tk.Tk()
root.geometry("520x150")

# Define a function to be called when the Search button is clicked
def on_search_clicked(event=None):
    keyword = keyword_entry.get() # Get the keyword entered by the user
    exact_match = exact_match_var.get() # Get the value of the exact match checkbox
    result_text = ""
    with open(file_path_string, 'r') as file:
        for i, line in enumerate(file, start=1):
            if exact_match:
                if result_text == "":
                    result_text = f"Found keyword:\n"
                if keyword == line.strip():
                    result_text += f"At line {i}: {line}"
            else:
                if result_text == "":
                    result_text = f"Found keyword '{keyword}':\n"
                if keyword in line:
                    result_text += f"At line {i}: {line}"
        if result_text:
            result_label.config(text=result_text)
        else:
            result_label.config(text=f"Keyword '{keyword}' not found in file")

# Choose a file path
file_label = tk.Label(root, text="File Path:")
file_label.grid(row=0, column=0)

file_path_string = "Path of the file"
file_path_entry = tk.Label(root, width=50, state="disabled", text=file_path_string, anchor="w")
file_path_entry.grid(row=0, column=1)

choose_file_button = tk.Button(root, text="Choose", command=open_file_dialog)
choose_file_button.grid(row=0, column=2)

# Keyword input field
keyword_label = tk.Label(root, text="Keyword:")
keyword_label.grid(row=1, column=0)

keyword_entry = tk.Entry(root, text="Test")
keyword_entry.grid(row=1, column=1, sticky="ew")
keyword_entry.bind("<Return>", lambda event: on_search_clicked())

# Exact match checkbox
exact_match_var = tk.BooleanVar()
exact_match_checkbox = tk.Checkbutton(root, text="Exact Match", variable=exact_match_var, onvalue=True, offvalue=False)
exact_match_checkbox.grid(row=1, column=2, sticky="e")

# Search button
search_button = tk.Button(root, text="Search", command=on_search_clicked, state="disabled")
search_button.grid(row=2, column=1, sticky="ew")

# Result label
result_label = tk.Label(root, text="")
result_label.grid(row=3, column=1)

# Start the tkinter event loop
root.mainloop()
