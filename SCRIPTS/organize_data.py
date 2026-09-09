"""
Veri Düzenleyici - Mevcut DATA/processed/ yapısına göre
SKILL/ klasöründen dosyaları işler ve DATA/processed/ altına kaydeder
"""

import pandas as pd
import os
import shutil
from pathlib import Path

print("=" * 50)
print("📂 VERİ DÜZENLEYİCİ (Organizer)")
print("=" * 50)

# === KONFIGÜRASYON ===
SKILL_DIR = Path("SKILL")
PROCESSED_DIR = Path("DATA/processed")
ARCHIVE_DIR = Path("DATA/raw/archive")

# Klasörleri oluştur
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

# === ADIM 1: Skill Gems dosyalarını birleştir ===
print("\n📌 1. Aktif Skill'ler birleştiriliyor...")

skill_files = [
    "Skill Gems.csv",
    "Item Skill Gems Summary.csv",
    "Skill Gems Gemcutting.csv"
]

active_skills_list = []
for file_name in skill_files:
    file_path = SKILL_DIR / file_name
    if file_path.exists():
        df = pd.read_csv(file_path)
        active_skills_list.append(df)
        print(f"   ✅ {file_name} yüklendi ({len(df)} satır)")
    else:
        print(f"   ⚠️ {file_name} bulunamadı, atlanıyor.")

if active_skills_list:
    active_skills = pd.concat(active_skills_list, ignore_index=True)
    active_skills.to_csv(PROCESSED_DIR / "active_skills.csv", index=False)
    print(f"   ✅ Birleştirildi: {len(active_skills)} satır → active_skills.csv")
else:
    print("   ❌ Hiç skill dosyası bulunamadı!")

# === ADIM 2: Support Gems.csv'yi işle ===
print("\n📌 2. Support Gem'ler işleniyor...")

support_path = SKILL_DIR / "Support Gems.csv"
if support_path.exists():
    support_df = pd.read_csv(support_path)
    support_df.to_csv(PROCESSED_DIR / "support_gems.csv", index=False)
    print(f"   ✅ support_gems.csv kaydedildi ({len(support_df)} satır)")
else:
    print(f"   ⚠️ Support Gems.csv bulunamadı!")

# === ADIM 3: Kullanılmayan dosyaları arşivle ===
print("\n📌 3. Kullanılmayan dosyalar arşivleniyor...")

archive_files = [
    "Meta Skill Gem.csv",
    "Unknown Support.csv",
    "placeholder.txt"
]

for file_name in archive_files:
    src = SKILL_DIR / file_name
    dst = ARCHIVE_DIR / file_name
    if src.exists():
        shutil.move(str(src), str(dst))
        print(f"   📦 {file_name} → DATA/raw/archive/")
    else:
        print(f"   ⚠️ {file_name} bulunamadı, atlanıyor.")

# === ADIM 4: Sonuçları göster ===
print("\n" + "=" * 50)
print("📊 İŞLEM ÖZETİ")
print("=" * 50)

if PROCESSED_DIR.exists():
    files = list(PROCESSED_DIR.glob("*.csv"))
    print(f"\n📁 DATA/processed/ içeriği ({len(files)} dosya):")
    for f in files:
        df = pd.read_csv(f)
        print(f"   {f.name}: {len(df)} satır")

if ARCHIVE_DIR.exists():
    files = list(ARCHIVE_DIR.glob("*"))
    print(f"\n📁 DATA/raw/archive/ içeriği ({len(files)} dosya):")
    for f in files:
        print(f"   {f.name}")

print("\n✅ Düzenleme tamamlandı!")
