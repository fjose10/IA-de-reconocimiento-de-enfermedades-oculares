## Tabla de contenidos

1. [OculaDetect](#Nombre)
2. [Descripción](#descripción)
3. [Arquitectura](#Arquitectura)
4. [Proceso](#Proceso)
5. [Estado del proyecto](#EstadoDelProyecto)

# Nombre
* OculaDetect

# Descripción
OculaDetect es un modelo de reconocimiento de imágenes de capas convolucionales capaz de reconocer y distinguir entre un ojo humano sano o con tres enfermedades oculares: retinopatía adiabática, glaucoma y cataratas. 

# Arquitectura

El proyecto utiliza una arquitectura basada en tensorflow y keras y en esencia es un modelo secuencial con dos capas convolucionales, dos capas de pooling y dos capas densas. Abajo se adjunta la estructura del modelo y el script que funciona para el entrenamiento del mismo:
![image](https://github.com/user-attachments/assets/39f89f24-6436-40c9-8e09-9c2c349ca638)

Los objetos "X_data" e "Y_data" provienen de imágenes pre-tratadas con diferentes filtros. 

# Proceso

-El dataset es obtenido de una recopilación de diferentes estudios y otros datasets de Kagle. El dataset completo se puede encontrar en el siguiente link: https://www.kaggle.com/datasets/gunavenkatdoddi/eye-diseases-classification/data
-Las imágenes de entrenamiento fueron pre-tratadas con dos filtros, un filtro equalizador que hace que la imágen sea más nítida y un filtro por segmentación de clústeres. El código que hace posible los filtros se muestra debajo.
![image](https://github.com/user-attachments/assets/6594cc73-9064-4e4b-b703-6409e67f55f1)

Las métricas de evaluación del modelo son simples, validándose en métodos de cuán preciso es en base a la división ya hecha por los humanos (accuracy) y brindando un puntaje de confianza a la hora de hacer una predicción. 
El modelo posee una interfaz simple en donde se puede escoger o subir una imagen de los archivos. Así, pudiera tenerse una imágen de cualquier otro dataset y aún así se le aplicarían los mismos filtros necesarios para hacer la predicción, lo que lo hace adaptable. 

# Estado del proyecto:
El proyecto está aún en proceso de mejoría, aunque ya es funcional. Se está hablando sobre implementar funcionalidades de mapa de calor, que pudieran funcionar para entender mejor cómo y por qué se detecta x o y enfermedad. 

# Actualización:
Se mejoró la interfaz y ahora se muestran tanto las imágenes filtradas como las imágenes originales. Adicionalmente, para ciertas pruebas donde el puntaje de confianza sea menor a 0.75, ahora se muestran las dos etiquetas con mayor puntaje.
