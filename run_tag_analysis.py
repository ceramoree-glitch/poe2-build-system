import sys
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
- name: 🧮 Muhasebeci Ajanını Test Et
  run: |
    python SCRIPTS/test_accountant.py
- name: 🧠 Ajan sistemini çalıştır
  run: |
    python SCRIPTS/agent_system.py
# Modül yollarını ekle
sys.path.insert(0, str(Path(__file__).parent.parent / 'SRC'))

from cleaners.tag_cleaner import TagCleaner
from analyzers.tag_filter import TagFilter
from reports.tag_report import TagReporter

print("=" * 50)
print("🚀 PoE2 Etiket Analiz Sistemi")
print("=" * 50)

# 1. Verileri temizle ve etiketle
print("\n📂 Adım 1: Veriler temizleniyor...")
cleaner = TagCleaner()

# Skill verilerini temizle
try:
    skill_cleaned = cleaner.clean_skill_data(
        'SKILL/skill_gems.csv',
        'DATA/processed/skills_with_tags.csv'
    )
    print(f"✅ Skill verisi temizlendi: {len(skill_cleaned)} satır")
except Exception as e:
    print(f"❌ Skill temizleme hatası: {e}")
    skill_cleaned = None

# Unique verilerini temizle
try:
    unique_cleaned = cleaner.clean_unique_data(
        'UNIQUE/armour_uniques.csv',
        'DATA/processed/uniques_with_tags.csv'
    )
    print(f"✅ Unique verisi temizlendi: {len(unique_cleaned)} satır")
except Exception as e:
    print(f"❌ Unique temizleme hatası: {e}")
    unique_cleaned = None

# 2. Etiket filtreleme
print("\n🔍 Adım 2: Etiket filtreleme...")
filter_tool = TagFilter()
filter_tool.load_data()

# Popüler etiketleri bul
popular_tags = ['fire', 'cold', 'lightning', 'chaos', 'physical', 'spell', 'attack', 'melee', 'minion']

for tag in popular_tags:
    result = filter_tool.get_stats_by_tag(tag)
    print(f"  🏷️ {tag}: {result['skill_count']} skill, {result['unique_count']} unique")

# 3. Rapor oluştur
print("\n📊 Adım 3: Rapor oluşturuluyor...")

# Verileri yükle
try:
    skill_df = pd.read_csv('DATA/processed/skills_with_tags.csv')
    unique_df = pd.read_csv('DATA/processed/uniques_with_tags.csv')
    
    reporter = TagReporter(skill_df, unique_df)
    report = reporter.generate_tag_analysis()
    
    # Raporu kaydet
    import os
    os.makedirs('OUTPUTS/reports/daily', exist_ok=True)
    os.makedirs('OUTPUTS/reports/weekly', exist_ok=True)
    
    report_file = f'OUTPUTS/reports/daily/tag_analysis_{datetime.now().strftime("%Y-%m-%d")}.json'
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Rapor kaydedildi: {report_file}")
    
    # Özet göster
    print("\n📈 Özet:")
    print(f"  Toplam skill: {report['summary']['total_skill_tags']}")
    print(f"  En popüler tag'ler: {', '.join(report['summary']['top_tags'])}")
    
except Exception as e:
    print(f"❌ Rapor oluşturma hatası: {e}")

print("\n✅ Tüm işlemler tamamlandı!")
