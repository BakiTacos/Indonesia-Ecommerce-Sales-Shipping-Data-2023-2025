import pandas as pd
from pathlib import Path
import re

# =========================
#  KONFIGURASI FOLDER
# =========================

RAW_DIR = Path("RAW")     # folder input
CLEAN_DIR = Path("CLEAN") # folder output
CLEAN_DIR.mkdir(exist_ok=True)

# =========================
#  NAMA KOLOM (SAMA PERSIS DGN HEADER-MU)
# =========================

COL_ORDER_ID        = "No. Pesanan"
COL_STATUS          = "Status Pesanan"
COL_CANCEL_REASON   = "Alasan Pembatalan"
COL_SHIP_OPTION     = "Opsi Pengiriman"
COL_ORDER_TIME      = "Waktu Pesanan Dibuat"
COL_PAYMENT_METHOD  = "Metode Pembayaran"
COL_PRODUCT_NAME    = "Nama Produk"
COL_QTY             = "Jumlah"
COL_RETURNED_QTY    = "Returned quantity"
COL_DISCOUNT        = "Total Diskon"
COL_WEIGHT          = "Total Berat"
COL_SHIP_PAID       = "Ongkos Kirim Dibayar oleh Pembeli"
COL_SHIP_DISC       = "Estimasi Potongan Biaya Pengiriman"
COL_TOTAL_PAYMENT   = "Total Pembayaran"
COL_SHIP_EST        = "Perkiraan Ongkos Kirim"
COL_CITY            = "Kota/Kabupaten"
COL_PROVINCE        = "Provinsi"


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

    # Peralatan mandi & kamar mandi
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

    # Seal / baut / kunci / roof / skrup
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

    # Stempel / alat kantor kecil
    if "stempel" in n or "stamp" in n:
        return "Stempel / Alat Kantor"

    # Pot tanaman
    if "pot tanaman" in n or "pot siram" in n or "siraman bunga" in n or "pot bunga" in n:
        return "Pot Tanaman / Bunga"

    # Cobek dan ulekan
    if "cobek" in n or "ulekan" in n:
        return "Cobek / Ulekan"

    # Default
    return "Other"


# =========================
#  FUNGSI BERSIHKAN FORMAT RUPIAH
# =========================

def fix_rupiah(x):
    if isinstance(x, str):
        x = x.strip()
        x = x.replace(",", "").replace(".", "")
        if x.isdigit():
            return int(x)
    return x


# =========================
#  FUNGSI BERSIHKAN 'Total Berat'
# =========================

def fix_weight(x):
    if isinstance(x, str):
        x = x.lower()
        x = x.replace("gr", "").replace("gram", "")
        x = x.replace(" ", "")
        if x.isdigit():
            return int(x)
    return x





# =========================
#  FUNGSI CLEANING SATU FILE
#  (dengan global counter untuk order_id)
# =========================

