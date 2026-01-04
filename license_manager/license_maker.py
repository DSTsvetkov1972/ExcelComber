import json
import base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import os
from datetime import datetime
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
from PySide6.QtCore import QFile, QIODevice
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import base64

def load_public_key_from_pem(filename):
    """Загружает публичный ключ из PEM файла"""
    with open(filename, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return public_key


def encrypt_dict_with_public_key(data_dict, public_key):
    """
    Шифрует словарь с использованием публичного ключа RSA
    
    Args:
        data_dict: словарь для шифрования
        public_key: публичный RSA ключ
    """
    # Конвертируем словарь в JSON строку
    json_data = json.dumps(data_dict, ensure_ascii=False)
    print(json_data)
    
    # Преобразуем в байты
    data_bytes = json_data.encode('utf-8')
    
    # Определяем максимальный размер данных для RSA
    # Для RSA-2048: 256 байт - 42 байта для padding = 214 байт
    max_chunk_size = public_key.key_size // 8 - 42
    
    if len(data_bytes) <= max_chunk_size:
        print("Данные помещаются в один блок")
        encrypted = public_key.encrypt(
            data_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(encrypted).decode()
    else:
        print("Разделяем на чанки")
        chunks = []
        for i in range(0, len(data_bytes), max_chunk_size):
            chunk = data_bytes[i:i + max_chunk_size]
            encrypted_chunk = public_key.encrypt(
                chunk,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            chunks.append(base64.b64encode(encrypted_chunk).decode())
        
        return json.dumps(chunks, ensure_ascii=False)


def save_encrypted_dict_to_file(encrypted_data, filename="encrypted_data.bin"):
    """Сохраняет зашифрованные данные в файл"""
    
    # Если это список чанков (JSON строка), сохраняем как есть
    if isinstance(encrypted_data, str) and encrypted_data.startswith('['):
        data_to_save = encrypted_data.encode('utf-8')
    else:
        # Иначе это base64 строка
        data_to_save = encrypted_data.encode('utf-8')
    
    with open(filename, "wb") as f:
        f.write(data_to_save)
    
    print(f"✓ Зашифрованные данные сохранены в {filename}")
    return filename


if __name__ == "__main__":

    data_dict = {
        'user': 'Цветков Дмитрий',
        'trial_finish': f"{datetime(2026, 12, 31)}"}

    public_key_pem = os.path.join(os.getcwd(),'keys_manager', 'public_key.pem')
    license_file = os.path.join(os.getcwd(), 'license_manager', 'license')
   
    public_key = load_public_key_from_pem(public_key_pem)
    encrypted_data = encrypt_dict_with_public_key(data_dict, public_key)
    save_encrypted_dict_to_file(encrypted_data, filename=license_file)
