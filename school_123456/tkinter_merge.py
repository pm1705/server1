import tkinter as tk
from tkinter import ttk

data = {
    "months": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    "days": ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
    "seasons": ["Spring", "Summer", "Fall", "Winter"],
    "continents": ["Asia", "Africa", "North America", "South America", "Antarctica", "Europe", "Australia"],
}

current_list = "months"

def change_list(name):
    global current_list
    current_list = name
    title.config(text=name)
    update_buttons()

def button_pressed(item):
    print(current_list, item)

def update_buttons():
    global current_list
    if current_list:
        for widget in frame.winfo_children():
            widget.destroy()
        for i, item in enumerate(data[current_list]):
            if search_items.get().lower() in item.lower():
                button = tk.Button(frame, text=f"{i}: {item}", width=30, command=lambda item=item: button_pressed(item))
                button.pack()

        # Update the scroll region of the canvas
        canvas.configure(scrollregion=canvas.bbox("all"))

def on_mousewheel(event):
    # Scroll the canvas vertically
    canvas.yview_scroll(-int(event.delta/120), "units")

root = tk.Tk()
root.geometry("600x400")

list_frame = tk.Frame(root)
list_frame.pack(side=tk.TOP)

buttons_frame = tk.Frame(list_frame)
buttons_frame.pack(side=tk.TOP)

for name in data.keys():
    button = tk.Button(buttons_frame, text=name, width=10, command=lambda name=name: change_list(name))
    button.pack(side=tk.LEFT)

search_label = tk.Label(list_frame, text="Search:")
search_label.pack(side=tk.TOP)

search_items = tk.StringVar()

search_entry = tk.Entry(list_frame, textvariable=search_items)
search_entry.pack(side=tk.TOP)

search_button = tk.Button(list_frame, text="Search", command=update_buttons)
search_button.pack(side=tk.TOP)

title = tk.Label(list_frame, text=current_list)
title.pack()

canvas = tk.Canvas(list_frame, height=200)
canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)

# Bind mousewheel events to the canvas
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.bind("<MouseWheel>", on_mousewheel)

update_buttons()

root.mainloop()
