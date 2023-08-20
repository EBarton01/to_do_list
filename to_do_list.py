import tkinter as tk
from tkinter import ttk, filedialog
import os
import datetime

def on_button_click():
    text = entry.get()
    if text:
        working_on_list.insert("", "end", values=(text,))
        entry.delete(0, tk.END)

def delete_selected():
    selected_item = working_on_list.focus() or completed_list.focus()
    if selected_item:
        widget = working_on_list if working_on_list.focus() else completed_list
        widget.delete(selected_item)

def move_to_completed(event):
    selected_item = working_on_list.focus()
    if selected_item:
        values = working_on_list.item(selected_item, "values")
        completed_list.insert("", "end", values=values)
        working_on_list.delete(selected_item)

def move_to_working_on(event):
    selected_item = completed_list.focus()
    if selected_item:
        values = completed_list.item(selected_item, "values")
        working_on_list.insert("", "end", values=values)
        completed_list.delete(selected_item)

def switch_selected_item(event):
    selected_item = working_on_list.focus() or completed_list.focus()
    if selected_item and not entry.get():
        widget = working_on_list if working_on_list.focus() else completed_list
        values = widget.item(selected_item, "values")
        other_widget = completed_list if widget == working_on_list else working_on_list
        other_widget.insert("", "end", values=values)
        widget.delete(selected_item)

def submit_with_enter(event):
    if entry.get():
        on_button_click()
    else:
        switch_selected_item(event)

def delete_selected_with_backspace(event):
    delete_selected()

def focus_textbox(event):
    entry.focus_set()

def focus_first_item_working_on(event):
    working_on_list.focus_set()
    first_item = working_on_list.get_children()[0]
    working_on_list.selection_set(first_item)
    working_on_list.focus(first_item)

def focus_first_item_completed(event):
    completed_list.focus_set()
    first_item = completed_list.get_children()[0]
    completed_list.selection_set(first_item)
    completed_list.focus(first_item)

def focus_next_item(event):
    widget = working_on_list if working_on_list.focus() else completed_list
    selected_item = widget.focus()
    if selected_item:
        next_item = widget.next(selected_item)
        if next_item:
            widget.selection_set(next_item)
            widget.focus(next_item)

def focus_previous_item(event):
    widget = working_on_list if working_on_list.focus() else completed_list
    selected_item = widget.focus()
    if selected_item:
        prev_item = widget.prev(selected_item)
        if prev_item:
            widget.selection_set(prev_item)
            widget.focus(prev_item)

def save_file():
    date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = os.path.join(os.path.dirname(__file__), f"{date_time}.txt")
    with open(file_path, "w") as file:
        file.write("Working On:\n")
        for item in working_on_list.get_children():
            values = working_on_list.item(item, "values")
            if values:
                file.write(values[0] + "\n")
        file.write("\nCompleted:\n")
        for item in completed_list.get_children():
            values = completed_list.item(item, "values")
            if values:
                file.write(values[0] + "\n")
    print(f"File saved as {file_path}")

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            working_on = True
            completed = False
            for line in file:
                line = line.strip()
                if line == "Working On:":
                    working_on = True
                    completed = False
                elif line == "Completed:":
                    working_on = False
                    completed = True
                elif line:
                    if working_on:
                        working_on_list.insert("", "end", values=(line,))
                    elif completed:
                        completed_list.insert("", "end", values=(line,))

def open_shortcuts():
    shortcuts_window = tk.Toplevel()
    shortcuts_window.title("Shortcuts")
    
    shortcuts_text = (
        "Alt + E: Focus on the text box\n"
        "Alt + W: Select the first item in the 'Working On' list\n"
        "Alt + C: Select the first item in the 'Completed' list\n"
        "Alt + M: Switch the selected item between lists\n"
        "Up Arrow: Focus on the previous item in the list\n"
        "Down Arrow: Focus on the next item in the list\n"
        "Backspace: Delete the selected item\n"
        "Enter: Add Item from Textbox"
    )
    
    shortcuts_label = tk.Label(shortcuts_window, text=shortcuts_text, padx=10, pady=10)
    shortcuts_label.pack()

def open_about():
    about_window = tk.Toplevel()
    about_window.title("About")
    
    about_text = (
        "To do list\n"
        "Created by Eric Barton\n"
        "2023"
    )
    
    about_label = tk.Label(about_window, text=about_text, padx=10, pady=10)
    about_label.pack()

def switch_selected_with_alt_m(event):
    switch_selected_item(event)

# Create the main window
window = tk.Tk()
window.title("To do List")

# Create a menu bar
menubar = tk.Menu(window)
window.config(menu=menubar)

# Create a File menu
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.quit)

# Create a Tools menu
tools_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Tools", menu=tools_menu)
tools_menu.add_command(label="Shortcuts", command=open_shortcuts)

# Create an About menu
about_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="About", menu=about_menu)
about_menu.add_command(label="Open About", command=open_about)

# Create a frame to hold the "Working On" and "Completed" Treeview widgets
frame = tk.Frame(window)
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create a Treeview widget for "Working On" tasks
working_on_list = ttk.Treeview(frame, columns=("text",), show="headings")
working_on_list.heading("text", text="Working On")
working_on_list.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

# Set up column attributes for "Working On" tasks
working_on_list.column("text", anchor="w")

# Create a Treeview widget for "Completed" tasks
completed_list = ttk.Treeview(frame, columns=("text",), show="headings")
completed_list.heading("text", text="Completed")
completed_list.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

# Set up column attributes for "Completed" tasks
completed_list.column("text", anchor="w")

# Create a frame to hold the text box and buttons
input_frame = tk.Frame(window)
input_frame.pack(side=tk.BOTTOM, padx=10, pady=10, fill=tk.X)

# Create an entry widget (text box)
entry = tk.Entry(input_frame)
entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
entry.bind("<Return>", submit_with_enter)

# Create an "Add" button
add_button = tk.Button(input_frame, text="Add", command=on_button_click)
add_button.pack(side=tk.LEFT, padx=10)

# Create a "Delete" button
delete_button = tk.Button(input_frame, text="Delete", command=delete_selected)
delete_button.pack(side=tk.LEFT, padx=10)

# Bind double-click events to move tasks between lists
working_on_list.bind("<Double-1>", move_to_completed)
completed_list.bind("<Double-1>", move_to_working_on)

# Bind <BackSpace> key event to delete_selected
window.bind("<BackSpace>", delete_selected_with_backspace)

# Bind Alt + T to focus the text box
window.bind("<Alt-e>", focus_textbox)

# Bind Alt + W to navigate "Working On" list
window.bind("<Alt-w>", focus_first_item_working_on)

# Bind Alt + C to navigate "Completed" list
window.bind("<Alt-c>", focus_first_item_completed)

# Bind Alt + M to switch selected item between lists
window.bind("<Alt-m>", switch_selected_with_alt_m)

# Bind up and down arrow keys to navigate through items
window.bind("<Up>", focus_previous_item)
window.bind("<Down>", focus_next_item)

# Start the Tkinter event loop
window.mainloop()
