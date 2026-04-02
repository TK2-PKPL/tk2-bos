SITE_NAME = "Kelompok 2 Secure Portal"
SITE_TAGLINE = "Website biodata kelompok dengan autentikasi Google dan pengaturan tampilan yang dibatasi oleh otorisasi"
PROJECT_CONTEXT = "Website ini adalah lanjutan dari Tugas 1. Fokus Tugas 2 diletakkan pada implementasi autentikasi Google, pemisahan hak editor dan viewer, serta audit log untuk perubahan tampilan website."
TEAM_MEMBERS = [
    {"name": "A. Sheriqa Dewina Ihsan", "student_id": "2406360722", "role": "Project lead dan dokumentasi", "email": "andisheriqadewina@gmail.com", "bio": "Mengelola arah pengerjaan tugas dan memastikan hasil akhir sesuai dengan kebutuhan keamanan.", "accent": "Koordinasi tim"},
    {"name": "Elizabeth Meilanny Sitanggang", "student_id": "2306001002", "role": "Backend dan autentikasi", "email": "bagas@example.com", "bio": "Menangani login Google, validasi token, sesi Django, dan kontrol akses di sisi server.", "accent": "Server side auth"},
    {"name": "Gilang Adjie Saputra", "student_id": "2406399655", "role": "Frontend dan pengalaman pengguna", "email": "citra@example.com", "bio": "Merancang tampilan halaman publik, dashboard, dan panel pengaturan tema.", "accent": "UI yang rapi"},
    {"name": "Rashika Maharani", "student_id": "2306001004", "role": "Pengujian dan audit", "email": "damar@example.com", "bio": "Menguji skenario editor dan viewer serta memeriksa jejak aktivitas pada audit log.", "accent": "Quality assurance"},
    {"name": "Syafiq Faqih", "student_id": "2406439715", "role": "Project lead dan dokumentasi", "email": "syafiq.fqh@gmail.com", "bio": "Mengelola arah pengerjaan tugas dan memastikan hasil akhir sesuai dengan kebutuhan keamanan.", "accent": "Koordinasi tim"},

]
FEATURE_CARDS = [
    {"title": "Biodata publik", "description": "Seluruh pengunjung dapat melihat profil kelompok tanpa harus login."},
    {"title": "Login Google", "description": "Autentikasi dilakukan menggunakan akun Google dan diverifikasi kembali di backend Django."},
    {"title": "Editor dan viewer", "description": "Email anggota kelompok menjadi editor sedangkan akun lain hanya menjadi viewer."},
    {"title": "Panel tema", "description": "Editor dapat mengganti warna dan font website secara aman dan terkontrol."},
]
TASK_ONE_HIGHLIGHTS = [
    "Least privilege dan role based access control",
    "Manajemen sesi dan validasi identitas di sisi server",
    "Audit log untuk akuntabilitas perubahan",
    "Pemisahan autentikasi dan otorisasi secara tegas",
]
AUTHORIZATION_RULES = [
    "Guest hanya dapat melihat halaman publik",
    "Viewer dapat login dan melihat dashboard tanpa hak edit",
    "Editor dapat mengubah warna dan font website",
    "Setiap perubahan tema dicatat ke audit log",
]
