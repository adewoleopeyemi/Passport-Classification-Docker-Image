from flask import Flask, redirect, url_for, render_template, request, flash
import os
from flask_assets import Environment, Bundle

import firebase_admin
from firebase_admin import credentials, db
from google.cloud import storage
from firebase_admin import storage
import requests
import pyrebase
from keras.preprocessing.image import ImageDataGenerator
#from PIL import Image
import urllib.request
from keras.models import load_model
import numpy as np
import shutil

import os

from datetime import datetime

import h5py
import json



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


@app.route("/multipleImagePredict", methods=["GET"])
def multipleImagePredict():
    return render_template("multiple_image_predict.html")


@app.route("/folderImagesPredict", methods=["GET"])
def folderImagesPredict():
    return render_template("folder_images_predict.html")



@app.route("/predictOneImage", methods=["POST", "GET"])
def predictOneImage():
    if request.method == "POST":
        img_url = request.files["image"]
        apikey = request.form["apikey"]
        
        print(f'this is the url {img_url.filename}')
        if img_url.filename == "":
            flash('Please upload an image')
            return redirect(url_for("folderImagesPredict"))
        else:
        
            UPLOAD_FOLDER = './test/test'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            #save image to local directory for upload to firebase storage
            path = os.path.join(app.config['UPLOAD_FOLDER'], img_url.filename)
            img_url.save(path)






            if not firebase_admin._apps:
                #fetch credentials
                cred = credentials.Certificate("service_account.json")
                firebase_admin.initialize_app(cred, {'databaseURL': 'https://xxxxx.firebaseio.com/'})


            ##validate API KEY
            ref = db.reference('ApiKey')
            apiKeyType = ref.child(apikey).child("type").get()

            if apiKeyType == None:
                flash('Invalid API Key')
                return redirect(url_for("oneImagePredict"))
            else:

                #image_url = sys.argv[1] #we pass the url as an argument

                config = {"apiKey": "xxxxx",
                            "authDomain": "xxxxx.firebaseapp.com",
                            "databaseURL": "https://xxxxx.firebaseio.com",
                            "projectId": "xxxxx",
                            "storageBucket": "xxxxx.appspot.com",
                            "messagingSenderId": "xxxxx",
                            "appId": "1:xxxxx:web:xxxxx",
                            "measurementId": "xxxxx"}

                today = datetime.now()


                firebase = pyrebase.initialize_app(config)
                storage = firebase.storage()
                path_on_cloud = f'images/{today}.jpg'
                storage.child(path_on_cloud).put(path)

                upload_url = storage.child(path_on_cloud).get_url(token=None)




                #Download Image
                '''
                with urllib.request.urlopen(upload_url) as url:
                    with open('test/temp.jpg', 'wb') as f:
                        f.write(url.read())
                '''


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
                loaded_model = load_model('model/model1-94%.h5')

                #make prediciton
                predict = loaded_model.predict_generator(test_generator) 
                array  = np.array(predict)
                ind = np.argmax(predict)
                _class = ind
                print(array,ind,_class)

                #remove image from local directory
                os.remove(path)

                #return class
                if _class == 0:
                    flash("BAD BACKGROUND")
                    return redirect(url_for("oneImagePredict"))
                elif _class == 1:
                    flash("BLURRY")
                    return redirect(url_for("oneImagePredict"))
                elif _class == 2:
                    flash("FACE IN BACKGROUND")
                    return redirect(url_for("oneImagePredict"))
                elif _class == 3:
                    flash("GOOD IMAGE")
                    return redirect(url_for("oneImagePredict"))
                elif _class == 4:
                    flash("INVALID PASSPORT")
                    return redirect(url_for("oneImagePredict"))
                elif _class == 5:
                    flash("NO HUMAN FACE")
                    return redirect(url_for("oneImagePredict"))
                elif _class == 6:
                    flash("STAPLE DEFACED")
                    return redirect(url_for("oneImagePredict"))
                else:
                    return "500"
            
    else:
        return "Use a POST request to access this API, check documentation at "
        
        

