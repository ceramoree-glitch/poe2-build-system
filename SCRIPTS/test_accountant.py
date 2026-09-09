"""
Muhasebeci Ajanı Test Scripti
"""

import sys
from pathlib import Path

# SRC klasörünü Python path'ine ekle
sys.path.insert(0, str(Path(__file__).parent.parent / 'SRC'))

print("🧮 Muhasebeci Ajanı Testi")
print("-" * 40)

try:
    from agents.accountant import Accountant
    
    # Muhasebeciyi başlat
    accountant = Accountant()
    
    if accountant.is_ready:
        print("✅ Muhasebeci hazır!")
        
        # Örnek veriler (Fireball build)
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
        
        # DPS hesapla
        print("\n🔥 Fireball Build DPS Hesaplaması:")
        result = accountant.calculate_dps(skill, supports, equipment)
        
        if "error" in result:
            print(f"❌ Hata: {result['error']}")
        else:
            print(f"🎯 Toplam DPS: {result['dps']:,.2f}")
            print("\n📊 Detaylı Döküm:")
            for key, value in result.get("breakdown", {}).items():
                print(f"   {key}: {value}")
        
        # Formül bilgileri
        print("\n📐 Kullanılan Formül:")
        formula = accountant.get_formula()
        print(f"   {formula.get('main', 'Bilinmiyor')}")
        
        # Hasar pipeline adımları
        print("\n🔧 Hasar Pipeline Adımları:")
        pipeline = accountant.get_pipeline()
        for step in pipeline[:5]:  # İlk 5 adımı göster
            print(f"   {step.get('step')}. {step.get('name')}")
        
        # Kural özeti
        summary = accountant.get_rules_summary()
        print(f"\n📊 Kural Özeti:")
        print(f"   Ad: {summary.get('name', 'Bilinmiyor')}")
        print(f"   Versiyon: {summary.get('version', 'Bilinmiyor')}")
        print(f"   Durum: {summary.get('status', 'Bilinmiyor')}")
        
    else:
        print("❌ Muhasebeci hazır değil!")
        print("   Kural dosyasını kontrol edin: CONSTITUTION/dps_calculation_rules.json")
        
except ImportError as e:
    print(f"❌ Modül yüklenemedi: {e}")
    print("   SRC/agents/ klasöründe accountant.py olduğundan emin olun.")
except Exception as e:
    print(f"❌ Beklenmeyen hata: {e}")
