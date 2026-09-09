"""
Mimar Ajanı - Sadece sizin CSV verilerinizi okur
"""

import pandas as pd
from pathlib import Path


class Architect:
    def __init__(self):
        self.name = "Architect"
        self.skills = []
        self.supports = []
        self.ascendancies = []
        self.load_data()
    
    def load_data(self):
        """Sizin CSV dosyalarınızı yükler - Başka hiçbir veri kullanılmaz"""
        
        # 1. Skill verileri (SKILL klasörü)
        skill_files = list(Path('SKILL').glob('*.csv'))
        if skill_files:
            df = pd.read_csv(skill_files[0])
            self.skills = df.to_dict('records')
            print(f"✅ [Mimar] {len(self.skills)} skill yüklendi: {skill_files[0].name}")
        
        # 2. Support verileri (SKILL klasöründe 'support' içeren dosya)
        support_files = list(Path('SKILL').glob('*support*.csv'))
        if support_files:
            df = pd.read_csv(support_files[0])
            self.supports = df.to_dict('records')
            print(f"✅ [Mimar] {len(self.supports)} support yüklendi: {support_files[0].name}")
        
        # 3. Ascendancy verileri (ASCENDANCY klasörü)
        asc_files = list(Path('ASCENDANCY').glob('*.csv'))
        if asc_files:
            df = pd.read_csv(asc_files[0])
            self.ascendancies = df.to_dict('records')
            print(f"✅ [Mimar] {len(self.ascendancies)} ascendancy yüklendi: {asc_files[0].name}")
    
    def select_builds(self, skill_count=10, support_count=5, ascendancy_count=2):
        """Sizin verilerinizden build'leri seçer"""
        
        if not self.skills:
            print("❌ [Mimar] Skill verisi yok! SKILL/ klasörünü kontrol edin.")
            return []
        
        # Mevcut skill'lerden seç
        selected_skills = self.skills[:skill_count]
        
        builds = []
        for skill in selected_skills:
            # Support'lar (mevcut kadarıyla)
            supports = self.supports[:support_count] if self.supports else []
            
            # Ascendancy'ler (mevcut kadarıyla)
            ascendancies = self.ascendancies[:ascendancy_count] if self.ascendancies else []
            
            builds.append({
                "skill": skill,
                "supports": supports,
                "ascendancies": ascendancies
            })
        
        return builds
