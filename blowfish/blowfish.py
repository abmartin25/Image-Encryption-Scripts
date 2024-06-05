from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import pad, unpad
from PIL import Image
import io
import os

def encrypt_image_blowfish(input_image_path, output_image_path, key):
    image = Image.open(input_image_path)
    img_byte_array = io.BytesIO()
    image.save(img_byte_array, format=image.format)
    img_bytes = img_byte_array.getvalue()
    
    cipher = Blowfish.new(key, Blowfish.MODE_CBC)
    padded_data = pad(img_bytes, Blowfish.block_size)
    iv = cipher.iv
    encrypted_data = iv + cipher.encrypt(padded_data)
    
    with open(output_image_path, 'wb') as f:
        f.write(encrypted_data)
    print(f"Encryption successful. Encrypted image saved to '{output_image_path}'.")

def decrypt_image_blowfish(encrypted_image_path, output_image_path, key):
    with open(encrypted_image_path, 'rb') as f:
        iv = f.read(Blowfish.block_size)
        encrypted_data = f.read()
    
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), Blowfish.block_size)
    
    img_byte_array = io.BytesIO(decrypted_data)
    image = Image.open(img_byte_array)
    image.save(output_image_path)
    print(f"Decryption successful. Decrypted image saved to '{output_image_path}'.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Encrypt or decrypt an image using Blowfish.")
    parser.add_argument("mode", choices=["encrypt", "decrypt"], help="Mode: encrypt or decrypt")
    parser.add_argument("input_image_path", help="Path to the input image")
    parser.add_argument("output_image_path", help="Path to save the output image")
    parser.add_argument("key", help="Encryption/Decryption key")

    args = parser.parse_args()
    key = bytes(args.key, encoding="utf-8")
    
    if args.mode == "encrypt":
        encrypt_image_blowfish(args.input_image_path, args.output_image_path, key)
    elif args.mode == "decrypt":
        decrypt_image_blowfish(args.input_image_path, args.output_image_path, key)

