'''
    Project: LZW Compression & Decompression Tool
    To fulfil the requirement of FIT Course by Pham@PTIT
    Nguyen Thanh Trung - B23DCCN861 - group 12
    Dang Phi Long - B23DCCN497 - group 12
    Tran Trung Kien - B23DCCN469 - group 12
    Pham Anh Tu - B23DCCN875 - group 12   
'''
from file_handler import load_compressed_file
from lzw import lzw_compress, lzw_decompress

def lzw_compress_verbose(uncompressed: bytes):
    dict_size = 256
    dictionary = {bytes([i]): i for i in range(dict_size)}
    w = b""
    result = []

    print("=== Từ điển ban đầu ===")
    for k, v in dictionary.items():
        if v < 128:
            print(f"{repr(k)} : {v}")

    print("\n=== Quá trình mã hóa ===")
    for c in uncompressed:
        wc = w + bytes([c])
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            print(f"Thêm vào từ điển: {repr(wc)} = {dict_size}")
            dictionary[wc] = dict_size
            dict_size += 1
            w = bytes([c])

    if w:
        result.append(dictionary[w])

    print("\n=== Từ điển cuối cùng (chỉ phần thêm) ===")
    for k, v in dictionary.items():
        if v >= 256:
            print(f"{v}: {repr(k)}")

    return result

if __name__ == "__main__":
    import sys
    import hashlib

    if len(sys.argv) != 2:
        print("Cách dùng: python show_dict_from_lzw.py <file.lzw>")
        sys.exit(1)

    file_path = sys.argv[1]
    ext, compressed_codes, stored_hash = load_compressed_file(file_path)

    print(f"🔍 Đọc file: {file_path}")
    print(f"Đuôi file gốc: .{ext}")
    print(f"Tổng số mã nén: {len(compressed_codes)}")

    if stored_hash != b'\x00' * 32:
        password = input("🔐 Nhập mật khẩu: ")
        input_hash = hashlib.sha256(password.encode()).digest()
        if input_hash != stored_hash:
            print("❌ Sai mật khẩu!")
            sys.exit(1)

    # Giải nén rồi nén lại để tái tạo từ điển
    decompressed_data = lzw_decompress(compressed_codes)
    print("\n✅ Đã giải nén. Bắt đầu nén lại để hiển thị từ điển...")
    lzw_compress_verbose(decompressed_data)
