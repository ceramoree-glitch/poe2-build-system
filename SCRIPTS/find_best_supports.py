"""
En İyi 5 Support Gem Kombinasyonunu Bulan Script
"""

import sys
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
        print("   Lütfen CONSTITUTION/dps_calculation_rules.json dosyasını kontrol edin.")
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
        {"name": "Controlled Destruction", "more_damage": 1.30},
        {"name": "Elemental Focus", "more_damage": 1.20},
        {"name": "Faster Casting", "more_cast_speed": 1.25},
        {"name": "Arcane Surge", "more_damage": 1.10, "more_cast_speed": 1.15},
        {"name": "Concentrated Effect", "more_damage": 1.30},
        {"name": "Burning Damage", "more_damage": 1.20},
        {"name": "Ignite Proliferation", "more_damage": 1.10},
        {"name": "Deadly Ailments", "more_damage": 1.20},
        {"name": "Swift Affliction", "more_damage": 1.15},
        {"name": "Efficacy", "more_damage": 1.10}
    ]
    
    # Fireball ile uyumlu olanları filtrele
    compatible_supports = []
    for support in support_pool:
        compatible = True
        # Uyumsuz olanları filtrele
        if "Lightning" in support["name"]:
            compatible = False
        if "Cold" in support["name"]:
            compatible = False
        if "Physical" in support["name"]:
            compatible = False
        if "Chain" in support["name"]:
            compatible = False
        if "Pierce" in support["name"]:
            compatible = False
        
        if compatible:
            compatible_supports.append(support)
    
    print(f"   Toplam Support Havuzu: {len(support_pool)}")
    print(f"   Uyumlu Support'lar: {len(compatible_supports)}")
    for s in compatible_supports[:5]:
        more = s.get('more_damage', 1.0)
        speed = s.get('more_cast_speed', 1.0)
        print(f"      - {s['name']} (more_damage: {more}x, more_cast_speed: {speed}x)")

    # --- 3. Kombinasyonları Dene ---
    print("\n📌 3. Kombinasyonlar Test Ediliyor...")
    
    k = 5
    if len(compatible_supports) < k:
        print(f"❌ Yeterli support gem yok! {len(compatible_supports)} tane mevcut, {k} tane gerekli.")
        sys.exit(1)
    
    combinations = list(itertools.combinations(compatible_supports, k))
    print(f"   Toplam Kombinasyon: {len(combinations)}")

    # Her kombinasyon için DPS hesapla
    best_dps = 0
    best_combination = None
    best_result = None
    
    # Tüm kombinasyonları dene
    total = len(combinations)
    for i, combo in enumerate(combinations):
        # İlerleme göster (her 50'de bir)
        if i % max(1, total // 20) == 0:
            progress = (i / total) * 100
            print(f"   Test ediliyor: %{progress:.1f} ({i+1}/{total})...")
        
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
    
    if best_combination is None:
        print("❌ Hiçbir kombinasyon bulunamadı!")
        sys.exit(1)
    
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
        if not effects:
            effects.append("no damage modifiers")
        print(f"   {i}. {support['name']}: {', '.join(effects)}")
    
    # DPS detayları
    if best_result:
        print("\n📊 DPS Detayları:")
        breakdown = best_result.get("breakdown", {})
        for key, value in breakdown.items():
            if isinstance(value, float):
                print(f"   {key}: {value:.4f}")
            else:
                print(f"   {key}: {value}")

    print("\n" + "=" * 60)
    print("✅ Tarama tamamlandı!")

except ImportError as e:
    print(f"❌ Modül yüklenemedi: {e}")
    print("   SRC/agents/ klasöründe accountant.py olduğundan emin olun.")
except Exception as e:
    print(f"❌ Beklenmeyen hata: {e}")
    import traceback
    traceback.print_exc()
