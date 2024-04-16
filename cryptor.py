from Cryptodome.Cipher import AES,PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from io import BytesIO

import base64
import zlib
def generate():
    new_key=RSA.generate(2048)
    private_key=new_key.export_key()
    public_key=new_key.public_key().export_key()
    with open('key.pri','wb') as f:
        f.write(private_key)
    with open('key.pub','wb') as f:
        f.write(public_key)
def get_rsa_cipher(keytype):
    with open(f'key.{keytype}') as f:
        key=f.read()
    rsakey=RSA.import_key(key)
    return (PKCS1_OAEP.new(rsakey),rsakey.size_in_bytes())
def encrypt(plaintext):
    compressed_text=zlib.compress(plaintext)
    seession_key=get_random_bytes(16)
    cipher_aes=AES.new(seession_key,AES.MODE_EAX)

    ciphertext,tag=cipher_aes.encrypt_and_digest(compressed_text)
    cipher_rsa,_=get_rsa_cipher('pub')
    encrypted_session_key=cipher_rsa.encrypt(seession_key)
    
    msg_payload=encrypted_session_key+cipher_aes.nonce+tag+ciphertext
    encrypted=base64.encodebytes(msg_payload)
    return encrypted

def decrypt(encrypted):
    encrypted_bytes=BytesIO(base64.decodebytes(encrypted))
    cipher_rsa,keysize_in_bytes=get_rsa_cipher('pri')
    # print(keysize_in_bytes)
    encrypted_session_key=encrypted_bytes.read(keysize_in_bytes)
    nonce=encrypted_bytes.read(16)
    tag=encrypted_bytes.read(16)
    ciphertext=encrypted_bytes.read()

    seession_key=cipher_rsa.decrypt(encrypted_session_key)
    cipher_aes=AES.new(seession_key,AES.MODE_EAX,nonce=nonce)
    decrypted=cipher_aes.decrypt_and_verify(ciphertext,tag)

    plaintext=zlib.decompress(decrypted)
    return plaintext
if __name__=="__main__":
    # generate()
    # plaintext=b'hey there you'
    # encrypted=encrypt(plaintext)
    encrypted=b'tFqfPesGwvVeBs8x4hSNuKtNWk4xV6B5amZztcb1Zl5ZPGKc6iOky8FV1sXbEyXD8itT/jJEvVLy\nHGaIGztfuHG1dDAPp/JCWvZamREN8bsgFjy2PGxB+8DZVmNzKUFBWWGjpq5bzj9Oltcgb2mR/7la\npocuMLHpt+/4wlZNsBFVE9DU3CyBdH1z75bQ7zFWaY0/751ebqWT/EfTbx9m5qlwGsHZHDl/p+O7\nLBLRqaoXjj1Z4fXxPrfqIS9u0CIMlye1m1gXp7IcLJDpZTTFGO8X8zWWunqZhfPuDuBzr8OMVkHC\nnw/V/1+U8zhW9sRJigl8Rc0U5s8GMH20A+p/ziNmmIrZhCaa5irhnDi4iPC7/vwCOx4i58WHKP/5\nif9L0AwUmeeos7lAAk/vf7mKillC\n'
    decrypted=decrypt(encrypted)
    print(decrypted)