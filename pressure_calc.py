#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
气压计算工具 — 2D多项式标定 (传感器 24505322#)

用法:
    python pressure_calc.py              # 交互模式, 逐组输入
    python pressure_calc.py 62825 60345  # 单组计算
    python pressure_calc.py table        # 输出 x,y 参数表

公式:
    x = (f1 - 65000) / 3800
    y = (f2 - 59000) / 3700
    P = Σ k[i][j] * x^j * y^i

对标 C 代码: Drivers/BSP/pin/pressure_calc.c
"""

import sys

# =====================================================================
# 标定系数矩阵 (与 pressure_calc.c 完全一致)
# =====================================================================
K = [
    [ 661.933891,   628.383544,    19.318891,   -65.337509,   869.761164,  4363.371597],
    [-538.863937,   -11.107721,  -210.360991,  3472.179803, 22136.615546,          0.0],
    [ -31.061953,  -225.548104,  5228.960876, 45020.691682,          0.0,          0.0],
    [ -80.166787,  3521.446816, 45853.375261,          0.0,          0.0,          0.0],
    [ 894.836195, 23392.128518,          0.0,          0.0,          0.0,          0.0],
    [4781.604294,          0.0,          0.0,          0.0,          0.0,          0.0],
]

DELTA_PS1 = 65000.0
PS1       = 3800.0
DELTA_PS2 = 59000.0
PS2       = 3700.0


def calc_pressure(f1_hz, f2_hz):
    """单组频率 → 气压 (Hz 单位输入)"""
    x = (f1_hz - DELTA_PS1) / PS1
    y = (f2_hz - DELTA_PS2) / PS2

    # 预计算 x, y 各次幂
    xp = [1.0] * 6
    yp = [1.0] * 6
    for i in range(1, 6):
        xp[i] = xp[i - 1] * x
        yp[i] = yp[i - 1] * y

    result = 0.0
    for i in range(6):
        for j in range(6 - i):
            result += K[i][j] * xp[j] * yp[i]

    return result, x, y


# =====================================================================
# 命令行接口
# =====================================================================

def interactive():
    """交互模式: 逐组输入, 立即输出"""
    print("=" * 55)
    print("  气压计算工具 — 多项式标定 (24505322#)")
    print("=" * 55)
    print()
    print("  f1 f2        输入频率 (Hz), 空格分隔")
    print("  table        输出 xy 参数表")
    print("  quit / q     退出")
    print("  ?            帮助")
    print()

    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not line:
            continue

        if line.lower() in ('quit', 'q', 'exit'):
            break
        if line.lower() == 'table':
            show_table()
            continue
        if line == '?':
            print("  f1 f2 → 计算气压 | table → 参数表 | q → 退出")
            continue

        parts = line.split()
        if len(parts) >= 2:
            try:
                f1 = float(parts[0])
                f2 = float(parts[1])
            except ValueError:
                print(f"  错误: 无法解析 '{line}'")
                continue

            p, x, y = calc_pressure(f1, f2)
            print(f"  f1={f1:.3f}  f2={f2:.3f}  →  P = {p:.2f}")
        else:
            print(f"  格式错误: 需要两个数字 (f1 f2), 收到 '{line}'")


def show_table():
    """输出归一化参数参考表"""
    print()
    print("  归一化公式:")
    print("    x = (f1 - 65000) / 3800")
    print("    y = (f2 - 59000) / 3700")
    print()
    print("  f1 (Hz)      x           f2 (Hz)      y")
    print("  " + "-" * 44)
    for hz in [57000, 59000, 61000, 63000, 65000, 67000, 69000, 71000, 73000]:
        x = (hz - DELTA_PS1) / PS1
        y = (hz - DELTA_PS2) / PS2
        print(f"  {hz:>6}      {x:>+7.4f}      {hz:>6}      {y:>+7.4f}")
    print()
    print("  多项式: 21项 (i=0..5, j=0..5-i)")


def main():
    args = sys.argv[1:]

    if not args:
        interactive()
        return

    if args[0].lower() == 'table':
        show_table()
        return

    # 单组模式
    try:
        f1 = float(args[0])
        f2 = float(args[1])
    except (ValueError, IndexError):
        print(f"用法: {sys.argv[0]}  f1_hz  f2_hz")
        print(f"示例: {sys.argv[0]}  62825  60345")
        sys.exit(1)

    p, x, y = calc_pressure(f1, f2)
    print(f"f1  = {f1:.3f} Hz")
    print(f"f2  = {f2:.3f} Hz")
    print(f"x   = {x:.4f}")
    print(f"y   = {y:.4f}")
    print(f"P   = {p:.2f}")


if __name__ == '__main__':
    main()
