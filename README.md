🚀 Plume Push TX Bot
Bot ini secara otomatis mengirimkan token PLUME ke semua wallet aktif (EOA) yang bertransaksi di blok terbaru Plume Network.
✅ Cocok untuk airdrop, marketing, dan distribusi token massal
✅ Gratis dan open-source
✅ Aman dari kegagalan (skip kontrak, hanya kirim ke wallet)
✅ Jalan nonstop 24/7

✨ Fitur
🔄 Loop otomatis membaca blok terbaru

🛡️ Filter kontrak → hanya wallet manusia (EOA)

⏱️ Delay random untuk anti-spam

📦 Kirim ke semua penerima unik di blok terbaru

📜 Log transaksi TX Hash

⚡ Instalasi
1️⃣ Clone repository
bash
Copy
Edit
git clone https://github.com/kevinnft/plume-push-tx.git
cd plume-push-tx
2️⃣ Install dependencies
bash
Copy
Edit
pip install web3 eth_account
3️⃣ Edit private key
Buka file bot.py dan ganti:

python
Copy
Edit
SENDER_PRIVATE_KEY = "0xPRIVATE_KEY_KAMU"
▶️ Cara Menjalankan
bash
Copy
Edit
python bot.py
Bot akan:

Memantau blok terbaru

Mengirim PLUME otomatis ke semua wallet yang aktif transaksi

Skip kontrak dan alamat sendiri

Menampilkan TX Hash setiap pengiriman

📄 Contoh Output
yaml
Copy
Edit
📦 Blok terbaru: 15804728 | Jumlah TX: 6
✅ [1] Kirim 0.00000336 PLUME ke 0xC8...BC78 | TX: 0xbb...2d69
✅ [2] Kirim 0.00000183 PLUME ke 0x0F...C7e7 | TX: 0x82...d03d
...
💡 Tips
Pastikan wallet punya cukup gas PLUME

Gunakan VPS agar bot jalan nonstop

Bisa diintegrasikan dengan campaign airdrop atau token distribution

🤝 Kontribusi
Pull request dan ide baru sangat diterima!

📜 Lisensi
MIT License – Bebas digunakan & dimodifikasi.

