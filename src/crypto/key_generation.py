from cryptography.hazmat.primitives.asymmetric import ec

key: str = None         # Ready key
ServerKey: str = None   # For client
cipher = None           # Fernet object
private_key = None