#!/usr/bin/env python3
"""
stop_loop_demo.py — 10 秒親眼看到「AI 知道什麼時候該停」的最小閉迴路示範
========================================================================
零第三方套件、零領域知識，直接用 Python 標準庫示範：
  1. 案例一（階乘 factorial 邊界錯誤）：
     故意埋一個 `factorial(0)` 回傳 `0` 的錯 ➔ 第 1 步抓到邊界失敗 ➔ 第 2 步修正通過 ➔ 立即自己收手停機。
  2. 案例二（字串反轉 reverse_text 代理死胡同）：
     故意給一個矛盾條件讓修改沒有進展 ➔ 連續 2 步沒有淨推進 ➔ 外部煞車自動喊停，不空燒額度。
"""
from __future__ import annotations

import argparse
import sys
import time
from typing import Callable, List, Tuple


def test_factorial_suite(fn: Callable[[int], int]) -> Tuple[int, int, List[str]]:
    cases = [
        (5, 120, "一般正整數 factorial(5) == 120"),
        (1, 1, "最小正整數 factorial(1) == 1"),
        (0, 1, "邊界條件 factorial(0) == 1"),
    ]
    passed = 0
    errors: List[str] = []
    for n, expected, label in cases:
        try:
            actual = fn(n)
        except Exception as exc:
            errors.append(f"{label} -> 發生例外：{exc}")
            continue
        if actual == expected:
            passed += 1
        else:
            errors.append(f"{label} -> 預期 {expected}，實測拿到 {actual}")
    return passed, len(cases), errors


def candidate_step_1_buggy(n: int) -> int:
    # 故意埋錯：漏掉 n == 0 時應回傳 1，導致 factorial(0) 回傳 0
    if n < 0:
        raise ValueError("n 不可為負數")
    return n * candidate_step_1_buggy(n - 1) if n > 1 else n


def candidate_step_2_fixed(n: int) -> int:
    # 修正邊界條件：n <= 1 時回傳 1
    if n < 0:
        raise ValueError("n 不可為負數")
    return 1 if n <= 1 else n * candidate_step_2_fixed(n - 1)


def run_demo(delay: float = 0.35) -> int:
    print("====================================================================")
    print("【示範 1】寫一個階乘函式 factorial(n)（故意埋 n=0 的邊界條件錯誤）")
    print("====================================================================")
    candidates = [
        ("第 1 步（初稿）", candidate_step_1_buggy, "if n > 1: return n * f(n-1) else: return n"),
        ("第 2 步（修正邊界）", candidate_step_2_fixed, "if n <= 1: return 1 else: return n * f(n-1)"),
        ("第 3 步（備用）", candidate_step_2_fixed, "不會執行到這一步，因為第 2 步已經自己停了"),
    ]

    prev_passed = 0
    zero_gain_streak = 0
    for idx, (title, fn, snippet) in enumerate(candidates, start=1):
        time.sleep(delay)
        passed, total, errors = test_factorial_suite(fn)
        gain = passed - prev_passed
        prev_passed = max(prev_passed, passed)
        print(f"\n▶ {title}")
        print(f"  程式碼：{snippet}")
        print(f"  測試結果：{passed}/{total} 通過（本步推進：{gain:+d}）")
        for err in errors:
            print(f"  ❌ 抓到問題：{err}")

        if passed == total:
            print("\n🛑 [它自己停了！] 外部檢查確認 3/3 測試全數通過。")
            print(f"   總共只跑 {idx} 步就自動收手，不繼續多燒半步額度。\n")
            break

        if gain <= 0:
            zero_gain_streak += 1
            if zero_gain_streak >= 2:
                print("\n🛑 [它自己停了！] 連續 2 步沒有推進，自動拉下煞車。\n")
                break
        else:
            zero_gain_streak = 0

    print("====================================================================")
    print("【示範 2】字串反轉 reverse_text(s) 遇到死胡同時，幾步內自動收手？")
    print("====================================================================")
    print("  情境：如果測試環境卡住、或修改方向連續 2 步都沒讓通過數增加：")
    simulated_scores = [
        ("第 1 步（嘗試修改 A）", 2, 3, "卡在空白字元邊界條件（通過 2/3）"),
        ("第 2 步（嘗試修改 B）", 2, 3, "依然卡在同一題（通過 2/3，推進 +0）"),
        ("第 3 步（嘗試修改 C）", 2, 3, "依然卡在同一題（通過 2/3，推進 +0）"),
    ]
    best = 2
    no_progress = 0
    for step_label, score, total, note in simulated_scores:
        time.sleep(delay)
        gain = score - best
        if score > best:
            best = score
            no_progress = 0
        else:
            no_progress += 1
        print(f"  ▶ {step_label}：{note}")
        if no_progress >= 2:
            print("\n🛑 [它自己停了！] 偵測到連續 2 步沒有實質推進，自動收手並回報卡關原因。")
            print("   不會像沒人管的 AI 一樣原地轉圈圈跑完 200 步把你的額度燒光。")
            break

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="最小閉迴路「它知道何時該停」終端機示範")
    parser.add_argument("--fast", action="store_true", help="零延遲立即印出完整輸出")
    args = parser.parse_args()
    return run_demo(delay=0.0 if args.fast else 0.35)


if __name__ == "__main__":
    raise SystemExit(main())
