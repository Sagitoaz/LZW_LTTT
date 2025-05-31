'''
    Project: LZW Compression & Decompression Tool
    To fulfil the requirement of FIT Course by Pham@PTIT
    Nguyen Thanh Trung - B23DCCN861 - group 12
    Dang Phi Long - B23DCCN497 - group 12
    Tran Trung Kien - B23DCCN469 - group 12
    Pham Anh Tu - B23DCCN875 - group 12   
'''
from file_handler import load_compressed_file

# Đường dẫn tới file .lzw
file_path = "mahoa.lzw"  #  Đổi thành tên file bạn muốn đọc

# Đọc file và lấy dữ liệu
ext, compressed_codes, stored_hash = load_compressed_file(file_path)

# In kết quả
print("Đuôi file gốc:", ext)
print("Mã nén LZW (dạng số):")
print(compressed_codes)

# Nếu file có mật khẩu:
if stored_hash != b'\x00' * 32:
    print("(📌 File có mật khẩu bảo vệ — mã SHA-256)")
