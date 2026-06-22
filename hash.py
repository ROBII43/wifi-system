import hashlib

password = "Robii43535.."
hashed = hashlib.sha256(password.encode()).hexdigest()

print(hashed)