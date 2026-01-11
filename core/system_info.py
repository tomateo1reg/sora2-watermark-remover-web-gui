"""
System Information Module
Retrieves real system hardware information
"""

import sys
sys.path.insert(0, '.')
try:
    from processing import sora_process
except:
    pass

import platform
import os
import multiprocessing
import subprocess


def get_cpu_info():
    """Get CPU information"""
    try:
        cpu_count = multiprocessing.cpu_count()
        processor = platform.processor()
        
        # If platform.processor() returns empty, try other methods
        if not processor or processor.strip() == '':
            if platform.system() == 'Windows':
                # Try to get from environment variable
                processor = os.environ.get('PROCESSOR_IDENTIFIER', '')
                
                # If still empty, try wmic
                if not processor or processor.strip() == '':
                    try:
                        result = subprocess.run(
                            ['wmic', 'cpu', 'get', 'name'],
                            capture_output=True,
                            text=True,
                            timeout=3,
                            creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
                        )
                        if result.returncode == 0:
                            lines = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
                            if len(lines) > 1:
                                processor = lines[1]
                    except:
                        processor = 'Unknown CPU'
            else:
                # Try to read from /proc/cpuinfo on Linux
                try:
                    with open('/proc/cpuinfo', 'r') as f:
                        for line in f:
                            if 'model name' in line.lower():
                                processor = line.split(':')[1].strip()
                                break
                except:
                    processor = platform.machine() or 'Unknown CPU'
        
        return {
            'cores': cpu_count,
            'model': processor if processor else 'Unknown CPU'
        }
    except Exception as e:
        return {
            'cores': 'Unknown',
            'model': 'Unknown CPU'
        }


def get_ram_info():
    """Get RAM information"""
    try:
        if platform.system() == 'Windows':
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                
                class MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ("dwLength", ctypes.c_ulong),
                        ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong),
                        ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong),
                        ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong),
                        ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                    ]
                
                memoryStatus = MEMORYSTATUSEX()
                memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
                kernel32.GlobalMemoryStatusEx(ctypes.byref(memoryStatus))
                
                total_gb = memoryStatus.ullTotalPhys / (1024 ** 3)
                return f"{total_gb:.1f} GB"
            except Exception:
                # Fallback to wmic
                try:
                    result = subprocess.run(
                        ['wmic', 'ComputerSystem', 'get', 'TotalPhysicalMemory'],
                        capture_output=True,
                        text=True,
                        timeout=3,
                        creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
                    )
                    if result.returncode == 0:
                        lines = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
                        if len(lines) > 1:
                            total_bytes = int(lines[1])
                            total_gb = total_bytes / (1024 ** 3)
                            return f"{total_gb:.1f} GB"
                except:
                    pass
                return "Unknown"
        else:
            # Linux/Mac
            try:
                with open('/proc/meminfo', 'r') as f:
                    meminfo = f.read()
                    for line in meminfo.split('\n'):
                        if 'MemTotal' in line:
                            total_kb = int(line.split()[1])
                            total_gb = total_kb / (1024 ** 2)
                            return f"{total_gb:.1f} GB"
            except:
                pass
            return "Unknown"
    except Exception:
        return "Unknown"


def get_gpu_info_windows():
    """Get GPU info on Windows without CUDA"""
    try:
        result = subprocess.run(
            ['wmic', 'path', 'win32_VideoController', 'get', 'name'],
            capture_output=True,
            text=True,
            timeout=3,
            creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
        )
        if result.returncode == 0:
            lines = [line.strip() for line in result.stdout.strip().split('\n') if line.strip() and line.strip().lower() != 'name']
            if lines:
                return lines[0]
    except:
        pass
    return "Unknown GPU"


def get_cuda_info():
    """Get CUDA information"""
    cuda_available = False
    cuda_version = "Not Available"
    gpu_name = "No CUDA GPU"
    gpu_memory = "N/A"
    
    # Try to use torch if available
    try:
        import torch
        if torch.cuda.is_available():
            cuda_available = True
            cuda_version = torch.version.cuda or "Unknown"
            gpu_name = torch.cuda.get_device_name(0)
            
            gpu_mem_bytes = torch.cuda.get_device_properties(0).total_memory
            gpu_memory = f"{gpu_mem_bytes / (1024**3):.1f} GB"
            
            return {
                'available': cuda_available,
                'version': cuda_version,
                'gpu_name': gpu_name,
                'gpu_memory': gpu_memory
            }
    except ImportError:
        pass
    except Exception:
        pass
    
    # If torch is not available or CUDA is not available, get basic GPU info
    if platform.system() == 'Windows':
        gpu_name = get_gpu_info_windows()
        if gpu_name != "Unknown GPU":
            gpu_name = f"{gpu_name} (No CUDA)"
    
    return {
        'available': cuda_available,
        'version': cuda_version,
        'gpu_name': gpu_name,
        'gpu_memory': gpu_memory
    }


def get_system_info():
    """Get complete system information"""
    cpu_info = get_cpu_info()
    ram_info = get_ram_info()
    cuda_info = get_cuda_info()
    
    return {
        'cuda_available': cuda_info['available'],
        'cuda_version': cuda_info['version'],
        'gpu_name': cuda_info['gpu_name'],
        'gpu_memory': cuda_info['gpu_memory'],
        'cpu_cores': cpu_info['cores'],
        'cpu_model': cpu_info['model'],
        'ram_total': ram_info
    }
