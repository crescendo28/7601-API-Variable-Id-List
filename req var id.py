import requests
import json
import time

# --- Konfigurasi ---
# Ganti dengan API key Anda yang sebenarnya
API_KEY = "a5afe9584ab3c835086ccfc9a342a764"
DOMAIN = "7601"
# Nama file untuk menyimpan hasil
OUTPUT_FILENAME = "D:/BPS Majene/[Latsar]/Aktualisasi/Database/bps_data_lengkap.json"

def unduh_semua_data_api(base_url, api_key):
    """
    Mengambil data dari semua halaman yang tersedia dari API BPS 
    dan berhenti secara otomatis ketika tidak ada lagi data yang ditemukan.
    """
    semua_data = []
    halaman = 1

    while True:
        # Membangun URL untuk halaman saat ini
        url = f"{base_url}/page/{halaman}/key/{api_key}/"
        
        print(f"Mengambil data dari halaman {halaman}...")

        try:
            respons = requests.get(url)
            # Memberikan error jika status code tidak berhasil (misal: 404, 500)
            respons.raise_for_status()
            data = respons.json()

            # Memeriksa apakah data tersedia dan daftar variabel tidak kosong
            if data.get('data-availability') == 'available' and data.get('data') and data['data'][1]:
                # Data aktual berada di dalam kunci 'data'][1]
                data_halaman_ini = data['data'][1]
                semua_data.extend(data_halaman_ini)
                print(f"-> Berhasil! Ditemukan {len(data_halaman_ini)} item di halaman {halaman}.")
                
                # Lanjut ke halaman berikutnya
                halaman += 1
                
                # Jeda singkat agar tidak membebani server API
                time.sleep(0.5) 
            else:
                # Jika 'data-availability' adalah 'not-available' atau daftar data kosong, proses selesai.
                print("-> Tidak ada data lagi yang tersedia. Proses pengunduhan berhenti.")
                break

        except requests.exceptions.RequestException as e:
            print(f"Terjadi kesalahan saat meminta data: {e}")
            break
        except json.JSONDecodeError:
            print(f"Gagal memproses JSON dari halaman {halaman}. Mungkin ada masalah dengan respons API.")
            break

    return semua_data

# --- Eksekusi Utama ---
if __name__ == "__main__":
    print("Memulai proses untuk mengunduh semua data dari API BPS...")
    
    # Membangun URL dasar
    base_url = f"https://webapi.bps.go.id/v1/api/list/model/var/domain/{DOMAIN}"

    # 1. Panggil fungsi untuk mengunduh semua data
    data_lengkap = unduh_semua_data_api(base_url, API_KEY)

    # 2. Jika data berhasil diunduh, simpan ke file
    if data_lengkap:
        try:
            with open(OUTPUT_FILENAME, "w", encoding="utf-8") as f:
                json.dump(data_lengkap, f, indent=4, ensure_ascii=False)
            print(f"\nSUKSES! Semua data telah disimpan ke dalam file: '{OUTPUT_FILENAME}'")
            print(f"Total {len(data_lengkap)} item data berhasil diunduh.")
        except IOError as e:
            print(f"\nGagal menyimpan file: {e}")
    else:
        print("\nTidak ada data yang diunduh. File tidak dibuat.")