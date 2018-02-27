BASE64_PAD = '='
BASE64_PAD_ASCII = 61
table_b2a_base64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
# [table_a2b_base64.__setitem__(ord(c), i) for i, c in enumerate(table_b2a_base64)]
table_a2b_base64 = [
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1, 63,
    52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, 0, -1, -1,  # PAD -> 0
    -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
    15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1,
    -1, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
    41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, -1, -1, -1, -1, -1
]


# Base64 encoding/decoding

def b64encode(s, altchars=None):
    ascii_data = ''
    leftchar = 0
    leftbits = 0
    bin_len = len(s)

    for bin_data in s:
        leftchar = (leftchar << 8) | bin_data  # 左移 8 位 0，或操作补在最后
        leftbits += 8
        # 查看每组 6-bit 数据是否准备好
        while leftbits >= 6:
            this_ch = leftchar >> (leftbits - 6) & 0b111111  # 左边只取最右边 6 bits
            leftbits -= 6
            ascii_data += table_b2a_base64[this_ch]
    # 补后缀
    if leftbits == 2:
        ascii_data += table_b2a_base64[(leftchar & 0b11) << 4]
        ascii_data += BASE64_PAD
        ascii_data += BASE64_PAD
    elif leftbits == 4:
        ascii_data += table_b2a_base64[(leftchar & 0b1111) << 2]
        ascii_data += BASE64_PAD

    return ascii_data.encode()


def b64decode(s, altchars=None, validate=False):
    ascii_len = len(s)
    leftchar = 0
    leftbits = 0
    bin_data = bytearray()

    for ascii_data in s:
        this_ch = ascii_data
        if this_ch == BASE64_PAD_ASCII:
            continue
        this_ch = table_a2b_base64[ascii_data]
        if this_ch == -1:
            continue

        leftchar = (leftchar << 6) | this_ch
        leftbits += 6
        if leftbits >= 8:  # 因为 6 + 8 < 16 所以不需要用 while
            leftbits -= 8
            bin_data.append((leftchar >> leftbits) & 0xff)  # 右移剩下的，就是得到的 byte
            leftchar &= ((1 << leftbits) - 1)  # 只保留没有匹配的 bits

    return bytes(bin_data)
