import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate(r"binwise-admin-firebase-adminsdk-fbsvc-2cfb759cdc.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://binwise-admin-default-rtdb.firebaseio.com/'
    })

# Export reference
ref = db.reference('/bins')

