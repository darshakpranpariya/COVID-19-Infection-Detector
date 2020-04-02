import numpy as np
import cv2
import os
import tensorflow as tf
from django.http import HttpResponse
from django.shortcuts import render
from tensorflow.python.keras.models import model_from_json
from c19d.models import IM

def index(request):
    if request.method == 'POST':
        myfil = request.FILES['document']

        json_file = open('static/cnn/model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights("static/cnn/model.h5")
        print("Loaded model from disk")
        loaded_model.compile(loss='sparse_categorical_crossentropy',
                             optimizer='adam', metrics=['accuracy'])

        # return render(request,'index.html',c)
        answer = {"result":""}
        ob = IM(Img=request.FILES['document'])
        ob.save()
        print("images/" + str(request.FILES['document']))
        ia = cv2.imread("images/" + str(request.FILES['document']), cv2.IMREAD_GRAYSCALE)
        na = cv2.resize(ia, (50, 50))
        t = np.array(cv2.resize(ia, (50, 50)).reshape(-1, 50, 50, 1))
        t = tf.cast(t, tf.float32)
        print(t);
        p = loaded_model.predict(t,steps=1)
        if(p[0][0] == 1.0):
            answer["result"]="Not infected by coronavirus"
            # print("Not infected by coronavirus")
        else:
            answer["result"]="Infected by coronavirus"
            # print("Infected by coronavirus")
        ob.delete()
        os.remove("images/" + str(request.FILES['document']))
        return render(request,"index.html",answer)
    return render(request, 'index.html')
