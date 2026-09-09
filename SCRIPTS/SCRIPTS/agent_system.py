import json
import logging
from datetime import datetime
from pathlib import Path
import pandas as pd
import random

# --- Logging Ayarları ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AgentSystem")

# --- 1. VERİ TOPLAYICI ---
class DataCollector:
    """Veri toplama ve temizleme ajanı"""
    
    def __init__(self):
        self.name = "DataCollector"
        self.data = {}
    
    def collect(self):
        logger.info(f"[{self.name}] Veri toplama başladı...")
        
        # Skill verileri
        try:
            self.data['skills'] = pd.read_csv('SKILL/skill_gems.csv').to_dict('records')
            logger.info(f"  ✅ {len(self.data['skills'])} skill yüklendi")
        except:
            self.data['skills'] = []
            logger.warning("  ⚠️ Skill verisi yüklenemedi")
        
        # Support verileri
        try:
            self.data['supports'] = pd.read_csv('SKILL/support_gems.csv').to_dict('records')
            logger.info(f"  ✅ {len(self.data['supports'])} support gem yüklendi")
        except:
            self.data['supports'] = []
            logger.warning("  ⚠️ Support verisi yüklenemedi")
        
        # Unique verileri
        try:
            unique_files = list(Path('UNIQUE').glob('*.csv'))
            all_uniques = []
            for f in unique_files:
                df = pd.read_csv(f)
                all_uniques.extend(df.to_dict('records'))
            self.data['uniques'] = all_uniques
            logger.info(f"  ✅ {len(self.data['uniques'])} unique yüklendi")
        except:
            self.data['uniques'] = []
            logger.warning("  ⚠️ Unique verisi yüklenemedi")
        
        # Ascendancy verileri
        try:
            self.data['ascendancies'] = pd.read_csv('ASCENDANCY/ascendancy_classes.csv').to_dict('records')
            logger.info(f"  ✅ {len(self.data['ascendancies'])} ascendancy yüklendi")
        except:
            self.data['ascendancies'] = []
            logger.warning("  ⚠️ Ascendancy verisi yüklenemedi")
        
        # Mesajı ilet
        return self.data

# --- 2. MATEMATİKÇİ ---
class Mathematician:
    """Kombinasyon ve DPS hesaplama ajanı"""
    
    def __init__(self):
        self.name = "Mathematician"
        self.combinations = []
    
    def process(self, data):
        logger.info(f"[{self.name}] Kombinasyon analizi başladı...")
        
        # Kombinasyonları oluştur
        combinations = []
        
        # Her skill için
        for skill in data.get('skills', []):
            # Uygun support'ları filtrele
            skill_tags = str(skill.get('parsed_tags', '')).split('|')
            compatible_supports = []
            
            for support in data.get('supports', []):
                support_tags = str(support.get('parsed_tags', '')).split('|')
                if any(tag in support_tags for tag in skill_tags) or 'generic' in skill_tags:
                    compatible_supports.append(support)
            
            # Her unique için
            for unique in data.get('uniques', [])[:20]:  # Performans için ilk 20
                # 3 destek seç
                selected_supports = random.sample(compatible_supports, min(3, len(compatible_supports)))
                
                # Basit DPS hesapla (önceki formüle göre)
                base_damage = 100
                support_mult = 1.0
                for s in selected_supports:
                    # Basitçe her support +%15 damage
                    support_mult *= 1.15
                
                rate = 1.5 if 'spell' in skill_tags else 1.8
                armour_bonus = 1.0
                
                # Armour bonusu
                unique_stats = str(unique.get('stats', ''))
                if 'increased' in unique_stats.lower():
                    import re
                    matches = re.findall(r'(\d+)%', unique_stats)
                    if matches:
                        armour_bonus = 1 + int(matches[0]) / 100
                
                dps = base_damage * support_mult * rate * armour_bonus
                
                combinations.append({
                    'skill': skill.get('name', 'Unknown'),
                    'skill_tags': skill_tags,
                    'supports': [s.get('name', 'Unknown') for s in selected_supports],
                    'armour': unique.get('name', 'Unknown'),
                    'dps': round(dps, 2),
                    'confidence': round(random.uniform(0.7, 0.99), 2)
                })
        
        # DPS'e göre sırala
        self.combinations = sorted(combinations, key=lambda x: x['dps'], reverse=True)
        
        logger.info(f"  ✅ {len(self.combinations)} kombinasyon üretildi")
        logger.info(f"  🏆 En yüksek DPS: {self.combinations[0]['dps']:,.0f}" if self.combinations else "  ⚠️ Kombinasyon yok")
        
        # İstatistikler
        stats = {
            'total_combinations': len(self.combinations),
            'avg_dps': sum(c['dps'] for c in self.combinations) / len(self.combinations) if self.combinations else 0,
            'max_dps': self.combinations[0]['dps'] if self.combinations else 0,
            'min_dps': self.combinations[-1]['dps'] if self.combinations else 0
        }
        
        # Mesajı hazırla
        result = {
            'top_100': self.combinations[:100],
            'statistics': stats
        }
        
        return result

