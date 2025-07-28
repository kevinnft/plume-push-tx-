import time
import random
from web3 import Web3
from eth_account import Account

# --- Konfigurasi ---
RPC_URL = "https://rpc.plume.org"
CHAIN_ID = 98866
SENDER_PRIVATE_KEY = "isi_pkey"  # ganti dengan private key kamu
GAS_LIMIT = 21000
MIN_AMOUNT = 0.000001
MAX_AMOUNT = 0.00001

# --- Koneksi ke RPC Plume ---
w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = Account.from_key(SENDER_PRIVATE_KEY)
sender_address = account.address

# --- Ambil daftar address ---
with open("address.txt", "r") as f:
    addresses = [line.strip() for line in f if line.strip()]

print(f"🔧 Total target address: {len(addresses)}")
print(f"🔑 Wallet kamu: {sender_address}\n")

# --- Loop tanpa henti ---
while True:
    for i, target_address in enumerate(addresses, start=1):
        try:
            # Hitung amount random & biaya gas
            random_amount = random.uniform(MIN_AMOUNT, MAX_AMOUNT)
            value = w3.to_wei(random_amount, "ether")
            gas_price = w3.eth.gas_price
            gas_cost = gas_price * GAS_LIMIT
            balance = w3.eth.get_balance(sender_address)

            # Skip jika saldo gak cukup
            if balance < value + gas_cost:
                print(f"[{i}] ⚠️ Saldo tidak cukup, sisa: {w3.from_wei(balance, 'ether'):.6f} PLUME")
                time.sleep(10)
                continue

            nonce = w3.eth.get_transaction_count(sender_address)

            tx = {
                "to": target_address,
                "value": value,
                "gas": GAS_LIMIT,
                "gasPrice": gas_price,
                "nonce": nonce,
                "chainId": CHAIN_ID,
            }

            signed_tx = w3.eth.account.sign_transaction(tx, private_key=SENDER_PRIVATE_KEY)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print(f"[{i}] ✅ Sent {random_amount:.8f} PLUME to {target_address} | TX: {w3.to_hex(tx_hash)}")

        except Exception as e:
            print(f"[{i}] ❌ Gagal kirim ke {target_address}: {str(e)}")

        delay = random.uniform(3, 5)
        time.sleep(delay)
