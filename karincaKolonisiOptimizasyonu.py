# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 16:45:41 2022

@author: omer
"""

'''
    Kenar seçme olasılıkları (i,j) = t(i,j)^a * l(i,j)^b / toplam t(i,j)^a * l(i,j)^b
        Burada t => kenardaki feromon seviyesi (i, j)
              l => kenar kalitesi = 1/(kenar uzunluğu)
              a,b = t ve l'nin etkisini artırın veya azaltın
    Ardından, RULET ÇARKI tekniği ile bir sonraki yolu (kenarı) seçmek için olasılıkları kullanın:
        Olasılıkların kümülatif toplamının hesaplanması
        1 ile 0 arasında rastgele bir sayı oluşturun
        Seçilecek yol (kenar), oluşturulan rasgele sayının ait olduğu aralığa bağlıdır.

Feromonların güncellenmesi:
    Eğer k'inci karınca kenarda hareket ediyorsa (i, j) o zaman
    k. karıncanın bu kenarda biriktirdiği feromon(i,j) = 1/Lk (Lk, k. karınca turunun toplam uzunluğudur)
    Aksi takdirde 0
    Bir kenardaki Feromon seviyesi:
        buharlaşma olmadan => her karınca tarafından bırakılan feromonların toplamı
        buharlaşma ile => her karınca tarafından bırakılan feromonların toplamı artı
                                [(1-p)*kenardaki mevcut feromon seviyesi] (p buharlaşma oranıdır)
        küresel en iyi turun referansını kullanarak => her tur tamamlandığında, en iyiye belirli miktarda feromon ekliyoruz
            şimdiye kadar elde ettiğimiz tur => en iyi turu oluşturan her kenara e.1/Lk feromonları ekleniyor (burada e, takviye faktörüdür)
            pozitif bir tamsayı ve Lk en iyi turun toplam uzunluğudur) bu süreç arka plan programı eylemlerinden biridir
            daha iyi sonuçlar almak için bir Karınca Kolonisi Optimizasyonu'na performans gösterebilecektir.
    
'''
import fonksiyonlar
import veri

#Grafik (şehirlerin listesi, komşuları, her komşu arasındaki mesafe ve feromon seviyesi)
graf = veri.grafGR17
kopyaGraf = graf.copy()

#algoritma parametreleri
baslangicSehri='633'
buharlasmaOranı=0.5
karincaOrani=500
a=1
b=1
enIyiTurlar=[]

#Karınca Kolonisi Optimizasyonu performanslarını iyileştirmek için kullanılan parametre
asParameter, acsParameter = 4, .3
for i in range(0, karincaOrani):
    suAnkiSehir = baslangicSehri
    ziyaretEdilenSehirler = [baslangicSehri]
    toplamMesafe = 0
    isHamiltonian = True
    while(len(ziyaretEdilenSehirler) < len(graf) and isHamiltonian):
        adaySehirler = fonksiyonlar.AdaySehirler(graf.get(suAnkiSehir), ziyaretEdilenSehirler)
        if len(adaySehirler) > 0 :
            sonrakiSehir = fonksiyonlar.SonrakiSehir(adaySehirler, a, b, acsParameter)
            suAnkiSehir = sonrakiSehir.get('isim')
            toplamMesafe += sonrakiSehir.get('mesafe')
            ziyaretEdilenSehirler.append(suAnkiSehir)
        else : isHamiltonian = False
    if isHamiltonian:
        isHamiltonian = False
        for sehir in graf.get(suAnkiSehir):
            if sehir.get('isim') == baslangicSehri:
                toplamMesafe += sehir.get('mesafe')
                ziyaretEdilenSehirler.append(sehir.get('isim'))
                isHamiltonian = True
                break
        if isHamiltonian:
            print(f'Ziyaret Edilen Sehirler : {ziyaretEdilenSehirler}')
            found = False
            for tur in enIyiTurlar:
                if tur['isim'] == ziyaretEdilenSehirler:
                    tur['Sayi'] += 1
                    found = True
            if found == False:
                enIyiTurlar.append({'isim': ziyaretEdilenSehirler,'toplam mesafe': toplamMesafe, 'Sayi' : 1}) 
            fonksiyonlar.GuncellemeFeromonlar(graf, kopyaGraf, toplamMesafe, ziyaretEdilenSehirler, buharlasmaOranı, enIyiTurlar, asParameter)

print('----------------------')
enIyiTurlar.sort(key = lambda x: x['Sayi'], reverse=False)
for tur in enIyiTurlar:
    print(f'{tur} \n')
enIyiTurlar.sort(key = lambda x: x['toplam mesafe'], reverse=False)
print(enIyiTurlar[0])






'''       ------------------------Orjinal Kodlar------------------------
import functions
import data

#Graph (list of the cities, their neighbors, the distance and pheromone level between each neighbors)
graph = data.graphGR17
graphCopy = graph.copy()
#algorithm parameters
startCity, evaporationRate, antsNumber, a, b, bestTours = '633', 0.5, 50000, 1, 1, []
#parameter used to improve aco performances
asParameter, acsParameter = 4, .3
for i in range(0, antsNumber):
    currentCity = startCity
    visitedCities = [startCity]
    totalDistance = 0
    isHamiltonian = True
    while(len(visitedCities) < len(graph) and isHamiltonian):
        candidateCities = functions.getCandidateCities(graph.get(currentCity), visitedCities)
        if len(candidateCities) > 0 :
            nextCity = functions.getNextCity(candidateCities, a, b, acsParameter)
            currentCity = nextCity.get('name')
            totalDistance += nextCity.get('distance')
            visitedCities.append(currentCity)
        else : isHamiltonian = False
    if isHamiltonian:
        isHamiltonian = False
        for city in graph.get(currentCity):
            if city.get('name') == startCity:
                totalDistance += city.get('distance')
                visitedCities.append(city.get('name'))
                isHamiltonian = True
                break
        if isHamiltonian:
            print(f'Visited cities : {visitedCities}')
            found = False
            for tour in bestTours:
                if tour['name'] == visitedCities:
                    tour['count'] += 1
                    found = True
            if found == False:
                bestTours.append({'name': visitedCities,'total distance': totalDistance, 'count' : 1}) 
            functions.updatePheromones(graph, graphCopy, totalDistance, visitedCities, evaporationRate, bestTours, asParameter)

print('----------------------')
bestTours.sort(key = lambda x: x['count'], reverse=False)
for tour in bestTours:
    print(f'{tour} \n')
bestTours.sort(key = lambda x: x['total distance'], reverse=False)
print(bestTours[0])

'''