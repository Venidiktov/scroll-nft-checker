from web3 import Web3
import json
import time
import random


web3 = Web3(Web3.HTTPProvider('https://rpc.ankr.com/scroll'))

if not web3.is_connected():
    print("Не удалось подключиться к Ethereum через RPC.")
    exit()

with open('abi.json', 'r') as abi_file:
    data = json.load(abi_file)
    contract_abi = json.loads(data[0]['result'])
  
contract_address = Web3.to_checksum_address('0x74670a3998d9d6622e32d0847ff5977c37e0ec91')

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

with open('wallets.txt', 'r') as file:
    wallets = [line.strip() for line in file]


with open('wallets_without_nft.txt', 'w') as file:
    pass


address_number = 0

for wallet_address in wallets:
    if web3.is_address(wallet_address):
        checksum_address = Web3.to_checksum_address(wallet_address)
        try:            
            nft_balance = contract.functions.balanceOf(checksum_address).call()
            address_number += 1  

            if nft_balance == 0:                
                print(f"{address_number}. Адрес без NFT: {checksum_address}")
                with open('wallets_without_nft.txt', 'a') as file:
                    file.write(f"{address_number}. {checksum_address}\n")
            else:
                print(f"{address_number}. Адрес: {checksum_address}, Баланс NFT: {nft_balance}")
        except Exception as e:
            print(f"Ошибка при проверке адреса {checksum_address}: {e}")
    else:
        print(f"Некорректный адрес: {wallet_address}")
   
    time.sleep(random.randint(5, 10))
