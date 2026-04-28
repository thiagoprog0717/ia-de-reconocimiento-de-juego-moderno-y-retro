# ================================
# 1. IMPORTAR LIBRERÍAS
# ================================
import tensorflow as tf
import numpy as np
from PIL import Image, ImageOps
import os

def clasificador(img):
    # ================================
    # 3. CARGAR MODELO TFLITE
    # ================================
    interpreter = tf.lite.Interpreter(model_path="model.tflite")
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()


    # ================================
    # 4. CARGAR LABELS
    # ================================
    class_names = open("labels.txt").readlines()

    # ================================
    # 5. PREPROCESAR IMAGEN
    # ================================
    image = Image.open(img).convert("RGB")

    # Redimensionar a 224x224
    image = ImageOps.fit(image, (224, 224))

    # ⚠️ IMPORTANTE: modelo UINT8 → NO normalizar
    image_array = np.asarray(image).astype(np.uint8)

    # Expandir dimensiones (1, 224, 224, 3)
    data = np.expand_dims(image_array, axis=0)

    # ================================
    # 6. HACER PREDICCIÓN
    # ================================
    interpreter.set_tensor(input_details[0]['index'], data)
    interpreter.invoke()

    prediction = interpreter.get_tensor(output_details[0]['index'])

    # ================================
    # 7. RESULTADO
    # ================================
    index = np.argmax(prediction)
    scale, zero_point = output_details[0]['quantization']

    confidence = (prediction[0][index] - zero_point) * scale
    class_name = class_names[index]
    class_name = class_names[index][2:].strip()
    print(f"\n🔮 Predicción: {class_name.strip()} ({confidence*100:.2f}%)")
    return(class_name,confidence)