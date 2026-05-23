# Knapsack Projesi - Genetik Algoritma Çözümü
# Operatörler: Tek noktalı çaprazlama, bit-flip mutasyon, turnuva seçimi

import json
import time
import numpy as np
import os


def uygunluk(kromozom, agirliklar, degerler, kapasite):
    toplam_agirlik = np.dot(kromozom, agirliklar)
    toplam_deger   = np.dot(kromozom, degerler)
    # Kapasite aşılıyorsa birey geçersiz sayılır
    if toplam_agirlik > kapasite:
        return 0
    return toplam_deger


def populasyon_olustur(pop_boyutu, n, agirliklar, kapasite, rng):
    populasyon = []
    for _ in range(pop_boyutu):
        birey = rng.integers(0, 2, size=n)
        # Kapasite aşılıyorsa rastgele eşya çıkararak tamir et
        while np.dot(birey, agirliklar) > kapasite:
            birler = np.where(birey == 1)[0]
            if len(birler) == 0:
                break
            birey[rng.choice(birler)] = 0
        populasyon.append(birey)
    return np.array(populasyon)


def turnuva_secimi(populasyon, uygunluklar, k=3, rng=None):
    # k aday arasından en yüksek uygunluktaki bireyi seç
    indisler = rng.choice(len(populasyon), size=k, replace=False)
    en_iyi   = indisler[np.argmax(uygunluklar[indisler])]
    return populasyon[en_iyi].copy()


def tek_nokta_caprazlama(ebeveyn1, ebeveyn2, rng):
    nokta  = rng.integers(1, len(ebeveyn1))
    yavru1 = np.concatenate([ebeveyn1[:nokta], ebeveyn2[nokta:]])
    yavru2 = np.concatenate([ebeveyn2[:nokta], ebeveyn1[nokta:]])
    return yavru1, yavru2


def bit_flip_mutasyon(kromozom, mutasyon_orani, rng):
    # Her bit için verilen olasılıkla 0→1 veya 1→0 çevir
    maske = rng.random(len(kromozom)) < mutasyon_orani
    return np.where(maske, 1 - kromozom, kromozom)


def tamir_et(kromozom, agirliklar, kapasite, rng):
    # Kapasite aşımını rastgele eşya çıkararak gider
    birey = kromozom.copy()
    while np.dot(birey, agirliklar) > kapasite:
        birler = np.where(birey == 1)[0]
        if len(birler) == 0:
            break
        birey[rng.choice(birler)] = 0
    return birey


def knapsack_ga(agirliklar, degerler, kapasite,
                pop_boyutu=100, nesil_sayisi=300,
                caprazlama_orani=0.8, mutasyon_orani=0.02,
                tohum=42):
    """
    Döndürür: (en iyi değer, seçilen indeksler, toplam süre, nesil geçmişi)
    """
    n   = len(agirliklar)
    rng = np.random.default_rng(tohum)

    agirlik_dizi = np.array(agirliklar)
    deger_dizi   = np.array(degerler)

    baslangic  = time.perf_counter()
    populasyon = populasyon_olustur(pop_boyutu, n, agirlik_dizi, kapasite, rng)

    en_iyi_birey = None
    en_iyi_deger = 0
    gecmis       = []  # Yakınsama grafiği için her neslin en iyi değeri

    for nesil in range(nesil_sayisi):
        uygunluklar = np.array([
            uygunluk(birey, agirlik_dizi, deger_dizi, kapasite) for birey in populasyon
        ])

        # Elitizm: bu neslin en iyisi genel en iyiden daha iyi ise güncelle
        nesil_en_iyi = np.argmax(uygunluklar)
        if uygunluklar[nesil_en_iyi] > en_iyi_deger:
            en_iyi_deger = uygunluklar[nesil_en_iyi]
            en_iyi_birey = populasyon[nesil_en_iyi].copy()

        gecmis.append(en_iyi_deger)

        # Yeni nesil üret; en iyi bireyi doğrudan aktar (elitizm)
        yeni_populasyon = [en_iyi_birey.copy()]

        while len(yeni_populasyon) < pop_boyutu:
            e1 = turnuva_secimi(populasyon, uygunluklar, k=3, rng=rng)
            e2 = turnuva_secimi(populasyon, uygunluklar, k=3, rng=rng)

            if rng.random() < caprazlama_orani:
                y1, y2 = tek_nokta_caprazlama(e1, e2, rng)
            else:
                y1, y2 = e1.copy(), e2.copy()

            y1 = bit_flip_mutasyon(y1, mutasyon_orani, rng)
            y2 = bit_flip_mutasyon(y2, mutasyon_orani, rng)

            y1 = tamir_et(y1, agirlik_dizi, kapasite, rng)
            y2 = tamir_et(y2, agirlik_dizi, kapasite, rng)

            yeni_populasyon.extend([y1, y2])

        populasyon = np.array(yeni_populasyon[:pop_boyutu])

    gecen_sure = time.perf_counter() - baslangic
    secilen    = list(np.where(en_iyi_birey == 1)[0]) if en_iyi_birey is not None else []
    return en_iyi_deger, secilen, gecen_sure, gecmis


def ornegi_yukle(dosya_yolu):
    with open(dosya_yolu) as f:
        return json.load(f)


if __name__ == "__main__":
    boyutlar = [100, 1000, 10000]

    for n in boyutlar:
        yol = f"data/knapsack_n{n}.json"
        if not os.path.exists(yol):
            print(f"[!] {yol} bulunamadı.")
            continue

        ornek = ornegi_yukle(yol)
        print(f"\n--- N={n} ---")

        # Büyük problemlerde nesil sayısını azalt
        nesil = 300 if n <= 1000 else 150

        en_iyi, secilen, sure, gecmis = knapsack_ga(
            ornek["agirliklar"], ornek["degerler"], ornek["kapasite"],
            pop_boyutu=100, nesil_sayisi=nesil
        )

        print(f"  GA Bulunan Değer : {en_iyi}")
        print(f"  Seçilen Eleman   : {len(secilen)}")
        print(f"  Süre             : {sure:.4f} saniye")