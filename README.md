# 🍛 Restoran Nusantara: Analisis Penjualan & Dashboard 

🔗 **Dashboard:** https://restoran-nusantara-dashboard.streamlit.app/

<!-- Seret screenshot dashboard ke baris kosong di bawah ini, lalu hapus baris komentar ini -->

## Latar Belakang (Studi Kasus)
**Skenario:** Sebuah restoran UMKM memiliki data transaksi 6 bulan dalam bentuk file CSV. Pemilik ingin tahu menu apa yang paling menguntungkan, jam berapa restoran paling ramai, dan apakah diskon yang diberikan efektif.

<img width="1920" height="962" alt="image" src="https://github.com/user-attachments/assets/ab5ea302-364f-416f-885f-3d56280fb7d5" />

**Deliverable:**
1. Data yang sudah dibersihkan dan divalidasi
2. Analisis beserta rekomendasi bisnis
3. Dashboard interaktif yang bisa dipantau secara mandiri

> Catatan: project ini adalah studi kasus portofolio dengan dataset simulasi.

## Pertanyaan Bisnis
1. Bagaimana tren pendapatan bulanan?
2. Menu dan kategori apa yang paling berkontribusi?
3. Kapan restoran paling ramai?
4. Bagaimana pola pembayaran, tipe pesanan, dan efek diskon?

## Pembersihan Data
Dataset: 3.008 baris transaksi (Januari–Juni 2026) dari satu outlet.
- 8 transaksi dobel dihapus (3.008 → 3.000 transaksi)
- 12 data `payment_method` kosong diisi `Unknown`
- Total transaksi divalidasi (harga × jumlah − diskon), semuanya konsisten
- Ditambah fitur: jam, bulan, dan nama hari

## Temuan Utama
- Total pendapatan **Rp108,8 juta**, rata-rata **Rp36.278** per transaksi
- **Nasi Goreng Spesial** menu terlaris (Rp17,0 juta), disusul Nasi Ayam Bakar dan Ayam Geprek
- Es Teh Manis laku 565 unit tetapi hanya menyumbang Rp3,9 juta karena harganya murah
- Makanan 85,9% pendapatan, Minuman 10,9%, Snack 3,1%
- Jam ramai merata (jam 10–22), puncak di jam 15.00
- Pembayaran non-tunai ±75% (QRIS ±44%)
- Jumlah item per transaksi tidak naik saat ada diskon (±1,7 item)

## Rekomendasi
- Jadikan 3 menu teratas sebagai andalan dan jaga stoknya
- Buat paket bundling makanan + minuman untuk menaikkan nilai transaksi
- Evaluasi ulang diskon, karena belum terbukti menaikkan pembelian
- Pertahankan staf yang stabil sepanjang hari

## Tools
Python · Pandas · Matplotlib · Seaborn · Plotly · Streamlit · Google Colab

## Isi Repository
- `app.py`: dashboard Streamlit
- `Analisis_Restoran_Nusantara.ipynb`: notebook analisis (cleaning, EDA, insight)
- `data/`: dataset
- `.streamlit/config.toml`: tema dashboard

---
Dibuat oleh **Ihsan Amiruddin**. Terbuka untuk jasa analisis data dan dashboard.
