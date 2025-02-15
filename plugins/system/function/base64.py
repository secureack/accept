import base64
from charset_normalizer import detect

def base64encode(string,encoding="auto"):
    if encoding != "auto":
        return base64.b64encode(string.encode(encoding)).decode()
    return base64.b64encode(string.encode()).decode()

def base64decode(base64String,encoding="auto"):
    encodedString = base64.b64decode(base64String.encode())
    if encoding == "auto":
        encodedString = base64.b64decode(base64String.encode())
        detector = detect(encodedString)
        if detector["confidence"] > 0.5:
            return encodedString.decode(detector["encoding"])
        return encodedString.decode()
    else:
        return encodedString.decode(encoding)