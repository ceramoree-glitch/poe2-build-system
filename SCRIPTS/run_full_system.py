"""
Tüm Ajanları Çalıştıran Ana Sistem
Sadece sizin CSV verilerinizle çalışır
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# SRC klasörünü Python path'ine ekle
sys.path.insert(0, str(Path(__file__).parent.parent / 'SRC'))

from agents.architect import Architect
from agents.chief import Chief


def main():
    print("=" * 60)
    print("⚔️ POE2 BUILD OPTIMIZER - TAM SİSTEM")
    print("=" * 60)
    
    # 1. Mimar build'leri seçsin
    print("\n📌 Adım 1: Mimar Build'leri Seçiyor...")
    architect = Architect()
    builds = architect.select_builds(10, 5, 2)
    
    if not builds:
        print("❌ Hiç build oluşturulamadı! Verilerinizi kontrol edin.")
        print("   SKILL/ klasöründe skill CSV'niz var mı?")
        print("   ASCENDANCY/ klasöründe ascendancy CSV'niz var mı?")
        return
    
    print(f"✅ {len(builds)} build oluşturuldu.")
    
    # 2. Şef değerlendirsin
    print("\n📌 Adım 2: Şef Build'leri Değerlendiriyor...")
    chief = Chief()
    results = chief.evaluate_builds(builds)
    
    if not results:
        print("❌ Hiç build değerlendirilemedi!")
        return
    
    print(f"✅ {len(results)} build değerlendirildi.")
    
    # 3. Raporu kaydet
    report_dir = Path("OUTPUTS/reports/builds")
    report_dir.mkdir(parents=True, exist_ok=True)
    
    report_file = report_dir / f"full_report_{datetime.now().strftime('%Y-%m-%d')}.json"
    
    report_data = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_builds": len(results),
        "ranked_builds": results
    }
    
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Rapor kaydedildi: {report_file}")
    
    # 4. Sonuçları göster
    print("\n" + "=" * 60)
    print("🏆 NİHAİ SIRALAMA")
    print("=" * 60)
    
    if results:
        print(f"\n🥇 EN İYİ BUILD:")
        print(f"   Skill: {results[0]['skill']}")
        print(f"   DPS: {results[0]['dps']:,.2f}")
        print(f"   Support'lar: {', '.join(results[0]['supports'][:3])}")
        print(f"   Ascendancy: {', '.join(results[0]['ascendancies'])}")
    
    print("\n🏆 SIRALAMA (Top 5):")
    for i, build in enumerate(results[:5], 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        print(f"   {medal} {build['skill']} - {build['dps']:,.2f} DPS")
    
    print("\n✅ Sistem tamamlandı!")


if __name__ == "__main__":
    main()
