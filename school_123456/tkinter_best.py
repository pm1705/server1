import tkinter as tk
import firebase_admin
from firebase_admin import db
from firebase_admin import storage

from school_123456.main import send_print
from school_123456.VARS import SCHOOL_ID

data = {
    "teacher_list": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    "student_list": ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
    "teacher_request_list": ["Spring", "Summer", "Fall", "Winter"],
    "student_request_list": ["Asia", "Africa", "North America", "South America", "Antarctica", "Europe", "Australia"],
}

current_list = "teacher_request_list"

cred = firebase_admin.credentials.Certificate(
    r'C:\Users\Administrator\Desktop\beta-printproj-firebase-adminsdk-538we-16a33f34dd.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://beta-printproj-default-rtdb.europe-west1.firebasedatabase.app',
    'storageBucket': 'beta-printproj.appspot.com'
})


def print_teacher(item_num, button):
    pass


def print_student(item_num, button):
    bucket = storage.bucket()
    blob = bucket.blob('' + NEED_PRINTING2[list(NEED_PRINTING2.keys())[item_num]]["file_id"] + "pdf")
    blob.download_to_filename(
        r'C:\Users\Administrator\PycharmProjects\firebase_connect\school_123456\files_to_print\file.pdf')
    send_print(r'C:\Users\Administrator\PycharmProjects\firebase_connect\school_123456\files_to_print\file.pdf')

    ref = db.reference('schools/' + SCHOOL_ID + '/student_prints/' + list(NEED_PRINTING2.keys())[item_num])
    ref.update({"printed": True})

    button.pack_forget()


def show_teacher_list(item):
    print(item)


def show_student_list(item):
    value = 0  # shared variable for storing the input value

    def update_credits_in_fb():
        global value

        ref = db.reference('schools/' + SCHOOL_ID + '/users/students/' + data["students"][data["student_list"].index(item)][0])
        print(data["students"][data["student_list"].index(item)], value)
        ref.update({"credits": data["students"][data["student_list"].index(item)][1]+int(value)})

        change_list("student_list")

    def return_value():
        global value  # use the shared variable
        value = input_box.get()
        window.destroy()
        update_credits_in_fb()

    def return_zero():
        global value  # use the shared variable
        value = 0
        window.destroy()

    window = tk.Tk()
    window.title("Window Title")

    input_label = tk.Label(window, text="Enter a value:")
    input_label.pack()

    input_box = tk.Entry(window)
    input_box.pack()

    ok_button = tk.Button(window, text="OK", command=lambda: return_value())
    ok_button.pack(side=tk.LEFT)

    zero_button = tk.Button(window, text="Return Zero", command=lambda: return_zero())
    zero_button.pack(side=tk.LEFT)

    window.mainloop()


def show_teacher_request_list(item):
    bucket = storage.bucket()
    blob = bucket.blob('' + data["teacher_request"][data["teacher_request_list"].index(item)][1] + "pdf")
    blob.download_to_filename(
        r'C:\Users\Administrator\PycharmProjects\firebase_connect\school_123456\files_to_print\file.pdf')
    send_print(r'C:\Users\Administrator\PycharmProjects\firebase_connect\school_123456\files_to_print\file.pdf')

    ref = db.reference('schools/' + SCHOOL_ID + '/requests/' + data["teacher_request"][data["teacher_request_list"].index(item)][0])
    ref.update({"relevant": False})

    change_list("teacher_request_list")


def show_student_request_list(item):
    bucket = storage.bucket()
    print('' + data["student_request"][data["student_request_list"].index(item)][1] + "pdf")
    blob = bucket.blob('' + data["student_request"][data["student_request_list"].index(item)][1] + "pdf")
    blob.download_to_filename(
        r'C:\Users\Administrator\PycharmProjects\firebase_connect\school_123456\files_to_print\file.pdf')
    send_print(r'C:\Users\Administrator\PycharmProjects\firebase_connect\school_123456\files_to_print\file.pdf')

    ref = db.reference('schools/' + SCHOOL_ID + '/student_prints/' + data["student_request"][data["student_request_list"].index(item)][0])
    ref.update({"printed": True})


    change_list("student_request_list")


def update_data():

    global data

    ref = db.reference('schools/' + SCHOOL_ID + '/users/teachers')
    fb_data = ref.get()
    teacher_list = []
    teacher_id = []
    if fb_data != "" and fb_data is not None:
        for i in fb_data:
            teacher_list.append(fb_data[i]["name"])
            teacher_id.append(i)
    print(teacher_list)


    ref = db.reference('schools/' + SCHOOL_ID + '/users/students')
    fb_data = ref.get()
    student_list = []
    student_id = []
    if fb_data != "" and fb_data is not None:
        for i in fb_data:
            student_list.append(fb_data[i]["name"] + ", " + str(fb_data[i]["credits"]) + " credits")
            student_id.append([i, fb_data[i]["credits"]])
    print(student_list)

    ref = db.reference('schools/' + SCHOOL_ID + '/requests')
    fb_data = ref.get()
    request_list = []
    request_id = []
    if fb_data != "" and fb_data is not None:
        for i in fb_data:
            if fb_data[i]["approved"] and fb_data[i]["relevant"]:
                request_list.append(fb_data[i]["user_name"] + ", " + str(fb_data[i]["copies"]) + " copies")
                request_id.append([i, fb_data[i]["file_id"]])
    print(request_list)

    ref = db.reference('schools/' + SCHOOL_ID + '/student_prints')
    fb_data = ref.get()
    student_prints_list = []
    student_prints_id = []
    if fb_data != "" and fb_data is not None:
        for i in fb_data:
            if not fb_data[i]["printed"]:
                student_prints_list.append(fb_data[i]["user_name"] + ", " + str(fb_data[i]["copies"]) + " copies")
                student_prints_id.append([i, fb_data[i]["file_id"]])
    print(student_prints_list)

    data = {
        "teacher_list": teacher_list,
        "student_list": student_list,
        "teacher_request_list": request_list,
        "student_request_list": student_prints_list,
        "teachers": teacher_id,
        "students": student_id,
        "teacher_request": request_id,
        "student_request": student_prints_id,
    }

    print(teacher_id, student_id, request_id, student_prints_id)


def change_list(name):
    global current_list
    current_list = name
    title.config(text=name)
    update_data()
    update_buttons()


def button_pressed(item):
    if current_list == "teacher_list":
        show_teacher_list(item)
    if current_list == "student_list":
        show_student_list(item)
    if current_list == "teacher_request_list":
        show_teacher_request_list(item)
    if current_list == "student_request_list":
        show_student_request_list(item)


def update_buttons():
    global current_list
    if current_list:
        for widget in frame.winfo_children():
            widget.destroy()
        for i, item in enumerate(data[current_list]):
            if search_items.get().lower() in item.lower():
                button = tk.Button(frame, text=f"{item}", width=60, command=lambda item=item: button_pressed(item))
                button.pack()


root = tk.Tk()
root.geometry("600x480")
root.configure(bg="white")

list_frame = tk.Frame(root)
list_frame.configure(bg="white")
list_frame.pack(side=tk.TOP)

buttons_frame = tk.Frame(list_frame)
buttons_frame.configure(bg="white")
buttons_frame.pack(side=tk.TOP)

for name in data.keys():
    button = tk.Button(buttons_frame, text=name, width=20, height=3, command=lambda name=name: change_list(name), bg="#A4B8EC")
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

frame = tk.Frame(list_frame)
frame.pack()

change_list(current_list)

root.mainloop()
