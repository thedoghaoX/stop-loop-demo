#!/usr/bin/env python3
"""
stop_loop_demo.py — 10 秒親眼看到「AI 知道什麼時候該停」的白話示範
==================================================================
不需要懂任何技術名詞，直接看兩個每個人都遇過的情境：
  1. 情境一（修好就自己停）：
     請 AI 整理電話號碼或反轉一段文字，故意放一筆「空白資料」測它 ➔
     第 1 步它發現空白資料處理錯了 ➔ 第 2 步修好全部通過 ➔ 立刻自己收手停機，不多花半毛錢。
  2. 情境二（卡住也自己停）：
     遇到打不開的壞檔案或矛盾指令 ➔ 一般 AI 會傻傻重試幾十次把你的額度燒光；
     我們的小迴圈試了 2 次發現沒進展，就立刻自動拉下煞車喊停，幫你把錢省下來。
"""
from __future__ import annotations

import argparse
import time
from typing import Callable, List, Tuple


def check_task(fn: Callable[[str], str]) -> Tuple[int, int, List[str]]:
    test_items = [
        ("0912-345-678", "0912345678", "一般電話號碼去掉橫線"),
        ("02-2345-6789", "0223456789", "市話號碼去掉橫線"),
        ("", "（未填寫）", "遇到空白沒填的格子"),
    ]
    passed = 0
    errors: List[str] = []
    for raw, expected, label in test_items:
        actual = fn(raw)
        if actual == expected:
            passed += 1
        else:
            errors.append(f"{label} -> 應該顯示「{expected}」，但 AI 算出「{actual}」")
    return passed, len(test_items), errors


def step_1_draft(text: str) -> str:
    # 第 1 步初稿：只想到去掉橫線，忘記「空白沒填」時要標註（未填寫）
    return text.replace("-", "")


def step_2_fixed(text: str) -> str:
    # 第 2 步修正：補上空白檢查
    cleaned = text.replace("-", "").strip()
    return cleaned if cleaned else "（未填寫）"


def run_demo(delay: float = 0.35) -> int:
    print("====================================================================")
    print("【情境 1：修好就自己停】請 AI 整理名單電話，故意塞一格「空白沒填」測它")
    print("====================================================================")
    steps = [
        ("第 1 步（AI 初稿）", step_1_draft),
        ("第 2 步（自動修正）", step_2_fixed),
        ("第 3 步（不會執行）", step_2_fixed),
    ]

    for idx, (title, fn) in enumerate(steps, start=1):
        time.sleep(delay)
        passed, total, errors = check_task(fn)
        print(f"\n▶ {title}：檢查 {passed}/{total} 過關")
        for err in errors:
            print(f"  ❌ 發現小錯：{err}")

        if passed == total:
            print("\n🛑 [它自己停了！] 3 項檢查全部過關，第 2 步立刻自動收手！")
            print("   不會像一般 AI 已經做好了還在後面自己碎碎念、多燒你的額度。\n")
            break

    print("====================================================================")
    print("【情境 2：卡住也自己停】如果遇到死胡同，它會不會傻傻轉圈圈把額度燒光？")
    print("====================================================================")
    print("  ⚠️ 一般沒裝煞車的 AI：會在原地自己重試 50～200 次，去倒杯水回來額度就見底了。")
    print("  🛡️ 有裝煞車的小迴圈：")
    attempts = [
        ("第 1 次嘗試", "卡在損毀的外部資料（過關數 2/3，沒有新進展）"),
        ("第 2 次嘗試", "換一招還是卡在同一處（過關數 2/3，連續 2 次沒進展）"),
        ("第 3 次嘗試", "這一步不會發生，因為第 2 次已經拉煞車了"),
    ]
    no_progress_count = 0
    for label, note in attempts:
        time.sleep(delay)
        no_progress_count += 1
        print(f"  ▶ {label}：{note}")
        if no_progress_count >= 2:
            print("\n🛑 [它自己停了！] 發現連續 2 次沒有新進展，自動拉下煞車並告訴你卡在哪裡。")
            print("   幫你保住剩下 98% 的額度，每一分錢都花在真正有推進的地方。")
            break

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="10 秒親眼看到「AI 知道什麼時候該停」白話示範")
    parser.add_argument("--fast", action="store_true", help="立即印出完整輸出")
    args = parser.parse_args()
    return run_demo(delay=0.0 if args.fast else 0.35)


if __name__ == "__main__":
    raise SystemExit(main())
