from hashlib import md5

x: bytes = "Hello World".encode(encoding="UTF-8")
print(x)

hashMD5 = md5(string=x)

print(hashMD5.hexdigest())
