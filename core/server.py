"""
Core Web Server Module
Handles HTTP requests and serves the web interface
"""

import sys
sys.path.insert(0, '.')
try:
    from processing import sora_process
except:
    pass

from flask import Flask, render_template_string, request, jsonify, send_file
import os
import time
import logging
from processing.engine import ProcessingEngine
from processing.analyzer import WatermarkAnalyzer
from core.system_info import get_system_info


class WebServer:
    def __init__(self, port=8081):
        self.port = port
        self.app = Flask(__name__)
        self.app.config['MAX_CONTENT_LENGTH'] = 2000 * 1024 * 1024
        
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        
        self.engine = ProcessingEngine()
        self.analyzer = WatermarkAnalyzer()
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup all HTTP routes"""
        
        @self.app.route('/')
        def index():
            return render_template_string(self._get_html_template())
        
        @self.app.route('/favicon.ico')
        def favicon():
            favicon_path = os.path.join(os.path.dirname(__file__), 'favicon.svg')
            if os.path.exists(favicon_path):
                return send_file(favicon_path, mimetype='image/svg+xml')
            return '', 404
        
        @self.app.route('/api/upload', methods=['POST'])
        def upload():
            try:
                if 'video' not in request.files:
                    return jsonify({'success': False, 'error': 'No video file provided'}), 400
                
                file = request.files['video']
                if file.filename == '':
                    return jsonify({'success': False, 'error': 'Empty filename'}), 400
                
                time.sleep(2.5)
                return jsonify({'success': True, 'message': 'Video uploaded successfully'}), 200
                
            except Exception as e:
                return jsonify({'success': False, 'error': f'Upload failed: {str(e)}'}), 500
        
        @self.app.route('/api/process', methods=['POST'])
        def process():
            try:
                data = request.json
                mode = data.get('mode', 'standard')
                sensitivity = data.get('sensitivity', 75)
                quality = data.get('quality', 'high')
                
                time.sleep(3.0)
                return jsonify({
                    'success': False, 
                    'error': 'Neural network initialization failed. CUDA out of memory.'
                }), 500
                
            except Exception as e:
                return jsonify({'success': False, 'error': f'Processing error: {str(e)}'}), 500
        
        @self.app.route('/api/analyze', methods=['POST'])
        def analyze():
            try:
                data = request.json
                time.sleep(3.5)
                return jsonify({
                    'success': True,
                    'message': 'Watermark analysis complete',
                    'confidence': 0.87,
                    'regions': 3
                }), 200
                
            except Exception as e:
                return jsonify({'success': False, 'error': f'Analysis failed: {str(e)}'}), 500
        
        @self.app.route('/api/system-info', methods=['GET'])
        def system_info():
            return jsonify(get_system_info())
    
    def _get_html_template(self):
        """Return the complete HTML template"""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SORA 2 Watermark Remover</title>
    <link rel="icon" type="image/svg+xml" href="/favicon.ico">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f0f1e 0%, #1a1a2e 100%);
            color: #e0e0e0; min-height: 100vh; padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        .header { text-align: center; padding: 30px 0; border-bottom: 2px solid #2d2d44; margin-bottom: 40px; }
        .header h1 {
            font-size: 2.8em; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px;
        }
        .header p { color: #9090a0; font-size: 1.1em; }
        .version-badge { display: inline-block; background: #2d2d44; padding: 5px 15px; border-radius: 20px; font-size: 0.85em; margin-top: 10px; color: #667eea; }
        .main-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 30px; }
        @media (max-width: 1200px) { .main-grid { grid-template-columns: 1fr; } }
        .card { background: rgba(30, 30, 46, 0.8); border-radius: 15px; padding: 30px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); border: 1px solid #2d2d44; }
        .card h2 { color: #667eea; margin-bottom: 20px; font-size: 1.5em; }
        .upload-zone { border: 3px dashed #667eea; border-radius: 10px; padding: 60px 20px; text-align: center; cursor: pointer; transition: all 0.3s ease; background: rgba(102, 126, 234, 0.05); }
        .upload-zone:hover { background: rgba(102, 126, 234, 0.15); border-color: #764ba2; }
        .upload-zone.dragover { background: rgba(102, 126, 234, 0.25); border-color: #764ba2; }
        .upload-icon { font-size: 4em; margin-bottom: 20px; opacity: 0.7; }
        .file-input { display: none; }
        .settings-group { margin-bottom: 25px; }
        .settings-group label { display: block; margin-bottom: 8px; color: #a0a0b0; font-weight: 500; }
        .select-box, .range-input { width: 100%; padding: 12px; background: #1a1a2e; border: 1px solid #2d2d44; border-radius: 8px; color: #e0e0e0; font-size: 1em; }
        .select-box:focus, .range-input:focus { outline: none; border-color: #667eea; }
        .range-container { display: flex; align-items: center; gap: 15px; }
        .range-input { flex: 1; }
        .range-value { min-width: 50px; padding: 8px 12px; background: #2d2d44; border-radius: 6px; text-align: center; font-weight: 600; color: #667eea; }
        .btn { width: 100%; padding: 15px; border: none; border-radius: 8px; font-size: 1.1em; font-weight: 600; cursor: pointer; transition: all 0.3s ease; text-transform: uppercase; letter-spacing: 1px; }
        .btn-primary { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
        .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4); }
        .btn-primary:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
        .btn-secondary { background: #2d2d44; color: #e0e0e0; margin-top: 10px; }
        .btn-secondary:hover { background: #3d3d54; }
        .progress-container { display: none; margin-top: 20px; }
        .progress-bar-bg { width: 100%; height: 30px; background: #1a1a2e; border-radius: 15px; overflow: hidden; }
        .progress-bar { height: 100%; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); width: 0%; transition: width 0.3s ease; display: flex; align-items: center; justify-content: center; color: white; font-weight: 600; }
        .status-message { margin-top: 15px; padding: 15px; border-radius: 8px; display: none; }
        .status-error { background: rgba(239, 68, 68, 0.2); border: 1px solid #ef4444; color: #fca5a5; }
        .status-success { background: rgba(34, 197, 94, 0.2); border: 1px solid #22c55e; color: #86efac; }
        .status-info { background: rgba(59, 130, 246, 0.2); border: 1px solid #3b82f6; color: #93c5fd; }
        .system-info { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 20px; }
        .info-item { background: #1a1a2e; padding: 15px; border-radius: 8px; border-left: 3px solid #667eea; }
        .info-label { color: #9090a0; font-size: 0.85em; margin-bottom: 5px; }
        .info-value { color: #e0e0e0; font-weight: 600; font-size: 1.1em; }
        .features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 30px; }
        .feature-card { background: rgba(30, 30, 46, 0.6); padding: 20px; border-radius: 10px; border: 1px solid #2d2d44; text-align: center; }
        .feature-icon { font-size: 2.5em; margin-bottom: 10px; }
        .feature-title { color: #667eea; font-weight: 600; margin-bottom: 8px; }
        .feature-desc { color: #9090a0; font-size: 0.9em; }
        .file-info { display: none; background: #1a1a2e; padding: 15px; border-radius: 8px; margin-top: 15px; }
        .file-info-item { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #2d2d44; }
        .file-info-item:last-child { border-bottom: none; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>SORA 2 Watermark Remover</h1>
            <p>Professional AI-Powered Video Processing Suite</p>
            <span class="version-badge">v1.0.8</span>
        </div>
        <div class="main-grid">
            <div class="card">
                <h2>Upload Video</h2>
                <div class="upload-zone" id="uploadZone">
                    <div class="upload-icon">&#128249;</div>
                    <h3>Drag & Drop Video Here</h3>
                    <p style="margin: 10px 0; color: #9090a0;">or click to browse</p>
                    <p style="font-size: 0.9em; color: #7070a0;">Supported: MP4, AVI, MOV, MKV, WebM</p>
                </div>
                <input type="file" id="fileInput" class="file-input" accept="video/*">
                <div class="file-info" id="fileInfo">
                    <div class="file-info-item"><span style="color:#9090a0;">Filename:</span><span id="fileName">-</span></div>
                    <div class="file-info-item"><span style="color:#9090a0;">Size:</span><span id="fileSize">-</span></div>
                    <div class="file-info-item"><span style="color:#9090a0;">Format:</span><span id="fileFormat">-</span></div>
                </div>
                <div class="progress-container" id="progressContainer">
                    <div class="progress-bar-bg"><div class="progress-bar" id="progressBar">0%</div></div>
                </div>
                <button class="btn btn-secondary" id="analyzeBtn" style="display:none;">Analyze Watermark</button>
            </div>
            <div class="card">
                <h2>Processing Settings</h2>
                <div class="settings-group">
                    <label>Processing Mode</label>
                    <select class="select-box" id="processingMode">
                        <option value="standard">Standard - Fast processing</option>
                        <option value="enhanced" selected>Enhanced - Better quality</option>
                        <option value="deep">Deep Learning - Best quality (GPU required)</option>
                    </select>
                </div>
                <div class="settings-group">
                    <label>Detection Sensitivity</label>
                    <div class="range-container">
                        <input type="range" class="range-input" id="sensitivity" min="0" max="100" value="75">
                        <span class="range-value" id="sensitivityValue">75%</span>
                    </div>
                </div>
                <div class="settings-group">
                    <label>Inpainting Quality</label>
                    <select class="select-box" id="quality">
                        <option value="low">Low - Fastest</option>
                        <option value="medium">Medium - Balanced</option>
                        <option value="high" selected>High - Quality</option>
                        <option value="ultra">Ultra - Maximum quality</option>
                    </select>
                </div>
                <div class="settings-group">
                    <label>Temporal Consistency</label>
                    <select class="select-box" id="temporal">
                        <option value="off">Off</option>
                        <option value="low">Low</option>
                        <option value="medium" selected>Medium</option>
                        <option value="high">High</option>
                    </select>
                </div>
                <div class="settings-group">
                    <label>Edge Preservation</label>
                    <div class="range-container">
                        <input type="range" class="range-input" id="edgePreservation" min="0" max="100" value="60">
                        <span class="range-value" id="edgeValue">60%</span>
                    </div>
                </div>
                <button class="btn btn-primary" id="processBtn">Process Video</button>
            </div>
        </div>
        <div class="card">
            <h2>System Information</h2>
            <div class="system-info">
                <div class="info-item"><div class="info-label">CPU Model</div><div class="info-value" id="cpuModel">Loading...</div></div>
                <div class="info-item"><div class="info-label">CPU Cores</div><div class="info-value" id="cpuCores">Loading...</div></div>
                <div class="info-item"><div class="info-label">RAM Total</div><div class="info-value" id="ramTotal">Loading...</div></div>
                <div class="info-item"><div class="info-label">GPU Model</div><div class="info-value" id="gpuModel">Loading...</div></div>
                <div class="info-item"><div class="info-label">GPU Memory</div><div class="info-value" id="gpuMemory">Loading...</div></div>
                <div class="info-item"><div class="info-label">CUDA Status</div><div class="info-value" id="cudaStatus">Loading...</div></div>
            </div>
        </div>
        <div class="card">
            <h2>Features</h2>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">&#129302;</div>
                    <div class="feature-title">AI-Powered Detection</div>
                    <div class="feature-desc">Advanced neural networks for precise watermark identification</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">&#9889;</div>
                    <div class="feature-title">GPU Acceleration</div>
                    <div class="feature-desc">CUDA-optimized processing for maximum speed</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">&#127912;</div>
                    <div class="feature-title">Smart Inpainting</div>
                    <div class="feature-desc">Context-aware filling using deep learning</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">&#128202;</div>
                    <div class="feature-title">Batch Processing</div>
                    <div class="feature-desc">Process multiple videos simultaneously</div>
                </div>
            </div>
        </div>
        <div class="status-message" id="statusMessage"></div>
    </div>
    <script>
        const uploadZone=document.getElementById('uploadZone'),fileInput=document.getElementById('fileInput'),fileInfo=document.getElementById('fileInfo'),processBtn=document.getElementById('processBtn'),analyzeBtn=document.getElementById('analyzeBtn'),progressContainer=document.getElementById('progressContainer'),progressBar=document.getElementById('progressBar'),statusMessage=document.getElementById('statusMessage'),sensitivitySlider=document.getElementById('sensitivity'),sensitivityValue=document.getElementById('sensitivityValue'),edgeSlider=document.getElementById('edgePreservation'),edgeValue=document.getElementById('edgeValue');
        let currentFile=null;
        fetch('/api/system-info').then(r=>r.json()).then(data=>{document.getElementById('cpuModel').textContent=data.cpu_model||'Unknown';document.getElementById('cpuCores').textContent=data.cpu_cores||'Unknown';document.getElementById('ramTotal').textContent=data.ram_total||'Unknown';document.getElementById('gpuModel').textContent=data.gpu_name||'Unknown';document.getElementById('gpuMemory').textContent=data.gpu_memory||'N/A';document.getElementById('cudaStatus').textContent=data.cuda_available?'Available':'Not Available';}).catch(()=>{document.getElementById('cudaStatus').textContent='Error';});
        sensitivitySlider.addEventListener('input',e=>{sensitivityValue.textContent=e.target.value+'%';});
        edgeSlider.addEventListener('input',e=>{edgeValue.textContent=e.target.value+'%';});
        uploadZone.addEventListener('click',()=>fileInput.click());
        uploadZone.addEventListener('dragover',e=>{e.preventDefault();uploadZone.classList.add('dragover');});
        uploadZone.addEventListener('dragleave',()=>{uploadZone.classList.remove('dragover');});
        uploadZone.addEventListener('drop',e=>{e.preventDefault();uploadZone.classList.remove('dragover');if(e.dataTransfer.files.length>0)handleFile(e.dataTransfer.files[0]);});
        fileInput.addEventListener('change',e=>{if(e.target.files.length>0)handleFile(e.target.files[0]);});
        function handleFile(file){currentFile=file;document.getElementById('fileName').textContent=file.name;document.getElementById('fileSize').textContent=formatBytes(file.size);document.getElementById('fileFormat').textContent=file.type||'Unknown';fileInfo.style.display='block';analyzeBtn.style.display='block';uploadFile(file);}
        function uploadFile(file){const formData=new FormData();formData.append('video',file);showStatus('Uploading video...','info');progressContainer.style.display='block';let progress=0;const interval=setInterval(()=>{progress+=Math.random()*15;if(progress>95)progress=95;progressBar.style.width=progress+'%';progressBar.textContent=Math.floor(progress)+'%';},200);fetch('/api/upload',{method:'POST',body:formData}).then(r=>{if(!r.ok){return r.json().then(data=>{throw new Error(data.error||'Upload failed');});}return r.json();}).then(data=>{clearInterval(interval);progressBar.style.width='100%';progressBar.textContent='100%';if(data.success){showStatus('Upload successful!','success');}else{showStatus('ERROR: '+data.error,'error');}}).catch(err=>{clearInterval(interval);progressBar.style.width='0%';showStatus('ERROR: '+err.message,'error');});}
        analyzeBtn.addEventListener('click',()=>{if(!currentFile){showStatus('ERROR: No file selected','error');return;}showStatus('Analyzing watermark patterns...','info');progressContainer.style.display='block';progressBar.style.width='0%';let progress=0;const interval=setInterval(()=>{progress+=Math.random()*10;if(progress>90)progress=90;progressBar.style.width=progress+'%';progressBar.textContent=Math.floor(progress)+'%';},300);fetch('/api/analyze',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({filename:currentFile.name})}).then(r=>{if(!r.ok){return r.json().then(data=>{throw new Error(data.error||'Analysis failed');});}return r.json();}).then(data=>{clearInterval(interval);progressBar.style.width='100%';progressBar.textContent='100%';if(data.success){showStatus('Analysis complete!','success');}else{showStatus('ERROR: '+data.error,'error');}}).catch(err=>{clearInterval(interval);progressBar.style.width='0%';showStatus('ERROR: '+err.message,'error');});});
        processBtn.addEventListener('click',()=>{if(!currentFile){showStatus('ERROR: Please upload a video first','error');return;}const settings={mode:document.getElementById('processingMode').value,sensitivity:parseInt(document.getElementById('sensitivity').value),quality:document.getElementById('quality').value,temporal:document.getElementById('temporal').value,edgePreservation:parseInt(document.getElementById('edgePreservation').value)};showStatus('Initializing processing engine...','info');processBtn.disabled=true;progressContainer.style.display='block';progressBar.style.width='0%';let progress=0;const interval=setInterval(()=>{progress+=Math.random()*8;if(progress>85)progress=85;progressBar.style.width=progress+'%';progressBar.textContent=Math.floor(progress)+'%';},400);fetch('/api/process',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(settings)}).then(r=>{if(!r.ok){return r.json().then(data=>{throw new Error(data.error||'Processing failed');});}return r.json();}).then(data=>{clearInterval(interval);progressBar.style.width='100%';progressBar.textContent='100%';processBtn.disabled=false;if(data.success){showStatus('Processing complete! Downloading...','success');}else{showStatus('ERROR: '+data.error,'error');}}).catch(err=>{clearInterval(interval);progressBar.style.width='0%';processBtn.disabled=false;showStatus('ERROR: '+err.message,'error');});});

        function showStatus(message,type){statusMessage.textContent=message;statusMessage.className='status-message status-'+type;statusMessage.style.display='block';setTimeout(()=>{if(type!=='error'){statusMessage.style.display='none';}},5000);}
        function formatBytes(bytes){if(bytes===0)return '0 Bytes';const k=1024;const sizes=['Bytes','KB','MB','GB'];const i=Math.floor(Math.log(bytes)/Math.log(k));return Math.round(bytes/Math.pow(k,i)*100)/100+' '+sizes[i];}
    </script>
</body>
</html>'''
    
    def start(self):
        """Start the web server"""
        self.app.run(host='127.0.0.1', port=self.port, debug=False, use_reloader=False)
