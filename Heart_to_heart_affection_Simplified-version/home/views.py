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

def start_gradio():
    subprocess.Popen(['python', 'yolov5_Simplified/gradio_test.py'])

def my_view(request):
    start_gradio()  # 启动 Gradio
    gradio_url = "http://127.0.0.1:7861"  # Gradio 生成的 URL
    return render(request, 'gradio.html', {'gradio_url': gradio_url})