import streamlit as st
import cv2
import numpy as np
from PIL import Image

# 1. Set up the Streamlit page
st.set_page_config(page_title="Face Detector", page_icon="👤")

st.title("Simple Face Detection & Counting")
st.write("Upload an image, and this app will detect and count the faces in it using OpenCV.")

# 2. Load Haar Cascade Classifier
# Using caching so it only loads once
@st.cache_resource
def load_cascade():
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    return cv2.CascadeClassifier(cascade_path)

face_cascade = load_cascade()

# 3. Image uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 4. Read the image
    image = Image.open(uploaded_file)
    
    # Convert PIL Image to an OpenCV compatible numpy array
    img_array = np.array(image)
    
    # Handle different image formats (RGB, RGBA, Grayscale)
    if len(img_array.shape) == 3 and img_array.shape[2] == 3:
        img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    elif len(img_array.shape) == 3 and img_array.shape[2] == 4:
        img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGR)
    else:
        img_cv = img_array.copy()

    # Convert to grayscale for Haar Cascade
    if len(img_cv.shape) == 3:
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    else:
        gray = img_cv

    # 5. Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    
    # 6. Draw bounding boxes
    for (x, y, w, h) in faces:
        cv2.rectangle(img_cv, (x, y), (x+w, y+h), (0, 255, 0), 3)
        
    # Convert BGR back to RGB for Streamlit display
    if len(img_cv.shape) == 3:
        img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    else:
        img_rgb = img_cv
        
    # 7. Display the results
    st.image(img_rgb, caption="Processed Image", use_container_width=True)
    
    # Display the total face count
    if len(faces) > 0:
        st.success(f"Number of faces detected: {len(faces)}")
    else:
        st.warning("No faces detected in this image.")
