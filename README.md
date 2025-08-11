İnme Tespiti İçin Derin Öğrenme Modelleri
Bu proje, Sağlık Bakanlığı tarafından sağlanan TEKNOFEST 2021 veri seti kullanılarak, bilgisayarlı tomografi (BT) beyin görüntülerinden inme (stroke) tespiti yapmak amacıyla geliştirilmiştir. Projede dört farklı derin öğrenme modeli tasarlanmış, eğitilmiş ve karşılaştırılmıştır:

VGG16: Önceden eğitilmiş ağırlıklarla transfer öğrenme uygulanmış, üstüne özel sınıflandırıcılar eklenerek ince ayar yapılmıştır.

CBAM-ResNet18: Kanal ve uzaysal dikkat mekanizmalarını içeren CBAM modülü ile desteklenen ResNet18 mimarisi kullanılmıştır.

DenseNet121: Katmanlar arası yoğun bağlantılar sayesinde güçlü özellik çıkarımı sağlayan model fine-tuning ile optimize edilmiştir.

CNN + LSTM + PSO: Uzamsal özellikleri çıkaran CNN ile zaman serisi bağıntılarını öğrenen LSTM katmanlarının birleşimi. Model hiperparametreleri, Parçacık Sürü Optimizasyonu (PSO) ile otomatik olarak optimize edilmiştir.

Veri Seti ve Ön İşleme
Toplamda 6781 DICOM formatındaki BT kesiti, 2227'si inme var, 4554'ü inme yok sınıfında.

DICOM dosyalar, pydicom kütüphanesi ile okunup Hounsfield Unit (HU) dönüşümü uygulanarak PNG formatına çevrilmiştir.

Her görüntü, kendi özel window level (WL) ve window width (WW) değerlerine göre kontrast optimize edilmiştir.

Kemik ve gereksiz bölgeler morfolojik işlemlerle filtrelenmiş, yalnızca beyin dokusu korunmuştur.

Görüntüler 224x224 boyutuna ölçeklendirilmiş ve piksel değerleri [0,1] aralığında normalleştirilmiştir.

Veri artırma teknikleri (döndürme, yatay çevirme, yakınlaştırma, kontrast artırma) sınıf dengesizliğini gidermek için uygulanmıştır.

Veri, %70 eğitim, %15 doğrulama ve %15 test olacak şekilde stratified sampling yöntemiyle bölünmüştür.

Model Eğitimi ve Optimizasyon
Tüm modeller Adam optimizasyon algoritması ve binary crossentropy kayıp fonksiyonu kullanılarak eğitilmiştir.

Erken durdurma (Early Stopping) ve öğrenme oranı azaltma (ReduceLROnPlateau) teknikleri uygulanmıştır.

CNN+LSTM modelinin LSTM katman sayısı, dropout oranı ve öğrenme oranı PSO algoritması ile optimize edilmiştir.

Eğitim batch size 64, epoch sayısı 50 olarak belirlenmiş, aşırı öğrenme engellenmiştir.

Performans ve Sonuçlar
Model	Accuracy	Precision	Recall	F1-Score
VGG16	0.8946	0.8912	0.8925	0.8909
CBAM-ResNet18	0.9679	0.9651	0.9754	0.9708
DenseNet121	0.9870	0.9810	0.9832	0.9830
CNN+LSTM+PSO	0.9630	0.9623	0.9657	0.9617

Model performansları, doğruluk, precision, recall ve F1-score ile değerlendirilmiştir.

CNN+LSTM+PSO modeli, zaman serisi verisini de işleyerek dengeli ve hızlı sonuçlar sunmuştur.

Modellemenin genellenebilirliği, farklı bir dış veri seti (Brain Stroke CT Image Dataset) ile test edilmiştir.

Proje süresince karşılaşılan zorluklar arasında DICOM’dan PNG’ye dönüşüm, kemik çıkarma işlemleri ve büyük veri seti ile çalışma yer almaktadır. Bu sorunlar özel algoritmalar ve bulut tabanlı çözümlerle aşılmıştır.

