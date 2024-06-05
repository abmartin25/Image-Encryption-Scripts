import argparse
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from PIL import Image
import io
import os
from Crypto.Hash import SHA256, HMAC

def decrypt_image(encrypted_image_path, iv_path, output_image_path, key):
    with open(iv_path, 'rb') as f:
        unique_iv = f.read()
    
    with open(encrypted_image_path, 'rb') as f:
        iv = f.read(AES.block_size)
        encrypted_data = f.read()

    cipher = AES.new(key, AES.MODE_CBC, unique_iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

    img_byte_array = io.BytesIO(decrypted_data)
    image = Image.open(img_byte_array)
    
    image.save(output_image_path)
    print(f"Decryption successful. Decrypted image saved to '{output_image_path}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Decrypt an image.")
    parser.add_argument("encrypted_image_path", help="Path to the encrypted image")
    parser.add_argument("iv_path", help="Path to the IV file")
    parser.add_argument("output_image_path", help="Path to save the decrypted image")
    parser.add_argument("key", help="Decryption key")

    args = parser.parse_args()
    key = bytes(args.key, encoding="utf-8")
    decrypt_image(args.encrypted_image_path, args.iv_path, args.output_image_path, key)

