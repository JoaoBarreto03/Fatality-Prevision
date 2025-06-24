# main.py

import streamlit as st
import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import RidgeCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor
from scipy.stats.mstats import winsorize


# ---------- Treinamento (executa 1x se arquivos não existirem) ----------
def treinar_modelos():
    if os.path.exists("scaler.pkl") and os.path.exists("voting_model.pkl"):
        return  # já treinado

    df = pd.read_excel('base_com_hdr_e_gdp.xlsx')
    df['gdp_hdi_interaction'] = df['gdp'] * df['hdi']

    cols_num = ['OFDA/BHA Response', 'No. Homeless', 'gdp', 'hdi', 'gdp_hdi_interaction']
    for c in cols_num:
        df[c] = winsorize(df[c], limits=[0.01, 0.01])

    X = df[cols_num]
    y = df['Total Deaths']

    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.3, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    models = {
        'rf': RandomForestRegressor(n_estimators=200, random_state=42),
        'gbm': GradientBoostingRegressor(learning_rate=0.05, n_estimators=500, max_depth=7, subsample=0.8, random_state=42)
    }

    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    S_train = np.zeros((len(X_train), len(models)))

    for idx, (name, model) in enumerate(models.items()):
        for i, (tr_i, val_i) in enumerate(kf.split(X_train_scaled)):
            model.fit(X_train_scaled[tr_i], y_train.iloc[tr_i])
            S_train[val_i, idx] = model.predict(X_train_scaled[val_i])

    meta = RidgeCV(alphas=[0.1, 1.0, 10.0], cv=5)
    meta.fit(S_train, y_train)

    joblib.dump(scaler, "scaler.pkl")

    # VotingRegressor como modelo final
    voting = VotingRegressor([
        ('rf', models['rf']),
        ('gbm', models['gbm'])
    ])
    voting.fit(X_train_scaled, y_train)
    joblib.dump(voting, "voting_model.pkl")

    print("✅ Modelos treinados e salvos com sucesso.")


# ---------- Predição ----------
def predict_deaths(ofda_response, homeless, gdp, hdi):
    scaler = joblib.load("scaler.pkl")
    model = joblib.load("voting_model.pkl")
    gdp_hdi_interaction = gdp * hdi
    input_data = np.array([[ofda_response, homeless, gdp, hdi, gdp_hdi_interaction]])
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)
    return prediction[0]


# ---------- Execução principal ----------
treinar_modelos()

st.set_page_config(page_title="Previsão de Fatalidades", layout="centered")
st.title("🌪️ Previsão de Fatalidades em Desastres")
st.markdown("Preencha os dados do evento abaixo:")

with st.form("formulario"):
    col1, col2 = st.columns(2)

    with col1:
        st.text_input("Disaster Group")
        st.text_input("Disaster Type")
        st.text_input("Disaster Subtype")
        st.text_input("Event Name")
        st.text_input("Country")
        magnitude = st.number_input("Magnitude", min_value=0.0)
        year = st.number_input("Year", min_value=1900, max_value=2100, step=1)
        gdp = st.number_input("GDP", min_value=0.0)
        hdi = st.number_input("HDI", min_value=0.0, max_value=1.0, step=0.01)
        homeless = st.number_input("No. Homeless", min_value=0.0)

    with col2:
        st.text_input("Disaster Subgroup")
        st.text_input("Magnitude Scale")
        ofda_response = st.checkbox("OFDA/BHA Response")
        st.checkbox("Declaration")

    submit = st.form_submit_button("Prever Fatalidades")

    if submit:
        try:
            resultado = predict_deaths(int(ofda_response), homeless, gdp, hdi)
            st.success(f"✅ Fatalidades previstas: **{resultado:.0f}**")
        except Exception as e:
            st.error(f"Erro ao prever: {e}")
