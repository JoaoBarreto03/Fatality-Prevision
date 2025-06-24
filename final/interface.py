import streamlit as st
from predict import predict_deaths

st.set_page_config(page_title="Previsão de Fatalidades", layout="centered")

st.title("🌪️ Previsão de Fatalidades em Desastres")
st.markdown("Preencha os dados do evento abaixo:")

with st.form("formulario"):

    # Colunas organizadas
    col1, col2 = st.columns(2)

    with col1:
        disaster_group = st.text_input("Disaster Group")
        disaster_type = st.text_input("Disaster Type")
        disaster_subtype = st.text_input("Disaster Subtype")
        event_name = st.text_input("Event Name")
        country = st.text_input("Country")
        magnitude = st.number_input("Magnitude", min_value=0.0)
        year = st.number_input("Year", min_value=1900, max_value=2100, step=1)
        gdp = st.number_input("GDP", min_value=0.0)
        hdi = st.number_input("HDI", min_value=0.0, max_value=1.0, step=0.01)
        homeless = st.number_input("No. Homeless", min_value=0.0)

    with col2:
        disaster_subgroup = st.text_input("Disaster Subgroup")
        magnitude_scale = st.text_input("Magnitude Scale")
        ofda_response = st.checkbox("OFDA/BHA Response")
        declaration = st.checkbox("Declaration")

    submit = st.form_submit_button("Prever Fatalidades")

    if submit:
        try:
            prediction = predict_deaths(int(ofda_response), homeless, gdp, hdi)
            st.success(f"✅ Fatalidades previstas: **{prediction:.0f}**")
        except Exception as e:
            st.error(f"Erro ao prever: {e}")
