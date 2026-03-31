# Tugas 2 Authentication and Authorization dengan Django

Project ini dibuat untuk memenuhi brief Tugas 2 yang meminta website biodata kelompok dengan akses publik, login Google, serta kontrol perubahan warna dan font hanya untuk akun anggota kelompok.

## Ringkasan fitur

- Halaman biodata kelompok dapat dibuka tanpa login
- Login menggunakan Google Identity Services
- Verifikasi token dilakukan di backend Django
- Role dibagi menjadi editor dan viewer
- Hanya editor yang dapat mengubah warna dan font website
- Setiap login dan perubahan tema dicatat pada audit log
- Tersedia mode preview lokal saat Google client ID belum diisi

## Struktur project

- `accounts` berisi custom user dan proses login Google
- `core` berisi halaman publik, dashboard, pengaturan tema, audit log, dan konteks website
- `templates` berisi template HTML
- `static` berisi CSS dan JavaScript
- `core/team_data.py` berisi biodata kelompok yang mudah diganti

## Cara menjalankan project

1. Install dependency

```bash
pip install -r requirements.txt
```

2. Salin file environment

```bash
cp .env.example .env
```

3. Isi nilai pada file `.env`

- `SECRET_KEY`
- `GOOGLE_CLIENT_ID`
- `TEAM_EDITOR_EMAILS`

4. Jalankan migrasi

```bash
python manage.py migrate
```

5. Jalankan server

```bash
python manage.py runserver
```

6. Buka browser di `http://127.0.0.1:8000`

## Konfigurasi Google

1. Buat OAuth client ID untuk web di Google Cloud Console
2. Tambahkan origin lokal seperti `http://127.0.0.1:8000` dan `http://localhost:8000`
3. Isi nilai client ID pada `.env`

## Cara mengganti biodata kelompok

Buka file `core/team_data.py` lalu ganti nama, NPM, email, peran, dan bio anggota.

## Mode preview lokal

Jika `GOOGLE_CLIENT_ID` belum diisi dan `DEBUG=True`, halaman beranda akan menampilkan tombol demo untuk masuk sebagai editor atau viewer. Tombol ini dipakai untuk pengujian lokal dan tidak aktif saat `DEBUG=False`.
