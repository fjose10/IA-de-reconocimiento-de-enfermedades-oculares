import os
import numpy as np
from keras.preprocessing.image import load_img, img_to_array
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib


'''Este script sirve para entrenar al modelo. Utilizando unas funciones y los archivos de la carpeta "Training", ajusta el modelo.
En este caso está configurado para dos etiquetas solamente (Para las pruebas) pero hay que entrenarlo con todas las enfermedades.
Las imagenes fueron tratadas con Equalize-Histogram y segmentación por k-means de cv2. 
'''

def load_images_from_folder(folder, target_size):

    '''
    Esta función carga las imágenes desde el folder y les va asignando una etiqueta. Una por una, lee la imágen, la convierte en un array con keras
    y le asigna a label la etiqueta que corresponde al nombre de la carpeta. Al final, devuelve un array de numpy con la lista de todas las
    imagenes tratadas.
    '''

    images = []
    labels = []

    class_names = sorted(os.listdir(folder))

    for class_name in class_names:

        class_folder = os.path.join(folder, class_name)

        for filename in os.listdir(class_folder):
            img_path = os.path.join(class_folder, filename)
            img = load_img(img_path, target_size=target_size)
            img_array = img_to_array(img)
            images.append(img_array)
            labels.append(class_name)

    return np.array(images), np.array(labels)

#Path a la carpeta de entrenamiento
training_path = os.path.join('Training')

#Carga de las imágenes y normalización
X_data_1, Y_data = load_images_from_folder(training_path, (224, 224))
X_data = X_data_1 / 255.0

#Codificación de las etiquetas (En la función se le asignan 0's, 1's,...), pero como queremos ver el nombre de la enfermedad se codifican y el numero de ellas
label_encoder = LabelEncoder()
Y_data_encoded = label_encoder.fit_transform(Y_data)
num_classes = len(label_encoder.classes_)

#Esto almacena el "Codificador de etiquetas" para que sepan cúales son las etiquetas
joblib.dump(label_encoder, os.path.join('Model', 'label_encoder.joblib'))

#División de los datos de entrenamiento y validación
X_train, X_val, Y_train, Y_val = train_test_split(X_data, Y_data_encoded, test_size=0.25, random_state=1234)


#Definición del modelo (Esto puede ajustarse)
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(num_classes, activation='softmax')
])

#Compilación del modelo y entrenamiento con 10 épocas. 
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(X_train, Y_train, epochs=15, batch_size=32, validation_data=(X_val,Y_val))

#Path donde se almacenará el modelo y la función para guardarlo entrenado con todos los pesos. 
model.save(os.path.join('Model', 'modelo_entrenado.h5'))
