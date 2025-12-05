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

COL_ORDER_ID = "No. Pesanan"
COL_PRODUCT_NAME = "Nama Produk"
COL_CANCEL_REASON   = "Alasan Pembatalan"

# =========================
#  FUNGSI KATEGORISASI PRODUK
# =========================

def categorize_product(name: str) -> str:
    """
    Ubah 'Nama Produk' menjadi kategori umum.
    Aturan disesuaikan dengan isi dataset (rak, baskom, keranjang, toples,
    celengan LPG, gagang pintu, weather seal, sapu, sikat, pot tanaman, dll).
    """
    if not isinstance(name, str):
        return "Other"

    n = name.lower()

    # === Kategori paling spesifik dulu ===

    # Aksesoris ID Card / Name Tag
    if "id card" in n or "name tag" in n or "kartu identitas" in n:
        return "Aksesoris ID Card"

    # Celengan (termasuk bentuk tabung gas, nanas, dll.)
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

    # Rak (rak susun, rak cuci piring, rak serbaguna)
    if n.startswith("rak") or " rak " in n:
        return "Rak / Rak Serbaguna"

    # Keranjang (belanja, baju, buah, serbaguna)
    if "keranjang" in n:
        return "Keranjang"

    # Nampan / tray / tampah / baki
    if ("nampan" in n or "tampah" in n or " tray " in n or
        "round tray" in n or "baki" in n):
        return "Nampan / Tray"

    # Piring
    if "piring" in n or "plate" in n:
        return "Piring"

    # Mangkok (umum, bukan sambal/baskom)
    if "mangkok" in n or "mangkuk" in n:
        return "Mangkok"

    # Teko / jug / eskan / pitcher
    if ("teko" in n or "water jug" in n or "eskan" in n or
        "pitcher" in n or "jug" in n):
        return "Teko / Jug"

    # Saringan / strainer / tirisan / ayakan
    if ("saringan" in n or "strainer" in n or "filter" in n or
        "ayakan" in n or "tirisan" in n):
        return "Saringan / Strainer"

    # Peralatan makan (sendok, garpu, set steak, sendok teh)
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

    # Talenan / cutting board
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

    # Aksesoris pintu (engsel, grendel, handle, tarikan, selot, knob)
    if ("engsel" in n or "grendel" in n or "selot" in n or
        "handle" in n or "tarikan" in n or "knob" in n or "door lock" in n):
        return "Aksesoris Pintu"

    # Peralatan mandi & kamar mandi (tempat sabun, sikat WC, dll.)
    if ("tempat sabun" in n or "soap" in n or "toilet" in n or
        "wc" in n or "kamar mandi" in n):
        return "Peralatan Kamar Mandi"
    if "spons mandi" in n or "shower puff" in n or "bath sponge" in n:
        return "Aksesoris Mandi"
    if "gayung" in n:
        return "Gayung"

    # Peralatan kebersihan (sapu, sikat lantai/baju, bola kawat)
    if "sapu" in n:
        return "Sapu / Pembersih Lantai"
    if "sikat" in n or "scourer" in n or "bola kawat" in n:
        return "Sikat / Pembersih"

    # Seal / baut / kunci / roof / skrup
    if ("weather seal" in n or "roof seal" in n or "penutup skrup" in n or
        "skrup" in n or "baut" in n or "drilling screw" in n):
        return "Seal / Baut / Roof"
    if "kunci l" in n or "kunci " in n:
        return "Perkakas"

    # Perlengkapan packing (tali strapping, gesper plastik)
    if ("gesper plastik" in n or "tali strapping" in n or
        "strapping band" in n or "packing" in n or "packingan" in n):
        return "Perlengkapan Packing"

    # Aksesoris motor (kalau muncul di bulan lain)
    if "motor" in n or "busi" in n or "spion" in n or "oli" in n:
        return "Aksesoris Motor"

    # Plastik (kantong, wadah plastik umum)
    if "plastik" in n:
        return "Plastik / Wadah Plastik"

    # Perkakas umum
    if "obeng" in n or "screwdriver" in n or "kunci inggris" in n:
        return "Perkakas"

    # Stempel / alat kantor kecil
    if "stempel" in n or "stamp" in n:
        return "Stempel / Alat Kantor"

    # Pot tanaman / siram bunga
    if "pot tanaman" in n or "pot siram" in n or "siraman bunga" in n or "pot bunga" in n:
        return "Pot Tanaman / Bunga"

    # Cobek dan ulekan
    if "cobek" in n or "ulekan" in n:
        return "Cobek / Ulekan"

    # Default
    return "Other"


# =========================
#  FUNGSI ANONIMISASI ORDER ID
# =========================

def anonymize_order_ids(df, col_order_id=COL_ORDER_ID):
    """
    Membuat mapping:
        original_id → ORD_000001
    Dengan aturan:
    - Jika original ID muncul berkali-kali → pakai ORD yang sama
    - Konsisten dalam satu file
    """
    unique_ids = df[col_order_id].dropna().unique()

    mapping = {
        oid: f"ORD_{i:07d}"
        for i, oid in enumerate(unique_ids, start=1)
    }

    df["order_id"] = df[col_order_id].map(mapping)
    return df


# =========================
#  PROSES SATU FILE RAW
# =========================

def process_raw_file(path: Path) -> pd.DataFrame:
    print(f"Processing RAW → PUBLIC: {path.name}")

    df = pd.read_excel(path)

    # 1) Anonimisasi order ID (konsisten)
    df = anonymize_order_ids(df)

    # 2) Tambahkan kategori produk
    df["product_category"] = df[COL_PRODUCT_NAME].apply(categorize_product)

   
    # 3) Drop nama produk (sangat aman untuk publik)
    if COL_PRODUCT_NAME in df.columns:
        df = df.drop(columns=[COL_PRODUCT_NAME])

    # 4) Drop order ID asli
    df = df.drop(columns=[COL_ORDER_ID])

    # rapikan urutan kolom
    new_cols = ["order_id", "product_category"] + [c for c in df.columns if c not in ["order_id", "product_category"]]
    df = df[new_cols]

    return df


# =========================
#  MAIN
# =========================

def main():
    raw_files = sorted(RAW_DIR.glob("*.xlsx"))

    if not raw_files:
        print("Tidak ada file RAW ditemukan.")
        return

    for f in raw_files:
        df_public = process_raw_file(f)

        out_path = PUBLIC_DIR / f"{f.stem}_public.xlsx"
        df_public.to_excel(out_path, index=False)

        print(f"   → Saved public file: {out_path.name}")


if __name__ == "__main__":
    main()