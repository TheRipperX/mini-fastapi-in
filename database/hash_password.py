from cryptography.fernet import Fernet


class Hash_Pass():

    key_org = None
    f_Fernet = None

    def __init__(self):
        self.key_org = b'_HJCli5Bt0ubHOvcW0l7UeUmCwLfTyW6Y0oaDtJISmg='
        self.f_Fernet = Fernet(self.key_org)
    
    def hash_password(self, password):
        pass_is_hash = bytes(password, encoding="utf-8")
        
        encrypt = self.f_Fernet.encrypt(pass_is_hash)

        return encrypt


    
    def unhash_password(self, password):
        decrypt_pass = self.f_Fernet.decrypt(password)

        return decrypt_pass





