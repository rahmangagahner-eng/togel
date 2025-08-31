#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BBFS 3D HYBRID v11.0
✅ Gabungan: 3D Terpanas + Run + Cycle + Dingin
✅ Prediksi 6 digit BBFS untuk tembus 3D
✅ Backtest otomatis
"""

import os
import json
import time
from collections import Counter
from typing import List, Tuple

# ──────────────────────────────────────────────────────────────
# Warna & Tampilan
# ──────────────────────────────────────────────────────────────
RESET = "\033[0m"

def colored(text: str, color: str = "white", style: str = "normal") -> str:
    styles = {"normal": 0, "bold": 1, "dim": 2}
    colors = {
        "red": 31, "green": 32, "yellow": 33, "blue": 34,
        "magenta": 35, "cyan": 36, "white": 37,
        "bright_red": 91, "bright_green": 92, "bright_yellow": 93,
        "bright_blue": 94, "bright_magenta": 95, "bright_cyan": 96,
    }
    s = styles.get(style, 0)
    c = colors.get(color, 37)
    return f"\033[{s};{c}m{text}{RESET}"

def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")

# ──────────────────────────────────────────────────────────────
# Banner
# ──────────────────────────────────────────────────────────────
BANNER = colored(r"""
   ____           _       _    ____ _  __
  / ___| ___ _ __| |_ ___| |  / ___| |/ /
 | |  _ / _ \ '__| __/ _ \ | | |   | ' / 
 | |_| |  __/ |  | ||  __/ | | |___| . \ 
  \____|\___|_|   \__\___|_|  \____|_|\_\
                                        
        🔮 BBFS 3D HYBRID v11.0
     Gabungan Terbaik: 3D Terpanas + Run + Cycle
