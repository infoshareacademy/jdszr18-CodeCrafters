
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Konfiguracja strony
st.set_page_config(
    page_title="PawMatch - Znajdź idealnego psa",
    page_icon="",
    layout="wide"
)

# Wczytaj dane
@st.cache_data
def load_data():
    return pd.read_csv("dogs_cleaned.csv")

df = load_data()

# Funkcja algorytmu dopasowania
def calculate_match_score(dog_row, user_profile):
    score = 0
    max_score = 100
    reasons = []
    
    # Mieszkanie (25 pkt)
    if user_profile['living'] == 'Mieszkanie':
        apt_score = dog_row.get('Adapts Well To Apartment Living', 3)
        size = dog_row.get('Size', 3)
        if apt_score >= 4 and size <= 2:
            score += 25
            reasons.append(" Idealny do mieszkania")
        elif apt_score >= 3:
            score += 15
            reasons.append(" Pasuje do mieszkania")
        else:
            score += 5
    else:
        score += 20
        if dog_row.get('Size', 3) >= 3:
            reasons.append(" Dużo miejsca na ruch")
    
    # Dzieci (30 pkt)
    if user_profile['kids']:
        kid_score = dog_row.get('Kid-Friendly', 3)
        if kid_score >= 4:
            score += 25
            reasons.append(" Uwielbia dzieci")
        elif kid_score >= 3:
            score += 15
        else:
            score += 5
    else:
        score += 20
    
    # Doświadczenie (20 pkt) 
    exp_map = {'Początkujący': 'beginner', 'Średnio zaawansowany': 'intermediate', 'Zaawansowany': 'advanced'}
    exp_level = exp_map.get(user_profile['experience'], 'beginner')
    
    if exp_level == 'beginner':
        novice_score = dog_row.get('Good For Novice Owners', 3)
        if novice_score >= 4:
            score += 15
            reasons.append(" Łatwy dla początkujących")
        elif novice_score >= 3:
            score += 10
    else:
        score += 15
        if dog_row.get('Intelligence', 3) >= 4:
            reasons.append(" Bardzo inteligentny")
    
    # Aktywność (25 pkt)
    activity_map = {'Bardzo niska': 1, 'Niska': 2, 'Średnia': 3, 'Wysoka': 4, 'Bardzo wysoka': 5}
    user_energy = activity_map.get(user_profile['activity'], 3)
    dog_energy = dog_row.get('Energy Level', 3)
    
    energy_diff = abs(user_energy - dog_energy)
    energy_score = max(0, 25 - (energy_diff * 5))
    score += energy_score
    
    if energy_diff <= 1:
        reasons.append(" Pasuje do Twojej aktywności")
    
    return min(100, score), reasons[:3]

