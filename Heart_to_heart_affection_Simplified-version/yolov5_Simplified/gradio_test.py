import torch
import gradio as gr

Title="宠物种类识别"
des="将图片放入指定区域提交"
model=torch.hub.load("./", "custom", path="runs/train/exp18/weights/best.pt",source="local")
base_conf , base_iou = 0.25, 0.45

def det_image(img,conf,iou):
    model.conf = conf
    model.iou = iou
    return model(img).render()[0]

gr.Interface(inputs=["image",gr.Slider(minimum=0,maximum=1,value=base_conf),gr.Slider(minimum=0,maximum=1,value=base_iou)],
             outputs=["image"],
             fn=det_image,
             title=Title,
             description=des,
             examples=[["yolov5_Simplified/006.jpg", base_conf, base_iou],["yolov5_Simplified/American Curl_12.jpg", base_conf, base_iou]]).launch()