@app.route("/xxxxx", methods=["POST", "GET"])
def xxxxx():
    if request.method == "POST":
        uploaded_files = request.files.getlist("image")
        apikey = request.form["apikey"]

        if not uploaded_files or not any(f for f in uploaded_files):
            flash('Please upload a folder')
            return redirect(url_for("multipleImagePredict"))
        else:

            config = {"apiKey": "xxxxx",
                            "authDomain": "xxxxx.firebaseapp.com",
                            "databaseURL": "https://xxxxx.firebaseio.com",
                            "projectId": "xxxxx",
                            "storageBucket": "xxxxx.appspot.com",
                            "messagingSenderId": "xxxxx",
                            "appId": "1:xxxxx:web:xxxxx",
                            "measurementId": "xxxxx"}


            UPLOAD_FOLDER = './test/test'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



            #save images to local directory for upload to firebase storage
            for file in uploaded_files:
                path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(path)

                #save to firebase
                today = datetime.now()

                firebase = pyrebase.initialize_app(config)
                storage = firebase.storage()
                path_on_cloud = f'images/{today}.jpg'
                storage.child(path_on_cloud).put(path)

                upload_url = storage.child(path_on_cloud).get_url(token=None)


            if not firebase_admin._apps:
                #fetch credentials
                cred = credentials.Certificate("service_account.json")
                firebase_admin.initialize_app(cred, {'databaseURL': 'https://xxxxx.firebaseio.com/'})


            ##validate API KEY
            ref = db.reference('ApiKey')
            apiKeyType = ref.child(apikey).child("type").get()

            if apiKeyType == None:
                flash('Invalid API Key')
                return redirect(url_for("oneImagePredict"))
            else:
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
                loaded_model = load_model('model/model1-94%.h5')

                #make prediciton
                predict = loaded_model.predict_generator(test_generator) 
                array  = np.array(predict)
                result = {}
                for i, rows in enumerate(array):
                    _class = np.argmax(rows)
                    result[uploaded_files[i].filename] = _class


                today = datetime.now()
                current_directory = os.getcwd()
                final_directory = os.path.join(current_directory, f'result_{today}')
                if not os.path.exists(final_directory):
                    os.makedirs(final_directory) 

                error = 0
                currentProgress = 0
                resultDisplayed = {}

                for key, value in result.items():
                    if value == 0:
                        #BAD BACKGROUND
                        if os.path.exists(f"{final_directory}/BAD_BACKGROUND") == True:
                            try:
                                shutil.move(f"{UPLOAD_FOLDER}/{key}" , f"{final_directory}/BAD_BACKGROUND")
                                resultDisplayed["BAD_BACKGROUND"] += 1
                            except:
                                error += 1
                        else:
                            #make directory
                            os.mkdir(f"{final_directory}/BAD_BACKGROUND")
                            try:
                                shutil.move(f"{UPLOAD_FOLDER}/{key}" , f"{final_directory}/BAD_BACKGROUND")
                                resultDisplayed["BAD_BACKGROUND"] = 1
                            except Exception as e:
                                error += 1
                            currentProgress +=1

                    elif value == 1:
                        #BLURRY
                        if os.path.exists(f"{final_directory}/BLURRY") == True:
                            try:
                                shutil.move(f"{UPLOAD_FOLDER}/{key}" , f"{final_directory}/BLURRY")
                                resultDisplayed["BLURRY"] += 1
                            except:
                                error += 1
                        else:
                            #make directory
                            os.mkdir(f"{final_directory}/BLURRY")
                            try:
                                shutil.move(f"{UPLOAD_FOLDER}/{key}" , f"{final_directory}/BLURRY")
                                resultDisplayed["BLURRY"] = 1
                            except Exception as e:
                                error += 1
                            currentProgress +=1

                    elif value == 2:
                        #FACE_IN_BACKGROUND
                        if os.path.exists(f"{final_directory}/FACE_IN_BACKGROUND") == True:
                            try:
                                shutil.move(f"{UPLOAD_FOLDER}/{key}" , f"{final_directory}/FACE_IN_BACKGROUND")
                                resultDisplayed["FACE_IN_BACKGROUND"] += 1
                            except:
                                error += 1
                        else:
                            #make directory
                            os.mkdir(f"{final_directory}/FACE_IN_BACKGROUND")
                            try:
                                shutil.move(f"{UPLOAD_FOLDER}/{key}" , f"{final_directory}/FACE_IN_BACKGROUND")
                                resultDisplayed["FACE_IN_BACKGROUND"] = 1
                            except Exception as e:
                                error += 1
                            currentProgress +=1

                    elif value == 3:
                        #GOOD_IMAGES
                        if os.path.exists(f"{final_directory}/GOOD_IMAGES") == True:
                            try:
                                shutil.move(f"{UPLOAD_FOLDER}/{key}" , f"{final_directory}/GOOD_IMAGES")
                                resultDisplayed["GOOD_IMAGES"] += 1
                            except:
                                error += 1
                        else:
                            #make directory
                            os.mkdir(f"{final_directory}/GOOD_IMAGES")
                            try:
                                shutil.move(f"{UPLOAD_FOLDER}/{key}" , f"{final_directory}/GOOD_IMAGES")
                                resultDisplayed["GOOD_IMAGES"] = 1
                            except Exception as e:
                                error += 1
                            currentProgress +=1


                    elif value == 4:
                        #INVALID_PASSPORT
                        if os.path.exists(f"{final_directory}/INVALID_PASSPORT") == True:
                            try:
                                shutil.move(f"{UPLOAD_FOLDER}/{key}" , f"{final_directory}/INVALID_PASSPORT")
                                resultDisplayed["INVALID_PASSPORT"] += 1
                            except:
                                error += 1
                        else:
                            #make directory
                            os.mkdir(f"{final_directory}/INVALID_PASSPORT")
                            try:
                                shutil.move(f"{UPLOAD_FOLDER}/{key}" , f"{final_directory}/INVALID_PASSPORT")
                                resultDisplayed["INVALID_PASSPORT"] = 1
                            except Exception as e:
                                error += 1
                            currentProgress +=1



                    elif value == 5:
                        #NO_HUMAN_FACE
                        if os.path.exists(f"{final_directory}/NO_HUMAN_FACE") == True:
                            try:
                                shutil.move(f"{UPLOAD_FOLDER}/{key}" , f"{final_directory}/NO_HUMAN_FACE")
                                resultDisplayed["NO_HUMAN_FACE"] += 1
                            except:
                                error += 1
                        else:
                            #make directory
                            os.mkdir(f"{final_directory}/NO_HUMAN_FACE")
                            try:
                                shutil.move(f"{UPLOAD_FOLDER}/{key}" , f"{final_directory}/NO_HUMAN_FACE")
                                resultDisplayed["NO_HUMAN_FACE"] = 1
                            except Exception as e:
                                error += 1
                            currentProgress +=1


                    elif value == 6:
                        #STAPLED_FACE
                        if os.path.exists(f"{final_directory}/STAPLED_FACE") == True:
                            try:
                                shutil.move(f"{UPLOAD_FOLDER}/{key}" , f"{final_directory}/STAPLED_FACE")
                                resultDisplayed["STAPLED_FACE"] += 1
                            except:
                                error += 1
                        else:
                            #make directory
                            os.mkdir(f"{final_directory}/STAPLED_FACE")
                            try:
                                shutil.move(f"{UPLOAD_FOLDER}/{key}" , f"{final_directory}/STAPLED_FACE")
                                resultDisplayed["STAPLED_FACE"] = 1
                            except Exception as e:
                                error += 1
                            currentProgress +=1
                                    
                #make zip file
                shutil.make_archive(f'result_{today}', 'zip', final_directory)

                #upload to firebase
                firebase = pyrebase.initialize_app(config)
                storage = firebase.storage()
                path_on_cloud = f'results/{today}.zip'
                storage.child(path_on_cloud).put(f'{final_directory}.zip')

                upload_url = storage.child(path_on_cloud).get_url(token=None)



                resultDisplayed["downloadLink"] = upload_url

                print(f'result directory {upload_url}')
                print(result)



                 #remove image from local directory
                shutil.rmtree(final_directory)
                os.remove(f'{final_directory}.zip') 

                '''
                for filename in os.listdir(final_directory):
                    file_path = os.path.join(final_directory, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print('Failed to delete %s. Reason: %s' % (file_path, e))
                '''

                return render_template("multipleImagesPopUp.html", data=resultDisplayed)

    else:
        return "Use a POST request to access this API, check documentation at "
    
    
    