# Główna aplikacja
def main():
    # Header
    st.title(" PawMatch - Znajdź idealnego psa!")
    st.markdown("### Dopasujemy rasę psa do Twojego stylu życia")
    
    # Sidebar - formularz użytkownika
    st.sidebar.header(" Twój profil")
    
    with st.sidebar:
        st.markdown("###  Mieszkanie")
        living = st.selectbox("Gdzie mieszkasz?", 
                             ["Mieszkanie", "Dom z ogrodem", "Dom bez ogrodu"])
        
        if living == "Mieszkanie":
            apartment_size = st.slider("Wielkość mieszkania (m²)", 20, 120, 60)
        
        st.markdown("###  Rodzina")
        has_kids = st.checkbox("Mam dzieci")
        if has_kids:
            kids_age = st.selectbox("Wiek dzieci", 
                                   ["0-3 lata", "4-8 lat", "9-12 lat", "13+ lat"])
        
        st.markdown("###  Doświadczenie")
        experience = st.selectbox("Twoje doświadczenie z psami",
                                 ["Początkujący", "Średnio zaawansowany", "Zaawansowany"])
        
        st.markdown("###  Aktywność")
        activity = st.selectbox("Twój poziom aktywności",
                               ["Bardzo niska", "Niska", "Średnia", "Wysoka", "Bardzo wysoka"])
        
        exercise_time = st.slider("Czas na spacery dziennie (minuty)", 15, 180, 60)
        
        st.markdown("###  Budżet")
        budget = st.slider("Budżet miesięczny (PLN)", 200, 2000, 800)
        
        # Przycisk analizy
        analyze = st.button(" Znajdź mojego idealnego psa!", type="primary")
    
    # Główna część aplikacji
    if analyze:
        # Profil użytkownika
        user_profile = {
            'living': living,
            'kids': has_kids,
            'experience': experience,
            'activity': activity,
            'exercise_time': exercise_time,
            'budget': budget
        }
        
        # Oblicz dopasowania
        matches = []
        for idx, dog in df.iterrows():
            score, reasons = calculate_match_score(dog, user_profile)
            matches.append({
                'breed': dog['Breed Name'],
                'score': score,
                'reasons': reasons,
                'size': dog.get('Dog Size', 'Unknown'),
                'group': dog.get('Dog Breed Group', 'Unknown'),
                'energy': dog.get('Energy Level', 3),
                'friendliness': dog.get('All Around Friendliness', 3),
                'apartment': dog.get('Adapts Well To Apartment Living', 3),
                'kids': dog.get('Kid-Friendly', 3),
                'novice': dog.get('Good For Novice Owners', 3)
            })
        
        # Sortuj według wyniku
        matches.sort(key=lambda x: x['score'], reverse=True)
        top_matches = matches[:10]
        
        # Wyświetl wyniki
        st.markdown("##  Twoje najlepsze dopasowania")
        
        # Top 3 z detalami
        cols = st.columns(3)
        for i, match in enumerate(top_matches[:3]):
            with cols[i]:
                st.markdown(f"### #{i+1} {match['breed']}")
                st.markdown(f"**{match['score']:.0f}% dopasowanie**")
                
                # Pasek postępu
                st.progress(match['score']/100)
                
                # Szczegóły
                st.markdown(f" **Rozmiar:** {match['size']}")
                st.markdown(f" **Grupa:** {match['group']}")
                
                # Powody
                if match['reasons']:
                    st.markdown("**Dlaczego pasuje:**")
                    for reason in match['reasons']:
                        st.markdown(f"• {reason}")
                
                # Cechy w skali 1-5
                st.markdown("**Kluczowe cechy:**")
                st.markdown(f" Energia: {'' * int(match['energy'])}")
                st.markdown(f" Przyjazność: {'' * int(match['friendliness'])}")
                if living == "Mieszkanie":
                    st.markdown(f" Mieszkanie: {'' * int(match['apartment'])}")
                if has_kids:
                    st.markdown(f" Z dziećmi: {'' * int(match['kids'])}")
        
        # Wykres wszystkich wyników
        st.markdown("##  Wszystkie wyniki dopasowania")
        
        # Przygotuj dane do wykresu
        chart_data = pd.DataFrame([
            {'Rasa': m['breed'], 'Dopasowanie (%)': m['score'], 'Grupa': m['group']} 
            for m in top_matches
        ])
        
        fig = px.bar(chart_data, x='Dopasowanie (%)', y='Rasa', 
                     color='Grupa', orientation='h',
                     title='Top 10 ras dla Twojego profilu')
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
        
        # Statystyki
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Najlepsze dopasowanie", f"{top_matches[0]['score']:.0f}%")
        with col2:
            st.metric("Średnie dopasowanie", f"{np.mean([m['score'] for m in top_matches]):.0f}%")
        with col3:
            ideal_count = len([m for m in matches if m['score'] >= 80])
            st.metric("Idealne dopasowania", f"{ideal_count} ras")
        with col4:
            good_count = len([m for m in matches if m['score'] >= 60])
            st.metric("Dobre dopasowania", f"{good_count} ras")

    else:
        # Strona powitalna
        st.markdown("""
        ## Jak to działa?
        
        1. **Wypełnij formularz** po lewej stronie
        2. **Kliknij przycisk** "Znajdź mojego idealnego psa"
        3. **Zobacz wyniki** - otrzymasz spersonalizowane rekomendacje
        4. **Porównaj rasy** - szczegółowe informacje o każdej rasie
        
        ###  Nasza baza danych zawiera:
        """)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Liczba ras", len(df))
        with col2:
            st.metric("Cechy analizowane", "41")
        with col3:
            st.metric("Kryteria dopasowania", "4")
        
        # Przykładowe statystyki
        st.markdown("###  Rozkład rozmiarów w naszej bazie")
        size_counts = df['Dog Size'].value_counts()
        fig = px.pie(values=size_counts.values, names=size_counts.index, 
                     title="Rozkład rozmiarów psów w bazie danych")
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
