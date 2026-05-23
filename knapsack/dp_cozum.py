# Knapsack Projesi - Dinamik Programlama Çözümü
# Zaman Karmaşıklığı: O(n x W)
# Alan Karmaşıklığı: O(n x W)

import json
import time
import sys


def knapsack_dp(agirliklar, degerler, kapasite):
    n = len(agirliklar)

    # Tablo boyutu 500 MB'ı aşacaksa bellek taşmasını önlemek için erken çık
    tahmini_mb = (n * kapasite * 8) / (1024 ** 2)
    if tahmini_mb > 500:
        print(f"  [!] Uyarı: DP tablosu ~{tahmini_mb:.0f} MB olacak, atlanıyor.")
        return None, [], -1

    baslangic = time.perf_counter()

    # (n+1) x (kapasite+1) boyutunda DP tablosu, başlangıçta sıfır
    dp = [[0] * (kapasite + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        a = agirliklar[i - 1]
        d = degerler[i - 1]
        for c in range(kapasite + 1):
            if a <= c:
                # Bu eşyayı al veya alma, hangisi daha iyiyse seç
                dp[i][c] = max(dp[i - 1][c], dp[i - 1][c - a] + d)
            else:
                # Eşya kapasiteye sığmıyor, almadan devam et
                dp[i][c] = dp[i - 1][c]

    # Tabloyu geriye doğru izleyerek seçilen eşyaları bul
    secilen = []
    c = kapasite
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i - 1][c]:
            secilen.append(i - 1)
            c -= agirliklar[i - 1]

    gecen_sure = time.perf_counter() - baslangic
    return dp[n][kapasite], secilen[::-1], gecen_sure


def ornegi_yukle(dosya_yolu):
    with open(dosya_yolu) as f:
        return json.load(f)


if __name__ == "__main__":
    import os
    boyutlar = [100, 1000, 10000]

    for n in boyutlar:
        yol = f"data/knapsack_n{n}.json"
        if not os.path.exists(yol):
            print(f"[!] {yol} bulunamadı. Önce data_generator.py çalıştır.")
            continue

        ornek = ornegi_yukle(yol)
        print(f"\n--- N={n} ---")

        en_iyi, secilen, sure = knapsack_dp(
            ornek["agirliklar"], ornek["degerler"], ornek["kapasite"]
        )

        if en_iyi is None:
            print("  DP bellek limitini aştı, atlandı.")
        else:
            print(f"  Optimal Değer : {en_iyi}")
            print(f"  Seçilen Eleman: {len(secilen)}")
            print(f"  Süre          : {sure:.4f} saniye")