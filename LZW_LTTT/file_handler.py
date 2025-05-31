'''
    Project: LZW Compression & Decompression Tool
    To fulfil the requirement of FIT Course by Pham@PTIT
    Nguyen Thanh Trung - B23DCCN861 - group 12
    Dang Phi Long - B23DCCN497 - group 12
    Tran Trung Kien - B23DCCN469 - group 12
    Pham Anh Tu - B23DCCN875 - group 12   
'''
import struct
import hashlib

def read_binary_file(file_path: str) -> bytes:
    with open(file_path, 'rb') as f:
        return f.read()

def write_binary_file(file_path: str, data: bytes):
    with open(file_path, 'wb') as f:
        f.write(data)

def get_best_format(max_code: int):
    if max_code <= 255:
        return 'B', 1
    elif max_code <= 65535:
        return 'H', 2
    else:
        return 'I', 4

def save_compressed_file(file_path: str, compressed_data: list, original_extension: str, password: str = ""):
    max_code = max(compressed_data) if compressed_data else 0
    fmt_char, size = get_best_format(max_code)
    password_hash = hashlib.sha256(password.encode()).digest() if password else b'\x00' * 32

    with open(file_path, 'wb') as f:
        # Ghi định dạng ('B', 'H', 'I')
        f.write(fmt_char.encode('utf-8'))

        # Ghi độ dài đuôi file + đuôi
        ext_bytes = original_extension.encode('utf-8')
        f.write(struct.pack('B', len(ext_bytes)))
        f.write(ext_bytes)

        # Ghi hash mật khẩu (32 byte)
        f.write(password_hash)

        # Ghi mã nén
        for code in compressed_data:
            f.write(struct.pack('>' + fmt_char, code))

def load_compressed_file(file_path: str):
    compressed_data = []
    with open(file_path, 'rb') as f:
        fmt_char = f.read(1).decode('utf-8')
        size = {'B': 1, 'H': 2, 'I': 4}[fmt_char]

        ext_len = struct.unpack('B', f.read(1))[0]
        ext = f.read(ext_len).decode('utf-8')

        # Đọc hash mật khẩu (32 byte)
        stored_hash = f.read(32)

        while True:
            bytes_read = f.read(size)
            if len(bytes_read) < size:
                break
            (code,) = struct.unpack('>' + fmt_char, bytes_read)
            compressed_data.append(code)

    return ext, compressed_data, stored_hash
