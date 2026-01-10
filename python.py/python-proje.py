#İskonto; bir mal veya hizmetin liste fiyatı üzerinden yapılan indirimdir.
# Belirli bir süre ve faiz oranı için iskonto faktörünü (v^n) hesaplama
def iskonto_faktoru_hesapla(faiz_orani, sure):
    v = 1 / (1 + faiz_orani)
    return v ** sure

#Bir sigorta şirketinin 10 yıl sonra kesin olarak 1.000.000 TL ödeme yapacağını varsayalım.
# Şirketin bu yükümlülüğü karşılamak için bugün kenara ne kadar para koyması gerektiğini farklı faiz oranlarıyla test edelim.
gelecekteki_tutar = 1000000  # 1 Milyon TL
sure = 10                     # Yıl
# Farklı teknik faiz oranları için bugünkü değer analizi
faiz_oranlari = [0.03, 0.05, 0.10] # %3, %5 ve %10

print(f"{'Faiz Oranı':<12} | {'İskonto Faktörü (v^10)':<25} | {'Bugünkü Değer (PV)':<20}")
print("-" * 65)

for r in faiz_oranlari:
    # Fonksiyonun çağrılması
    v_n = iskonto_faktoru_hesapla(r, sure)
    bugunku_deger = gelecekteki_tutar * v_n
    
    print(f"%{r*100:<10.0f} | {v_n:<25.6f} | {bugunku_deger:>15,.2f} TL")


# x yaşındaki birinin n yıl daha yaşama olasılığını (npx) hesaplama.
def hayatta_kalma_olasiligi(yas, sure, mortalite_tablosu):
    lx = mortalite_tablosu[yas]
    lx_n = mortalite_tablosu[yas + sure]
    return lx_n / lx

# ilk önce Örnek Bir Mortalite Tablosu (lx) Oluşturalım
# Bu tablo, her yaşta kaç kişinin hayatta kaldığını gösterir.
# (Gerçek hayatta TRH-2010 veya CSO-2001 gibi tablolar kullanılır)
mortalite_tablosu = {
    30: 95000,   # 30 yaşında 95.000 kişi hayatta
    35: 94200,
    40: 93000,
    50: 89000,
    60: 80000,
    65: 72000    # 65 yaşında 72.000 kişi hayatta
}
#30 yaşındaki birinin 65 yaşına kadar yaşama olasılığını bulalım
yas_baslangic = 30
sure = 35 # 65 yaşına kadar olan süre (65 - 30)

# Olasılığı hesaplayalım
olasilik = hayatta_kalma_olasiligi(yas_baslangic, sure, mortalite_tablosu)

print(f"--- Hayatta Kalma Analizi ---")
print(f"Mevcut Yaş: {yas_baslangic}")
print(f"Hedef Yaş : {yas_baslangic + sure}")
print(f"Bu kişinin {sure} yıl daha yaşama ihtimali: %{olasilik * 100:.2f}")

#Annüite (Emekli Maaşı/Taksit) Hesaplama
#Annüite,belirli bir süre boyunca yapılan düzenli ödemelerin bugünkü değeridir.

def pesin_annuite_degeri(yas, sure, faiz_orani, mortalite_tablosu):
# x yaşında başlayan n yıl süreli peşin ödemeli annüite değerini (äx:n) hesaplar.
    toplam_deger = 0
    for t in range(sure):
        v_t = iskonto_faktoru_hesapla(faiz_orani, t)
        tpx = hayatta_kalma_olasiligi(yas, t, mortalite_tablosu)
        toplam_deger += v_t * tpx
    return toplam_deger

# 65 yaşındaki bir bireye, yaşarsa 10 yıl boyunca her yılın başında 100.000 TL emekli maaşı ödenecektir.
# Yıllık teknik faiz oranının %8 olduğu bir senaryoda bu yükümlülüğün bugünkü finansal karşılığını bulalım.

# Gerekli Yardımcı Fonksiyonlar;

def iskonto_faktoru_hesapla(faiz_orani, sure):
    return (1 / (1 + faiz_orani)) ** sure

def hayatta_kalma_olasiligi(yas, sure, mortalite_tablosu):
    # lx+n / lx hesabı
    return mortalite_tablosu[yas + sure] / mortalite_tablosu[yas]

# Basit bir mortalite verisi (65-75 yaş arası hayatta kalanlar)
mortalite_verisi = {
    65: 100000, 66: 97500, 67: 94800, 68: 91900, 69: 88700,
    70: 85200, 71: 81300, 72: 77000, 73: 72200, 74: 66900, 75: 61000
}

yas = 65
sure = 10
faiz = 0.08
yillik_maas = 100000

# 1. Annüite Katsayısını (äx:n) hesaplama
katsayi = pesin_annuite_degeri(yas, sure, faiz, mortalite_verisi)

# 2. Toplam Rezerv/Maliyet Hesabı
toplam_maliyet = yillik_maas * katsayi

print(f"--- 65 Yaş Emeklilik Analizi ---")
print(f"Annüite Faktörü (ä65:10) : {katsayi:.4f}")
print(f"Gelecekteki Toplam Ödeme  : {yillik_maas * sure:,.2f} TL")
print(f"Gereken Mevcut Fon Tutarı: {toplam_maliyet:,.2f} TL")

#Prim ve Rezerv Hesaplama
#Sigortacılıkta Prim, riskin üstlenilmesi karşılığında alınan bedeldir;
# Rezerv (Karşılık) ise şirketin gelecekteki yükümlülüklerini yerine getirmek için ayırdığı tutardır.
# Sigortacılıkta Net Tek Prim, gelecekteki tazminatların bugünkü değerine eşittir. 

def net_tek_prim_vefat(yas, sure, faiz_orani, mortalite_tablosu, tazminat):
#n yıllık bir hayat sigortası için net tek primi hesaplar.
    ntp = 0
    for t in range(sure):
        # t. yılda vefat etme olasılığı (t|qx)
        t_erteleme_hayatta_kalma = hayatta_kalma_olasiligi(yas, t, mortalite_tablosu)
        bir_yillik_vefat = 1 - hayatta_kalma_olasiligi(yas + t, 1, mortalite_tablosu)
        v_t_plus_1 = iskonto_faktoru_hesapla(faiz_orani, t + 1)
        
        ntp += v_t_plus_1 * t_erteleme_hayatta_kalma * bir_yillik_vefat
    
    return ntp * tazminat

def matematiksel_rezerv(gecen_sure, toplam_sure, yas, faiz_orani, mortalite_tablosu, yillik_prim):
    #Prospektif yöntemle t. yıl sonundaki rezervi hesaplar.
    # Gelecekteki yükümlülüklerin bugünkü değeri - Gelecekteki primlerin bugünkü değeri
    kalan_sure = toplam_sure - gecen_sure
    guncel_yas = yas + gecen_sure
    
    yukumluluk = net_tek_prim_vefat(guncel_yas, kalan_sure, faiz_orani, mortalite_tablosu, 100000)
    gelir = yillik_prim * pesin_annuite_degeri(guncel_yas, kalan_sure, faiz_orani, mortalite_tablosu)
    
    return max(0, yukumluluk - gelir)

