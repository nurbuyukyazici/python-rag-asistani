\# Test Raporu — Python RAG Asistanı



\## Test Yöntemi

Sistem, 3 kategori altında farklı sorularla test edildi: dökümanda kesin bilgi bulunan sorular, kısmen ilgili/belirsiz sorular, ve tamamen alakasız sorular. Amaç, sistemin doğru bilgiyi bulup bulamadığını ve alakasız sorularda uydurma (halüsinasyon) yapmadan doğru şekilde reddedip reddetmediğini ölçmekti.



\## Sonuçlar



| Soru | Kategori | Benzerlik Skoru | Sonuç |

|---|---|---|---|

| GIL nedir? | Dökümanda var | 0.393 | Doğru cevaplandı |

| Virtual environment neden kullanılır? | Dökümanda var | 0.950 | Doğru cevaplandı |

| Tuple ile liste arasındaki fark nedir? | Dökümanda var | 1.219 | Doğru cevaplandı |

| List comprehension nedir? | Dökümanda var | Yüksek | Doğru cevaplandı |

| Python hızlı mı? | Belirsiz/kısmi | 0.385 | Doğru şekilde reddedildi |

| Bugün hava nasıl? | Alakasız | 0.228 | Doğru şekilde reddedildi |

| En iyi pizza tarifi nedir? | Alakasız | 0.250 | Doğru şekilde reddedildi |



\## Bulgular



\*\*Extractive yaklaşıma geçiş:\*\* Geliştirme sürecinde, üretici (generative) modelin (qwen3-1.7b) teknik konularda tutarsız ve bazen hatalı özetler ürettiği gözlemlendi. Bu riski ortadan kaldırmak için sistem, model yorumlaması yerine en alakalı kaynak paragrafı doğrudan sunan bir \*\*extractive\*\* yaklaşıma geçirildi. Bu değişiklik sonrası tüm testlerde doğru ve güvenilir sonuçlar alındı.



\*\*Hibrit arama:\*\* Yalnızca anlamsal (embedding tabanlı) aramanın bazı durumlarda yanlış paragrafı öne çıkardığı görüldü (örn. "GIL nedir?" sorusu başta yanlış bir paragrafla eşleşiyordu). Bunu düzeltmek için anahtar kelime eşleşme bonusu eklenerek hibrit bir arama sistemi oluşturuldu.



\*\*Benzerlik eşiği:\*\* 0.30 değerindeki eşik, geçerli soruları kabul edip alakasız soruları reddetme konusunda dengeli bir sonuç verdi.

