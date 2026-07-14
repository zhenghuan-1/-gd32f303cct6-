#!/usr/bin/env python3
"""校验和计算器 — 输入帧内容(不含\r和校验和)，输出完整帧"""

import sys

def calc_checksum(s):
    """计算 XOR 校验和: # 到 \r (含)"""
    full = s + '\r'  # 加上帧尾
    ck = 0
    for b in full.encode('ascii'):
        ck ^= b
    return ck

if len(sys.argv) > 1:
    # 命令行模式
    cmd = sys.argv[1]
else:
    # 交互模式
    cmd = input("输入帧内容 (不含\\r和校验和, 例: #0100P3): ").strip()

if cmd:
    if not cmd.startswith('#'):
        cmd = '#' + cmd

    ck = calc_checksum(cmd)
    result = cmd + '\r' + f'{ck:02X}'
    hex_str = ' '.join(f'{b:02X}' for b in result.encode('ascii'))

    print()
    print(f"完整帧: {result}")  # \r 不可见但包含
    print(f"HEX:    {hex_str}")
    print(f"校验和: {ck:02X}")
else:
    print("用法: python checksum.py '#0100P3'")
    print("或直接运行, 输入帧内容")
