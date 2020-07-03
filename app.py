from flask import Flask, redirect, url_for, render_template, request
import os
from flask_assets import Environment, Bundle

app = Flask(__name__)

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
        print(img_url, apikey)
        return ""

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
        
        
        
        
        
        
        
