import cv2

def update_detection_yolo(frame, model):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = model(frame_rgb, verbose=False)

    # Dicionário para armazenar o objeto com maior confiança para cada classe de interesse
    best_objects = {}
    for object in results[0]:
        box = object.boxes.data[0]
        confidence = box[4]
        class_id = int(box[5])

        if class_id in [67, 47]:
            if class_id not in best_objects or confidence > best_objects[class_id]['confidence']:
                best_objects[class_id] = {'object': object, 'confidence': confidence}

    # Extrair apenas os objetos do dicionário
    detected_objects = [info['object'] for info in best_objects.values()]

    return detected_objects