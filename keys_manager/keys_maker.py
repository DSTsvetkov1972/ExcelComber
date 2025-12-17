from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import os

class AsymmetricCryptoSystem:
    def __init__(self, password):
        self.password = password
        self.private_key = None
        self.public_key = None
    
    def generate_keys(self):
        """Генерация ключевой пары"""
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        self.public_key = self.private_key.public_key()
    
    def save_keys(
            self,
            private_path=os.path.join(os.getcwd(), "keys_manager", "private_key.pem"),
            public_path=os.path.join(os.getcwd(), "keys_manager", "public_key.pem")
            ):
        """Сохранение ключей в файлы"""
        # Сохраняем приватный ключ с шифрованием
        with open(private_path, "wb") as f:
            f.write(self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.BestAvailableEncryption(
                    self.password.encode()
                )
            ))
        
        # Сохраняем публичный ключ
        with open(public_path, "wb") as f:
            f.write(self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
    
    def encrypt_message(self, message, public_key=None):
        """Шифрование сообщения"""
        if public_key is None:
            public_key = self.public_key
        
        encrypted = public_key.encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted
    
    def decrypt_message(self, encrypted_message):
        """Дешифрование сообщения"""
        decrypted = self.private_key.decrypt(
            encrypted_message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted.decode()

# Использование
password = "Rostiks"
crypto = AsymmetricCryptoSystem(password)

# Генерация ключей
crypto.generate_keys()

# Сохранение ключей
crypto.save_keys()

# Шифрование сообщения
message = "Секретное сообщение!"
encrypted = crypto.encrypt_message(message)
print(f"Зашифрованное сообщение: {encrypted.hex()}")

# Дешифрование
decrypted = crypto.decrypt_message(encrypted)
print(f"Расшифрованное сообщение: {decrypted}")