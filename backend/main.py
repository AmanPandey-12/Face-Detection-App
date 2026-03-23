from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from PIL import Image
import io
import base64

app = FastAPI(title="Face Detection API")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for simplicity and local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Haar Cascade
cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascade_path)

@app.get("/")
def home():
    return {"message": "Face Detection API is running"}

@app.post("/detect")
async def detect_faces(file: UploadFile = File(...)):
    try:
        # Read image contents
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Convert PIL Image to OpenCV format
        img_array = np.array(image)
        
        # Handle different image formats
        if len(img_array.shape) == 3 and img_array.shape[2] == 3:
            img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        elif len(img_array.shape) == 3 and img_array.shape[2] == 4:
            img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGR)
        else:
            img_cv = img_array.copy()

        # Convert to grayscale for detection
        if len(img_cv.shape) == 3:
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        else:
            gray = img_cv

        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        # Draw bounding boxes (green)
        for (x, y, w, h) in faces:
            cv2.rectangle(img_cv, (x, y), (x+w, y+h), (0, 255, 0), 3)
            
        # Convert resulting image to JPEG format
        success, encoded_image = cv2.imencode('.jpg', img_cv)
        if not success:
            return {"error": "Could not process image"}
            
        # Convert to base64 for returning to frontend
        b64_image = base64.b64encode(encoded_image.tobytes()).decode('utf-8')
        base64_string = f"data:image/jpeg;base64,{b64_image}"

        return {
            "face_count": len(faces),
            "processed_image": base64_string
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
