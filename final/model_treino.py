# model_treino.py

import numpy as np
import pandas as pd
from scipy.stats.mstats import winsorize
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, KFold
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import RidgeCV
import joblib

# 1. Carrega dataset
df = pd.read_excel('base_com_hdr_e_gdp.xlsx')

# 2. Engenharia de atributos
df['gdp_hdi_interaction'] = df['gdp'] * df['hdi']

# 3. Winsorize
cols_num = ['OFDA/BHA Response', 'No. Homeless', 'gdp', 'hdi', 'gdp_hdi_interaction']
for c in cols_num:
    df[c] = winsorize(df[c], limits=[0.01, 0.01])

# 4. X e y
X = df[cols_num]
y = df['Total Deaths']

# 5. Divisão
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 6. Escalamento
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 7. Modelos base
models = {
    'rf': RandomForestRegressor(n_estimators=200, random_state=42),
    'gbm': GradientBoostingRegressor(learning_rate=0.05, n_estimators=500, max_depth=7, subsample=0.8, random_state=42)
}

# 8. Stacking manual
kf = KFold(n_splits=5, shuffle=True, random_state=42)
S_train = np.zeros((len(X_train), len(models)))
S_test = np.zeros((len(X_test), len(models)))

for idx, (name, model) in enumerate(models.items()):
    S_test_fold = np.zeros((len(X_test), kf.get_n_splits()))
    for i, (tr_i, val_i) in enumerate(kf.split(X_train_scaled)):
        model.fit(X_train_scaled[tr_i], y_train.iloc[tr_i])
        S_train[val_i, idx] = model.predict(X_train_scaled[val_i])
        S_test_fold[:, i] = model.predict(X_test_scaled)
    S_test[:, idx] = S_test_fold.mean(axis=1)

# 9. Meta-modelo
meta = RidgeCV(alphas=[0.1, 1.0, 10.0], cv=5)
meta.fit(S_train, y_train)

# 10. Salvar
joblib.dump(meta, 'stacking_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

from sklearn.ensemble import VotingRegressor

voting = VotingRegressor([
    ('rf', models['rf']),
    ('gbm', models['gbm'])
])
voting.fit(X_train_scaled, y_train)

joblib.dump(voting, 'voting_model.pkl')

print("Modelos salvos com sucesso.")
