import shutil

from django.contrib.sites import requests
from django.shortcuts import render
import torch
from django.http import JsonResponse
from django.views import View
from django.core.files.storage import FileSystemStorage
import os
import os
import requests
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import torch
import gradio as gr
from threading import Thread
from django.http import HttpResponse
import cv2
import numpy as np
from PIL import Image
import subprocess
# Create your views here.
def home(request):
    return render(request, 'home.html')

# def start_gradio():
#     subprocess.Popen(['python', 'yolov5_Simplified/gradio_test.py'])
#
# def my_view(request):
#     start_gradio()  # 启动 Gradio
#     gradio_url = "http://127.0.0.1:7861"  # Gradio 生成的 URL
#     return render(request, 'gradio.html', {'gradio_url': gradio_url})
# detection/views.py

import os
import subprocess
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# detection/views.py

# detection/views.py

# views.py

# views.py

# views.py

# views.py

# views.py

import os
import subprocess
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import shutil

YOLO_SCRIPT_PATH = r"D:\实训项目简洁版\Heart_to_heart_affection_Simplified-version - 副本 (2)\yolov5_Simplified\detect.py"
YOLO_WEIGHTS_PATH = r"D:\实训项目简洁版\Heart_to_heart_affection_Simplified-version - 副本 (2)\yolov5_Simplified\runs\train\exp18\weights\best.pt"
YOLO_SOURCE_DIR = os.path.join(settings.BASE_DIR, 'media', 'uploads')
YOLO_PROJECT_DIR = os.path.join(settings.BASE_DIR, 'media', 'detection')
YOLO_NAME = 'results'

def index(request):
    if request.method == 'POST' and 'upload' in request.POST:
        uploaded_file = request.FILES['image']
        fs = FileSystemStorage(location=YOLO_SOURCE_DIR)
        filename = fs.save(uploaded_file.name, uploaded_file)
        uploaded_file_url = fs.url(os.path.join('uploads', filename))

        request.session['uploaded_image'] = os.path.join(YOLO_SOURCE_DIR, filename)
        request.session['uploaded_image_url'] = uploaded_file_url

        request.session.pop('processed_image', None)
        request.session.pop('processed_image_url', None)
        request.session.pop('detected_classes', None)

        return render(request, 'index.html', {
            'uploaded_image_url': uploaded_file_url,
            'has_uploaded': True,
            'has_processed': False
        })

    elif request.method == 'POST' and 'detect' in request.POST:
        uploaded_image_path = request.session.get('uploaded_image')
        uploaded_image_url = request.session.get('uploaded_image_url')
        if not uploaded_image_path:
            return render(request, 'index.html', {'error_message': '请先上传图片'})

        try:
            # 捕获 detect.py 的输出
            result = subprocess.run([
                'python', YOLO_SCRIPT_PATH,
                '--weights', YOLO_WEIGHTS_PATH,
                '--source', YOLO_SOURCE_DIR,
                '--project', YOLO_PROJECT_DIR,
                '--name', YOLO_NAME,
                '--exist-ok'
            ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # 解析输出以提取种类信息
            output = result.stdout
            detected_classes = []
            detected_classes_line = ""
            for line in output.split('\n'):
                if "Detected classes:" in line:
                    detected_classes_line = line
                    break

            if detected_classes_line:
                # 提取种类信息
                detected_classes_str = detected_classes_line.split("Detected classes: ")[1]
                detected_classes = detected_classes_str.strip().split(", ")
                detected_classes = [cls.strip() for cls in detected_classes if cls.strip()]

            # 在视图中处理 detected_classes
            detected_classes = [cls.strip("[]'") for cls in detected_classes]

            result_filename = os.path.basename(uploaded_image_path)
            processed_image_path = os.path.join(YOLO_PROJECT_DIR, YOLO_NAME, result_filename)
            processed_image_url = f'/media/detection/{YOLO_NAME}/{result_filename}'

            request.session['processed_image'] = processed_image_path
            request.session['processed_image_url'] = processed_image_url
            request.session['detected_classes'] = detected_classes

            return render(request, 'index.html', {
                'uploaded_image_url': uploaded_image_url,
                'processed_image_url': processed_image_url,
                'has_uploaded': True,
                'has_processed': True,
                'detected_classes': detected_classes
            })

        except subprocess.CalledProcessError as e:
            return render(request, 'index.html', {'error_message': '检测失败，请重试'})

    elif request.method == 'POST' and 'clear' in request.POST:
        uploaded_image_path = request.session.get('uploaded_image')
        processed_image_path = request.session.get('processed_image')

        if uploaded_image_path and os.path.exists(uploaded_image_path):
            os.remove(uploaded_image_path)

        if processed_image_path and os.path.exists(processed_image_path):
            os.remove(processed_image_path)

        request.session.pop('uploaded_image', None)
        request.session.pop('uploaded_image_url', None)
        request.session.pop('processed_image', None)
        request.session.pop('processed_image_url', None)
        request.session.pop('detected_classes', None)

        return render(request, 'index.html', {
            'has_uploaded': False,
            'has_processed': False
        })

    return render(request, 'index.html', {
        'has_uploaded': False,
        'has_processed': False
    })

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import shutil

@csrf_exempt
def clear_images_on_exit(request):
    if request.method == 'POST':
        print("清除图片的请求已收到")  # 添加日志打印
        uploaded_image_path = request.session.get('uploaded_image')
        processed_image_path = request.session.get('processed_image')

        if uploaded_image_path and os.path.exists(uploaded_image_path):
            os.remove(uploaded_image_path)
            print(f"已删除图片: {uploaded_image_path}")

        if processed_image_path and os.path.exists(processed_image_path):
            os.remove(processed_image_path)
            print(f"已删除图片: {processed_image_path}")

        request.session.pop('uploaded_image', None)
        request.session.pop('uploaded_image_url', None)
        request.session.pop('processed_image', None)
        request.session.pop('processed_image_url', None)
        request.session.pop('detected_classes', None)

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})