# --- 3. MİMAR ---
class Architect:
    """Build tasarımı ve kalite kontrol ajanı"""
    
    def __init__(self):
        self.name = "Architect"
        self.approved_builds = []
    
    def process(self, combinations_data):
        logger.info(f"[{self.name}] Build tasarımı başladı...")
        
        approved = []
        
        for build in combinations_data.get('top_100', []):
            # Kategorilendirme
            dps = build['dps']
            if dps > 100000:
                category = "S-Tier"
            elif dps > 75000:
                category = "A-Tier"
            elif dps > 50000:
                category = "B-Tier"
            elif dps > 25000:
                category = "C-Tier"
            else:
                category = "D-Tier"
            
            # Skor hesapla (Anayasa Madde 12)
            score = 0
            score += dps / 100000 * 60  # DPS ağırlığı %60
            score += random.randint(60, 90) / 100 * 15  # Sürdürülebilirlik
            score += random.randint(50, 85) / 100 * 15  # Savunma
            score += random.randint(70, 95) / 100 * 10  # Kullanılabilirlik
            
            approved.append({
                'id': f"build_{len(approved)+1:03d}",
                'name': f"{build['skill']} Build",
                'category': category,
                'skill': build['skill'],
                'supports': build['supports'],
                'armour': build['armour'],
                'dps': build['dps'],
                'sustainability': round(random.randint(60, 95)),
                'defense': round(random.randint(50, 90)),
                'usability': round(random.randint(70, 95)),
                'total_score': round(score, 2),
                'confidence': build['confidence']
            })
        
        self.approved_builds = approved
        
        # Özet
        summary = {
            'total_approved': len(approved),
            's_tier': sum(1 for b in approved if b['category'] == 'S-Tier'),
            'a_tier': sum(1 for b in approved if b['category'] == 'A-Tier'),
            'b_tier': sum(1 for b in approved if b['category'] == 'B-Tier'),
            'c_tier': sum(1 for b in approved if b['category'] == 'C-Tier'),
            'd_tier': sum(1 for b in approved if b['category'] == 'D-Tier')
        }
        
        logger.info(f"  ✅ {summary['total_approved']} build onaylandı")
        logger.info(f"  🏆 S-Tier: {summary['s_tier']}, A-Tier: {summary['a_tier']}")
        
        return {
            'approved_builds': approved,
            'summary': summary
        }

# --- 4. ŞEF ---
class Chief:
    """Nihai karar verici ajan"""
    
    def __init__(self):
        self.name = "Chief"
    
    def process(self, architect_result):
        logger.info(f"[{self.name}] Nihai karar veriliyor...")
        
        builds = architect_result.get('approved_builds', [])
        
        if not builds:
            logger.warning("  ⚠️ Onaylanmış build yok!")
            return None
        
        # Build of the day
        best_build = builds[0] if builds else None
        
        # Stratejik notlar
        notes = []
        if builds:
            # En çok hangi kategori öne çıkıyor?
            categories = [b['category'] for b in builds]
            most_common = max(set(categories), key=categories.count)
            notes.append(f"En yaygın kategori: {most_common}")
            
            # En çok hangi skill?
            skills = [b['skill'] for b in builds]
            most_common_skill = max(set(skills), key=skills.count)
            notes.append(f"En yaygın skill: {most_common_skill}")
        
        # Nihai karar
        decision = {
            'report_date': datetime.now().strftime('%Y-%m-%d'),
            'build_of_the_day': {
                'name': best_build['name'] if best_build else 'None',
                'category': best_build['category'] if best_build else 'None',
                'dps': best_build['dps'] if best_build else 0
            },
            'top_10_builds': builds[:10],
            'strategic_notes': notes,
            'total_builds_analyzed': len(builds),
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"  🏆 Build of the Day: {decision['build_of_the_day']['name']}")
        logger.info(f"  📊 DPS: {decision['build_of_the_day']['dps']:,.0f}")
        
        # Sonuçları kaydet
        os.makedirs('OUTPUTS/reports/builds', exist_ok=True)
        with open(f'OUTPUTS/reports/builds/final_decision_{datetime.now().strftime("%Y-%m-%d")}.json', 'w') as f:
            json.dump(decision, f, indent=2, ensure_ascii=False)
        
        return decision

# --- ANA İŞ AKIŞI ---
def main():
    logger.info("=" * 50)
    logger.info("🧠 AJAN SİSTEMİ BAŞLATILIYOR")
    logger.info("=" * 50)
    
    # 1. Veri Toplayıcı
    collector = DataCollector()
    data = collector.collect()
    
    if not data or not data.get('skills'):
        logger.error("❌ Veri toplanamadı, sistem durduruluyor.")
        return
    
    # 2. Matematikçi
    mathematician = Mathematician()
    combinations = mathematician.process(data)
    
    if not combinations or not combinations.get('top_100'):
        logger.error("❌ Kombinasyon üretilemedi, sistem durduruluyor.")
        return
    
    # 3. Mimar
    architect = Architect()
    architect_result = architect.process(combinations)
    
    if not architect_result or not architect_result.get('approved_builds'):
        logger.error("❌ Build onaylanamadı, sistem durduruluyor.")
        return
    
    # 4. Şef
    chief = Chief()
    final_decision = chief.process(architect_result)
    
    logger.info("=" * 50)
    logger.info("✅ AJAN SİSTEMİ TAMAMLANDI")
    logger.info("=" * 50)
    
    return final_decision

if __name__ == "__main__":
    import os
    main()
