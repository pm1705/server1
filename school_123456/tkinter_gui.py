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


def receive_reqs():
    global NEED_PRINTING, canvas, button_frame
    print("aaa")
    ref_requests = db.reference('schools/' + SCHOOL_ID + '/requests')
    data = ref_requests.get()
    need_printing = {}
    for i in data.keys():
        if data[i]["approved"] == True and data[i]["relevant"] == True:
            need_printing[i] = data[i]
    display_request = []
    for i in need_printing.keys():
        display_request.append("" + data[i]["user_name"] + ", " + str(data[i]["copies"]) + " copies")
    NEED_PRINTING = need_printing
    print(need_printing)
    canvas.pack_forget()
    canvas = tk.Canvas(window)
    button_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=button_frame, anchor=tk.NW)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    buttons = []
    for i, day in enumerate(display_request):
        button = tk.Button(button_frame, text=day, width=30, font=("Ariel", 13))
        button.pack(side=tk.TOP)
        button.config(command=lambda item_num=i, btn=button: print_selected_item(item_num, btn))


label = tk.Label(window, text="Approved prints", pady=15, font=("Ariel", 13), width=30, background="white",height=1)
label.pack()
refresh = tk.Button(window, text="Refresh", command=lambda: receive_reqs())
refresh.pack()


def print_selected_item(item_num, button):
    bucket = storage.bucket()
    print(list(NEED_PRINTING.keys()))
    blob = bucket.blob('' + NEED_PRINTING[list(NEED_PRINTING. keys())[item_num]]["file_id"] + "pdf")
    blob.download_to_filename(r'C:\Users\Administrator\PycharmProjects\firebase_connect\school_123456\files_to_print\file.pdf')
    send_print(r'C:\Users\Administrator\PycharmProjects\firebase_connect\school_123456\files_to_print\file.pdf')

    ref = db.reference('schools/' + SCHOOL_ID + '/requests/' + list(NEED_PRINTING. keys())[item_num])
    print('schools/' + SCHOOL_ID + '/requests/' + list(NEED_PRINTING. keys())[item_num])
    ref.update({"relevant" : False})

    button.pack_forget()

button_frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox(tk.ALL))
canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

window.mainloop()