def clean_one_file(path: Path, start_counter: int):
    """
    Membersihkan satu file dan mengembalikan:
    - grouped: dataframe hasil clean
    - next_counter: nilai counter berikutnya untuk dipakai file selanjutnya
    """
    print(f"Processing: {path.name}")

    df = pd.read_excel(
        path,
        dtype={
            COL_SHIP_PAID: str,
            COL_SHIP_EST: str,
            COL_DISCOUNT: str,
            COL_TOTAL_PAYMENT: str,
            COL_SHIP_DISC: str,
        }
    )

    if COL_ORDER_ID not in df.columns:
        raise ValueError(f"Kolom '{COL_ORDER_ID}' tidak ditemukan di file {path.name}")

    # kategori produk
    if COL_PRODUCT_NAME in df.columns:
        df["product_category"] = df[COL_PRODUCT_NAME].apply(categorize_product)
    else:
        df["product_category"] = "Unknown"

    # rupiah → int
    for col in [COL_SHIP_PAID, COL_SHIP_EST, COL_DISCOUNT, COL_TOTAL_PAYMENT, COL_SHIP_DISC]:
        if col in df.columns:
            df[col] = df[col].apply(fix_rupiah)

    # berat → gram int
    if COL_WEIGHT in df.columns:
        df[COL_WEIGHT] = df[COL_WEIGHT].apply(fix_weight)
        df[COL_WEIGHT] = pd.to_numeric(df[COL_WEIGHT], errors="coerce")

    # bersihkan alasan pembatalan
   
    # agregasi per order
    agg_dict = {}

    if COL_QTY in df.columns:
        agg_dict["total_qty"] = (COL_QTY, "sum")
    if COL_WEIGHT in df.columns:
        agg_dict["total_weight_gr"] = (COL_WEIGHT, "sum")
    if COL_RETURNED_QTY in df.columns:
        agg_dict["total_returned_qty"] = (COL_RETURNED_QTY, "sum")

    def first_if_exists(col_name, new_name=None):
        if col_name in df.columns:
            agg_dict[new_name or col_name] = (col_name, "first")

    first_if_exists(COL_DISCOUNT, COL_DISCOUNT)

    agg_dict["product_categories"] = (
        "product_category",
        lambda x: ", ".join(sorted(set(x)))
    )
    agg_dict["num_product_categories"] = (
        "product_category",
        lambda x: len(set(x))
    )

    first_if_exists(COL_STATUS, "Status Pesanan")
    first_if_exists(COL_CANCEL_REASON, "Alasan Pembatalan")
    first_if_exists(COL_SHIP_OPTION, "Opsi Pengiriman")
    first_if_exists(COL_PAYMENT_METHOD, "Metode Pembayaran")
    first_if_exists(COL_CITY, "Kota/Kabupaten")
    first_if_exists(COL_PROVINCE, "Provinsi")
    first_if_exists(COL_SHIP_PAID, "Ongkos Kirim Dibayar oleh Pembeli")
    first_if_exists(COL_SHIP_DISC, "Estimasi Potongan Biaya Pengiriman")
    first_if_exists(COL_TOTAL_PAYMENT, "Total Pembayaran")
    first_if_exists(COL_SHIP_EST, "Perkiraan Ongkos Kirim")
    first_if_exists(COL_ORDER_TIME, COL_ORDER_TIME)

    grouped = df.groupby(COL_ORDER_ID).agg(**agg_dict).reset_index()

    # anonimkan ID dengan counter global
    grouped.rename(columns={COL_ORDER_ID: "order_id_original"}, inplace=True)
    n_rows = len(grouped)

    grouped.insert(
        0,
        "order_id",
        [f"ORD_{i:07d}" for i in range(start_counter, start_counter + n_rows)]
    )

    grouped = grouped.drop(columns=["order_id_original"])

    next_counter = start_counter + n_rows
    return grouped, next_counter


# =========================
#  MAIN: PROSES SEMUA FILE DI RAW
# =========================

def main():
    all_clean = []

    xlsx_files = sorted(RAW_DIR.glob("*.xlsx"))
    if not xlsx_files:
        print(f"Tidak ada file .xlsx di folder '{RAW_DIR.resolve()}'")
        return

    counter = 1  # global counter untuk semua bulan

    for f in xlsx_files:
        cleaned, counter = clean_one_file(f, counter)

        out_path = CLEAN_DIR / f"{f.stem}_clean.xlsx"
        cleaned.to_excel(out_path, index=False)
        print(f"  -> Saved cleaned file: {out_path.name}")

        cleaned["source_file"] = f.name
        all_clean.append(cleaned)

    if all_clean:
        combined = pd.concat(all_clean, ignore_index=True)
        combined_out = CLEAN_DIR / "all_months_clean.xlsx"
        combined.to_excel(combined_out, index=False)
        print(f"\nCombined all months saved as: {combined_out.name}")


if __name__ == "__main__":
    main()
