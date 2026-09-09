"""
Ham Scraper CSV'sini Kural Tabanlı Temizleme
DATA/raw/skills_raw.csv dosyasını işler, temizler ve DATA/processed/cleaned_skills.csv olarak kaydeder.
"""

import pandas as pd
import os
import sys
from pathlib import Path

# === KONFIGÜRASYON ===
RAW_CSV_PATH = "DATA/raw/skills_raw.csv"
OUTPUT_CSV_PATH = "DATA/processed/cleaned_skills.csv"

def main():
    print("=" * 50)
    print("🧹 SKILL VERİSİ ÖN İŞLEME")
    print("=" * 50)

    # === ADIM 1: Veriyi yükle ===
    print("\n📂 Ham veri yükleniyor...")
    
    if not Path(RAW_CSV_PATH).exists():
        print(f"❌ Hata: {RAW_CSV_PATH} bulunamadı!")
        print("   Lütfen ham CSV dosyasını DATA/raw/ klasörüne yükleyin.")
        sys.exit(1)
    
    df = pd.read_csv(RAW_CSV_PATH)
    print(f"✅ Yüklendi: {len(df)} satır, {len(df.columns)} sütun")
    print(f"   Sütunlar: {', '.join(df.columns[:8])} ...")

    # === ADIM 2: web_scraper_order, web_scraper_start_url, image sütunlarını kaldır ===
    print("\n🗑️ Gereksiz sütunlar temizleniyor...")
    remove_cols = ["web_scraper_order", "web_scraper_start_url", "image"]
    removed = [c for c in remove_cols if c in df.columns]
    df.drop(columns=removed, inplace=True, errors="ignore")
    print(f"   Kaldırıldı: {removed if removed else '(hiçbiri mevcut değil)'}")

    # === ADIM 3: name5'ten name46'ya kadar olan sütunları sil ===
    cols_to_drop = [f"name{i}" for i in range(5, 47)]
    removed_range = [c for c in cols_to_drop if c in df.columns]
    df.drop(columns=removed_range, inplace=True, errors="ignore")
    print(f"   Kaldırıldı: name5 - name46 arası ({len(removed_range)} sütun)")

    # === ADIM 4: name sütununu skill_name olarak yeniden adlandır ===
    if "name" in df.columns:
        df.rename(columns={"name": "skill_name"}, inplace=True)
        print("   ✏️ name → skill_name")

    # === ADIM 5: name3, name4 ve diğer etiket sütunlarını birleştir ===
    print("\n🏷️ Etiketler birleştiriliyor...")
    tag_columns = ["name3", "name4", "name2", "tags"]
    existing_tag_cols = [c for c in tag_columns if c in df.columns]
    print(f"   Kullanılan etiket sütunları: {existing_tag_cols}")

    def merge_tags(row):
        all_tags = []
        for col in existing_tag_cols:
            val = row.get(col, "")
            if pd.notna(val) and str(val).strip():
                val_str = str(val).strip()
                if "," in val_str:
                    all_tags.extend([t.strip() for t in val_str.split(",") if t.strip()])
                else:
                    all_tags.append(val_str)
        unique_tags = list(set(all_tags))
        return ", ".join(unique_tags) if unique_tags else ""

    df["tags"] = df.apply(merge_tags, axis=1)
    print(f"   ✅ Etiketler birleştirildi")

    # === ADIM 6: Sadece skill_name ve tags sütunlarını tut ===
    print("\n📊 Final veri oluşturuluyor...")
    df_final = df[["skill_name", "tags"]].copy()
    print(f"   Satır: {len(df_final)}")
    print(f"   Sütunlar: {', '.join(df_final.columns)}")

    # === ADIM 7: Çıktıyı kaydet ===
    os.makedirs(os.path.dirname(OUTPUT_CSV_PATH), exist_ok=True)
    df_final.to_csv(OUTPUT_CSV_PATH, index=False, encoding='utf-8')
    print(f"\n✅ Kaydedildi: {OUTPUT_CSV_PATH}")

    # === ADIM 8: Örnek veri göster ===
    print("\n📋 İlk 5 satır:")
    print(df_final.head().to_string(index=False))

    print("\n" + "=" * 50)
    print("✅ ÖN İŞLEME TAMAMLANDI")
    print("=" * 50)

if __name__ == "__main__":
    main()
