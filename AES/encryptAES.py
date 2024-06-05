import argparse
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from PIL import Image
import io
import os
from Crypto.Hash import SHA256, HMAC

def encrypt_image(input_image_path, output_image_path, key):
    image = Image.open(input_image_path)
    iv = get_random_bytes(AES.block_size)
    image_hash = SHA256.new(os.path.basename(input_image_path).encode("utf-8")).hexdigest()
    key_specific = HMAC.new(key, msg=image_hash.encode("utf-8"), digestmod=SHA256).digest()
    unique_iv = HMAC.new(key_specific, msg=os.urandom(16), digestmod=SHA256).digest()[:16]
    
    img_byte_array = io.BytesIO()
    image.save(img_byte_array, format=image.format)
    img_bytes = img_byte_array.getvalue()
    
    cipher = AES.new(key, AES.MODE_CBC, unique_iv)
    padded_data = pad(img_bytes, AES.block_size)
    encrypted_data = iv + cipher.encrypt(padded_data)
    
    with open(output_image_path, 'wb') as f:
        f.write(encrypted_data)
    
    iv_path = os.path.join(os.path.dirname(output_image_path), f"{os.path.basename(input_image_path)}.iv")
    with open(iv_path, 'wb') as f:
        f.write(unique_iv)
    
    print(f"Encryption successful. Encrypted image saved to '{output_image_path}'.")
    print(f"IV file saved to '{iv_path}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encrypt an image.")
    parser.add_argument("input_image_path", help="Path to the input image")
    parser.add_argument("output_image_path", help="Path to save the encrypted image")
    parser.add_argument("key", help="Encryption key")

    args = parser.parse_args()
    key = bytes(args.key, encoding="utf-8")
    encrypt_image(args.input_image_path, args.output_image_path, key)

