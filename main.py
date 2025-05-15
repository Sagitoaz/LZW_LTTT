from lzw import lzw_compress, lzw_decompress
from file_handler import read_binary_file, write_binary_file, save_compressed_file, load_compressed_file

# Bước 1: Đọc file gốc
data = read_binary_file("example.txt")

# Bước 2: Nén dữ liệu
compressed = lzw_compress(data)
save_compressed_file("example.lzw", compressed)
print(f"Original size: {len(data)} bytes, Compressed codes: {len(compressed)}")

# Bước 3: Đọc file nén & giải nén
compressed_data = load_compressed_file("example.lzw")
decompressed = lzw_decompress(compressed_data)

# Bước 4: Ghi lại file phục hồi
write_binary_file("recovered_example.txt", decompressed)
