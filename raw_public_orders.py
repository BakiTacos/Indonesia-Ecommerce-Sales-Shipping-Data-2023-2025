import pandas as pd
import re
from pathlib import Path

# =========================
#  KONFIGURASI FOLDER
# =========================

RAW_DIR = Path("RAW")                 # input private
PUBLIC_DIR = Path("RAW_PUBLIC")       # output aman
PUBLIC_DIR.mkdir(exist_ok=True)

# =========================
#  NAMA KOLOM (HEADER RAW)
# =========================

COL_ORDER_ID      = "No. Pesanan"
COL_PRODUCT_NAME  = "Nama Produk"
COL_CANCEL_REASON = "Alasan Pembatalan"

# =========================
#  FUNGSI KATEGORISASI PRODUK
# =========================

def categorize_product(name: str) -> str:
    """
    Ubah 'Nama Produk' menjadi kategori umum.
    """
    if not isinstance(name, str):
        return "Other"

    n = name.lower()

    # Aksesoris ID Card / Name Tag
    if "id card" in n or "name tag" in n or "kartu identitas" in n:
        return "Aksesoris ID Card"

    # Celengan
    if "celengan" in n:
        return "Celengan"

    # Lunch box / bekal / bento / rantang
    if "lunch" in n or "bekal" in n or "bento" in n or "rantang" in n:
        return "Lunch Box / Rantang"

    # Botol, gelas, mug, cangkir, drink
    if ("botol" in n or "tumbler" in n or "drink" in n or
        "mug" in n or "cangkir" in n or "gelas" in n):
        return "Botol / Gelas / Mug"

    # Toples / sealware / jar
    if "toples" in n or "sealware" in n or "jar" in n:
        return "Toples / Sealware"

    # Baskom / mixing bowl / mangkok besar
    if "baskom" in n or "mixing bowl" in n:
        return "Baskom / Mangkok Besar"

    # Mangkok sambal / saus
    if "sambal" in n or "saos" in n or "saus" in n:
        return "Mangkok Sambal / Saus"

    # Tempat nasi / bakul nasi / wakul
    if "tempat nasi" in n or "bakul nasi" in n or "sangku nasi" in n or "wakul" in n:
        return "Tempat Nasi"

    # Rak
    if n.startswith("rak") or " rak " in n:
        return "Rak / Rak Serbaguna"

    # Keranjang
    if "keranjang" in n:
        return "Keranjang"

    # Nampan / tray / tampah / baki
    if ("nampan" in n or "tampah" in n or " tray " in n or
        "round tray" in n or "baki" in n):
        return "Nampan / Tray"

    # Piring
    if "piring" in n or "plate" in n:
        return "Piring"

    # Mangkok (umum)
    if "mangkok" in n or "mangkuk" in n:
        return "Mangkok"

    # Teko / jug / eskan / pitcher
    if ("teko" in n or "water jug" in n or "eskan" in n or
        "pitcher" in n or "jug" in n):
        return "Teko / Jug"

    # Saringan / strainer
    if ("saringan" in n or "strainer" in n or "filter" in n or
        "ayakan" in n or "tirisan" in n):
        return "Saringan / Strainer"

    # Peralatan makan
    if "sendok" in n or "garpu" in n or "steak" in n:
        return "Peralatan Makan"

    # Pisau / alat potong
    if "pisau" in n or "knife" in n or "parutan" in n:
        return "Pisau / Alat Potong"

    # Spatula / sutil
    if "spatula" in n or "sutil" in n:
        return "Spatula"

    # Chopper, penggiling, blender manual, mixer
    if "chopper" in n or "penggiling" in n or "blender" in n or "mixer" in n:
        return "Pengolah Bumbu / Sayur"

    # Talenan
    if "talenan" in n or "cutting board" in n:
        return "Talenan"

    # Kuas roti / baking brush
    if ("baking brush" in n or "kuas roti" in n or
        ("kuas" in n and "roti" in n)):
        return "Kuas Baking / Masak"

    # Gantungan / hanger baju
    if ("gantungan baju" in n or "hanger" in n or
        ("gantungan" in n and "baju" in n)):
        return "Gantungan Baju / Hanger"

    # Bangku / kursi kecil
    if ("bangku" in n or "kursi jongkok" in n or
        ("kursi" in n and "mini" in n)):
        return "Bangku / Kursi Kecil"

    # Tempat sampah
    if "tempat sampah" in n or "keranjang sampah" in n or "tong sampah" in n:
        return "Tempat Sampah"

    # Aksesoris pintu
    if ("engsel" in n or "grendel" in n or "selot" in n or
        "handle" in n or "tarikan" in n or "knob" in n or "door lock" in n):
        return "Aksesoris Pintu"

    # Peralatan kamar mandi
    if ("tempat sabun" in n or "soap" in n or "toilet" in n or
        "wc" in n or "kamar mandi" in n):
        return "Peralatan Kamar Mandi"
    if "spons mandi" in n or "shower puff" in n or "bath sponge" in n:
        return "Aksesoris Mandi"
    if "gayung" in n:
        return "Gayung"

    # Peralatan kebersihan
    if "sapu" in n:
        return "Sapu / Pembersih Lantai"
    if "sikat" in n or "scourer" in n or "bola kawat" in n:
        return "Sikat / Pembersih"

    # Seal / baut / skrup / roof
    if ("weather seal" in n or "roof seal" in n or "penutup skrup" in n or
        "skrup" in n or "baut" in n or "drilling screw" in n):
        return "Seal / Baut / Roof"
    if "kunci l" in n or "kunci " in n:
        return "Perkakas"

    # Perlengkapan packing
    if ("gesper plastik" in n or "tali strapping" in n or
        "strapping band" in n or "packing" in n or "packingan" in n):
        return "Perlengkapan Packing"

    # Aksesoris motor
    if "motor" in n or "busi" in n or "spion" in n or "oli" in n:
        return "Aksesoris Motor"

    # Plastik
    if "plastik" in n:
        return "Plastik / Wadah Plastik"

    # Perkakas umum
    if "obeng" in n or "screwdriver" in n or "kunci inggris" in n:
        return "Perkakas"

    # Stempel
    if "stempel" in n or "stamp" in n:
        return "Stempel / Alat Kantor"

    # Pot tanaman
    if "pot tanaman" in n or "pot siram" in n or "siraman bunga" in n or "pot bunga" in n:
        return "Pot Tanaman / Bunga"

    # Cobek / ulekan
    if "cobek" in n or "ulekan" in n:
        return "Cobek / Ulekan"

    return "Other"





