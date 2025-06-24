# predict.py
# predict.py

import joblib
import pandas as pd

def predict_deaths(ofda_response, homeless, gdp, hdi):
    scaler = joblib.load('scaler.pkl')
    model = joblib.load('voting_model.pkl')  # <- modelo agora é VotingRegressor

    X = pd.DataFrame([{
        'OFDA/BHA Response': ofda_response,
        'No. Homeless': homeless,
        'gdp': gdp,
        'hdi': hdi,
        'gdp_hdi_interaction': gdp * hdi
    }])
    
    X_scaled = scaler.transform(X)
    y_pred = model.predict(X_scaled)
    return y_pred[0]
