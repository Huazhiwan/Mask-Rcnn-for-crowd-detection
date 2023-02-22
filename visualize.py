import cv2
import numpy as np
import os
import sys
import coco
import utils
import model as modellib
import matplotlib
import matplotlib.pyplot as plt

ROOT_DIR = os.getcwd()

MODEL_DIR = os.path.join(ROOT_DIR, "logs")
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)


class InferenceConfig(coco.CocoConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1


config = InferenceConfig()
config.display()

model = modellib.MaskRCNN(
    mode="inference", model_dir=MODEL_DIR, config=config
)
model.load_weights(COCO_MODEL_PATH, by_name=True)
class_names = [
    'BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
               'bus', 'train', 'truck', 'boat', 'traffic light',
               'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
               'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
               'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
               'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
               'kite', 'baseball bat', 'baseball glove', 'skateboard',
               'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
               'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
               'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
               'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
               'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
               'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
               'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
               'teddy bear', 'hair drier', 'toothbrush'
]


def random_colors(N):
    np.random.seed(1)
    colors = [tuple(255 * np.random.rand(3)) for _ in range(N)]
    return colors


colors = random_colors(len(class_names))
class_dict = {
    name: color for name, color in zip(class_names, colors)
}


def apply_mask(image, mask, color, alpha=0.5):
    """apply mask to image"""
    for n, c in enumerate(color):
        image[:, :, n] = np.where(
            mask == 1,
            image[:, :, n] * (1 - alpha) + alpha * c,
            image[:, :, n]
        )
    return image


def display_instances(image, boxes, masks, ids, names, scores,fence):
    """
        take the image and results and apply the mask, box, and Label
    """
    n_instances = boxes.shape[0]
    people_count = 0
    people_in_fence = 0
    if not n_instances:
        print('NO INSTANCES TO DISPLAY')
    else:
        assert boxes.shape[0] == masks.shape[-1] == ids.shape[0]
    in_fence_flag = list(range(n_instances))
    for i in range(n_instances):
        if not np.any(boxes[i]):
            continue
        if i == 0:                  
            for j in range(n_instances):
                if names[ids[j]] == "person":
                    people_count = people_count+1
                    y1, x1, y2, x2 = boxes[j]
                    
                    if(is_in_poly([int((x1+x2)/2),(y2-1)],fence)==True):#框框下方中間
                        people_in_fence = people_in_fence+1
                        in_fence_flag[j] = 1
                    else:
                        in_fence_flag[j] = 0
                        
        if names[ids[i]] == "person":
            y1, x1, y2, x2 = boxes[i]
            label = names[ids[i]]
            color = class_dict[label]
            score = scores[i] if scores is not None else None
            caption = '{} {:.2f}'.format(label, score) if score else label
            mask = masks[:, :, i]
            
            
            image = apply_mask(image, mask, color)
            if(in_fence_flag[i]==1):
                image = cv2.rectangle(image, (x1, y1), (x2, y2), (0,97,255), 2)
                image = cv2.putText(
                    image, caption, (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,97,255), 2
                    )                
            else:
                image = cv2.rectangle(image, (x1, y1), (x2, y2), (0,255,0), 2)
                image = cv2.putText(
                    image, caption, (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0), 2
                    )   
            
            image = cv2.putText(image,'people count:'+str(people_count),(10,40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,(255,255,0))
            image = cv2.putText(image,'people in fence:'+str(people_in_fence),(10,70), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,(0,97,255))            
          
        
    return (people_count,people_in_fence,image)
    
def is_in_poly(p, poly):
    px, py = p
    flag = False
    i = 0
    length = len(poly)
    j = length - 1
    while i < length:
        x1, y1 = poly[i]
        x2, y2 = poly[j]
        if (x1 == px and y1 == py) or (x2 == px and y2 == py):
            flag = True
            break
        if y1 < py <= y2 or y2 < py <= y1:
            x = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
            if x == px:
                flag = True
                break
            elif x > px:
                flag = not flag
        j = i
        i += 1

    return flag
    

