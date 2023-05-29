import tkinter as tk
import firebase_admin
from firebase_admin import db
from firebase_admin import storage

from school_123456.main import send_print
from school_123456.VARS import SCHOOL_ID

cred = firebase_admin.credentials.Certificate(
    r'C:\Users\Administrator\Desktop\beta-printproj-firebase-adminsdk-538we-16a33f34dd.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://beta-printproj-default-rtdb.europe-west1.firebasedatabase.app',
    'storageBucket': 'beta-printproj.appspot.com'
})

NEED_PRINTING = {}
window = tk.Tk()
window.title("My Tkinter Window")
window.geometry("600x480")

canvas = tk.Canvas(window)
button_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=button_frame, anchor=tk.NW)


def print_teacher(item_num, button):
    bucket = storage.bucket()
    blob = bucket.blob('' + NEED_PRINTING[list(NEED_PRINTING.keys())[item_num]]["file_id"] + "pdf")
    blob.download_to_filename(
        r'C:\Users\Administrator\PycharmProjects\firebase_connect\school_123456\files_to_print\file.pdf')
    send_print(r'C:\Users\Administrator\PycharmProjects\firebase_connect\school_123456\files_to_print\file.pdf')

    ref = db.reference('schools/' + SCHOOL_ID + '/requests/' + list(NEED_PRINTING.keys())[item_num])
    ref.update({"relevant": False})

    button.pack_forget()


def print_student(item_num, button):
    bucket = storage.bucket()
    blob = bucket.blob('' + NEED_PRINTING2[list(NEED_PRINTING2.keys())[item_num]]["file_id"] + "pdf")
    blob.download_to_filename(
        r'C:\Users\Administrator\PycharmProjects\firebase_connect\school_123456\files_to_print\file.pdf')
    send_print(r'C:\Users\Administrator\PycharmProjects\firebase_connect\school_123456\files_to_print\file.pdf')

    ref = db.reference('schools/' + SCHOOL_ID + '/student_prints/' + list(NEED_PRINTING2.keys())[item_num])
    ref.update({"printed": True})

    button.pack_forget()


def receive_reqs():
    global NEED_PRINTING, NEED_PRINTING2, canvas, canvas2, button_frame, button_frame2, students_list, teachers_list

    teachers_list.pack_forget()
    students_list.pack_forget()

    teachers_list = tk.Listbox(teachers_frame, width=30)
    students_list = tk.Listbox(students_frame, width=30)

    NEED_PRINTING = {}
    NEED_PRINTING2 = {}

    ref_requests = db.reference('schools/' + SCHOOL_ID + '/requests')
    data = ref_requests.get()
    need_printing = {}
    if data != "":
        for i in data.keys():
            if data[i]["approved"] == True and data[i]["relevant"] == True:
                need_printing[i] = data[i]
    display_request = []
    for i in need_printing.keys():
        display_request.append("" + data[i]["user_name"] + ", " + str(data[i]["copies"]) + " copies")
    NEED_PRINTING = need_printing

    for i, teacher in enumerate(display_request):
        button = tk.Button(teachers_list, text=teacher, width=30, font=("Ariel", 13))
        button.pack(side=tk.TOP, fill="x")
        button.config(command=lambda item_num=i, btn=button: print_teacher(item_num, btn))

    teachers_list.pack(fill="both", expand=True)
    teachers_frame.pack(side="left", fill="y")

    ref_requests2 = db.reference('schools/' + SCHOOL_ID + '/student_prints')
    data2 = ref_requests2.get()
    need_printing2 = {}
    if data2 != "":
        for i in data2.keys():
            if data2[i]["printed"] == False:
                need_printing2[i] = data2[i]
    display_request2 = []
    for i in need_printing2.keys():
        display_request2.append("" + data2[i]["user_name"] + ", " + str(data2[i]["copies"]) + " copies")
    NEED_PRINTING2 = need_printing2

    for i, student in enumerate(display_request2):
        button2 = tk.Button(students_list, text=student, width=30, font=("Ariel", 13))
        button2.pack(side=tk.TOP, fill="x")
        button2.config(command=lambda item_num=i, btn=button2: print_student(item_num, btn))

    students_list.pack(fill="both", expand=True)
    students_frame.pack(side="left", fill="y")


def show_students(on_item_click=None):
    ref_requests = db.reference('schools/' + SCHOOL_ID + '/users/students')
    data = ref_requests.get()
    print(data)

    students_list = {}

    if data != "" and data is not None:
        for i in data.keys():
            students_list[i] = data[i]

    def button_click_handler(idx):
        # This function will be called when a button is clicked
        if on_item_click:
            on_item_click(idx)
        else:
            print(f"Button {idx} was clicked!")

    def search_button_click_handler():
        # This function will be called when the search button is clicked
        query = search_entry.get().lower()
        matching_items = [item for item in students_list if query in item.lower()]
        for button in button_list:
            button.pack_forget()
        for idx, item in enumerate(matching_items):
            button = tk.Button(button_frame, text=item, command=lambda idx=idx: button_click_handler(idx))
            button.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)
            button_list.append(button)

    window_students = tk.Tk()
    window_students.title("List Window")

    title_label = tk.Label(window_students, text="click student to add credits")
    title_label.pack()

    # Create a search bar and search button
    search_frame = tk.Frame(window_students)
    search_frame.pack(side=tk.TOP, fill=tk.X)
    search_entry = tk.Entry(search_frame)
    search_entry.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)
    search_button = tk.Button(search_frame, text="Search", command=search_button_click_handler)
    search_button.pack(side=tk.RIGHT, padx=5, pady=5)

    button_frame = tk.Frame(window_students)
    button_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    button_list = []

    for idx, item in enumerate(students_list):
        button = tk.Button(button_frame, text=item, command=lambda idx=idx: button_click_handler(idx))
        button.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)
        button_list.append(button)

    # Start the Tkinter main loop
    window.mainloop()


teachers_frame = tk.Frame(window)
teachers_label = tk.Label(teachers_frame, text="Teacher Requests:")
teachers_label.pack()
teachers_list = tk.Listbox(teachers_frame)

students_frame = tk.Frame(window)
students_label = tk.Label(students_frame, text="Student Requests:")
students_label.pack()
students_list = tk.Listbox(students_frame)


# Create the frame for the buttons
button_frame = tk.Frame(window)

# Create the three buttons and add them to the frame
refresh = tk.Button(button_frame, text="Refresh", command=lambda: receive_reqs())
button2 = tk.Button(button_frame, text="Student List", command=lambda: show_students())
button3 = tk.Button(button_frame, text="Teacher List", command=lambda: show_teachers())
refresh.pack(side="left")
button2.pack(side="left")
button3.pack(side="left")
button_frame.pack()

# Start the main event loop
window.mainloop()
