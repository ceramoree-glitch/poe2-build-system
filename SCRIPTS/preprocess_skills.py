"""
Ham Scraper CSV'sini Kural Tabanlı Temizleme
DATA/raw/ altındaki CSV'yi işler, temizler ve DATA/processed/ altına kaydeder
"""

import pandas as pd
import os
from pathlib import Path

# === KONFIGÜRASYON ===
RAW_CSV_PATH = "DATA/raw/skills_raw.csv"          # Ham scraper verisi
OUTPUT_CSV_PATH = "DATA/processed/cleaned_skills.csv"  # Temiz çıktı

# === ADIM 1: Veriyi yükle ===
print("📂 Ham veri yükleniyor...")
df = pd.read_csv(RAW_CSV_PATH)
print(f"✅ Yüklendi: {len(df)} satır, {len(df.columns)} sütun")

# === ADIM 2: Belirtilen sütunları kaldır ===
remove_cols = ["web_scraper_order", "web_scraper_start_url", "image"]
df.drop(columns=[c for c in remove_cols if c in df.columns], inplace=True, errors="ignore")
print(f"🗑️ web_scraper_order, web_scraper_start_url, image kaldırıldı.")

# === ADIM 3: name5'ten name46'ya kadar olan sütunları sil ===
cols_to_drop = [f"name{i}" for i in range(5, 47)]  # name5'ten name46'ya kadar
df.drop(columns=[c for c in cols_to_drop if c in df.columns], inplace=True, errors="ignore")
print(f"🗑️ name5'ten name46'ya kadar sütunlar kaldırıldı.")

# === ADIM 4: name sütununu skill_name olarak yeniden adlandır ===
if "name" in df.columns:
    df.rename(columns={"name": "skill_name"}, inplace=True)
    print("✏️ name → skill_name olarak yeniden adlandırıldı.")

# === ADIM 5: name3, name4 ve diğer etiket sütunlarını birleştir ===
# Etiket içerebilecek sütunlar: name3, name4, name2, tags (varsa)
tag_columns = ["name3", "name4", "name2", "tags"]
existing_tag_cols = [c for c in tag_columns if c in df.columns]

def merge_tags(row):
    """Birden fazla sütundaki etiketleri birleştirir, benzersiz yapar"""
    all_tags = []
    for col in existing_tag_cols:
        val = row.get(col, "")
        if pd.notna(val) and val != "":
            # Eğer değer virgülle ayrılmışsa ayır, değilse tek ekle
            if isinstance(val, str) and "," in val:
                all_tags.extend([t.strip() for t in val.split(",") if t.strip()])
            else:
                all_tags.append(str(val).strip())
    # Benzersiz yap ve virgülle birleştir
    unique_tags = list(set(all_tags))
    return ", ".join(unique_tags) if unique_tags else ""

df["tags"] = df.apply(merge_tags, axis=1)
print(f"🏷️ Etiketler birleştirildi: {len(existing_tag_cols)} sütundan.")

# === ADIM 6: Sadece skill_name ve tags sütunlarını tut ===
df_final = df[["skill_name", "tags"]].copy()
print(f"📊 Final veri: {len(df_final)} satır, 2 sütun (skill_name, tags)")

# === ADIM 7: Çıktıyı kaydet ===
os.makedirs(os.path.dirname(OUTPUT_CSV_PATH), exist_ok=True)
df_final.to_csv(OUTPUT_CSV_PATH, index=False)
print(f"✅ Kaydedildi: {OUTPUT_CSV_PATH}")
