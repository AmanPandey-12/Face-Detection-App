import { useState, useRef } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [isDragging, setIsDragging] = useState(false)
  
  const fileInputRef = useRef(null)

  const handleFileChange = (e) => {
    const selected = e.target.files[0]
    if (selected && selected.type.startsWith('image/')) {
      setFile(selected)
      setPreview(URL.createObjectURL(selected))
      setResult(null)
      setError(null)
    } else {
      setError("Please select a valid image file.")
    }
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)
    const dropped = e.dataTransfer.files[0]
    if (dropped && dropped.type.startsWith('image/')) {
      setFile(dropped)
      setPreview(URL.createObjectURL(dropped))
      setResult(null)
      setError(null)
    } else {
      setError("Please drop a valid image file.")
    }
  }

  const handleUploadClick = () => {
    fileInputRef.current.click()
  }

  const processImage = async () => {
    if (!file) return

    setLoading(true)
    setError(null)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await axios.post('http://localhost:8000/detect', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      if (response.data.error) {
        setError(response.data.error)
      } else {
        setResult({
          faceCount: response.data.face_count,
          processedImage: response.data.processed_image
        })
      }
    } catch (err) {
      setError("Failed to connect to the server. Is the FastAPI backend running?")
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const resetAll = () => {
    setFile(null)
    setPreview(null)
    setResult(null)
    setError(null)
  }

  return (
    <div className="app-container">
      <div className="header">
        <h1 className="title">FaceSight</h1>
        <p className="subtitle">AI-powered facial detection & counting</p>
      </div>

      <div className="glass-card">
        {loading ? (
          <div className="loader-container">
            <div className="loader"></div>
            <h3>Analyzing deep features...</h3>
            <p className="upload-subtext">Running Haar Cascade algorithms</p>
          </div>
        ) : result ? (
          <div className="results-container">
            <div className="stats-card">
              <div className="stat-item">
                <span className="stat-label">Faces Detected</span>
                <span className="stat-value">{result.faceCount}</span>
              </div>
              <button className="btn btn-secondary" onClick={resetAll}>
                Try Another
              </button>
            </div>
            
            <div className="image-preview">
              <img src={result.processedImage} alt="Processed with faces detected" />
            </div>
          </div>
        ) : preview ? (
          <div className="results-container">
            <div className="image-preview">
              <img src={preview} alt="Upload preview" />
            </div>
            <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
              <button className="btn btn-secondary" onClick={resetAll}>
                Cancel
              </button>
              <button className="btn" onClick={processImage}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                  <polyline points="17 8 12 3 7 8"></polyline>
                  <line x1="12" y1="3" x2="12" y2="15"></line>
                </svg>
                Detect Faces
              </button>
            </div>
          </div>
        ) : (
          <div 
            className={`upload-area ${isDragging ? 'dragging' : ''}`}
            onClick={handleUploadClick}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            <svg className="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
              <circle cx="8.5" cy="8.5" r="1.5"></circle>
              <polyline points="21 15 16 10 5 21"></polyline>
            </svg>
            <div className="upload-text">Drag & drop your image here</div>
            <div className="upload-subtext">or click to browse from your computer</div>
            <input 
              type="file" 
              className="file-input" 
              ref={fileInputRef} 
              onChange={handleFileChange} 
              accept="image/jpeg, image/png, image/jpg" 
            />
          </div>
        )}

        {error && <div className="error-message">{error}</div>}
      </div>
    </div>
  )
}

export default App
