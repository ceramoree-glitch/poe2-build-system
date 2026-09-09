import sys
import json
import os
import pandas as pd
from pathlib import Path
from datetime import datetime
from collections import Counter

# Modül yollarını ekle
sys.path.insert(0, str(Path(__file__).parent.parent / 'SRC'))

print("=" * 50)
print("🚀 PoE2 Etiket Analiz Sistemi")
print("=" * 50)

# --- 1. VERİLERİ TEMİZLE ---
print("\n📂 Adım 1: Veriler temizleniyor...")

# Skill verilerini temizle
skill_files = list(Path('SKILL').glob('*.csv'))
print(f"  Skill CSV dosyaları: {len(skill_files)} adet")

if len(skill_files) > 0:
    try:
        df_skill = pd.read_csv(skill_files[0])
        print(f"  ✅ Skill verisi: {len(df_skill)} satır")
        
        # Etiketleri parse et
        def parse_tags(row):
            name = str(row.get('name', '')).lower()
            stats = str(row.get('stats', '')).lower()
            
            tags = []
            if 'fire' in stats or 'fire' in name:
                tags.append('fire')
            if 'cold' in stats or 'cold' in name:
                tags.append('cold')
            if 'lightning' in stats or 'lightning' in name:
                tags.append('lightning')
            if 'chaos' in stats or 'chaos' in name:
                tags.append('chaos')
            if 'physical' in stats or 'physical' in name:
                tags.append('physical')
            if 'spell' in stats or 'spell' in name:
                tags.append('spell')
            if 'attack' in stats or 'attack' in name:
                tags.append('attack')
            if 'melee' in stats or 'melee' in name:
                tags.append('melee')
            if 'minion' in stats or 'minion' in name:
                tags.append('minion')
            if 'aura' in stats or 'aura' in name:
                tags.append('aura')
            if 'curse' in stats or 'curse' in name:
                tags.append('curse')
            
            return '|'.join(tags)
        
        df_skill['parsed_tags'] = df_skill.apply(parse_tags, axis=1)
        
        # Kategori (slot) belirle
        def get_category(row):
            name = str(row.get('name', '')).lower()
            if 'body' in name or 'coat' in name:
                return 'Body Armour'
            elif 'helmet' in name or 'hood' in name:
                return 'Helmet'
            elif 'gloves' in name:
                return 'Gloves'
            elif 'boots' in name:
                return 'Boots'
            elif 'shield' in name:
                return 'Shield'
            elif 'belt' in name:
                return 'Belt'
            elif 'amulet' in name:
                return 'Amulet'
            elif 'ring' in name:
                return 'Ring'
            return 'Other'
        
        df_skill['category'] = df_skill.apply(get_category, axis=1)
        
        # Kaydet
        os.makedirs('DATA/processed', exist_ok=True)
        df_skill.to_csv('DATA/processed/skills_with_tags.csv', index=False)
        print(f"  ✅ Skill verisi kaydedildi: DATA/processed/skills_with_tags.csv")
        
    except Exception as e:
        print(f"  ❌ Skill hatası: {e}")
        df_skill = None
else:
    df_skill = None

# Unique verilerini temizle
unique_files = list(Path('UNIQUE').glob('*.csv'))
print(f"  Unique CSV dosyaları: {len(unique_files)} adet")

if len(unique_files) > 0:
    try:
        df_unique = pd.read_csv(unique_files[0])
        print(f"  ✅ Unique verisi: {len(df_unique)} satır")
        
        # Slot belirle
        def get_slot(row):
            name = str(row.get('name', '')).lower()
            if 'body' in name or 'coat' in name:
                return 'Body Armour'
            elif 'helmet' in name or 'hood' in name:
                return 'Helmet'
            elif 'gloves' in name:
                return 'Gloves'
            elif 'boots' in name:
                return 'Boots'
            elif 'shield' in name:
                return 'Shield'
            elif 'belt' in name:
                return 'Belt'
            elif 'amulet' in name:
                return 'Amulet'
            elif 'ring' in name:
                return 'Ring'
            return 'Other'
        
        df_unique['slot'] = df_unique.apply(get_slot, axis=1)
        
        # Kaydet
        df_unique.to_csv('DATA/processed/uniques_with_tags.csv', index=False)
        print(f"  ✅ Unique verisi kaydedildi: DATA/processed/uniques_with_tags.csv")
        
    except Exception as e:
        print(f"  ❌ Unique hatası: {e}")
        df_unique = None
else:
    df_unique = None

# --- 2. RAPOR OLUŞTUR ---
print("\n📊 Adım 2: Rapor oluşturuluyor...")

try:
    # Temel rapor verileri
    report_data = {
        'date': datetime.now().isoformat(),
        'status': 'success',
        'files_processed': {
            'skill': len(skill_files) if skill_files else 0,
            'unique': len(unique_files) if unique_files else 0
        }
    }
    
    # Skill verilerinden etiket analizi
    if df_skill is not None and len(df_skill) > 0:
        # Popüler etiketler
        all_tags = []
        if 'parsed_tags' in df_skill.columns:
            for tags in df_skill['parsed_tags']:
                if pd.notna(tags):
                    all_tags.extend(str(tags).split('|'))
        
        tag_counts = Counter(all_tags)
        report_data['popular_tags'] = dict(tag_counts.most_common(10))
        
        # Kategori dağılımı
        if 'category' in df_skill.columns:
            report_data['categories'] = df_skill['category'].value_counts().to_dict()
        elif 'slot' in df_skill.columns:
            report_data['categories'] = df_skill['slot'].value_counts().to_dict()
        else:
            report_data['categories'] = {}
    
    # Unique verilerinden slot dağılımı
    if df_unique is not None and len(df_unique) > 0:
        if 'slot' in df_unique.columns:
            report_data['unique_categories'] = df_unique['slot'].value_counts().to_dict()
    
    # Raporu kaydet
    os.makedirs('OUTPUTS/reports/daily', exist_ok=True)
    report_file = f'OUTPUTS/reports/daily/tag_analysis_{datetime.now().strftime("%Y-%m-%d")}.json'
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    print(f"  ✅ Rapor kaydedildi: {report_file}")
    
except Exception as e:
    print(f"  ❌ Rapor hatası: {e}")
    report_data = {'status': 'error', 'message': str(e)}

# --- 3. ÖZET GÖSTER ---
print("\n📈 Özet:")

if df_skill is not None:
    print(f"  ✅ Skill: {len(df_skill)} satır")
    if 'popular_tags' in report_data and report_data['popular_tags']:
        top_tags = list(report_data['popular_tags'].items())[:5]
        print(f"  🏷️ Popüler tag'ler: {dict(top_tags)}")
    if 'categories' in report_data and report_data['categories']:
        print(f"  🗂️ Kategori dağılımı: {dict(list(report_data['categories'].items())[:5])}")

if df_unique is not None:
    print(f"  ✅ Unique: {len(df_unique)} satır")
    if 'unique_categories' in report_data and report_data['unique_categories']:
        print(f"  🗂️ Slot dağılımı: {dict(list(report_data['unique_categories'].items())[:5])}")

print("\n✅ Tüm işlemler tamamlandı!")
