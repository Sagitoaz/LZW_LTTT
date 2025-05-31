'''
    Project: LZW Compression & Decompression Tool
    To fulfil the requirement of FIT Course by Pham@PTIT
    Nguyen Thanh Trung - B23DCCN861 - group 12
    Dang Phi Long - B23DCCN497 - group 12
    Tran Trung Kien - B23DCCN469 - group 12
    Pham Anh Tu - B23DCCN875 - group 12   
'''
def lzw_compress(uncompressed: bytes) -> list:
    """Compress a string to a list of output symbols."""
    dict_size = 256
    dictionary = {bytes([i]): i for i in range(dict_size)}

    w = b""
    result = []
    for c in uncompressed:
        wc = w + bytes([c])
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = bytes([c])
    if w:
        result.append(dictionary[w])
    return result


def lzw_decompress(compressed: list) -> bytes:
    """Decompress a list of output ks to a string."""
    dict_size = 256
    dictionary = {i: bytes([i]) for i in range(dict_size)}

    w = bytes([compressed.pop(0)])
    result = bytearray(w)
    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + bytes([w[0]])
        else:
            raise ValueError('Bad compressed k: %s' % k)
        result.extend(entry)

        dictionary[dict_size] = w + bytes([entry[0]])
        dict_size += 1

        w = entry
    return bytes(result)
