import logging
import argparse
import json

import generation
import encrypting
import decrypting

logging.basicConfig(level=logging.INFO)
gen_logger = logging.getLogger("Генерация")
enc_logger = logging.getLogger("Шифрование")
dec_logger = logging.getLogger("Дешифрование")

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-gen', '--generation', help='Запускает режим генерации ключей', action="store_true")
group.add_argument('-enc', '--encryption', help='Запускает режим шифрования', action="store_true")
group.add_argument('-dec', '--decryption', help='Запускает режим дешифрования', action="store_true")
parser.add_argument('-iv', '--initializing_vector', type=int, choices=[128, 192, 256],
                    help='Количество бит для генерации ключа', required=True)
args = parser.parse_args()

with open('settings.json', 'r') as json_file:
    ways = json.load(json_file)

if args.generation:
    gen_logger.info("Генерация ключей")
    gen = generation.Generator(args.initializing_vector, ways)
    gen_logger.info("Запись открытого ключа..")
    gen.write_public_key()
    gen_logger.info("Запись закрытого ключа..")
    gen.write_secret_key()
    gen_logger.info("Запись результата симметричного ключа..")
    gen.write_result_key()
    gen_logger.info("Готово")
else:
    if args.encryption:
        enc = encrypting.Encryptor(ways)
        enc_logger.info("Шифрование..")
        enc.encrypt()
        enc_logger.info("Готово")
    else:
        dec = decrypting.Decryptor(ways)
        dec_logger.info("Дешифрование..")
        dec.decrypt()
        dec_logger.info("Готово")