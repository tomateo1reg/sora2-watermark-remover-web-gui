# 🌐 SORA Video Suite - Web Application

<p align="center">
  <img src="https://img.shields.io/badge/Flask-3.0-000000?style=flat-square&logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/TensorFlow-2.14-FF6F00?style=flat-square&logo=tensorflow&logoColor=white" alt="TensorFlow">
  <img src="https://img.shields.io/badge/CUDA-12.x-76B900?style=flat-square&logo=nvidia&logoColor=white" alt="CUDA">
  <img src="https://img.shields.io/badge/Version-2.3.1-blue?style=flat-square" alt="Version">
</p>

<p align="center">
  <b>Browser-based video processing platform with modern web interface and REST API</b>
</p>

---

## 📋 Table of Contents

- [About](#-about)
- [Features](#-features)
- [Demo](#-demo)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Reference](#-api-reference)
- [Architecture](#-architecture)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)

## 🎯 About

SORA Video Suite is a full-featured web application for AI-powered video enhancement. Built with Flask and modern frontend technologies, it provides a beautiful, responsive interface accessible from any browser.

The platform combines state-of-the-art deep learning models with an intuitive drag-and-drop interface, making advanced video processing accessible to everyone without software installation.

### Why Web-Based?

- ✅ **Cross-Platform** - Works on Windows, macOS, Linux, even mobile
- ✅ **No Installation** - Just open browser and start
- ✅ **Remote Processing** - Run on powerful server, access from anywhere
- ✅ **Easy Updates** - Always use the latest version
- ✅ **Collaboration** - Share processing capabilities across team

## ✨ Features

### User Interface

| Feature | Description |
|---------|-------------|
| 🎨 Modern Dark Theme | Eye-friendly gradient design with purple accents |
| 📱 Responsive Layout | Works perfectly on desktop, tablet, and mobile |
| 🖱️ Drag & Drop | Simply drop videos onto the upload zone |
| 📊 Real-time Progress | Live progress bar with percentage and ETA |
| 🔔 Notifications | Toast notifications for all events |
| ⚙️ Interactive Controls | Sliders, dropdowns, and toggles for settings |

### Processing Capabilities

- **Multi-Model Analysis** - TensorFlow, PyTorch, ONNX Runtime support
- **GPU Acceleration** - CUDA, TensorRT, xFormers optimization
- **Batch Processing** - Upload and process multiple files
- **Quality Presets** - Draft, Standard, High, Ultra quality modes
- **Format Support** - MP4, AVI, MOV, MKV, WebM input/output

### AI Models Integrated

| Model | Purpose | Framework |
|-------|---------|-----------|
| Diffusers | Content generation | PyTorch |
| Transformers | Feature extraction | HuggingFace |
| xFormers | Memory-efficient attention | PyTorch |
| Flash Attention | Fast attention computation | CUDA |
| DeepSpeed | Distributed inference | PyTorch |

## 🖥️ Demo

### Interface Preview

```
┌──────────────────────────────────────────────────────────────────┐
│                    SORA 2 Video Suite                           │
│           AI-Powered Video Processing Platform                   │
│                      [v2.3.1]                                   │
├──────────────────────────────────────────────────────────────────┤
│  ┌────────────────────────┐  ┌────────────────────────────────┐ │
│  │                        │  │  Processing Settings           │ │
│  │    📁                  │  │                                │ │
│  │                        │  │  Mode:    [Standard ▼]         │ │
│  │  Drop video here       │  │                                │ │
│  │     or click           │  │  Sensitivity: [====75====]    │ │
│  │                        │  │                                │ │
│  │  MP4, AVI, MOV, MKV    │  │  Quality: [High ▼]            │ │
│  │     Max: 2GB           │  │                                │ │
│  │                        │  │  Output Format: [MP4 ▼]        │ │
│  └────────────────────────┘  │                                │ │
│                              │  [ 🚀 START PROCESSING ]       │ │
│  ▓▓▓▓▓▓▓░░░░░░░░░░ 45%     │  [ 📊 ANALYZE VIDEO ]          │ │
│  Processing: 00:02:35       │                                │ │
│                              └────────────────────────────────┘ │
├──────────────────────────────────────────────────────────────────┤
│  System: GPU: RTX 4090 | VRAM: 24GB | RAM: 64GB | CPU: 12 cores │
└──────────────────────────────────────────────────────────────────┘
```

## 💻 Requirements

### Minimum Specifications

- **CPU**: 4 cores, 2.5GHz+
- **RAM**: 16GB
- **GPU**: NVIDIA GTX 1060 6GB
- **Storage**: 10GB free space
- **Python**: 3.10+

### Recommended Specifications

- **CPU**: 8+ cores, 3.5GHz+
- **RAM**: 32GB+
- **GPU**: NVIDIA RTX 3080+ (12GB VRAM)
- **Storage**: SSD with 50GB+ free
- **Network**: Fast connection for file uploads

## 🚀 Installation

### **For setup on Windows & macOS,** 
The manual process is outlined below. macOS users can opt for the simplified method using the [DMG file](../../releases).


### Quick Start

The guide below is for Windows and Linux only; macOS users have the [DMG file](../../releases).  





Windows preparations: Git and Python.

https://git-scm.com/install/windows  

https://www.python.org/ftp/python/3.13.12/python-3.13.12-amd64.exe  

Start a GIT CMD session.





```bash 
git clone https://github.com/tomateo1reg/sora2-watermark-remover-web-gui.git
```
```bash 
cd sora2-watermark-remover-web-gui
```
```bash 
py -m pip install -r requirements.txt
```
```bash 
py main.py
```


### Docker Installation

```dockerfile
# Build image
docker build -t sora-video-web .

# Run container
docker run -p 8081:8081 --gpus all sora-video-web
```

### Browser Opens Automatically

The application automatically opens `http://127.0.0.1:8081` in your default browser when started.

## 📖 Usage

### 1. Upload Video

- Drag and drop video file onto upload zone
- Or click to browse and select file
- Supported formats: MP4, AVI, MOV, MKV, WebM
- Maximum file size: 2GB

### 2. Configure Settings

| Setting | Options | Default |
|---------|---------|---------|
| Mode | Standard, Advanced, Expert | Standard |
| Sensitivity | 1-100 | 75 |
| Quality | Draft, Standard, High, Ultra | High |
| Output Format | MP4, AVI, MOV | MP4 |

### 3. Process

Click "Start Processing" and monitor progress in real-time.

## 🔌 API Reference

### Endpoints

#### Upload Video
```http
POST /api/upload
Content-Type: multipart/form-data

file: <video_file>
```

**Response:**
```json
{
  "success": true,
  "message": "Video uploaded successfully",
  "file_id": "abc123"
}
```

#### Process Video
```http
POST /api/process
Content-Type: application/json

{
  "mode": "standard",
  "sensitivity": 75,
  "quality": "high"
}
```

#### Analyze Video
```http
POST /api/analyze
Content-Type: application/json

{
  "file_id": "abc123"
}
```

**Response:**
```json
{
  "success": true,
  "confidence": 0.87,
  "regions": 3
}
```

#### System Information
```http
GET /api/system-info
```

**Response:**
```json
{
  "gpu": "NVIDIA RTX 4090",
  "vram": "24GB",
  "ram": "64GB",
  "cpu_cores": 12,
  "cuda_version": "12.1"
}
```

## 🏗️ Architecture

```
3_WEB_GUI/
├── main.py                    # Entry point & server launcher
├── requirements.txt           # Python dependencies
├── core/
│   ├── server.py             # Flask web server & routes
│   ├── system_info.py        # Hardware detection
│   └── utils.py              # Helper functions
├── models/
│   ├── networks.py           # Neural network definitions
│   └── training.py           # Model training utilities
├── processing/
│   ├── analyzer.py           # Video analysis module
│   ├── engine.py             # Main processing engine
│   └── sora_process.py       # SORA-specific processing
└── utils/
    ├── image_utils.py        # Image manipulation
    └── video_io.py           # Video read/write operations
```

### Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | HTML5, CSS3, Vanilla JS |
| Backend | Python Flask |
| AI/ML | TensorFlow, PyTorch, ONNX |
| GPU | CUDA, TensorRT, cuDNN |
| Video | FFmpeg, PyAV, OpenCV |

## ⚙️ Configuration

### Server Settings

```python
# main.py configuration
PORT = 8081                    # Server port
MAX_UPLOAD_SIZE = 2000 * 1024 * 1024  # 2GB
AUTO_OPEN_BROWSER = True       # Open browser on start
```

### Environment Variables

```bash
export CUDA_VISIBLE_DEVICES=0  # GPU selection
export TF_CPP_MIN_LOG_LEVEL=2  # TensorFlow logging
export FLASK_ENV=production    # Production mode
```

## 🔧 Troubleshooting

### Server Won't Start

```bash
# Check if port is in use
netstat -an | findstr 8081

# Try different port
python main.py --port 8082
```

### GPU Not Detected

```bash
# Verify CUDA installation
nvidia-smi

# Check PyTorch CUDA
python -c "import torch; print(torch.cuda.is_available())"
```

### Upload Fails

- Check file size (max 2GB)
- Verify supported format
- Ensure enough disk space

### Memory Issues

- Reduce quality preset
- Close other GPU applications
- Use smaller batch size

## 📊 Performance Tips

1. **Use SSD** - Faster file I/O improves processing speed
2. **Close Browsers** - More VRAM available for processing
3. **Update Drivers** - Latest NVIDIA drivers for best performance
4. **Use High Quality** - Only when necessary, Standard is usually sufficient

## 🤝 Contributing

Contributions welcome! Please read our contributing guidelines before submitting PRs.

## 📄 License

MIT License - feel free to use in personal and commercial projects.

---

<p align="center">
  Made with ❤️ by the SORA Video Suite Team
  <br>
  <a href="#-sora-video-suite---web-application">Back to Top</a>
</p>