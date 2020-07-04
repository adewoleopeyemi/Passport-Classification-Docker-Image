from flask import Flask, redirect, url_for, render_template, request, flash
import os
from flask_assets import Environment, Bundle

import firebase_admin
from firebase_admin import credentials, db
from google.cloud import storage
from firebase_admin import storage
import requests
import pyrebase
#from firebase import firebase

import os

from datetime import datetime



app = Flask(__name__)
app.secret_key = 'hbavdy3'





'''
assets = Environment(app)
assets.url = app.static_url_path
assets.debug = True

scss = Bundle('style2.scss', filters='pyscss', output='gen/all.css')
assets.register('scss_all', scss)
'''


@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("index.html")


@app.route("/oneImagePredict", methods=["GET"])
def oneImagePredict():
    return render_template("one_image_predict.html")



@app.route("/predictOneImage", methods=["POST", "GET"])
def predictOneImage():
    if request.method == "POST":
        img_url = request.files["image"]
        apikey = request.form["apikey"]
        
        UPLOAD_FOLDER = './test'
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        
        #save image
        path = os.path.join(app.config['UPLOAD_FOLDER'], img_url.filename)
        img_url.save(path)
        
        
        
        
        if not firebase_admin._apps:
            #fetch credentials
            cred = credentials.Certificate("service_account2.json")
            firebase_admin.initialize_app(cred, {'databaseURL': 'https://passport-image-classification.firebaseio.com/'})
        
        
        ##validate API KEY
        ref = db.reference('ApiKey')
        apiKeyType = ref.child(apikey).child("type").get()
        
        if apiKeyType == None:
            flash('Invalid API Key')
            return redirect(url_for("oneImagePredict"))
        else:
            
            #image_url = sys.argv[1] #we pass the url as an argument
            
            config = {"apiKey": "AIzaSyC1ayNr3CCXRv-cejofLx1_hNmsR-o7Coo",
                        "authDomain": "passport-image-classification.firebaseapp.com",
                        "databaseURL": "https://passport-image-classification.firebaseio.com",
                        "projectId": "passport-image-classification",
                        "storageBucket": "passport-image-classification.appspot.com",
                        "messagingSenderId": "39733434768",
                        "appId": "1:39733434768:web:85ec9477120baa9116fb15",
                        "measurementId": "G-FXCMDZNL6T"}
            
            today = datetime.now()
            
            
            firebase = pyrebase.initialize_app(config)
            storage = firebase.storage()
            path_on_cloud = f'images/{today}.jpg'
            storage.child(path_on_cloud).put(img_url)
            
            storage.
            '''
            from google.cloud import storage

            client = storage.Client()
            bucket = client.get_bucket('passport-image-classification')
            blob = bucket.blob('image.png')
            # use pillow to open and transform the file
            image = Image.open(img_url)
            # perform transforms
            image.save(outfile)
            of = open(outfile, 'rb')
            blob.upload_from_file(of)
            # or... (no need to use pillow if you're not transforming)
            blob.upload_from_filename(filename=outfile)
            
            '''
            
            
            
            
            
            '''
            bucket = storage.bucket()

            image_data = requests.get(img_url).content
            blob = bucket.blob('new_cool_image.jpg')
            blob.upload_from_string(
                    image_data,
                    content_type='image/jpg'
                )
            print(blob.public_url)
            '''

            '''
            
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="service_account.json"
            #firebase_instance = firebase.FirebaseApplication('https://passport-image-classification.firebaseio.com/')
            client = storage.Client()
            bucket = client.get_bucket('passport-image-classification')
            # posting to firebase storage
            imageBlob = bucket.blob("/")
            # imagePath = [os.path.join(self.path,f) for f in os.listdir(self.path)]
            imagePath = img_url
            imageBlob = bucket.blob("image.png")
            imageBlob.upload_from_filename(imagePath)
            ''' 
        
            return str(apiKeyType)

        '''
        #Download Image
        with urllib.request.urlopen(img_url) as url:
            with open('test/temp.jpg', 'wb') as f:
                f.write(url.read())


        #preprocess image
        test_gen = ImageDataGenerator(rescale=1./255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True)

        test_generator = test_gen.flow_from_directory(
                "test/",
                target_size=(224, 224),
                shuffle = False,
                class_mode='categorical',
                batch_size=1)

        #load model
        loaded_model = load_model('model/model1-.h5')

        #make prediciton
        predict = loaded_model.predict_generator(test_generator) 
        array  = np.array(predict)
        ind = np.argmax(predict)
        _class = ind+1
        
        #remove image from server
        os.remove('test/temp.jpg')

        #return class
        if _class == 0:
            return "BAD BACKGROUND"
        elif _class == 1:
            return "BLURRY"
        elif _class == 2:
            return "FACE_IN_BACKGROUND"
        elif _class == 3:
            return "GOOD_IMAGES"
        elif _class == 4:
            return "INVALID_PASSPORT"
        elif _class == 5:
            return "NO_HUMAN_FACE"
        elif _class == 6:
            return "STAPLED FACE"
        else:
            return "500"
        '''
    else:
        return "Use a POST request to access this API, check documentation at "
        
        

@app.route("/predictManyImages", methods=["POST", "GET"])
def predictManyImages():
    if request.method == "POST":
        img_url_array = request.form["img_url"]
        prediction_result = []
        
        #Image preprocessor
        test_gen = ImageDataGenerator(rescale=1./255,
                shear_range=0.2,
                zoom_range=0.2,
                horizontal_flip=True)
        
        #load model
        loaded_model = load_model('model/model1-.h5')
        
        for img_url in img_url_array:
            #Download Image
            with urllib.request.urlopen(img_url) as url:
                with open('test/temp.jpg', 'wb') as f:
                    f.write(url.read())


            #preprocess image
            test_generator = test_gen.flow_from_directory(
                    "test/",
                    target_size=(224, 224),
                    shuffle = False,
                    class_mode='categorical',
                    batch_size=1)

            

            #make prediciton
            predict = loaded_model.predict_generator(test_generator) 
            array  = np.array(predict)
            ind = np.argmax(predict)
            _class = ind+1

            #remove image from server
            os.remove('test/temp.jpg')

            #return class
            if _class == 0:
                prediction_result.append("BAD BACKGROUND")
            elif _class == 1:
                prediction_result.append("BLURRY")
            elif _class == 2:
                prediction_result.append("FACE_IN_BACKGROUND")
            elif _class == 3:
                prediction_result.append("GOOD_IMAGES")
            elif _class == 4:
                prediction_result.append("INVALID_PASSPORT")
            elif _class == 5:
                prediction_result.append("NO_HUMAN_FACE")
            elif _class == 6:
                prediction_result.append("STAPLED FACE")
            else:
                prediction_result.append("No Class")

        return prediction_result
    
    else:
        return "Use a POST request to access this API, check documentation at "
    
    
    
@app.route("/predictManyImagesFolder", methods=["POST", "GET"])
def predictManyImagesFolder(): 
    print("")

        
        
if __name__ == "_main_":
    app.run(debug=True)
        
        
        
        
        
        
        
