\# Kurulum Rehberi



Bu rehber, projeyi sıfırdan başka bir Windows bilgisayarda çalıştırmak için gereken adımları anlatır.



\## Gereksinimler



\- Windows 10/11

\- Python 3.11 veya üzeri

\- En az 4 GB boş disk alanı (modeller için)

\- Microsoft Foundry Local



\## Adım 1: Foundry Local Kurulumu



PowerShell'i yönetici olarak açıp şunu çalıştırın:

winget install Microsoft.FoundryLocal





Kurulumu doğrulayın:



foundry --version





\## Adım 2: Projeyi İndirme



git clone https://github.com/nurbuyukyazici/python-rag-asistani.git

cd python-rag-asistani





\## Adım 3: Python Bağımlılıklarını Kurma



pip install -r requirements.txt





\## Adım 4: Uygulamayı Başlatma



python app.py





İlk çalıştırmada embedding modeli otomatik olarak indirilecektir (yaklaşık 500 MB, birkaç dakika sürebilir).



\## Adım 5: Kullanma



Tarayıcıda şu adrese gidin:



http://localhost:5000





\## Sık Karşılaşılan Sorunlar



\*\*"foundry komutu tanınmıyor" hatası:\*\* PowerShell'i kapatıp yeniden açın, PATH güncellemesi için yeniden başlatma gerekebilir.



\*\*Model indirme hatası:\*\* İnternet bağlantınızı kontrol edin, ilk indirme internet gerektirir (sonraki çalıştırmalar tamamen yerel çalışır).



\*\*Port 5000 kullanımda hatası:\*\* `app.py` dosyasındaki `port=5000` değerini başka bir port numarasıyla (örn. 5001) değiştirin.



.

