
import pandas as pd
import numpy as np

class PawMatchSystem:
    """Kompletny system dopasowania psów do stylu życia"""
    
    def __init__(self, dogs_csv_path):
        self.dogs_df = pd.read_csv(dogs_csv_path)
        self.matches_history = []
    
    def calculate_match(self, dog_row, user_profile):
        """Główny algorytm dopasowania"""
        score = 0
        max_score = 100
        reasons = []
        
        # Mieszkanie (25%)
        if user_profile['living_type'] == 'apartment':
            apt_score = dog_row.get('Adapts Well To Apartment Living', 3)
            if apt_score >= 4:
                score += 25
                reasons.append("Idealny do mieszkania")
            elif apt_score >= 3:
                score += 15
        else:
            score += 20
        
        # Dzieci (30%)
        if user_profile['has_kids']:
            kid_score = dog_row.get('Kid-Friendly', 3)
            if kid_score >= 4:
                score += 25
                reasons.append("Uwielbia dzieci")
            elif kid_score >= 3:
                score += 15
        else:
            score += 20
        
        # Doświadczenie (20%)
        if user_profile['experience'] == 'beginner':
            novice_score = dog_row.get('Good For Novice Owners', 3)
            if novice_score >= 4:
                score += 15
                reasons.append("Łatwy dla początkujących")
        else:
            score += 15
        
        # Aktywność (25%)
        activity_map = {'low': 1, 'medium': 3, 'high': 4, 'very_high': 5}
        user_energy = activity_map.get(user_profile['activity_level'], 3)
        dog_energy = dog_row.get('Energy Level', 3)
        energy_match = max(0, 25 - (abs(user_energy - dog_energy) * 5))
        score += energy_match
        
        if abs(user_energy - dog_energy) <= 1:
            reasons.append("Pasuje do Twojego stylu życia")
        
        return {
            'score': min(100, score),
            'reasons': reasons[:3],
            'category': 'Idealny' if score >= 80 else 'Dobry' if score >= 60 else 'Możliwy'
        }
    
    def find_best_matches(self, user_profile, top_n=5):
        """Znajdź najlepsze dopasowania"""
        matches = []
        
        for idx, dog in self.dogs_df.iterrows():
            match = self.calculate_match(dog, user_profile)
            matches.append({
                'breed': dog['Breed Name'],
                'score': match['score'],
                'reasons': match['reasons'],
                'category': match['category']
            })
        
        matches.sort(key=lambda x: x['score'], reverse=True)
        return matches[:top_n]

# Przykład użycia:
# app = PawMatchSystem('dogs_cleaned.csv')
# user = {'living_type': 'apartment', 'has_kids': True, 'experience': 'beginner', 'activity_level': 'medium'}
# results = app.find_best_matches(user)
