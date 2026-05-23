# Knapsack Probleminde DP vs Genetik Algoritma

**Manisa Celal Bayar Üniversitesi — Yazılım Mühendisliği Bölümü**  
**Algoritma Analizi ve Tasarımı Dersi — 2025-2026 Bahar Dönemi**  
**Abdullah Durgun, Mustafa Yaşar Eroğlu**

---

## Proje Hakkında

Bu projede 0/1 Sırt Çantası Problemi (Knapsack Problem) üzerinde iki farklı algoritma karşılaştırılmıştır:

- **Dinamik Programlama (DP):** Kesin ve optimal çözüm üretir, büyük problemlerde bellek yetersizliği yaşar.
- **Genetik Algoritma (GA):** Sezgisel yaklaşım, tüm problem boyutlarında çalışır ancak optimal çözümü garanti etmez.

## Dosyalar

| Dosya | Açıklama |
|---|---|
| `veri_uretici.py` | Sentetik veri üretimi |
| `dp_cozum.py` | Dinamik Programlama çözümü |
| `ga_cozum.py` | Genetik Algoritma çözümü |
| `main.py` | Tüm deneyleri çalıştırır, grafikleri üretir |
| `bildiri.tex` | LaTeX akademik bildiri |

## Kurulum ve Çalıştırma

```bash
pip install numpy matplotlib
python ana_deney.py
```

## Sonuçlar

| N | DP Değer | GA Değer | Sapma | DP Süre | GA Süre |
|---|---|---|---|---|---|
| 100 | 4065 | 4056 | %0.22 | 0.05s | 1.56s |
| 1000 | 40397 | 31937 | %20.94 | 6.26s | 2.76s |
| 10000 | — (bellek taştı) | 273119 | — | — | 5.96s |
