"""
Veri Düzenleyici - SKILL/ klasöründeki 8 dosyayı temizler ve DATA/processed/ altına kaydeder
"""

import pandas as pd
import os
import shutil
from pathlib import Path

print("=" * 60)
print("📂 VERİ DÜZENLEYİCİ (Organizer) - Temizleme Adımları Aktif")
print("=" * 60)

# === KONFIGÜRASYON ===
SKILL_DIR = Path("SKILL")
PROCESSED_DIR = Path("DATA/processed")
ARCHIVE_DIR = Path("DATA/raw/archive")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)


def clean_skill_df(df, file_name=""):
    """
    Skill dataframe'ini temizler:
    - web_scraper_order, web_scraper_start_url, image silinir.
    - name5'ten name46'ya kadar tüm sütunlar silinir.
    - name → skill_name olarak yeniden adlandırılır.
    - name3, name4, name2, tags'den benzersiz tags oluşturulur.
    - Sadece skill_name ve tags sütunları döndürülür.
    """
    original_count = len(df)
    
    # 1. Gereksiz sütunları kaldır
    remove_cols = ["web_scraper_order", "web_scraper_start_url", "image"]
    removed = [c for c in remove_cols if c in df.columns]
    df.drop(columns=removed, inplace=True, errors="ignore")
    
    # 2. name5'ten name46'ya kadar sil
    cols_to_drop = [f"name{i}" for i in range(5, 47)]
    dropped = [c for c in cols_to_drop if c in df.columns]
    df.drop(columns=dropped, inplace=True, errors="ignore")
    
    # 3. name → skill_name
    if "name" in df.columns:
        df.rename(columns={"name": "skill_name"}, inplace=True)
    
    # 4. Etiketleri birleştir (name3, name4, name2, tags)
    tag_cols = ["name3", "name4", "name2", "tags"]
    existing_tags = [c for c in tag_cols if c in df.columns]
    
    def merge_tags(row):
        all_tags = []
        for col in existing_tags:
            val = row.get(col, "")
            if pd.notna(val) and str(val).strip():
                val_str = str(val).strip()
                if "," in val_str:
                    all_tags.extend([t.strip() for t in val_str.split(",") if t.strip()])
                else:
                    all_tags.append(val_str)
        unique = list(set(all_tags))
        return ", ".join(unique) if unique else ""
    
    df["tags"] = df.apply(merge_tags, axis=1)
    
    # 5. Sadece skill_name ve tags
    result = df[["skill_name", "tags"]].copy()
    result.dropna(subset=["skill_name"], inplace=True)
    
    print(f"   {file_name}: {original_count} → {len(result)} satır (temizlendi)")
    return result


# === ADIM 1: Aktif Skill'leri Birleştir ===
print("\n📌 1. Aktif Skill'ler birleştiriliyor...")

skill_files = [
    "Skill Gems.csv",
    "Item Skill Gems Summary.csv",
    "Skill Gems Gemcutting.csv"
]

active_list = []
for fname in skill_files:
    fpath = SKILL_DIR / fname
    if fpath.exists():
        df = pd.read_csv(fpath)
        cleaned = clean_skill_df(df, fname)
        active_list.append(cleaned)
    else:
        print(f"   ⚠️ {fname} bulunamadı, atlanıyor.")

if active_list:
    active_skills = pd.concat(active_list, ignore_index=True)
    active_skills.drop_duplicates(subset=["skill_name"], inplace=True)
    active_skills.to_csv(PROCESSED_DIR / "active_skills.csv", index=False)
    print(f"   ✅ Birleştirildi: {len(active_skills)} benzersiz skill → active_skills.csv")
else:
    print("   ❌ Hiç skill dosyası bulunamadı!")


# === ADIM 2: Support Gem'leri Birleştir ===
print("\n📌 2. Support Gem'ler birleştiriliyor...")

support_files = [
    "Support Gems.csv",
    "Spirit Gems.csv"
]

support_list = []
for fname in support_files:
    fpath = SKILL_DIR / fname
    if fpath.exists():
        df = pd.read_csv(fpath)
        cleaned = clean_skill_df(df, fname)
        support_list.append(cleaned)
    else:
        print(f"   ⚠️ {fname} bulunamadı, atlanıyor.")

if support_list:
    support_gems = pd.concat(support_list, ignore_index=True)
    support_gems.drop_duplicates(subset=["skill_name"], inplace=True)
    support_gems.to_csv(PROCESSED_DIR / "support_gems.csv", index=False)
    print(f"   ✅ Birleştirildi: {len(support_gems)} benzersiz support → support_gems.csv")
else:
    print("   ❌ Hiç support dosyası bulunamadı!")


# === ADIM 3: Ignore Edilecek Dosyaları Arşivle ===
print("\n📌 3. Ignore dosyaları arşivleniyor...")

ignore_files = [
    "Meta Skill Gem.csv",
    "Unknown Support.csv",
    "placeholder.txt"
]

for fname in ignore_files:
    src = SKILL_DIR / fname
    dst = ARCHIVE_DIR / fname
    if src.exists():
        shutil.move(str(src), str(dst))
        print(f"   📦 {fname} → DATA/raw/archive/")
    else:
        print(f"   ⚠️ {fname} bulunamadı, atlanıyor.")


# === ADIM 4: Sonuçları Göster ===
print("\n" + "=" * 60)
print("📊 İŞLEM ÖZETİ")
print("=" * 60)

if PROCESSED_DIR.exists():
    files = list(PROCESSED_DIR.glob("*.csv"))
    print(f"\n📁 DATA/processed/ içeriği ({len(files)} dosya):")
    for f in files:
        df = pd.read_csv(f)
        print(f"   {f.name}: {len(df)} satır, {len(df.columns)} sütun")

if ARCHIVE_DIR.exists():
    files = list(ARCHIVE_DIR.glob("*"))
    print(f"\n📁 DATA/raw/archive/ içeriği ({len(files)} dosya):")
    for f in files:
        print(f"   {f.name}")

print("\n✅ Temizleme ve düzenleme tamamlandı!")
