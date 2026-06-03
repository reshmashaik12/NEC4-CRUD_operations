import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os

data = {
    'age':[20,25,30,35,40,45,50],
    'salary':[25000,30000,35000,45000,55000,65000,80000]
}

df = pd.DataFrame(data)

X = df[['age']]
y = df['salary']

model = LinearRegression()
model.fit(X,y)

os.makedirs('ml_model', exist_ok=True)

joblib.dump(model,
            'ml_model/people_model.pkl')

print("Model Saved")