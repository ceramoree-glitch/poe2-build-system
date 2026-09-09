import sys
import json
import os
import pandas as pd
from pathlib import Path
from datetime import datetime

# Modül yollarını ekle
sys.path.insert(0, str(Path(__file__).parent.parent / 'SRC'))

print("=" * 50)
print("🚀 PoE2 Etiket Analiz Sistemi")
print("=" * 50)

# Veri klasörlerini kontrol et
print("\n📂 Klasör kontrolü:")
print(f"  SKILL klasörü: {'✅' if Path('SKILL').exists() else '❌'}")
print(f"  UNIQUE klasörü: {'✅' if Path('UNIQUE').exists() else '❌'}")
print(f"  ASCENDANCY klasörü: {'✅' if Path('ASCENDANCY').exists() else '❌'}")
print(f"  KEYWORDS klasörü: {'✅' if Path('KEYWORDS').exists() else '❌'}")

# 1. Verileri temizle
print("\n📂 Adım 1: Veriler temizleniyor...")

try:
    # Skill verilerini temizle
    skill_files = list(Path('SKILL').glob('*.csv'))
    print(f"  Skill CSV dosyaları: {len(skill_files)} adet")
    
    if len(skill_files) > 0:
        # Basit temizleme
        df_skill = pd.read_csv(skill_files[0])
        print(f"  ✅ Skill verisi: {len(df_skill)} satır")
        
        # Kategori ekle
        def classify_skill(row):
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
            if 'minion' in stats or 'minion' in name:
                tags.append('minion')
            
            return '|'.join(tags)
        
        df_skill['parsed_tags'] = df_skill.apply(classify_skill, axis=1)
        
        # Kaydet
        os.makedirs('DATA/processed', exist_ok=True)
        df_skill.to_csv('DATA/processed/skills_with_tags.csv', index=False)
        print(f"  ✅ Skill verisi kaydedildi: DATA/processed/skills_with_tags.csv")
        
except Exception as e:
    print(f"  ❌ Skill hatası: {e}")

try:
    # Unique verilerini temizle
    unique_files = list(Path('UNIQUE').glob('*.csv'))
    print(f"  Unique CSV dosyaları: {len(unique_files)} adet")
    
    if len(unique_files) > 0:
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

# 2. Rapor oluştur
print("\n📊 Adım 2: Rapor oluşturuluyor...")

try:
    report = {
        'date': datetime.now().isoformat(),
        'status': 'success',
        'files_processed': {
            'skill': len(skill_files) if 'skill_files' in locals() else 0,
            'unique': len(unique_files) if 'unique_files' in locals() else 0
        }
    }
    # ... (mevcut kodunuzun sonuna yakın bir yere, rapor oluşturma bölümüne ekleyin)

# --- Raporu zenginleştirme (Ekleme) ---
print("📊 Adım 4: Rapor zenginleştiriliyor...")

try:
    # processed klasöründeki en son verileri oku
    skill_df = pd.read_csv('DATA/processed/skills_with_tags.csv')
    
    # 1. Popüler etiketleri hesapla
    all_tags = []
    if 'parsed_tags' in skill_df.columns:
        for tags in skill_df['parsed_tags']:
            if pd.notna(tags):
                all_tags.extend(str(tags).split('|'))
    
    from collections import Counter
    tag_counts = Counter(all_tags)
    popular_tags = dict(tag_counts.most_common(10))
    
    # 2. Kategori dağılımını hesapla (örnek olarak 'slot' veya 'category' sütunundan)
    categories = {}
    if 'slot' in skill_df.columns:
        categories = skill_df['slot'].value_counts().to_dict()
    elif 'category' in skill_df.columns:
        categories = skill_df['category'].value_counts().to_dict()
    
    # 3. Ana rapor verilerine bu bilgileri ekle
    report_data['popular_tags'] = popular_tags
    report_data['categories'] = categories
    
    # Raporu tekrar kaydet
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    print(f"  ✅ Rapor zenginleştirildi: {report_file}")
    print(f"  🏷️ Popüler tag'ler: {dict(list(popular_tags.items())[:5])}")
    
except Exception as e:
    print(f"  ⚠️ Rapor zenginleştirme hatası: {e}")

# ... (mevcut kodunuzun devamı)
    # Raporu kaydet
    os.makedirs('OUTPUTS/reports/daily', exist_ok=True)
    report_file = f'OUTPUTS/reports/daily/tag_analysis_{datetime.now().strftime("%Y-%m-%d")}.json'
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"  ✅ Rapor kaydedildi: {report_file}")
    
except Exception as e:
    print(f"  ❌ Rapor hatası: {e}")

# 3. Özet göster
print("\n📈 Özet:")
try:
    if Path('DATA/processed/skills_with_tags.csv').exists():
        df = pd.read_csv('DATA/processed/skills_with_tags.csv')
        print(f"  ✅ Skill: {len(df)} satır")
        
        # Tag istatistikleri
        if 'parsed_tags' in df.columns:
            all_tags = []
            for tags in df['parsed_tags']:
                if pd.notna(tags):
                    all_tags.extend(str(tags).split('|'))
            
            from collections import Counter
            tag_counts = Counter(all_tags)
            print(f"  🏷️ Popüler tag'ler: {dict(tag_counts.most_common(5))}")
    
    if Path('DATA/processed/uniques_with_tags.csv').exists():
        df = pd.read_csv('DATA/processed/uniques_with_tags.csv')
        print(f"  ✅ Unique: {len(df)} satır")
        
        if 'slot' in df.columns:
            print(f"  🗂️ Slot dağılımı: {dict(df['slot'].value_counts().head(5))}")
            
except Exception as e:
    print(f"  ❌ Özet hatası: {e}")

print("\n✅ Tüm işlemler tamamlandı!")
