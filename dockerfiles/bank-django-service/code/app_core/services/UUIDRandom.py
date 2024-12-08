import random
import hashlib
import uuid

class UUIDRandom:
    @staticmethod    
    def hash(message:str):
        """Hash函數H()

        使用SHA256，Hash算法
        """
        h = hashlib.new('sha256')
        h.update(bytes(message, 'utf-8'))
        hex_string = h.hexdigest()
        return hex_string

    @staticmethod
    def random_uuid_string():
        random_number =str(random.randint(0,9999999))
        secret_message = UUIDRandom.hash(str(uuid.uuid4())+random_number)
        return secret_message
