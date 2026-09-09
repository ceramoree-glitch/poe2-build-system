"""
Muhasebeci Ajanı (Accountant Agent)
Görevi: PoE2 DPS hesaplama kurallarını okumak ve uygulamak
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional


class Accountant:
    """
    Muhasebeci Ajanı - DPS hesaplamalarından sorumludur
    """
    
    def __init__(self):
        self.name = "Accountant"
        self.rules = {}
        self.dps_formula = {}
        self.damage_pipeline = []
        self.is_ready = False
        
        # Kuralları yükle
        self.load_rules()
    
    def load_rules(self) -> bool:
        """
        DPS hesaplama kurallarını yükler
        Kaynak: CONSTITUTION/dps_calculation_rules.json
        """
        rules_path = Path("CONSTITUTION/dps_calculation_rules.json")
        
        if not rules_path.exists():
            print(f"⚠️ [Accountant] Kural dosyası bulunamadı: {rules_path}")
            self.is_ready = False
            return False
        
        try:
            with open(rules_path, 'r', encoding='utf-8') as f:
                self.rules = json.load(f)
            
            # Ana formülü al
            self.dps_formula = self.rules.get("formula", {})
            
            # Hasar pipeline'ını al
            self.damage_pipeline = self.rules.get("damage_pipeline", {}).get("steps", [])
            
            self.is_ready = True
            print(f"✅ [Accountant] Kurallar yüklendi (v{self.rules.get('version', '')})")
            print(f"   📊 {len(self.damage_pipeline)} hasar adımı yüklendi")
            return True
            
        except json.JSONDecodeError as e:
            print(f"❌ [Accountant] JSON okuma hatası: {e}")
            self.is_ready = False
            return False
        except Exception as e:
            print(f"❌ [Accountant] Beklenmeyen hata: {e}")
            self.is_ready = False
            return False
    
    def calculate_dps(self, skill_data: Dict, support_data: List[Dict], equipment_data: List[Dict]) -> Dict:
        """
        DPS hesaplar
        - skill_data: Skill bilgileri (base_damage, cast_time, damage_effectiveness, vb.)
        - support_data: Support gem listesi (more_damage, more_cast_speed, vb.)
        - equipment_data: Ekipman listesi (increased_damage, vb.)
        """
        if not self.is_ready:
            return {"error": "Kurallar yüklenmedi", "dps": 0}
        
        try:
            # 1. Flat Damage hesapla
            flat_damage = self._calculate_flat_damage(skill_data, equipment_data)
            
            # 2. Increased/Reduced topla
            increased_multiplier = self._calculate_increased_multiplier(equipment_data)
            
            # 3. More/Less çarpanları
            more_multiplier = self._calculate_more_multiplier(support_data)
            
            # 4. Kritik faktör
            crit_factor = self._calculate_crit_factor(skill_data, equipment_data)
            
            # 5. Hız (Attack/Cast Speed)
            speed = self._calculate_speed(skill_data, support_data, equipment_data)
            
            # 6. Final DPS
            hit_damage = flat_damage * increased_multiplier * more_multiplier
            dps = hit_damage * crit_factor * speed
            
            return {
                "dps": round(dps, 2),
                "breakdown": {
                    "flat_damage": flat_damage,
                    "increased_multiplier": increased_multiplier,
                    "more_multiplier": more_multiplier,
                    "crit_factor": crit_factor,
                    "speed": speed
                }
            }
            
        except Exception as e:
            print(f"❌ [Accountant] DPS hesaplama hatası: {e}")
            return {"error": str(e), "dps": 0}
    
    def _calculate_flat_damage(self, skill: Dict, equipment: List[Dict]) -> float:
        """Flat damage hesaplar (Base + Added)"""
        # Base damage (skill'den)
        base = skill.get("base_damage", 0)
        if isinstance(base, dict):
            base = (base.get("min", 0) + base.get("max", 0)) / 2
        
        # Damage effectiveness
        effectiveness = skill.get("damage_effectiveness", 100) / 100
        
        # Added damage (equipment'ten)
        added = 0
        for item in equipment:
            added += item.get("added_damage", 0)
        
        return (base + added) * effectiveness
    
    def _calculate_increased_multiplier(self, equipment: List[Dict]) -> float:
        """Increased/Reduced toplamını hesaplar"""
        total_inc = 0
        total_red = 0
        
        for item in equipment:
            total_inc += item.get("increased_damage", 0)
            total_red += item.get("reduced_damage", 0)
            
            # Elemental spesifik bonuslar
            for dmg_type in ["fire", "cold", "lightning", "chaos", "physical"]:
                key = f"increased_{dmg_type}_damage"
                total_inc += item.get(key, 0)
        
        return 1 + (total_inc - total_red) / 100
    
    def _calculate_more_multiplier(self, supports: List[Dict]) -> float:
        """More/Less çarpanlarını hesaplar (her biri ayrı çarpılır)"""
        multiplier = 1.0
        
        for support in supports:
            more = support.get("more_damage", 1.0)
            less = support.get("less_damage", 1.0)
            multiplier *= more * less
        
        return multiplier
    
    def _calculate_crit_factor(self, skill: Dict, equipment: List[Dict]) -> float:
        """Kritik faktörü hesaplar"""
        # Base crit chance (skill'den)
        crit_chance = skill.get("crit_chance", 5)
        
        # Crit multiplier (varsayılan 150%)
        crit_multiplier = skill.get("crit_multiplier", 150)
        
        # Ekipmandan bonuslar
        for item in equipment:
            crit_chance += item.get("crit_chance", 0)
            crit_multiplier += item.get("crit_multiplier", 0)
        
        # Formül: 1 + (Crit_Chance/100) × ((Crit_Multiplier/100) - 1)
        return 1 + (crit_chance / 100) * ((crit_multiplier / 100) - 1)
    
    def _calculate_speed(self, skill: Dict, supports: List[Dict], equipment: List[Dict]) -> float:
        """Attack/Cast Speed hesaplar"""
        # Base speed (skill'den)
        base_speed = skill.get("cast_time", 1.0)
        
        # Speed bonusları
        total_speed_inc = 0
        more_speed = 1.0
        
        for item in equipment:
            total_speed_inc += item.get("increased_speed", 0)
            total_speed_inc += item.get("increased_cast_speed", 0)
            total_speed_inc += item.get("increased_attack_speed", 0)
        
        for support in supports:
            more_speed *= support.get("more_cast_speed", 1.0)
            more_speed *= support.get("more_attack_speed", 1.0)
        
        # Hız = Base × (1 + İncreased%) × More
        return (1 / base_speed) * (1 + total_speed_inc / 100) * more_speed
    
    def get_formula(self) -> Dict:
        """Ana formülü döndürür"""
        return self.dps_formula
    
    def get_pipeline(self) -> List[Dict]:
        """Hasar pipeline'ını döndürür"""
        return self.damage_pipeline
    
    def get_rules_summary(self) -> Dict:
        """Kural özetini döndürür"""
        return {
            "name": self.rules.get("title", ""),
            "version": self.rules.get("version", ""),
            "status": self.rules.get("status", ""),
            "has_formula": bool(self.dps_formula),
            "has_pipeline": bool(self.damage_pipeline)
        }


