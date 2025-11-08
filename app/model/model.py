import re
from pathlib import Path
import numpy as np
from tensorflow.keras.models import load_model
from sklearn import preprocessing


BASE_DIR = Path(__file__).resolve(strict=True).parent
MODEL_PATH = BASE_DIR / "model.h5"

model = load_model(MODEL_PATH)

def predict_nutriscore(energi, protein, lemak, serat, natrium, gula):
    index_to_grade = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}
    input_data = np.array([[energi, protein, lemak, serat, natrium, gula]], dtype=np.float32)
    normalized_arr = preprocessing.normalize(input_data)
    predict = model.predict(normalized_arr)
    max_index = np.argmax(predict)
    grade = index_to_grade[max_index]

    return grade
