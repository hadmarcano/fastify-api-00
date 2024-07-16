from jwt import encode, decode


# encoded = encode({"some": "payload"}, "secret", algorithm="HS256")
# print(encoded)

# decoded = decode(encoded, "secret", algorithms=["HS256"])
# print(decoded)

def create_token(data: dict):
    token: str = encode(payload=data, key="secret", algorithm="HS256")
    return token
