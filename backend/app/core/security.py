from pwdlib import PasswordHash

password_has=PasswordHash.recommended()

def hash_password(password:str)->str:
    return password_has.hash(password)

def verify_password(password:str,hashed_password:str)->bool:
    return password_has.verify(password,hashed_password)

hashed=hash_password("rohit1234")
print(hashed)
print(verify_password("rohit1234",hashed))