""", "bright_cyan", "bold")

DATA_FILE = "sydney_lotto.json"

# ──────────────────────────────────────────────────────────────
# Load & Save Histori
# ──────────────────────────────────────────────────────────────
def load_history() -> List[str]:
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f).get("results", [])
    except:
        return []

def save_history(history: List[str]) -> None:
    with open(DATA_FILE, "w") as f:
        json.dump({"results": history}, f, indent=2)

# ──────────────────────────────────────────────────────────────
# Deteksi Pola Hybrid
# ──────────────────────────────────────────────────────────────
def deteksi_hybrid(history: List[str]) -> Dict[str, any]:
    if len(history) < 5:
        return {}

    # Ambil 3D: posisi 1,2,3 (ratusan, puluhan, satuan)
    all_3d = [res[1:] for res in history]
    ekors = [int(res[3]) for res in history]  # satuan
    digits = [d for res in history for d in res]

    pola = {}

    # 1. 3D Terpanas
    freq_3d = Counter(all_3d)
    pola["3d_hot"] = [pair for pair, _ in freq_3d.most_common(15)]

    # 2. Frekuensi digit di tiap posisi
    pos_ratusan = Counter([r[1] for r in history])
    pos_puluhan = Counter([r[2] for r in history])
    pos_satuan = Counter([r[3] for r in history])
    pola["pos_ratusan"] = [d for d, _ in pos_ratusan.most_common(4)]
    pola["pos_puluhan"] = [d for d, _ in pos_puluhan.most_common(4)]
    pola["pos_satuan"] = [d for d, _ in pos_satuan.most_common(4)]

    # 3. Run (Tren kenaikan/turun ekor)
    runs = [ekors[i] - ekors[i-1] for i in range(1, len(ekors))]
    avg_run = sum(runs) / len(runs) if runs else 0
    next_ekor = int((ekors[-1] + avg_run) % 10)
    pola["pred_ekor"] = str(next_ekor)

    # 4. Angka Dingin
    freq_digit = Counter(digits)
    pola["cold"] = [d for d, cnt in freq_digit.items() if cnt < 2]

    # 5. Cycle: deteksi ulang tiap 7-10 hari
    if len(history) >= 10:
        recent = history[-10:]
        cycle_3d = [r[1:] for r in recent]
        if len(set(cycle_3d)) < 8:  # stabil
            pola["cycle_stable"] = True
        else:
            pola["cycle_stable"] = False
    else:
        pola["cycle_stable"] = False

    return pola

# ──────────────────────────────────────────────────────────────
# Prediksi BBFS 6 Digit (Gabungan Hybrid)
# ──────────────────────────────────────────────────────────────
def generate_bbfs_hybrid(history: List[str]) -> Tuple[List[str], List[str]]:
    if len(history) < 10:
        return ["1", "2", "4", "5", "7", "8"], ["Data kurang"]

    pola = deteksi_hybrid(history)
    candidates = Counter()

    # 1. Dari 3D terpanas
    for t3 in pola["3d_hot"]:
        for d in t3:
            candidates[d] += 8

    # 2. Posisi kuat
    for d in pola["pos_ratusan"] + pola["pos_puluhan"] + pola["pos_satuan"]:
        candidates[d] += 6

    # 3. Prediksi ekor dari run
    if "pred_ekor" in pola:
        candidates[pola["pred_ekor"]] += 7

    # 4. Angka dingin
    for d in pola["cold"]:
        candidates[d] += 5

    # 5. Jika cycle stabil → ambil digit dari recent 3D
    if pola["cycle_stable"]:
        recent_digits = [d for r in history[-8:] for d in r[1:]]
        freq_recent = Counter(recent_digits)
        for d, _ in freq_recent.most_common(6):
            candidates[d] += 4

    # Ambil 6 digit terkuat
    top_6 = [item[0] for item in candidates.most_common(6)]
    alasan = [
        f"3D Panas: {len(pola['3d_hot'])} data",
        f"Posisi: R{pola['pos_ratusan'][:3]}, P{pola['pos_puluhan'][:3]}, S{pola['pos_satuan'][:3]}",
        f"Run: prediksi ekor {pola['pred_ekor']}",
        f"Dingin: {pola['cold']}",
        f"Cycle: {'Stabil' if pola['cycle_stable'] else 'Acak'}"
    ]

    return sorted(top_6, key=lambda x: int(x)), alasan

# ──────────────────────────────────────────────────────────────
# Backtest: Apakah 3D masuk BBFS?
# ──────────────────────────────────────────────────────────────
def backtest_hybrid(history: List[str]) -> None:
    if len(history) < 2:
        print(colored("\n❌ Butuh minimal 2 data!", "red"))
        input(colored("Enter...", "dim"))
        return

    tembus = 0
    total = len(history) - 1

    print(colored(f"\n🔍 BACKTEST: 3D dalam BBFS?", "bright_yellow", "bold"))

    for i in range(total):
        prev_batch = history[:i+1]
        actual = history[i+1]
        t3_actual = actual[1:]  # 3 digit terakhir
        d1, d2, d3 = t3_actual[0], t3_actual[1], t3_actual[2]

        bbfs, _ = generate_bbfs_hybrid(prev_batch)
        bbfs_set = set(bbfs)

        # Cek apakah ketiga digit ada di BBFS
        match = d1 in bbfs_set and d2 in bbfs_set and d3 in bbfs_set
        status = "✅" if match else "❌"

        if match:
            tembus += 1
        print(f"{status} {prev_batch[-1]} → {actual} | 3D: {t3_actual}")

    akurasi = (tembus / total) * 100
    warna = "green" if akurasi >= 70 else "yellow" if akurasi >= 50 else "red"
    print(colored(f"\n🎯 Akurasi 3D: {tembus}/{total} → {akurasi:.1f}%", warna, "bold"))
    input(colored("\nTekan Enter...", "dim"))

# ──────────────────────────────────────────────────────────────
# Animasi
# ──────────────────────────────────────────────────────────────
def loading():
    for _ in range(15):
        sys.stdout.write("\r" + colored("🧠", "cyan") + " Hybrid AI menganalisis...")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * 50 + "\r")

# ──────────────────────────────────────────────────────────────
# Menu
# ──────────────────────────────────────────────────────────────
def menu():
    while True:
        clear_screen()
        print(BANNER)
        history = load_history()
        print(colored(f"\n📁 Sydney Lotto: {len(history)} data", "blue", "dim"))
        print(colored("\n [1] Tambah Histori Manual", "cyan"))
        print(colored(" [2] Prediksi BBFS 6 Digit (Hybrid)", "bright_green"))
        print(colored(" [3] Backtest Otomatis", "bright_yellow"))
        print(colored(" [4] Hapus Data", "red"))
        print(colored(" [5] Keluar\n", "bright_red"))

        choice = input(colored("Pilih: ", "yellow")).strip()

        if choice == "1":
            print(colored("\nMasukkan 4D (kosongkan selesai):", "cyan"))
            added = 0
            while True:
                inp = input(f"Hasil {len(history) + added + 1}: ").strip()
                if not inp: break
                if inp.isdigit() and len(inp) == 4:
                    history.append(inp)
                    added += 1
                    print(colored("✓", "green"))
                else:
                    print(colored("✗ 4 digit!", "red"))
            if added > 0:
                save_history(history)

        elif choice == "2":
            if len(history) < 10:
                print(colored("\n⚠️ Butuh 10+ data!", "yellow"))
                input(colored("Enter...", "dim"))
                continue
            loading()
            bbfs, alasan = generate_bbfs_hybrid(history)
            clear_screen()
            print(BANNER)
            print(colored(f"\n🎯 BBFS 6 DIGIT (Hybrid AI):", "bright_magenta", "bold"))
            print(" → " + colored("  ".join(bbfs), "bright_yellow", "bold"))
            print(colored(f"\n💡 Alasan:", "dim"))
            for a in alasan:
                print(f"   • {a}")
            input(colored("\n\nEnter untuk kembali...", "dim"))

        elif choice == "3":
            backtest_hybrid(history)

        elif choice == "4":
            if input(colored("Hapus semua? (y/t): ", "red")).lower() == 'y':
                if os.path.exists(DATA_FILE):
                    os.remove(DATA_FILE)
                print(colored("🗑️ Dihapus", "green"))
                time.sleep(1)

        elif choice == "5":
            print(colored("\nSemoga 3D Anda tembus! 🍀", "bright_yellow"))
            break

        else:
            print(colored("Pilih 1-5!", "red"))
            input(colored("Enter...", "dim"))

# ──────────────────────────────────────────────────────────────
# Jalankan
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print(colored("\n\nDihentikan.", "red"))
