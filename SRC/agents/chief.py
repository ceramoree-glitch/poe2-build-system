"""
Şef Ajanı - Sadece sizin verilerinizle çalışır
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.accountant import Accountant


class Chief:
    def __init__(self):
        self.name = "Chief"
        self.accountant = Accountant()
        self.results = []
    
    def evaluate_builds(self, builds):
        """Build'leri değerlendirir"""
        
        for build in builds:
            skill = build["skill"]
            supports = build.get("supports", [])
            ascendancies = build.get("ascendancies", [])
            
            # Skill verilerini muhasebeciye gönder
            skill_data = {
                "name": skill.get("name", "Unknown"),
                "base_damage": skill.get("base_damage", 0),
                "damage_effectiveness": skill.get("damage_effectiveness", 100),
                "cast_time": skill.get("cast_time", 1.0)
            }
            
            # Support verileri
            support_data = []
            for s in supports:
                support_data.append({
                    "name": s.get("name", "Unknown"),
                    "more_damage": s.get("more_damage", 1.0),
                    "more_cast_speed": s.get("more_cast_speed", 1.0)
                })
            
            # Ascendancy bonusları
            equipment = []
            for asc in ascendancies:
                asc_bonus = {"name": asc.get("name", "Unknown")}
                for key in ["increased_damage", "increased_cast_speed", "increased_area_of_effect"]:
                    if key in asc:
                        asc_bonus[key] = asc[key]
                equipment.append(asc_bonus)
            
            # DPS hesapla
            result = self.accountant.calculate_dps(skill_data, support_data, equipment)
            
            self.results.append({
                "skill": skill.get("name", "Unknown"),
                "supports": [s.get("name", "Unknown") for s in supports],
                "ascendancies": [a.get("name", "Unknown") for a in ascendancies],
                "dps": result.get("dps", 0)
            })
        
        # DPS'e göre sırala
        self.results = sorted(self.results, key=lambda x: x["dps"], reverse=True)
        return self.results


# Test kodu
if __name__ == "__main__":
    print("=" * 60)
    print("👔 ŞEF AJANI TESTİ")
    print("=" * 60)
    
    # Örnek build verileri (sizin verilerinizle çalışacak)
    test_builds = [
        {
            "skill": {"name": "Fireball", "base_damage": 195, "damage_effectiveness": 180, "cast_time": 0.85},
            "supports": [
                {"name": "Spell Echo", "more_damage": 1.15, "more_cast_speed": 1.20},
                {"name": "Fire Penetration", "more_damage": 1.25}
            ],
            "ascendancies": [
                {"name": "Warbringer", "increased_fire_damage": 25}
            ]
        }
    ]
    
    chief = Chief()
    results = chief.evaluate_builds(test_builds)
    
    print("\n📊 Sonuçlar:")
    for r in results:
        print(f"   {r['skill']}: {r['dps']:,.2f} DPS")
        print(f"   Support'lar: {', '.join(r['supports'])}")
        print(f"   Ascendancy: {', '.join(r['ascendancies'])}")
