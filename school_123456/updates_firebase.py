import firebase_admin
from firebase_admin import db
from firebase_admin import storage

from school_123456.VARS import SCHOOL_ID

cred = firebase_admin.credentials.Certificate(
    r'C:\Users\Administrator\Desktop\beta-printproj-firebase-adminsdk-538we-16a33f34dd.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://beta-printproj-default-rtdb.europe-west1.firebasedatabase.app',
    'storageBucket': 'beta-printproj.appspot.com'
})

ref_requests = db.reference('schools/' + SCHOOL_ID + '/requests')
data = ref_requests.get()

need_printing = {}

for i in data.keys():
    if data[i]["approved"] == True and data[i]["relevant"] == True:
        need_printing[i] = data[i]

# for i in need_printing.keys():
#     print(need_printing[i]["file_id"] + "pdf")
#     bucket = storage.bucket()
#     blob = bucket.blob('' + need_printing[i]["file_id"] + "pdf")
#     blob.download_to_filename(r'C:\Users\Administrator\PycharmProjects\firebase_connect\school_123456\files_to_print\''[:-1] + need_printing[i]["file_id"] + "pdf" + ".pdf")

display_request = []

for i in need_printing.keys():
    display_request.append("" + data[i]["user_name"] + ", " + str(data[i]["copies"]) + " copies")

print(display_request)