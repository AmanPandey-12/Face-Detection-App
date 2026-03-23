import requests
import sys

url = 'http://localhost:8000/detect'
try:
    with open('assets/hero_preview.png', 'rb') as f:
        files = {'file': f}
        response = requests.post(url, files=files)
        
        print("Status:", response.status_code)
        data = response.json()
        
        if "error" in data:
            print("Error from server:", data["error"])
            sys.exit(1)
            
        print("Success! Response contains:")
        print("Keys:", data.keys())
        print("Face Count:", data.get("face_count"))
        if "processed_image" in data and data["processed_image"].startswith("data:image/jpeg;base64,"):
            print("Valid base64 image received!")
        else:
            print("Invalid image format received")
            sys.exit(1)
except Exception as e:
    print("Failed to test API:", e)
    sys.exit(1)
