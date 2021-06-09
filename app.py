import os
import json
import requests
import SessionState
import streamlit as st
import tensorflow as tf
from utils import load_and_prep_image, predict_json

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "xxxxxxxxx.json" # change for your GCP key
REGION = "region" # change for your GCP region (where your model is hosted)

st.title("Welcome to SoNI (Solousi taNI)")
st.header("Ketahui penyakit tanaman anda!")

@st.cache # cache the function so predictions aren't always redone (Streamlit refreshes every click)
def make_prediction(image):
    """
    Takes an image and uses model (a trained TensorFlow model) to make a
    prediction.

    Returns:
     image (preproccessed)
     pred_class (prediction class from desease)
     pred_conf (model confidence)
    """
    #prediction name
    desease = [
        'Jagung bercak',
        'Jagung karat',
        'Jagung hawar',
        'Jagung sehat',
        'Kentang hawar dini',
        'Kentang hawar',
        'Kentang sehat',
        'Tomat bercak bakteri',
        'Tomat hawar dini',
        'Tomat hawar',
        'Tomat jamur',
        'Tomat bercak septoria',
        'Tomat tungau laba-laba ',
        'Tomat bercak target',
        'Tomat virus daun keriting kuning',
        'Tomat virus mosaic',
        'Tomat sehat'
    ]

    image = load_and_prep_image(image)
    # Turn tensors into int16 (saves space of ML Engine "limit of 1.5MB per request")
    image = tf.cast(tf.expand_dims(image, axis=0), tf.int16)
    # image = tf.expand_dims(image, axis=0)
    preds = predict_json(region=REGION,
                         instances=image)

    index = tf.argmax(preds[0])
    pred_class = desease[index]
    pred_conf = tf.reduce_max(preds[0])*100
    return image, pred_class, pred_conf


# File uploader allows user to add their image
uploaded_file = st.file_uploader(label="Upload gambar",
                                 type=["png", "jpeg", "jpg"])

# Setup session state to remember state of app so refresh isn't always needed
session_state = SessionState.get(pred_button=False)

# condition if user doesn't upload an image
if not uploaded_file:
    st.warning("Tolong upload gambar.")
    st.stop()
# else (user uploaded an image)
else:
    session_state.uploaded_image = uploaded_file.read()
    st.image(session_state.uploaded_image, use_column_width=True)
    pred_button = st.button("Predict")

# Did the user press the predict button?
if pred_button:
    session_state.pred_button = True 

#result
if session_state.pred_button:
    session_state.image, session_state.pred_class, session_state.pred_conf = make_prediction(session_state.uploaded_image)
    st.write(f"Penyakit: {session_state.pred_class}, \
               Kecocokan: {session_state.pred_conf:.2f}%")