
"""
Kasus 5 - Tugas 7: Deteksi kemungkinan DNS Exfiltration dari log dnsmasq.

Pemakaian:
    python3 analisis_dns.py dns-k5.log

Skrip menghitung jumlah query berdasarkan domain induk,
memeriksa panjang label DNS, dan menandai label panjang
yang hanya berisi karakter hexadecimal.
"""

import re
import sys
from collections import Counter

# Pola untuk membaca query DNS dari log dnsmasq
PAT = re.compile(r"query\[\w+\] (\S+) from")

# Batas panjang label yang dianggap mencurigakan
BATAS_PANJANG_LABEL = 30

# Menyimpan jumlah query setiap domain induk
jumlah_domain = Counter()

# Menyimpan daftar query yang mencurigakan
mencurigakan = []


def analisis_dns(file_log):
    """Menganalisis log DNS untuk mencari indikasi eksfiltrasi."""

    with open(file_log, encoding="utf-8", errors="ignore") as f:
        for baris in f:
            m = PAT.search(baris)

            if not m:
                continue

            nama = m.group(1).rstrip(".")
            bagian = nama.split(".")

            if len(bagian) < 2:
                continue

            domain_induk = ".".join(bagian[-2:])
            jumlah_domain[domain_induk] += 1

            label = bagian[0]

            # Memeriksa label panjang yang hanya berisi karakter hex
            if (
                len(label) > BATAS_PANJANG_LABEL
                and re.fullmatch(r"[0-9a-fA-F]+", label)
            ):
                mencurigakan.append((len(label), nama))

    print("Jumlah query per domain induk:")
    for domain, jumlah in jumlah_domain.most_common():
        print(f"  {domain}: {jumlah}")

    print("\nQuery mencurigakan (label panjang berisi hex):")

    if mencurigakan:
        for panjang, nama in mencurigakan:
            print(f"  panjang={panjang}  {nama}")
    else:
        print("  Tidak ditemukan query mencurigakan.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Pemakaian: python3 analisis_dns.py dns-k5.log")
        sys.exit(1)

    analisis_dns(sys.argv[1])
