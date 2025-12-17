import json
import base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import os
import datetime
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
from PySide6.QtCore import QFile, QIODevice
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import base64

sys.path.append(os.getcwd())
import resources_rc


def read_resource(resource_path):
    """Читает данные из ресурса PySide6"""
    file = QFile(resource_path)
    
    if not file.exists():
        raise FileNotFoundError(f"Ресурс не найден: {resource_path}")
    
    if file.open(QIODevice.ReadOnly):
        data = bytes(file.readAll())
        file.close()
        return data
    else:
        raise IOError(f"Не удалось открыть ресурс: {resource_path}")
    

def decrypt_file_with_private_key(encrypted_file, private_key, output_file=None, password=None):
    """
    Расшифровывает файл, зашифрованный RSA публичным ключом
    
    Args:
        encrypted_file: путь к зашифрованному файлу
        private_key_file: путь к файлу с приватным ключом
        output_file: путь для сохранения расшифрованного файла (опционально)
        password: пароль для зашифрованного приватного ключа
    """
    
    
    
    # 2. Читаем зашифрованный файл
    print(f"Чтение зашифрованного файла {encrypted_file}...")
    with open(encrypted_file, "rb") as f:
        encrypted_data = f.read()
    
    print(f"✓ Прочитано {len(encrypted_data)} байт")
    
    # 3. Определяем формат зашифрованных данных
    try:
        # Пробуем декодировать как JSON (многоканковое шифрование)
        encrypted_str = encrypted_data.decode('utf-8')
        chunks = json.loads(encrypted_str)
        
        if isinstance(chunks, list):
            print(f"Обнаружено многоканковое шифрование: {len(chunks)} чанков")
            
            # Расшифровываем каждый чанк
            decrypted_chunks = []
            for i, chunk_b64 in enumerate(chunks, 1):
                print(f"  Расшифровка чанка {i}/{len(chunks)}...")
                chunk_data = base64.b64decode(chunk_b64)
                decrypted_chunk = private_key.decrypt(
                    chunk_data,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                decrypted_chunks.append(decrypted_chunk)
            
            decrypted_data = b''.join(decrypted_chunks)
        else:
            raise ValueError("Неверный формат JSON")
            
    except (json.JSONDecodeError, UnicodeDecodeError):
        # Если не JSON, то это single chunk в base64 или raw bytes
        print("Обнаружено одноканальное шифрование...")
        
        try:
            print('Пробуем декодировать как base64')
            encrypted_bytes = base64.b64decode(encrypted_data)
        except:
            print('Если не base64, используем как есть')
            encrypted_bytes = encrypted_data
        
        decrypted_data = private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
   
    return json.loads(decrypted_data.decode('utf-8'))


if __name__ == "__main__":


    private_key = serialization.load_pem_private_key(
        read_resource(":/keys_manager/private_key.pem"),
        password="Rostiks".encode(),  # Укажите пароль если ключ зашифрован
        backend=None    # default_backend будет использован автоматически
        )


    decrypted = decrypt_file_with_private_key(
        encrypted_file=os.path.join(os.getcwd(), 'license_manager', 'license'),
        private_key=private_key
    )

    print(decrypted)