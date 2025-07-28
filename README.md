🚀 Plume Push TX Bot – Auto Airdrop Sambil Rebahan
Sistem Requirements
2 core CPU

4GB RAM

Python 3.9+

✨ Fitur
Kirim otomatis token PLUME ke semua wallet aktif (EOA)

Skip kontrak → hanya wallet manusia

Delay random → anti-spam

Log TX Hash setiap transaksi

Jalan nonstop 24/7

Gratis & open-source

Buat screen

sql
Copy
Edit
sudo apt update && sudo apt install screen -y
nginx
Copy
Edit
screen -S plume-bot
Clone Repository

bash
Copy
Edit
git clone https://github.com/kevinnft/plume-push-tx
cd plume-push-tx
Buat environment

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
Install bahan

nginx
Copy
Edit
pip install web3 eth_account
Edit script

nginx
Copy
Edit
nano bot.py
Ganti SENDER_PRIVATE_KEY dengan private key wallet kamu

Klik ctrl + x → y → enter (untuk simpan & keluar)

Mainkan bot

nginx
Copy
Edit
python bot.py
🔑 Fungsi tambahan
Masuk screen bot

nginx
Copy
Edit
screen -r plume-bot
Keluar screen bot

css
Copy
Edit
ctrl + a + d
DISCLAIMER
Gunakan dengan bijak, semua risiko dan tanggung jawab ada di tangan pengguna.

☕ Donate for Coffee
EVM Address
0x7C8c8eF20a48901372775618330B294ab937C934

SOL Address
GvvSje68JxGQ1suRguLcTq27TwNUzTomed3mEtt1s1KE

© 2025 Plume Push TX Bot. All rights reserved.

