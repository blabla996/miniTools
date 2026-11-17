import hashlib as h

def breakPassword ():
    with open ("C:\\Users\\Aless\\Downloads\\rockyou.txt", "r", encoding="utf-8", errors="ignore") as f :
        goal = "cd0894152aa5eec36ec79eb2bcb90ca40f056804530f40732b4957a496b23dc8"
        for line in f:
            password = line.strip()
            # Hash the password candidate
            hash_object = h.sha256(password.encode("utf-8"))
            hash_hex = hash_object.hexdigest()
            
            # Compare with target
            if hash_hex == goal:
                print(f"[+] Password found: {password}")
                return password
    
    print("[-] Password not found in wordlist.")
    return None
            
            
def main () :
    breakPassword()
    password = "ariena"

# Convertimos a bytes con encode()
    hash_object = h.sha256(password.encode("utf-8"))
    
    hash_hex = hash_object.hexdigest()
    print(hash_hex)

if __name__ == "__main__":
    main()
        
