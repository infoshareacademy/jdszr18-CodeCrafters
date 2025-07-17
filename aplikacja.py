import streamlit as st
import pandas as pd
import numpy as np
import pickle

# 1️⃣ Wczytanie modelu i enkodera
# Model wytrenowany do przewidywania ras
with open('dog_breed_model_reduced.pkl', 'rb') as f:
    model = pickle.load(f)

# Enkoder do dekodowania etykiet ras
with open('label_encoder_y.pkl', 'rb') as f:
    label_encoder_y = pickle.load(f)

# 2️⃣ Mappings – przypisanie wartości liczbowych do cech
# Mappings wskazują, jak wartości tekstowe odpowiadają wartościom liczbowym w modelu
mappings = {
    'Tolerates Being Alone': {
        'Nie lubi zostawać sam': 1,
        'Czasami może zostać sam': 2,
        'Dobrze znosi samotność': 3
    },
    'Kid-Friendly': {
        'Nie przepada za dziećmi': 2,
        'Toleruje dzieci': 3,
        'Lubi dzieci': 4,
        'Uwielbia dzieci': 5
    },
    'Dog Friendly': {
        'Mało towarzyski': 2,
        'Toleruje inne psy': 3,
        'Lubi towarzystwo psów': 4,
        'Świetnie dogaduje się z psami': 5
    },
    'Friendly Toward Strangers': {
        'Bardzo nieufny': 1,
        'Nieśmiały': 2,
        'Neutralny': 3,
        'Przyjazny': 4,
        'Bardzo towarzyski': 5
    },
    'Size': {
        'Bardzo mały': 1,
        'Mały': 2,
        'Średni': 3,
        'Duży': 4,
        'Bardzo duży': 5
    },
    'Easy To Train': {
        'Bardzo trudno': 1,
        'Trudno': 2,
        'Średnio': 3,
        'Łatwo': 4,
        'Bardzo łatwo': 5
    },
    'Energy Level': {
        'Bardzo spokojny': 2,
        'Spokojny': 3,
        'Aktywny': 4,
        'Bardzo energiczny': 5
    }
}

# 3️⃣ Pytania do użytkownika
# Zbiór pytań, które będą zadawane użytkownikowi
questions = {
    'Tolerates Being Alone': "Jak radzi sobie pies, gdy zostaje sam w domu?",
    'Kid-Friendly': "Jak ważne jest, żeby pies lubił dzieci?",
    'Dog Friendly': "Czy pies powinien dobrze dogadywać się z innymi psami?",
    'Friendly Toward Strangers': "Jak otwarty na nowe osoby powinien być Twój pies?",
    'Size': "Jaki rozmiar psa preferujesz?",
    'Easy To Train': "Jak łatwo pies powinien się uczyć nowych rzeczy?",
    'Energy Level': "Jak bardzo aktywnego psa szukasz?"
}

# 4️⃣ Linki do opisów ras
# Słownik, który zawiera linki do szczegółowych opisów każdej z ras
breed_links = {
    "Australian Shepherd": "https://dogtime.com/dog-breeds/australian-shepherd",
    "Beagle": "https://dogtime.com/dog-breeds/beagle",
    "Bernese Mountain Dog": "https://dogtime.com/dog-breeds/bernese-mountain-dog",
    "Border Collie": "https://dogtime.com/dog-breeds/border-collie",
    "Boston Terrier": "https://dogtime.com/dog-breeds/boston-terrier",
    "Boxer": "https://dogtime.com/dog-breeds/boxer",
    "Cavalier King Charles Spaniel": "https://dogtime.com/dog-breeds/cavalier-king-charles-spaniel",
    "Chihuahua": "https://dogtime.com/dog-breeds/chihuahua",
    "Cocker Spaniel": "https://dogtime.com/dog-breeds/cocker-spaniel",
    "Dachshund": "https://dogtime.com/dog-breeds/dachshund",
    "French Bulldog": "https://dogtime.com/dog-breeds/french-bulldog",
    "German Shepherd Dog": "https://dogtime.com/dog-breeds/german-shepherd-dog",
    "German Shorthaired Pointer": "https://dogtime.com/dog-breeds/german-shorthaired-pointer",
    "Golden Retriever": "https://dogtime.com/dog-breeds/golden-retriever",
    "Great Dane": "https://dogtime.com/dog-breeds/great-dane",
    "Irish Setter": "https://dogtime.com/dog-breeds/irish-setter",
    "Jack Russell Terrier": "https://dogtime.com/dog-breeds/jack-russell-terrier",
    "Labrador Retriever": "https://dogtime.com/dog-breeds/labrador-retriever",
    "Maltese": "https://dogtime.com/dog-breeds/maltese",
    "Mastiff": "https://dogtime.com/dog-breeds/mastiff",
    "Pomeranian": "https://dogtime.com/dog-breeds/pomeranian",
    "Poodle": "https://dogtime.com/dog-breeds/poodle",
    "Rottweiler": "https://dogtime.com/dog-breeds/rottweiler",
    "Shih Tzu": "https://dogtime.com/dog-breeds/shih-tzu",
    "Siberian Husky": "https://dogtime.com/dog-breeds/siberian-husky",
    "Yorkshire Terrier": "https://dogtime.com/dog-breeds/yorkshire-terrier"
}

