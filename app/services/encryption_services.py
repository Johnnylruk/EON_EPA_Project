import hashlib
import gnupg
import os

class EncryptionService():
    
    def encrypt(self):
        gpg = gnupg.GPG()
        input_data = gpg.gen_key_input(
            

        )

        gpg.encrypt()
        return

    def decrypt(self):
        gpg = gnupg.GPG()
        input_data = gpg.gen_key_input(
            

        )

        gpg.decrypt()
        return


    def create_tls_connection():
        return ""