@app.route("/predictImagesInFolder", methods=["POST", "GET"])
def predictImagesInFolder(): 

    if request.method == "POST":
        uploaded_files = request.files.getlist("image")
        apikey = request.form["apikey"]

        if not uploaded_files or not any(f for f in uploaded_files):
            flash('Please upload a folder')
            return redirect(url_for("multipleImagePredict"))
        else:

            config = {"apiKey":xxxxx",
                            "authDomain": "xxxxx.firebaseapp.com",
                            "databaseURL": "xxxxx.firebaseio.com",
                            "projectId": "xxxxx",
                            "storageBucket": "xxxxx.appspot.com",
                            "messagingSenderId": "xxxxx",
                            "appId": "1:xxxxx:web:xxxxx",
                            "measurementId": "xxxxx"}


            

            UPLOAD_FOLDER = './test/test'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
            
            
            saveFolder(uploaded_files)

            if not firebase_admin._apps:
                #fetch credentials
                cred = credentials.Certificate("service_account.json")
                firebase_admin.initialize_app(cred, {'databaseURL': 'https://xxxxx.firebaseio.com/'})


            ##validate API KEY
            ref = db.reference('ApiKey')
            apiKeyType = ref.child(apikey).child("type").get()

            if apiKeyType == None:
                flash('Invalid API Key')
                return redirect(url_for("oneImagePredict"))
            else:
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
                loaded_model = load_model('model/model1-94%.h5')
                #make prediciton
                predict = loaded_model.predict_generator(test_generator) 
                array  = np.array(predict)
                result = {}
                for i, rows in enumerate(array):
                    _class = np.argmax(rows)
                    result[uploaded_files[i].filename] = _class


                today = datetime.now()
                current_directory = os.getcwd()
                final_directory = os.path.join(current_directory, f'result_{today}')
                if not os.path.exists(final_directory):
                    os.makedirs(final_directory) 

                error = 0
                currentProgress = 0
                resultDisplayed = {}

                for key, value in result.items():
                    if value == 0:
                        #BAD BACKGROUND
                        if os.path.exists(f"{final_directory}/BAD_BACKGROUND") == True:
                            try:
                                shutil.move(f"{UPLOAD_FOLDER}/{key}" , f"{final_directory}/BAD_BACKGROUND")
                                resultDisplayed["BAD_BACKGROUND"] += 1
                            except:
                                error += 1
                        else:
                            #make directory
                            os.mkdir(f"{final_directory}/BAD_BACKGROUND")
                            try:
                                shutil.move(f"{UPLOAD_FOLDER}/{key}" , f"{final_directory}/BAD_BACKGROUND")
                                resultDisplayed["BAD_BACKGROUND"] = 1
                            except Exception as e:
                                error += 1
                            currentProgress +=1

                    elif value == 1:
                        #BLURRY
                        if os.path.exists(f"{final_directory}/BLURRY") == True:
                            try:
                                shutil.move(f"{UPLOAD_FOLDER}/{key}" , f"{final_directory}/BLURRY")
                                resultDisplayed["BLURRY"] += 1
                            except:
                                error += 1
                        else:
                            #make directory
                            os.mkdir(f"{final_directory}/BLURRY")
                            try:
                                shutil.move(f"{UPLOAD_FOLDER}/{key}" , f"{final_directory}/BLURRY")
                                resultDisplayed["BLURRY"] = 1
                            except Exception as e:
                                error += 1
                            currentProgress +=1

                    elif value == 2:
                        #FACE_IN_BACKGROUND
                        if os.path.exists(f"{final_directory}/FACE_IN_BACKGROUND") == True:
                            try:
                                shutil.move(f"{UPLOAD_FOLDER}/{key}" , f"{final_directory}/FACE_IN_BACKGROUND")
                                resultDisplayed["FACE_IN_BACKGROUND"] += 1
                            except:
                                error += 1
                        else:
                            #make directory
                            os.mkdir(f"{final_directory}/FACE_IN_BACKGROUND")
                            try:
                                shutil.move(f"{UPLOAD_FOLDER}/{key}" , f"{final_directory}/FACE_IN_BACKGROUND")
                                resultDisplayed["FACE_IN_BACKGROUND"] = 1
                            except Exception as e:
                                error += 1
                            currentProgress +=1

                    elif value == 3:
                        #GOOD_IMAGES
                        if os.path.exists(f"{final_directory}/GOOD_IMAGES") == True:
                            try:
                                shutil.move(f"{UPLOAD_FOLDER}/{key}" , f"{final_directory}/GOOD_IMAGES")
                                resultDisplayed["GOOD_IMAGES"] += 1
                            except:
                                error += 1
                        else:
                            #make directory
                            os.mkdir(f"{final_directory}/GOOD_IMAGES")
                            try:
                                shutil.move(f"{UPLOAD_FOLDER}/{key}" , f"{final_directory}/GOOD_IMAGES")
                                resultDisplayed["GOOD_IMAGES"] = 1
                            except Exception as e:
                                error += 1
                            currentProgress +=1


                    elif value == 4:
                        #INVALID_PASSPORT
                        if os.path.exists(f"{final_directory}/INVALID_PASSPORT") == True:
                            try:
                                shutil.move(f"{UPLOAD_FOLDER}/{key}" , f"{final_directory}/INVALID_PASSPORT")
                                resultDisplayed["INVALID_PASSPORT"] += 1
                            except:
                                error += 1
                        else:
                            #make directory
                            os.mkdir(f"{final_directory}/INVALID_PASSPORT")
                            try:
                                shutil.move(f"{UPLOAD_FOLDER}/{key}" , f"{final_directory}/INVALID_PASSPORT")
                                resultDisplayed["INVALID_PASSPORT"] = 1
                            except Exception as e:
                                error += 1
                            currentProgress +=1



                    elif value == 5:
                        #NO_HUMAN_FACE
                        if os.path.exists(f"{final_directory}/NO_HUMAN_FACE") == True:
                            try:
                                shutil.move(f"{UPLOAD_FOLDER}/{key}" , f"{final_directory}/NO_HUMAN_FACE")
                                resultDisplayed["NO_HUMAN_FACE"] += 1
                            except:
                                error += 1
                        else:
                            #make directory
                            os.mkdir(f"{final_directory}/NO_HUMAN_FACE")
                            try:
                                shutil.move(f"{UPLOAD_FOLDER}/{key}" , f"{final_directory}/NO_HUMAN_FACE")
                                resultDisplayed["NO_HUMAN_FACE"] = 1
                            except Exception as e:
                                error += 1
                            currentProgress +=1


                    elif value == 6:
                        #STAPLED_FACE
                        if os.path.exists(f"{final_directory}/STAPLED_FACE") == True:
                            try:
                                shutil.move(f"{UPLOAD_FOLDER}/{key}" , f"{final_directory}/STAPLED_FACE")
                                resultDisplayed["STAPLED_FACE"] += 1
                            except:
                                error += 1
                        else:
                            #make directory
                            os.mkdir(f"{final_directory}/STAPLED_FACE")
                            try:
                                shutil.move(f"{UPLOAD_FOLDER}/{key}" , f"{final_directory}/STAPLED_FACE")
                                resultDisplayed["STAPLED_FACE"] = 1
                            except Exception as e:
                                error += 1
                            currentProgress +=1
                                    
                #make zip file
                shutil.make_archive(f'result_{today}', 'zip', final_directory)

                #upload to firebase
                firebase = pyrebase.initialize_app(config)
                storage = firebase.storage()
                path_on_cloud = f'results/{today}.zip'
                storage.child(path_on_cloud).put(f'{final_directory}.zip')

                upload_url = storage.child(path_on_cloud).get_url(token=None)



                resultDisplayed["downloadLink"] = upload_url

                print(f'result directory {upload_url}')
                print(result)



                 #remove image from local directory
                shutil.rmtree(final_directory)
                os.remove(f'{final_directory}.zip') 

                return render_template("multipleFolderImagesPopUp.html", data=resultDisplayed)
    else:
        return "Use a POST request to access this API, check documentation at "
            



