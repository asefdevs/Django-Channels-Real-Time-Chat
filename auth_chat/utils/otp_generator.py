import pyotp

def generate_secret_key():
    secret_key = pyotp.random_base32()
    return secret_key

def generate_otp(secret_key, interval: int = 300)->str:
    totp = pyotp.TOTP(secret_key,interval=interval)
    otp = totp.now()
    return otp

def verify_otp(secret_key, otp, interval: int = 300)->bool:
    totp = pyotp.TOTP(secret_key,interval=interval)
    return totp.verify(otp)