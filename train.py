import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split


data_path = "data"


def load_images(folder_path, label):
    images = []
    for filename in os.listdir(folder_path):
        img_path = os.path.join(folder_path, filename)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is not None:
            img = cv2.resize(img, (24, 24)) 
            images.append((img, label))
    return images


train_closed = load_images(os.path.join(data_path, "train/close eyes"), 0)
train_open   = load_images(os.path.join(data_path, "train/open eyes"), 1)


test_closed = load_images(os.path.join(data_path, "test/close eyes"), 0)
test_open   = load_images(os.path.join(data_path, "test/open eyes"), 1)


data = train_closed + train_open + test_closed + test_open

X = np.array([item[0] for item in data]).reshape(-1, 24, 24, 1) / 255.0
y = np.array([item[1] for item in data])
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense 
from sklearn.model_selection import train_test_split


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(24,24,1)),
    MaxPooling2D(2,2),
    Dropout(0.2),

    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Dropout(0.3),

    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.4),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test))
model.save("eye_state_model.h5") 