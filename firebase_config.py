import pyrebase

firebase_config = {
    "apiKey": "AIzaSyB2moxbIis0mdnvlp1-5MT5BvOYObQx8EU",
    "authDomain": "binwise-64045.firebaseapp.com",
    "databaseURL": "https://binwise-admin-default-rtdb.firebaseio.com/",  # leave this empty unless using Firebase Realtime DB
    "projectId": "binwise-64045",
    "storageBucket": "binwise-64045.firebasestorage.app",
    "messagingSenderId": "35051787509",
    "appId": "1:35051787509:web:cb68e36fc2eab94f56a1bc",
    "measurementId": "G-RB8GNH47M7"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

