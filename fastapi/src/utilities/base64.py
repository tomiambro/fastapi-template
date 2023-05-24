import base64


def base64_encode(data: str):
    # Convert the string to bytes
    bytes = data.encode("utf-8")

    # Encode the bytes using base64
    encoded_bytes = base64.b64encode(bytes)

    # Convert the encoded bytes back to a string
    encoded_string = encoded_bytes.decode("utf-8")

    return encoded_string
