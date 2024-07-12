# modelo.py
import numpy as np
import os
import cv2
from keras.saving import load_model
from keras.preprocessing.image import img_to_array
from PIL import Image, ImageOps
import joblib


# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Obtén la ruta absoluta del directorio del script actual
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construye la ruta absoluta a los archivos del modelo y el codificador de etiquetas
model_path = os.path.join(script_dir, '..', 'Model', 'modelo_entrenado.h5')
label_encoder_path = os.path.join(script_dir, '..', 'Model', 'label_encoder.joblib')

# Carga del modelo entrenado y del codificador de etiquetas
model = load_model(model_path, compile=False)
label_encoder = joblib.load(label_encoder_path)
# Carga del modelo entrenado y del codificador de etiquetas
model = load_model(model_path, compile=False)
label_encoder = joblib.load(label_encoder_path)

# Función para aplicar ecualización de histograma a una imagen en color
def equalize_histogram_color(image):
    img_np = np.array(image)
    img_yuv = cv2.cvtColor(img_np, cv2.COLOR_RGB2YUV)
    img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
    img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)
    return Image.fromarray(img_output)

# Función para aplicar segmentación por K-means a una imagen en color
def segment_image_kmeans_color(image, k=4):
    image_np = np.array(image)
    image_lab = cv2.cvtColor(image_np, cv2.COLOR_RGB2Lab)
    pixel_values = image_lab.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_PP_CENTERS)
    centers = np.uint8(centers)
    segmented_image = centers[labels.flatten()]
    segmented_image = segmented_image.reshape(image_lab.shape)

    # Conversión de Lab a RGB
    segmented_image = cv2.cvtColor(segmented_image, cv2.COLOR_Lab2RGB)
    return Image.fromarray(segmented_image)

def ejecutar_modelo(path_img):
    # Apertura de la imagen y aplicación de los filtros para que el modelo la reconozca
    image = Image.open(path_img)
    equalized_image = equalize_histogram_color(image)
    segmented_image = segment_image_kmeans_color(equalized_image, k=4)

    # Aquí se pre-procesa la imagen, redimensionándola al tamaño de entrada esperado por el modelo, convirtiéndola en un array y normalizándola.
    processed_image = segmented_image.resize((224, 224))
    processed_image = img_to_array(processed_image)
    processed_image = processed_image / 255.0

    # Ya que el modelo espera una entrada de tipo (None, 224, 224, 3), se debe añadir una dimensión "Batch"
    processed_image = np.expand_dims(processed_image, axis=0)

    # Predicción y score de confianza
    prediction = model.predict(processed_image)
    index = np.argmax(prediction)
    confidence_score = format(prediction[0][index], '.4f')
    # Decodificación de la etiqueta para su impresión
    predicted_labels_encoded = np.argmax(prediction, axis=1)
    predicted_labels = label_encoder.inverse_transform(predicted_labels_encoded)

    return predicted_labels, confidence_score