# --- Test Kodu ---
if __name__ == "__main__":
    print("🧮 Muhasebeci Ajanı Testi")
    print("-" * 40)
    
    # Muhasebeciyi başlat
    accountant = Accountant()
    
    if accountant.is_ready:
        print("✅ Muhasebeci hazır!")
        
        # Özet bilgiler
        summary = accountant.get_rules_summary()
        print(f"📊 Kural özeti: {summary.get('name')} (v{summary.get('version')})")
        print(f"📋 {len(accountant.get_pipeline())} hasar adımı yüklendi")
        
        # Örnek hesaplama
        print("\n🧪 Örnek DPS Hesaplama:")
        
        skill = {
            "base_damage": 195,
            "damage_effectiveness": 180,
            "cast_time": 0.85
        }
        
        supports = [
            {"more_damage": 1.15, "more_cast_speed": 1.20},
            {"more_damage": 1.25},
            {"more_damage": 1.30}
        ]
        
        equipment = [
            {"increased_damage": 10}
        ]
        
        result = accountant.calculate_dps(skill, supports, equipment)
        
        if "error" not in result:
            print(f"  🎯 DPS: {result['dps']:,.2f}")
            print(f"  📊 Detaylar:")
            for key, value in result.get("breakdown", {}).items():
                print(f"     {key}: {value}")
        else:
            print(f"  ❌ Hata: {result['error']}")
    
    else:
        print("❌ Muhasebeci hazır değil! Kural dosyasını kontrol edin.")
