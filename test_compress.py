from lzw import lzw_compress, lzw_decompress

with open("example.txt", "rb") as f:
    data = f.read()

compressed = lzw_compress(data)
print("Compressed size:", len(compressed))

decompressed = lzw_decompress(compressed)
assert decompressed == data

with open("recovered.txt", "wb") as f:
    f.write(decompressed)
