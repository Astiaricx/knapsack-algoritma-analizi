# Knapsack Projesi - Veri Üretici


import numpy as np
import json
import os


def rastgele_ornek_olustur(n, tohum=42):
    np.random.seed(tohum)
    agirliklar = np.random.randint(1, 50, size=n).tolist()
    degerler   = np.random.randint(1, 100, size=n).tolist()
    kapasite   = int(0.5 * sum(agirliklar))
    return {"n": n, "agirliklar": agirliklar, "degerler": degerler, "kapasite": kapasite}


def ornegi_kaydet(ornek, dosya_yolu):
    os.makedirs(os.path.dirname(dosya_yolu), exist_ok=True)
    with open(dosya_yolu, "w") as f:
        json.dump(ornek, f)
    print(f"[✓] Kaydedildi: {dosya_yolu}")


if __name__ == "__main__":
    boyutlar = [100, 1000, 10000]
    for n in boyutlar:
        ornek = rastgele_ornek_olustur(n, tohum=42)
        ornegi_kaydet(ornek, f"data/knapsack_n{n}.json")
        print(f"    N={n} → kapasite={ornek['kapasite']}, toplam_agirlik={sum(ornek['agirliklar'])}")