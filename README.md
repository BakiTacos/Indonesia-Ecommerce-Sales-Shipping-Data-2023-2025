# **Indonesia E-Commerce Sales (Dec 2023 – Nov 2025)**
## **📘 About This Dataset**
Dataset ini berisi kumpulan transaksi e-commerce di Indonesia mulai dari Desember 2023 hingga November 2025.
Setiap baris merepresentasikan satu pesanan yang dilakukan pembeli, lengkap dengan informasi kuantitas, berat, kategori produk, diskon, metode pembayaran, ongkos kirim, status pesanan, dan wilayah pembeli.

FORMAT FILE: xlsx

BAHASA: Bahasa Indonesia

MATA UANG: Rupiah

Dataset disediakan dalam dua versi:
1. CLEAN Files
Versi yang telah dibersihkan, dikonsolidasikan, distandardisasi kolomnya.

2. RAW_PUBLIC Files
Versi publik yang hanya mengalami minimal cleaning, dipertahankan mendekati bentuk aslinya tanpa transformasi berlebihan. Disediakan untuk keperluan transparansi, audit, dan eksplorasi awal.

## **🧩 Column Descriptions**
Berikut adalah penjelasan setiap kolom dalam dataset CLEAN & RAW_PUBLIC:
1. order_id: ID unik untuk setiap pesanan yang masuk ke sistem marketplace. (Dianonimkan)
2. total_qty: Total jumlah item yang dibeli dalam satu pesanan.
3. total_weight_gr: Total berat barang dalam gram, digunakan untuk perhitungan ongkos kirim.
4. total_returned_qty: Jumlah barang yang dikembalikan oleh pembeli (0 jika tidak ada pengembalian).
5. Total Diskon: Total diskon yang diterapkan pada pesanan, termasuk voucher, diskon platform, dan diskon seller.
6. product_categories: Kategorisasi produk yang ada dalam pesanan tersebut.
7. num_product_categories: Jumlah kategori produk yang terlibat dalam pesanan.
8. Status Pesanan: Status akhir pesanan (selesai, dibatalkan, dikembalikan, dll).
9. Alasan Pembatalan Jika pesanan dibatalkan, kolom ini menjelaskan alasan pembatalannya
10. Opsi Pengiriman: Jenis layanan pengiriman yang digunakan.
11. Metode Pembayaran: Metode pembayaran yang digunakan seperti COD, e-wallet, transfer bank, dan lainnya.
12. Kota/Kabupaten: Wilayah tujuan pengiriman kota/kabupaten.
13. Provinsi: Provinsi tujuan pengiriman pesanan.
14. Ongkos Kirim Dibayar oleh Pembeli: Ongkir aktual yang dibebankan kepada pembeli.
15. Estimasi Potongan Biaya Pengiriman: Subsidi atau potongan ongkos kirim yang ditanggung platform (jika ada).
16. Total Pembayaran: Jumlah akhir yang dibayar pembeli setelah diskon dan penyesuaian.
17. Perkiraan Ongkos Kirim: Estimasi ongkir yang dihitung oleh platform sebelum subsidi atau potongan.
18. Waktu Pesanan Dibuat: Waktu dan tanggal ketika pesanan dibuat oleh pembeli.

## **📊 Data Characteristics**
	•	Mencakup 24 bulan transaksi (Desember 2023 – November 2025).
	•	Konsisten dalam struktur kolom untuk memudahkan analisis jangka panjang.
	•	Tidak mengandung data pribadi pembeli seperti nama, telepon, atau alamat lengkap.
	•	Tersedia dalam dua versi (CLEAN dan RAW_PUBLIC) sesuai kebutuhan pengguna.
	•	Mendukung analisis penjualan, performa logistik, efektivitas diskon, dan perilaku pembayaran.

## **🎯 Potential Applications**

### 1. Machine Learning
	•	Prediksi pembatalan pesanan
	•	Prediksi ongkos kirim
	•	Prediksi risiko retur
	•	Segmentasi pembeli berdasarkan wilayah dan perilaku belanja

### 2. Business Insights & Analytics
	•	Analisis tren penjualan bulanan
	•	Kinerja penyedia layanan pengiriman
	•	Distribusi metode pembayaran
	•	Analisis volume dan berat pesanan untuk optimasi logistik

## **🔐 Privacy Notes**
Tidak ada informasi pribadi (PII) dalam dataset ini.
Seluruh informasi lokasi hanya berupa kota/kabupaten dan provinsi tanpa detail identitas pembeli.

## **🚀 Future Works**
Dataset ini akan diperluas ke beberapa Versi, yang akan mencakup beberapa peningkatan atau perubahan:
### 1. Multi E-Commerce Platform Integration
    • Versi ini akan menggabungkan data dari beberapa marketplace untuk memberikan gambaran lintas platform yang lebih komprehensif.
### 2. Dedicated Logistics Dataset
	•	Waktu barang diterima oleh pihak ekspedisi
	•	Waktu barang keluar dari gudang ekspedisi
	•	Waktu barang diterima oleh pembeli

### 3. Enhanced Time-Series Features
	•	Waktu pembayaran
	•	Waktu pesanan diproses seller
	•	Waktu resi dibuat
	•	Waktu barang di-pickup kurir

## **📄 LICENSE**
Dataset ini dirilis menggunakan lisensi CC0 1.0 Universal sehingga bebas digunakan untuk keperluan riset, analisis, dan komersial.

