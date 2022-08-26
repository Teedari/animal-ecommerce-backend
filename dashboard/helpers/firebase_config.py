from mimetypes import init
import pyrebase

firebaseConfig = {
  'apiKey': "AIzaSyBRuGfn6uqcNoCzZDHsqzUn7stvE2BSQiM",
  'authDomain': "animal-ecommerce-project.firebaseapp.com",
  'projectId': "animal-ecommerce-project",
  'storageBucket': "animal-ecommerce-project.appspot.com",
  'messagingSenderId': "78512254729",
  'appId': "1:78512254729:web:dad967b958923d74126dd8",
  "databaseURL": "gs://animal-ecommerce-project.appspot.com"
}

firebase = pyrebase.initialize_app(firebaseConfig)
class Firebase:
  def __init__(self, file):
    self.file = file
    self.storage = firebase.storage()
  def save(self):
    pass
    res = self.storage.child('public').put(self.file)
    print(res)