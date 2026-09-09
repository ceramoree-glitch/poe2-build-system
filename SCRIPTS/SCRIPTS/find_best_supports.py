"""
En İyi 5 Support Gem Kombinasyonunu Bulan Script
"""

import sys
import json
import itertools
from pathlib import Path

# SRC klasörünü Python path'ine ekle
sys.path.insert(0, str(Path(__file__).parent.parent / 'SRC'))

print("=" * 60)
print("🔍 EN İYİ 5 SUPPORT GEM KOMBİNASYONU BULUCU")
print("=" * 60)

try:
    from agents.accountant import Accountant
    
    # Muhasebeciyi başlat
    accountant = Accountant()
    
    if not accountant.is_ready:
        print("❌ Muhasebeci hazır değil!")
        sys.exit(1)
    
    print("\n✅ Muhasebeci hazır!")

    # --- 1. Skill Tanımla ---
    print("\n📌 1. Skill Tanımlanıyor...")
    
    skill = {
        "name": "Fireball",
        "base_damage": 195,
        "damage_effectiveness": 180,
        "cast_time": 0.85
    }
    print(f"   Skill: {skill['name']}")
    print(f"   Base Damage: {skill['base_damage']}")
    print(f"   Damage Effectiveness: {skill['damage_effectiveness']}%")
    print(f"   Cast Time: {skill['cast_time']}s")

    # --- 2. Support Gem Havuzu ---
    print("\n📌 2. Support Gem Havuzu Oluşturuluyor...")
    
    support_pool = [
        {"name": "Spell Echo", "more_damage": 1.15, "more_cast_speed": 1.20},
        {"name": "Fire Penetration", "more_damage": 1.25},
        {"name": "Controlled Destruction", "more_damage": 1.30, "crit_chance": -20},
        {"name": "Elemental Focus", "more_damage": 1.20},
        {"name": "Faster Casting", "more_cast_speed": 1.25},
        {"name": "Arcane Surge", "more_damage": 1.10, "more_cast_speed": 1.15},
        {"name": "Increased Critical Damage", "crit_multiplier": 30},
        {"name": "Increased Critical Strikes", "crit_chance": 10},
        {"name": "Lightning Penetration", "more_damage": 1.20},
        {"name": "Cold Penetration", "more_damage": 1.20},
        {"name": "Chaos Damage", "more_damage": 1.15},
        {"name": "Physical to Lightning", "more_damage": 1.10},
        {"name": "Chain", "more_damage": 1.10, "chains": 2},
        {"name": "Pierce", "more_damage": 1.05},
        {"name": "Fork", "more_damage": 1.05},
        {"name": "Multiple Projectiles", "more_damage": 0.90, "projectiles": 4},
        {"name": "Greater Multiple Projectiles", "more_damage": 0.80, "projectiles": 6},
        {"name": "Increased Area of Effect", "more_damage": 1.05},
        {"name": "Concentrated Effect", "more_damage": 1.30, "area_of_effect": -0.30},
        {"name": "Burning Damage", "more_damage": 1.20},
        {"name": "Ignite Proliferation", "more_damage": 1.10},
        {"name": "Deadly Ailments", "more_damage": 1.20},
        {"name": "Swift Affliction", "more_damage": 1.15},
        {"name": "Unbound Ailments", "more_damage": 1.10},
        {"name": "Efficacy", "more_damage": 1.10, "skill_duration": 1.20}
    ]
    
    # Skill etiketine göre filtrele (Fireball için sadece uygun olanları)
    compatible_supports = []
    for support in support_pool:
        # Fireball ile uyumlu olanlar
        compatible = True
        
        # Fireball ile uyumsuz olanları filtrele
        if "Lightning" in support["name"]:
            compatible = False
        if "Cold" in support["name"]:
            compatible = False
        if "Physical" in support["name"]:
            compatible = False
        if "Chain" in support["name"] and skill["name"] != "Spark":
            compatible = False
        if "Pierce" in support["name"] and skill["name"] != "Fireball":
            compatible = False
        
        if compatible:
            compatible_supports.append(support)
    
    print(f"   Toplam Support Havuzu: {len(support_pool)}")
    print(f"   Uyumlu Support'lar: {len(compatible_supports)}")
    for s in compatible_supports[:5]:
        print(f"      - {s['name']} (more_damage: {s.get('more_damage', 1.0)}x)")

    # --- 3. Kombinasyonları Dene ---
    print("\n📌 3. Kombinasyonlar Test Ediliyor...")
    
    # 5'li kombinasyonlar
    k = 5
    combinations = list(itertools.combinations(compatible_supports, k))
    print(f"   Toplam Kombinasyon: {len(combinations)}")

    if len(combinations) == 0:
        print("❌ Yeterli support gem yok!")
        sys.exit(1)

    # Her kombinasyon için DPS hesapla
    best_dps = 0
    best_combination = None
    best_result = None
    
    # Tüm kombinasyonları dene
    for i, combo in enumerate(combinations):
        # İlerleme göster
        if i % 10 == 0:
            print(f"   Test ediliyor: {i+1}/{len(combinations)}...")
        
        # DPS hesapla
        result = accountant.calculate_dps(skill, combo, [])
        
        if result.get("error"):
            continue
        
        dps = result.get("dps", 0)
        if dps > best_dps:
            best_dps = dps
            best_combination = combo
            best_result = result

    # --- 4. Sonuçları Göster ---
    print("\n" + "=" * 60)
    print("🏆 EN İYİ 5 SUPPORT KOMBİNASYONU")
    print("=" * 60)
    
    print(f"\n🔥 Skill: {skill['name']}")
    print(f"📊 Maksimum DPS: {best_dps:,.2f}")
    
    print("\n💎 Support Gem'ler:")
    for i, support in enumerate(best_combination, 1):
        more_dmg = support.get("more_damage", 1.0)
        more_speed = support.get("more_cast_speed", 1.0)
        effects = []
        if more_dmg > 1.0:
            effects.append(f"{int((more_dmg - 1) * 100)}% more damage")
        if more_speed > 1.0:
            effects.append(f"{int((more_speed - 1) * 100)}% more cast speed")
        print(f"   {i}. {support['name']}: {', '.join(effects)}")
    
    # DPS detayları
    print("\n📊 DPS Detayları:")
    breakdown = best_result.get("breakdown", {})
    for key, value in breakdown.items():
        print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Tarama tamamlandı!")

except ImportError as e:
    print(f"❌ Modül yüklenemedi: {e}")
    print("   SRC/agents/ klasöründe accountant.py olduğundan emin olun.")
except Exception as e:
    print(f"❌ Beklenmeyen hata: {e}")
