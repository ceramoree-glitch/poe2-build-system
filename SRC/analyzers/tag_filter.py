import pandas as pd
import json
from pathlib import Path

class TagFilter:
    def __init__(self):
        self.skill_data = None
        self.unique_data = None
    
    def load_data(self):
        """Temizlenmiş verileri yükler"""
        try:
            self.skill_data = pd.read_csv('DATA/processed/skills_with_tags.csv')
            print(f"✅ Skill verisi yüklendi: {len(self.skill_data)} satır")
        except:
            print("⚠️ Skill verisi bulunamadı")
        
        try:
            self.unique_data = pd.read_csv('DATA/processed/uniques_with_tags.csv')
            print(f"✅ Unique verisi yüklendi: {len(self.unique_data)} satır")
        except:
            print("⚠️ Unique verisi bulunamadı")
    
    def filter_by_tags(self, tags, data_type='skill'):
        """Etiketlere göre filtrele"""
        if data_type == 'skill' and self.skill_data is not None:
            df = self.skill_data
            # parsed_tags sütununda aranan etiketleri ara
            mask = df['parsed_tags'].apply(
                lambda x: any(tag in str(x) for tag in tags)
            )
            return df[mask]
        elif data_type == 'unique' and self.unique_data is not None:
            df = self.unique_data
            mask = df['parsed_stats'].apply(
                lambda x: any(tag in str(x) for tag in tags)
            )
            return df[mask]
        return pd.DataFrame()
    
    def get_stats_by_tag(self, tag):
        """Bir etiketin istatistiklerini çıkar"""
        results = {
            'tag': tag,
            'skill_count': 0,
            'unique_count': 0,
            'skills': [],
            'uniques': []
        }
        
        if self.skill_data is not None:
            filtered = self.filter_by_tags([tag], 'skill')
            results['skill_count'] = len(filtered)
            results['skills'] = filtered['name'].tolist()[:10]
        
        if self.unique_data is not None:
            filtered = self.filter_by_tags([tag], 'unique')
            results['unique_count'] = len(filtered)
            results['uniques'] = filtered['name'].tolist()[:10]
        
        return results

# Kullanım
if __name__ == "__main__":
    filter_tool = TagFilter()
    filter_tool.load_data()
    
    # Örnek: Fire etiketine sahip skill'leri bul
    fire_skills = filter_tool.filter_by_tags(['fire'], 'skill')
    print(f"🔥 Fire etiketli skill'ler: {len(fire_skills)} adet")
    print(fire_skills[['name', 'damage_type', 'skill_type']].head())
