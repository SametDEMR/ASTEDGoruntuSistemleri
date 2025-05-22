#23ttg5hackathon2025

# Göz Pedi Hata Tespit Sistemi
Bu proje, üretim sonrası göz pedlerinin yapısal doğruluğunu kontrol etmek amacıyla geliştirilmiş bir görüntü işleme tabanlı kalite kontrol sistemidir. Sistem, göz pedlerinde oluşabilecek yırtık, deformasyon, leke ve renk değişimleri gibi kusurları tespit eder ve kullanıcı tarafından belirlenen tolerans değerlerine göre ürünü kabul eder veya eler.

Bu projede kullanılan detect_defects_by_diff fonksiyonu, iki görüntü arasındaki yapısal farkları (defektleri) tespit eder. Aşağıda algoritmanın *model adımlarına göre* zaman ve mekân karmaşıklıkları sunulmuştur.


##  Karmaşıklık Notasyonu Zorunluluğu (Big-O)

| Adım | Zaman Karmaşıklığı (O) | Mekân Karmaşıklığı (O) |
|------|-------------------------|--------------------------|
| Görüntü Okuma (cv2.imread) | O(N) | O(N) |
| Yeniden Boyutlandırma (cv2.resize) | O(N) | O(N) |
| Histogram Eşitleme (cv2.equalizeHist) | O(N) | O(N) |
| Mutlak Fark (cv2.absdiff) | O(N) | O(N) |
| İkili Eşikleme (cv2.threshold) | O(N) | O(N) |
| Morfolojik Kapanış (cv2.morphologyEx) | O(N) | O(N) |
| Nesne Maskesi Oluşturma | O(N) | O(N) |
| Maskeyi Erozyonla Kırpma (cv2.erode) | O(N) | O(N) |
| Maskeyle Temizleme (cv2.bitwise_and) | O(N) | O(N) |
| Kontur Bulma (cv2.findContours) | O(N) | O(N) |
| Kontur Filtreleme ve Çizim | O(N) | O(1) |

##  Açıklama

- *N*: İşlenen görüntüdeki toplam piksel sayısıdır.
- Tüm işlemler, sabit çekirdek boyutları ve sabit sayıda geçiş (iterations) içerdiğinden, genel algoritma *lineer zaman ve mekân karmaşıklığına* sahiptir.
- Bu sayede yüksek çözünürlüklü görüntülerle çalışırken dahi algoritma performansı öngörülebilir ve optimize edilebilirdir.

##  Model Doğruluğu
| Metrik                  | Değer                                                        |
| ----------------------- | ------------------------------------------------------------ |
| **Doğruluk (Accuracy)** | **%76.00**                                                   |
| Test Koşulları          | Genişletilmiş simülasyon veri seti üzerinde test edilmiştir. |
| Hedef                   | Leke, deformasyon ve yırtık hatalarının tespiti              |

##  Gerçek Zamanlı Performans
| Platform              | Ortalama FPS                                          | Açıklama                                      |
| --------------------- | ----------------------------------------------------- | --------------------------------------------- |
| Bilgisayar (Test Cihazı) | **2.66 FPS**                                          | Giriş görüntüsü işleme süresi baz alınmıştır. |


## Simülasyon Ortamı
Projenin simülasyon ortamı, hasarlı göz pedi görsellerinin oluşturulması ve görüntü işleme algoritmalarının test edilmesi amacıyla Jupyter Notebook üzerinde çalışmaktadır.

## Kurulum ve Çalıştırma
Aşağıdaki Python kütüphanelerinin yüklü olduğundan emin olun:
opencv-python numpy matplotlib
notebooks/simulation.ipynb dosyasını Jupyter ortamında açarak çalıştırabilirsiniz.

Simülasyon, belirli hasar tiplerini (leke, yırtık, deformasyon) rastgele uygulayarak eğitim verisi üretir ve bu veriler üzerinde hata tespiti gerçekleştirir.

! Simülasyon sadece görsel işleme mantığını test eder, mobil uygulamayla şu anda entegre değildir.

### Mobil Uygulama
Mobil uygulama, gerçek zamanlı görüntü alarak hata tespiti yapan Android tabanlı bir prototiptir. Şu an için yalnızca geliştirici cihazında bilgisayara bağlı (debug modunda) çalıştırılmaktadır.

#### Geçici Kurulum (Debug)
-Android Studio ile proje klasörünü açın.

-Bağlı bir Android cihazda USB hata ayıklama (USB Debugging) aktif olmalıdır.

-Uygulama, MainActivity.java üzerinden başlatılabilir.

-Kamera görüntüsü alınıp OpenCV ile işlenerek sonuçlar gösterilir.

! Henüz bağımsız APK olarak dağıtım yapılmamıştır. Gerçek cihazda test için bilgisayar bağlantısı gereklidir.
                                        