# 5️⃣ Styl CSS – wygląd aplikacji
# Dodanie stylu do aplikacji, np. tło, marginesy, fonty
custom_css = """
<style>
header, [data-testid="stHeader"] {
    display: none;
}
[data-testid="stAppViewContainer"] {
    margin: 0 !important;
    padding: 0 !important;
    min-height: 100vh;
    background-image: url('https://www.caramella.pl/cache/files/2010586204/228-2---w-1200.jpg');
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-position: center center;
}
.block-container {
    padding-top: 0 !important;
    margin-top: 0 !important;
}
[data-testid="stAppViewContainer"] > .main {
    background-color: rgba(255, 255, 255, 0.5);
    margin: 10px auto 20px auto;
    max-width: 800px;
    border-radius: 16px;
    padding: 30px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
}
h1 {
    margin-top: 0 !important;
    font-weight: bold !important;
    color: #222 !important;
}
h2, h3, h4, h5, h6, p, label, div, span {
    color: #222 !important;
    font-weight: normal !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 6️⃣ Nagłówek aplikacji
# Wyświetlenie nagłówka na stronie aplikacji
st.markdown("""
<h1 style='text-align: center; font-size: 28px; color: #333; text-shadow: 1px 1px 2px #aaa;'>
🐕 DogMatcher – Znajdź idealnego psa dla siebie 🐕
</h1>
""", unsafe_allow_html=True)

# 7️⃣ Zbieranie danych od użytkownika
# Przechodzimy przez pytania i zapisujemy odpowiedzi w słowniku user_input
user_input = {}
for feature in mappings:
    choice = st.selectbox(questions[feature], options=list(mappings[feature].keys()), key=feature)
    user_input[feature] = mappings[feature][choice]

# 8️⃣ Predykcja – uzyskanie wyników dopasowania ras
if st.button("🔍 Znajdź najlepiej dopasowaną rasę"):
    input_df = pd.DataFrame([user_input])  # Zmienna z odpowiedziami użytkownika
    probabilities = model.predict_proba(input_df)[0]  # Predykcja
    classes = label_encoder_y.inverse_transform(np.arange(len(probabilities)))  # Klasyfikacja psów

    top_n = 3  # Liczba najlepszych ras do pokazania
    top_indices = np.argsort(probabilities)[::-1][:top_n]  # Top 3 rasy

    st.subheader("Najlepiej dopasowane rasy psów:")

    icons = ["🐾", "🐶", "🦴"]  # Ikony dla ras

    for idx, i in enumerate(top_indices):
        breed = classes[i]  # Nazwa rasy
        icon = icons[idx] if idx < len(icons) else "🐶"  # Ikona
        link = breed_links.get(breed)  # Link do opisu rasy
        if link:
            st.markdown(
                f"""<h3 style='font-size: 28px;'>
                    {icon} <a href='{link}' target='_blank' style='text-decoration:none; color: inherit;'>{breed}</a>
                   </h3>""",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<h3 style='font-size: 28px;'>{icon} {breed}</h3>",
                unsafe_allow_html=True
            )

    st.write("Kliknij w nazwę psa, aby dowiedzieć się więcej o swoim wymarzonym piesku.")