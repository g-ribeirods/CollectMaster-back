import bcrypt

def get_password_hash(password: str) -> str:
    """
    Cria um hash de senha usando bcrypt.
    """
    password_bytes = password.encode('utf-8')
    
    salt = bcrypt.gensalt()
    
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    
    return hashed_bytes.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha pura bate com o hash salvo.
    """
    try:
        plain_password_bytes = plain_password.encode('utf-8')
        
        hashed_password_bytes = hashed_password.encode('utf-8')
        
        return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)
    except Exception:
        return False