# =========================
#  FUNGSI ANONIMISASI ORDER ID (dengan global counter)
# =========================

def anonymize_order_ids(df, start_counter: int, col_order_id: str = COL_ORDER_ID):
    """
    Membuat mapping:
        original_id → ORD_0000001, ORD_0000002, ...
    Menggunakan counter global agar unik di semua file.
    """
    unique_ids = df[col_order_id].dropna().unique()

    mapping = {
        oid: f"ORD_{i:07d}"
        for i, oid in enumerate(unique_ids, start=start_counter)
    }

    df["order_id"] = df[col_order_id].map(mapping)
    next_counter = start_counter + len(unique_ids)
    return df, next_counter


# =========================
#  PROSES SATU FILE RAW
# =========================

def process_raw_file(path: Path, start_counter: int):
    print(f"Processing RAW → PUBLIC: {path.name}")

    df = pd.read_excel(path)

    # 1) Anonimisasi order ID (konsisten & global)
    df, next_counter = anonymize_order_ids(df, start_counter)

    # 2) Tambahkan kategori produk
    df["product_category"] = df[COL_PRODUCT_NAME].apply(categorize_product)

   

    # 4) Drop nama produk (privat)
    if COL_PRODUCT_NAME in df.columns:
        df = df.drop(columns=[COL_PRODUCT_NAME])

    # 5) Drop order ID asli
    df = df.drop(columns=[COL_ORDER_ID])

    # rapikan urutan kolom
    new_cols = ["order_id", "product_category"] + [
        c for c in df.columns if c not in ["order_id", "product_category"]
    ]
    df = df[new_cols]

    return df, next_counter


# =========================
#  MAIN
# =========================

def main():
    raw_files = sorted(RAW_DIR.glob("*.xlsx"))

    if not raw_files:
        print("Tidak ada file RAW ditemukan.")
        return

    counter = 1  # global counter untuk semua RAW_PUBLIC

    for f in raw_files:
        df_public, counter = process_raw_file(f, counter)

        out_path = PUBLIC_DIR / f"{f.stem}_public.xlsx"
        df_public.to_excel(out_path, index=False)

        print(f"   → Saved public file: {out_path.name}")

    print(f"Selesai. Total unique order_id (perkiraan): {counter - 1}")


if __name__ == "__main__":
    main()
