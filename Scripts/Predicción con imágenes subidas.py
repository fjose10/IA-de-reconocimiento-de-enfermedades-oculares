import numpy as np
import os
import cv2
from keras.models import load_model
from keras.preprocessing.image import img_to_array 
from PIL import Image, ImageOps  
from sklearn.preprocessing import LabelEncoder
import joblib


# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

#Carga del modelo entrenado y del codificador de etiquetas
model = load_model(os.path.join('Model', 'modelo_entrenado.h5'), compile=False)
label_encoder = joblib.load(os.path.join('Model', 'label_encoder.joblib'))


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

    #Conversión de Lab a RGB
    segmented_image = cv2.cvtColor(segmented_image, cv2.COLOR_Lab2RGB)

    return Image.fromarray(segmented_image)

#Aquí va el path de la imágen a testear, la cual está en la carpeta "Testing"
path_img = 'Testing/Normal/2609_right.jpg'

#Apertura de la imágen y aplicación de los filtros para que el modelo la reconozca
equalized_image = equalize_histogram_color(Image.open(path_img))
segmented_image= segment_image_kmeans_color(equalized_image, k = 5)

#Aquí se pre-procesa la imágen, redimensionandola al tamaño de entrada esperado por el modelo, convirtiéndola en un array y normalizandola.
processed_image = segmented_image.resize((224, 224))
processed_image = img_to_array(processed_image)
processed_image = processed_image / 255.0 

#Ya que el modelo espera una entrada de tipo (None, 224, 224, 3), se debe añadir una dimensión "Batch" nula
processed_image = np.expand_dims(processed_image, axis=0)

#Predicción y score de confianza
prediction = model.predict(processed_image)
index = np.argmax(prediction)
confidence_score = prediction[0][index]

#Decodificación de la etiqueta para su impresión
predicted_labels_encoded = np.argmax(prediction, axis=1)
predicted_labels = label_encoder.inverse_transform(predicted_labels_encoded)

# Mostrar resultados
for label in predicted_labels:
    print("Etiqueta predicha:", label)
print("Confidence Score:", confidence_score)
