from base64 import b64decode, b64encode

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


def decrypt_data(data: str, private_key: str) -> str:
    encrypted_data = b64decode(data)

    # 创建RSA解密器
    key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(key)

    # 使用解密器解密数据
    decrypted_data = cipher.decrypt(encrypted_data)

    # 将解密后的字节流转换为字符串并返回
    return decrypted_data.decode('utf-8')


def encrypt_data(data: str, public_key: str) -> str:
    # 创建RSA加密器
    key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(key)

    # 将数据转换为字节流
    data_bytes = data.encode('utf-8')

    # 使用加密器加密数据
    encrypted_data = cipher.encrypt(data_bytes)

    # 将加密后的字节流进行Base64编码并返回
    return b64encode(encrypted_data).decode('utf-8')
