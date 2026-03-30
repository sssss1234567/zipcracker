import zipfile
import itertools
import zlib

# 修复伪加密（本地头+中央目录都改）
def fix_fake(src, out):
    with open(src, 'rb') as f:
        data = f.read()
    
    # 修改本地文件头
    idx = 0
    while True:
        idx = data.find(b'PK\x03\x04', idx)
        if idx == -1:
            break
        data = data[:idx+6] + b'\x00' + data[idx+7:]
        idx += 4
    
    # 修改中央目录
    idx = 0
    while True:
        idx = data.find(b'PK\x01\x02', idx)
        if idx == -1:
            break
        data = data[:idx+6] + b'\x00' + data[idx+7:]
        idx += 4
    
    with open(out, 'wb') as f:
        f.write(data)
    print(f"✅ 修复完成，已保存为: {out}")

# CRC32 碰撞（可打印字符版）
def crc_reverse(target_crc, length):
    chars = range(0x20, 0x7F)
    for combo in itertools.product(chars, repeat=length):
        data = bytes(combo)
        if zlib.crc32(data) & 0xFFFFFFFF == target_crc:
            return data
    return b''

# 爆破密码
def brute_zip(zip_path, chars, min_len, max_len):
    zf = zipfile.ZipFile(zip_path)
    for L in range(min_len, max_len + 1):
        for pw_tuple in itertools.product(chars, repeat=L):
            pw = "".join(pw_tuple).encode()
            try:
                zf.extractall(pwd=pw)
                print("✅ 找到密码:", pw.decode())
                return
            except Exception:
                continue

# 主程序
if __name__ == "__main__":
    print("=== ZIP 工具箱 ===")
    print("1: 修复伪加密")
    print("2: CRC32 碰撞")
    print("3: 爆破密码")
    choice = input("请输入选项 > ")

    if choice == "1":
        src = input("请输入原ZIP文件路径: ")
        out = input("请输入修复后文件路径（如 fixed.zip）: ")
        fix_fake(src, out)

    elif choice == "2":
        crc = int(input("请输入CRC(0x...): "), 16)
        length = int(input("请输入长度: "))
        res = crc_reverse(crc, length)
        print(f"✅ 结果: {res}")
        if res:
            print(f"验证CRC: 0x{zlib.crc32(res) & 0xFFFFFFFF:08x}")

    elif choice == "3":
        path = input("请输入ZIP文件路径: ")
        brute_zip(path, "0123456789", 4, 6)

    else:
        print("❌ 选项无效")