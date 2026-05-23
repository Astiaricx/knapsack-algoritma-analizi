# Knapsack Projesi - Ana Deney Dosyası
# DP ve GA algoritmalarını çalıştırır, sonuçları karşılaştırır ve grafikleri üretir

import os
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'DejaVu Sans'

from veri_uretici import rastgele_ornek_olustur, ornegi_kaydet
from dp_cozum    import knapsack_dp
from ga_cozum    import knapsack_ga

os.makedirs("data",    exist_ok=True)
os.makedirs("results", exist_ok=True)

BOYUTLAR = [100, 1000, 10000]
GA_POP   = 100
GA_NESIL = {100: 300, 1000: 300, 10000: 150}
TOHUM    = 42


# ---------- ADIM 1: Veri Üretimi ----------

print("=" * 55)
print("  ADIM 1: Veri Üretimi")
print("=" * 55)

ornekler = {}
for n in BOYUTLAR:
    yol   = f"data/knapsack_n{n}.json"
    ornek = rastgele_ornek_olustur(n, tohum=TOHUM)
    ornegi_kaydet(ornek, yol)
    ornekler[n] = ornek


# ---------- ADIM 2: Deneyleri Çalıştır ----------

print("\n" + "=" * 55)
print("  ADIM 2: Deney Sonuçları")
print("=" * 55)

sonuclar     = []
ga_gecmisler = {}

for n in BOYUTLAR:
    ornek   = ornekler[n]
    A, D, K = ornek["agirliklar"], ornek["degerler"], ornek["kapasite"]

    print(f"\n--- N = {n} ---")

    dp_deger, dp_sec, dp_sure = knapsack_dp(A, D, K)

    if dp_deger is None:
        print("  [DP]  Bellek limiti aşıldı — atlandı.")
        dp_deger, dp_sure = None, None
    else:
        print(f"  [DP]  Değer={dp_deger}  Süre={dp_sure:.4f}s  Seçilen={len(dp_sec)}")

    ga_deger, ga_sec, ga_sure, gecmis = knapsack_ga(
        A, D, K, pop_boyutu=GA_POP, nesil_sayisi=GA_NESIL[n], tohum=TOHUM
    )
    ga_gecmisler[n] = gecmis
    print(f"  [GA]  Değer={ga_deger}  Süre={ga_sure:.4f}s  Seçilen={len(ga_sec)}")

    # Accuracy Gap: GA'nın optimal çözümden yüzde kaç saptığı
    if dp_deger and dp_deger > 0:
        bosluk = round((dp_deger - ga_deger) / dp_deger * 100, 2)
        print(f"  Accuracy Gap: %{bosluk}")
    else:
        bosluk = None

    sonuclar.append({
        "n": n,
        "dp_deger": dp_deger, "dp_sure": dp_sure,
        "ga_deger": ga_deger, "ga_sure": ga_sure,
        "accuracy_gap": bosluk
    })


# ---------- ADIM 3: Sonuçları Kaydet ----------

class NpCeviri(json.JSONEncoder):
    """NumPy veri tiplerini JSON uyumlu hale getirir."""
    def default(self, obj):
        if isinstance(obj, np.integer): return int(obj)
        if isinstance(obj, np.floating): return float(obj)
        return super().default(obj)

with open("results/ozet.json", "w") as f:
    json.dump(sonuclar, f, indent=2, cls=NpCeviri)

print("\n[✓] Özet kaydedildi: results/ozet.json")


# ---------- ADIM 4: Grafikleri Oluştur ----------

print("\n[...] Grafikler oluşturuluyor...")

gecerli = [s for s in sonuclar if s["dp_sure"] is not None]
ns      = [s["n"]       for s in gecerli]
dp_s    = [s["dp_sure"] for s in gecerli]
ga_s    = [s["ga_sure"] for s in gecerli]
boslu   = [s["accuracy_gap"] for s in gecerli]

# Grafik 1: Çalışma Süresi Karşılaştırması
fig, ax = plt.subplots(figsize=(8, 5))
x = np.arange(len(ns))
g = 0.35
ax.bar(x - g/2, dp_s, g, label="DP", color="#2196F3", alpha=0.85)
ax.bar(x + g/2, ga_s, g, label="GA", color="#FF5722", alpha=0.85)
ax.set_xticks(x)
ax.set_xticklabels([f"N={n}" for n in ns])
ax.set_ylabel("Süre (saniye)")
ax.set_title("DP vs GA — Çalışma Süresi Karşılaştırması")
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("results/fig1_runtime_comparison.png", dpi=150)
plt.close()
print("  [✓] fig1_runtime_comparison.png")

# Grafik 2: Accuracy Gap
if any(b is not None for b in boslu):
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar([f"N={n}" for n in ns], boslu, color="#4CAF50", alpha=0.85)
    ax.set_ylabel("Accuracy Gap (%)")
    ax.set_title("GA'nın Optimal Çözümden Sapması (Accuracy Gap)")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("results/fig2_accuracy_gap.png", dpi=150)
    plt.close()
    print("  [✓] fig2_accuracy_gap.png")

# Grafik 3: GA Yakınsama Eğrisi
fig, ax = plt.subplots(figsize=(9, 5))
renkler = ["#1565C0", "#E65100", "#2E7D32"]
for i, n in enumerate(BOYUTLAR):
    if n in ga_gecmisler:
        ax.plot(ga_gecmisler[n], label=f"N={n}", color=renkler[i], linewidth=1.5)
ax.set_xlabel("Nesil (Generation)")
ax.set_ylabel("En İyi Değer")
ax.set_title("GA Yakınsama Eğrisi")
ax.legend()
ax.grid(linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig("results/fig3_ga_convergence.png", dpi=150)
plt.close()
print("  [✓] fig3_ga_convergence.png")


# ---------- ADIM 5: Özet Tablo ----------

print("\n" + "=" * 65)
print("  ÖZET TABLOSU")
print("=" * 65)
print(f"{'N':>8} | {'DP Değer':>10} | {'GA Değer':>10} | {'Gap%':>7} | {'DP Süre':>9} | {'GA Süre':>9}")
print("-" * 65)

for s in sonuclar:
    dp_d = str(s["dp_deger"]) if s["dp_deger"] else "—"
    dp_t = f"{s['dp_sure']:.4f}s" if s["dp_sure"] else "—"
    print(f"{s['n']:>8} | {dp_d:>10} | {s['ga_deger']:>10} | {str(s['accuracy_gap']):>6}% | {dp_t:>9} | {s['ga_sure']:.4f}s")

print("\n[✓] Tüm sonuçlar 'results/' klasörüne kaydedildi.")