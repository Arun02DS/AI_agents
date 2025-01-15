from cryptography.fernet import Fernet
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

key = Fernet.generate_key()

class PII:
    def __init__(self, name, address, ssn, dob, email, phone):
        self.name = name
        self.address = address
        self.ssn = ssn
        self.dob = dob
        self.email = email
        self.phone = phone

    def encrypt(self):
        cipher = Fernet(key)
        encrypted_data = {}
        for attr in self.__dict__:
            encrypted_data[attr] = cipher.encrypt(getattr(self, attr).encode())
        return encrypted_data

    def decrypt(self, encrypted_data):
        cipher = Fernet(key)
        decrypted_data = {}
        for attr, value in encrypted_data.items():
            decrypted_data[attr] = cipher.decrypt(value).decode()
        return decrypted_data

def encrypt_pii(data):
    """Encrypt PII data using AES encryption."""
    cipher_suite = Fernet(secret_key)
    encrypted_data = cipher_suite.encrypt(data.encode('utf-8'))
    return encrypted_data

def decrypt_pii(encrypted_data):
    """Decrypt PII data using AES decryption."""
    cipher_suite = Fernet(secret_key)
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode('utf-8')
    return decrypted_data

def access_control(user_role, data):
    """Implement role-based access controls for PII data."""
    if user_role == 'admin':
        return data
    else:
        return None

def log_access(user, data, action):
    """Log access to PII data."""
    logger.info(f"User {user} {action} PII data at {datetime.now()}")

# Example usage
pii_data = PII("John Doe", "123 Main St", "123-45-6789", "1990-01-01", "johndoe@example.com", "123-456-7890")
encrypted_pii = pii_data.encrypt()
decrypted_pii = pii_data.decrypt(encrypted_pii)


user_role = 'admin'
data = access_control(user_role, pii_data)
print(data)

log_access('admin', pii_data, 'accessed')