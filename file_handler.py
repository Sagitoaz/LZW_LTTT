import struct

def read_binary_file(file_path: str) -> bytes:
    """Đọc nội dung file bất kỳ dưới dạng nhị phân."""
    with open(file_path, 'rb') as f:
        return f.read()

def write_binary_file(file_path: str, data: bytes):
    """Ghi dữ liệu nhị phân ra file."""
    with open(file_path, 'wb') as f:
        f.write(data)

def save_compressed_file(file_path: str, compressed_data: list, original_extension: str):
    """Lưu mã nén và đuôi file gốc vào file .lzw"""
    with open(file_path, 'wb') as f:
        # Ghi độ dài của đuôi + đuôi file
        ext_bytes = original_extension.encode('utf-8')
        f.write(struct.pack('B', len(ext_bytes)))  # 1 byte: độ dài
        f.write(ext_bytes)                         # n byte: đuôi file
        
        # Ghi mã nén
        for code in compressed_data:
            f.write(struct.pack('>I', code))

def load_compressed_file(file_path: str) -> tuple:
    """Trả về tuple (đuôi gốc, danh sách mã)"""
    compressed_data = []
    with open(file_path, 'rb') as f:
        # Đọc đuôi file
        ext_len = struct.unpack('B', f.read(1))[0]
        ext = f.read(ext_len).decode('utf-8')

        # Đọc mã
        while True:
            bytes_read = f.read(4)
            if len(bytes_read) < 4:
                break
            (code,) = struct.unpack('>I', bytes_read)
            compressed_data.append(code)
    return ext, compressed_data
