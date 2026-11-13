# Tugas 1 - Docker dan Volume

## 1. Pengujian persistensi volume

Volume: vol-k5
Container pertama: w-k5
File: laporan-k5.txt

NIM yang disimpan: 24552011131

Container pertama berhasil dihapus, kemudian file dibaca kembali menggunakan container baru.

Hasil: Data tetap tersedia setelah container pertama dihapus.

## 2. Pengujian komunikasi Nginx

Container target menggunakan nginx:alpine.
Container attacker menggunakan alpine.

Perintah pengujian:
wget -qO- http://target

Hasil: Halaman Welcome to nginx berhasil ditampilkan dari container attacker.

## 3. Pembersihan lab

Docker Compose berhasil menghentikan dan menghapus kedua container serta network.

## Kesimpulan

Docker Volume memungkinkan data tetap tersimpan meskipun container dihapus. Docker Compose memungkinkan komunikasi antarkontainer melalui jaringan internal.
