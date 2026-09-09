import pandas as pd
import json
import re
from pathlib import Path

class TagCleaner:
    def __init__(self):
        self.tag_classification = self.load_tags()
        self.cleaned_data = {}
    
    def load_tags(self):
        """Etiket sınıflandırmasını yükler"""
        try:
            with open('KEYWORDS/tag_classification.json', 'r') as f:
                return json.load(f)
        except:
            print("⚠️ Tag classification bulunamadı, varsayılan kullanılıyor")
            return self.default_tags()
    
    def default_tags(self):
        """Varsayılan etiketler"""
        return {
            "skill_tags": {
                "damage_type": {
                    "physical": ["Physical", "Phys"],
                    "fire": ["Fire", "Burn"],
                    "cold": ["Cold", "Freeze"],
                    "lightning": ["Lightning", "Shock"],
                    "chaos": ["Chaos", "Poison"]
                },
                "skill_type": {
                    "spell": ["Spell", "Cast"],
                    "attack": ["Attack", "Strike"],
                    "melee": ["Melee"],
                    "ranged": ["Projectile", "Bow"],
                    "minion": ["Minion", "Summon"],
                    "aura": ["Aura", "Buff"],
                    "curse": ["Curse", "Hex"]
                }
            },
            "support_tags": {
                "multiplier": ["More", "Increased"],
                "utility": ["Faster", "Pierce", "Chain"]
            }
        }
    
    def parse_tags(self, text):
        """Metinden etiketleri çıkarır"""
        if pd.isna(text):
            return []
        
        text = str(text).lower()
        found_tags = []
        
        # Tüm etiket kategorilerini tara
        for category, sub_categories in self.tag_classification.get("skill_tags", {}).items():
            for tag, keywords in sub_categories.items():
                for keyword in keywords:
                    if keyword.lower() in text:
                        found_tags.append(tag)
                        break
        
        return list(set(found_tags))  # Benzersiz etiketler
    
    def classify_skill(self, row):
        """Skill satırını sınıflandırır"""
        name = str(row.get('name', '')).lower()
        stats = str(row.get('stats', ''))
        tags = self.parse_tags(stats)
        
        # Ek olarak isimden de etiket çıkar
        name_tags = self.parse_tags(name)
        tags.extend(name_tags)
        
        # Damage tipini bul
        damage_types = [t for t in tags if t in ['physical', 'fire', 'cold', 'lightning', 'chaos']]
        skill_types = [t for t in tags if t in ['spell', 'attack', 'melee', 'ranged', 'minion', 'aura', 'curse']]
        
        return {
            'original_tags': list(set(tags)),
            'damage_type': damage_types[0] if damage_types else 'unknown',
            'skill_type': skill_types[0] if skill_types else 'unknown',
            'all_tags': list(set(tags))
        }
    
    def clean_skill_data(self, input_path, output_path):
        """Skill verilerini temizler"""
        df = pd.read_csv(input_path)
        print(f"🧹 Skill verisi temizleniyor: {len(df)} satır")
        
        # Sınıflandırma sütunları ekle
        classification = df.apply(self.classify_skill, axis=1)
        df['damage_type'] = classification.apply(lambda x: x['damage_type'])
        df['skill_type'] = classification.apply(lambda x: x['skill_type'])
        df['parsed_tags'] = classification.apply(lambda x: '|'.join(x['all_tags']))
        
        # Kaydet
        df.to_csv(output_path, index=False)
        print(f"✅ Temizlendi: {output_path}")
        return df
    
    def clean_unique_data(self, input_path, output_path):
        """Unique verilerini temizler"""
        df = pd.read_csv(input_path)
        print(f"🧹 Unique verisi temizleniyor: {len(df)} satır")
        
        # Slot tipini belirle
        def get_slot(row):
            name = str(row.get('name', '')).lower()
            if 'body' in name or 'coat' in name:
                return 'Body Armour'
            elif 'helmet' in name or 'hood' in name:
                return 'Helmet'
            elif 'gloves' in name:
                return 'Gloves'
            elif 'boots' in name:
                return 'Boots'
            elif 'shield' in name:
                return 'Shield'
            elif 'belt' in name:
                return 'Belt'
            elif 'amulet' in name:
                return 'Amulet'
            elif 'ring' in name:
                return 'Ring'
            return 'Other'
        
        df['slot'] = df.apply(get_slot, axis=1)
        
        # Stat'lardan etiket çıkar
        df['parsed_stats'] = df['stats'].apply(lambda x: '|'.join(self.parse_tags(str(x))))
        
        df.to_csv(output_path, index=False)
        print(f"✅ Temizlendi: {output_path}")
        return df

# Kullanım
if __name__ == "__main__":
    cleaner = TagCleaner()
    
    # Skill verilerini temizle
    cleaner.clean_skill_data(
        'SKILL/skill_gems.csv',
        'DATA/processed/skills_with_tags.csv'
    )
    
    # Unique verilerini temizle
    cleaner.clean_unique_data(
        'UNIQUE/armour_uniques.csv',
        'DATA/processed/uniques_with_tags.csv'
    )
    
    print("✅ Tüm etiket temizleme tamamlandı!")