def saveFolder(uploaded_files):
    cwd = os.getcwd()
    config = {"apiKey": "xxxxx",
                "authDomain": "xxxxx.firebaseapp.com",
                "databaseURL": "https://xxxxx.firebaseio.com",
                "projectId": "xxxxx",
                "storageBucket": "xxxxx.appspot.com",
                "messagingSenderId": "xxxxx",
                "appId": "1:xxxxx:web:xxxxx",
                "measurementId": "G-FXCMDZNL6T"}


    for folder in uploaded_files:
        if type(folder) == list:
            saveFolder(folder)
        else:
            path = os.path.join('./test/test', folder.filename)
            folder_path  = f'{folder.filename.split("/")[:-1]}'
            folder_path = folder_path[2:-2]
            folder_path = folder_path.replace("\', \'", "/")
            filePath = f"{cwd}/test/test/{folder_path}" 
            if os.path.exists(filePath) == True:
                folder.save(f'{filePath}/{folder.filename.split("/")[-1]}')
            else:
                os.mkdir(filePath)
                folder.save(f'{filePath}/{folder.filename.split("/")[-1]}')

            #save to firebase
            today = datetime.now()

            firebase = pyrebase.initialize_app(config)
            storage = firebase.storage()
            path_on_cloud = f'images/{today}.jpg'
            storage.child(path_on_cloud).put(f'{filePath}/{folder.filename.split("/")[-1]}')

            upload_url = storage.child(path_on_cloud).get_url(token=None)


            


    '''
    UPLOAD_FOLDER = './test/test'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    for folder in uploaded_files:
        if folder == []:
            path = os.path.join(app.config['UPLOAD_FOLDER'], folder.filename)
            file.save(path)
        else:
            saveFolder(folder)
    
    '''

        
        
if __name__ == "_main_":
    app.run(debug=True)
        
        
        
        
        
        
        
