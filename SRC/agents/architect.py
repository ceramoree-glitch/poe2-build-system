"""
Mimar Ajanı - Sizin CSV verilerinizi kullanır
"""

import pandas as pd
import json
import random
from pathlib import Path


class Architect:
    def __init__(self):
        self.name = "Architect"
        self.skills = []
        self.supports = []
        self.ascendancies = []
        self.load_data()
    
    def load_data(self):
        """Sizin CSV dosyalarınızı yükler"""
        
        # 1. Skill verileri (SKILL klasöründeki tüm CSV'ler)
        skill_files = list(Path('SKILL').glob('*.csv'))
        if skill_files:
            df = pd.read_csv(skill_files[0])
            self.skills = df.to_dict('records')
            print(f"✅ [Mimar] {len(self.skills)} skill yüklendi: {skill_files[0].name}")
        else:
            print("⚠️ [Mimar] Skill CSV bulunamadı! SKILL/ klasörünü kontrol edin.")
            self.skills = []
        
        # 2. Support verileri (SKILL klasöründe support varsa)
        support_files = list(Path('SKILL').glob('*support*.csv'))
        if support_files:
            df = pd.read_csv(support_files[0])
            self.supports = df.to_dict('records')
            print(f"✅ [Mimar] {len(self.supports)} support yüklendi: {support_files[0].name}")
        else:
            print("⚠️ [Mimar] Support CSV bulunamadı! SKILL/*support*.csv olmalı.")
            self.supports = []
        
        # 3. Ascendancy verileri
        asc_files = list(Path('ASCENDANCY').glob('*.csv'))
        if asc_files:
            df = pd.read_csv(asc_files[0])
            self.ascendancies = df.to_dict('records')
            print(f"✅ [Mimar] {len(self.ascendancies)} ascendancy yüklendi: {asc_files[0].name}")
        else:
            print("⚠️ [Mimar] Ascendancy CSV bulunamadı! ASCENDANCY/ klasörünü kontrol edin.")
            self.ascendancies = []
    
    def select_builds(self, skill_count=10, support_count=5, ascendancy_count=2):
        """Sizin verilerinizden build'leri seçer"""
        
        print(f"🏗️ [Mimar] {skill_count} skill, {support_count} support, {ascendancy_count} ascendancy seçiliyor...")
        
        # 10 farklı skill seç (mevcut kadarıyla)
        if not self.skills:
            print("❌ [Mimar] Hiç skill verisi yok!")
            return []
        
        selected_skills = self.skills[:skill_count]
        if len(self.skills) < skill_count:
            print(f"   ⚠️ Sadece {len(self.skills)} skill mevcut, hepsi kullanılıyor.")
            selected_skills = self.skills
        
        builds = []
        for skill in selected_skills:
            # Support'ları al (mevcut kadarıyla)
            selected_supports = []
            if self.supports:
                selected_supports = self.supports[:support_count]
                if len(self.supports) < support_count:
                    print(f"   ⚠️ {skill.get('name', 'Unknown')}: Sadece {len(self.supports)} support mevcut, hepsi kullanılıyor.")
                    selected_supports = self.supports
            
            # Ascendancy'leri al (mevcut kadarıyla)
            selected_asc = []
            if self.ascendancies:
                selected_asc = self.ascendancies[:ascendancy_count]
                if len(self.ascendancies) < ascendancy_count:
                    print(f"   ⚠️ {skill.get('name', 'Unknown')}: Sadece {len(self.ascendancies)} ascendancy mevcut, hepsi kullanılıyor.")
                    selected_asc = self.ascendancies
            
            builds.append({
                "skill": skill,
                "supports": selected_supports,
                "ascendancies": selected_asc
            })
        
        print(f"✅ [Mimar] {len(builds)} build oluşturuldu.")
        return builds
    
    def get_build_summary(self, builds):
        """Build özetini döndürür"""
        summary = []
        for b in builds:
            summary.append({
                "skill": b["skill"].get("name", "Unknown"),
                "support_count": len(b["supports"]),
                "support_names": [s.get("name", "Unknown") for s in b["supports"]],
                "ascendancy_count": len(b["ascendancies"]),
                "ascendancy_names": [a.get("name", "Unknown") for a in b["ascendancies"]]
            })
        return summary


# Test kodu
if __name__ == "__main__":
    print("=" * 60)
    print("🏗️ MİMAR AJANI TESTİ")
    print("=" * 60)
    
    architect = Architect()
    builds = architect.select_builds(10, 5, 2)
    
    if builds:
        summary = architect.get_build_summary(builds)
        print("\n📊 Build Özeti:")
        for item in summary:
            print(f"   {item['skill']}: {item['support_count']} support, {item['ascendancy_count']} ascendancy")
    else:
        print("❌ Hiç build oluşturulamadı!")
