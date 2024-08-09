import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        confidence = result['confidence']

        print(f"Detected encoding: {encoding} with confidence {confidence}")

        return encoding, confidence


def is_ascii(file_path):
    try:
        with open(file_path, 'r', encoding='ascii') as f:
            f.read()
        return True
    except UnicodeDecodeError:
        return False


def check_csv_encoding(file_path):
    encoding, confidence = detect_encoding(file_path)

    if encoding.lower() in ['utf-16', 'utf-16le', 'utf-16be']:
        print("The file is encoded in UTF-16.")
    elif is_ascii(file_path):
        print("The file is encoded in ASCII.")
    else:
        print(f"The file is encoded in {encoding}, not ASCII or UTF-16.")


# Example usage
file_path = 'data/summary.txt'
check_csv_encoding(file_path)