import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Wczytaj wytrenowany model oraz enkodery
model = joblib.load('dog_breed_model_reduced.pkl')
label_encoder_y = joblib.load('label_encoder_y.pkl')

# Opcjonalnie, jeśli chcesz użyć rozmiaru preferowanego jako selectbox
try:
    mappings = joblib.load('x_encoders.pkl')
except:
    mappings = {}

# Definicja cech i skal suwaków
feature_questions_and_scales = {
    'Tolerates Being Alone': ("Czy pies powinien dobrze znosić samotność?", 1, 5, 3),
    'Kid-Friendly': ("Jak bardzo pies powinien być przyjazny dla dzieci?", 1, 5, 4),
    'Dog Friendly': ("Jak ważne jest, aby pies był przyjazny dla innych psów?", 1, 5, 4),
    'Friendly Toward Strangers': ("Jak bardzo pies powinien być otwarty wobec obcych?", 1, 5, 4),
    'Size': ("Jaki rozmiar psa preferujesz (mały → duży)?", 1, 5, 3),
    'Easy To Train': ("Jak ważne jest, aby pies łatwo się uczył?", 1, 5, 4),
    'Energy Level': ("Jaki poziom energii psa Ci odpowiada?", 1, 5, 4),
}


# Konfiguracja aplikacji
st.set_page_config(page_title="Dopasuj rasę psa", page_icon="🐾")
st.title("🐕 Dopasuj rasę psa do siebie")

with st.form("dog_breed_form"):
    st.subheader("📋 Odpowiedz na kilka pytań:")
    user_input = {}

    for feature, (question, min_val, max_val, default_val) in feature_questions_and_scales.items():
        value = st.slider(question, min_value=min_val, max_value=max_val, value=default_val)
        user_input[feature] = value

    submitted = st.form_submit_button("🔍 Znajdź najlepiej dopasowaną rasę")

if submitted:
    input_df = pd.DataFrame([user_input])

    # Predykcja
    probabilities = model.predict_proba(input_df)[0]
    classes = label_encoder_y.inverse_transform(np.arange(len(probabilities)))

    top_n = 3
    top_indices = np.argsort(probabilities)[::-1][:top_n]

    st.subheader("🏆 Najlepiej dopasowane rasy psów:")
    for i in top_indices:
        breed = classes[i]
        prob = probabilities[i]
        st.markdown(f"### 🐶 {breed}")

    st.success("🎉 Powodzenia w wyborze pupila!")