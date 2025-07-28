import time
import random
from web3 import Web3
from eth_account import Account

# --- Konfigurasi ---
RPC_URL = "https://rpc.plume.org"
CHAIN_ID = 98866
SENDER_PRIVATE_KEY = "pvkey"
GAS_LIMIT = 21000
MIN_AMOUNT = 0.000001
MAX_AMOUNT = 0.00001

# --- Koneksi ke RPC Plume ---
w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = Account.from_key(SENDER_PRIVATE_KEY)
sender_address = account.address

print(f"🔑 Wallet: {sender_address}\n")

last_block = None
sent_addresses = set()

while True:
    try:
        block = w3.eth.get_block("latest", full_transactions=True)

        if last_block == block.number:
            time.sleep(2)
            continue
        last_block = block.number

        print(f"\n📦 Blok terbaru: {block.number} | Jumlah TX: {len(block.transactions)}")

        # Ambil semua address unik penerima
        unique_addresses = set(
            tx["to"] for tx in block.transactions
            if tx["to"] and tx["to"].lower() != sender_address.lower()
        )

        if not unique_addresses:
            print("⚠️ Tidak ada address wallet valid di blok ini")
            time.sleep(2)
            continue

        for idx, target_address in enumerate(unique_addresses, start=1):
            # Skip jika sudah dikirim sebelumnya
            if target_address in sent_addresses:
                continue

            # Skip jika address adalah kontrak
            code = w3.eth.get_code(target_address)
            if code != b'':
                print(f"⏭️ [{idx}] Skip kontrak: {target_address}")
                continue

            random_amount = random.uniform(MIN_AMOUNT, MAX_AMOUNT)
            value = w3.to_wei(random_amount, "ether")
            gas_price = w3.eth.gas_price
            gas_cost = gas_price * GAS_LIMIT
            balance = w3.eth.get_balance(sender_address)

            if balance < value + gas_cost:
                print(f"⚠️ [{idx}] Saldo tidak cukup: {w3.from_wei(balance, 'ether'):.6f} PLUME")
                break

            nonce = w3.eth.get_transaction_count(sender_address)

            tx_data = {
                "to": target_address,
                "value": value,
                "gas": GAS_LIMIT,
                "gasPrice": gas_price,
                "nonce": nonce,
                "chainId": CHAIN_ID,
            }

            signed_tx = w3.eth.account.sign_transaction(tx_data, private_key=SENDER_PRIVATE_KEY)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

            print(f"✅ [{idx}] Kirim {random_amount:.8f} PLUME ke {target_address} | TX: {w3.to_hex(tx_hash)}")
            sent_addresses.add(target_address)

            time.sleep(random.uniform(3, 5))

        # Reset daftar kiriman setiap blok baru
        sent_addresses.clear()

        time.sleep(2)

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        time.sleep(5)

