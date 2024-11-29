from  random import random
from random import randrange

def removeSehirIfExist(sehirListesi, sehir):
    for c in sehirListesi:
        if c.get('isim') == sehir:
            sehirListesi.remove(c)
            break

def AdaySehirler(adaySehirler, herzamanZiyaretEdilenSehirler):
    sonListe = adaySehirler.copy()
    for sehir in herzamanZiyaretEdilenSehirler:
        removeSehirIfExist(sonListe, sehir)
    return sonListe

def SonrakiSehir(adaySehirler, a, b, acsParameter):
    rand = random()
    if rand <= (1- acsParameter):
        toplamOlasiliklar = 0.0
        kenarOlasiliklar = []
        if len(adaySehirler) == 1 : kenarOlasiliklar.append(1)
        else :
            for sehir in adaySehirler:
                toplamOlasiliklar += (sehir.get('feromonlar')**a * (1/sehir.get('mesafe'))**b)
            if toplamOlasiliklar == 0 : return adaySehirler[randrange(len(adaySehirler))]
            for sehir in adaySehirler:
                kenarOlasiliklar.append((sehir.get('feromonlar')**a * (1/sehir.get('mesafe'))**b)/ toplamOlasiliklar)
        KumulatifToplam(kenarOlasiliklar)
        kenarOlasiliklar.append(0)
        randomNum = random()
        x = IkiliAramaYineleme(kenarOlasiliklar, randomNum)
        indexX = kenarOlasiliklar.index(x)
        if x < randomNum:
            indexX -= 1
        return adaySehirler[indexX]
    else : 
        sonrakiSehir = adaySehirler[0]
        maxProd = (sonrakiSehir.get('feromonlar') * (1/sonrakiSehir.get('mesafe'))**b)
        for i in range(1,len(adaySehirler)):
            prod = adaySehirler[i].get('feromonlar') * (1/adaySehirler[i].get('mesafe'))**b
            if prod > maxProd :
                maxProd = prod
                sonrakiSehir = adaySehirler[i]
        return sonrakiSehir



def KenarFeromonGüncelleme(sehirListesi, sehir, eklenecekFeromon, fact = 1):
    for c in sehirListesi:
        if c.get('isim') == sehir:
            c['feromonlar'] += eklenecekFeromon*fact

def FeromonBuharlasma(graf, buharlasmaOranı):
    for c1 in graf:
        for c2 in graf[c1]:
            c2['feromonlar'] = (1 - buharlasmaOranı)*c2['feromonlar']

def EnIyiKureselTakviye(graf, turlar, takviyeFaktoru = 1):
    enIyiTur = turlar[0].get('isim')
    toplamMesafe = turlar[0].get('toplam mesafe')
    for i in range(0, len(enIyiTur)-1):
        KenarFeromonGüncelleme(graf.get(enIyiTur [i]) , enIyiTur [i+1], takviyeFaktoru* 1/toplamMesafe)
        KenarFeromonGüncelleme(graf.get(enIyiTur [i+1]) , enIyiTur [i],  takviyeFaktoru* 1/toplamMesafe)


def GuncellemeFeromonlar(graf, kopyaGraf, toplamMesafe, ziyaretEdilenSehirler, buharlasmaOranı, turlar, asParameter):
    turlar.sort(key = lambda x: x['toplam mesafe'], reverse=False)
    graf = kopyaGraf.copy()

    w = asParameter if len(turlar) > asParameter else len(turlar)
    for j in range(0, w - 1):
        #buharlaşma
        FeromonBuharlasma(graf, buharlasmaOranı)
        r = j + 1
        #depozito feromonları
        for i in range(0, len(turlar[j]['isim'])-1):
            KenarFeromonGüncelleme(graf.get(turlar[j]['isim'][i]) , turlar[j]['isim'][i+1], 1/turlar[j]['toplam mesafe'],w - r)
            KenarFeromonGüncelleme(graf.get(turlar[j]['isim'][i+1]) , turlar[j]['isim'][i], 1/turlar[j]['toplam mesafe'],w - r)
    EnIyiKureselTakviye(graf, turlar, w)

    # for i in range(0, len(ziyaretEdilenSehirler)-1):
    #     KenarFeromonGüncelleme(graf.get(ziyaretEdilenSehirler[i]) , ziyaretEdilenSehirler[i+1], 1/toplamMesafe)
    #     KenarFeromonGüncelleme(graf.get(ziyaretEdilenSehirler[i+1]) , ziyaretEdilenSehirler[i], 1/toplamMesafe)
    #küresel en iyi tur takviyesi
    #EnIyiKureselTakviye(graf, turlar, takviyeFaktoru)
    
def KumulatifToplam(olasiliklar):
    olasiliklar.reverse();
    kumulatifToplam = 0
    for i in range(0,len(olasiliklar)):
        kumulatifToplam += olasiliklar[i]
        olasiliklar[i] = kumulatifToplam
    olasiliklar.reverse()
    olasiliklar[0] = round(olasiliklar[0]) 
    return olasiliklar

def IkiliAramaYineleme(liste, eleman):
    mid = 0
    start = 0
    end = len(liste)
    step = 0
    kopyaListe = liste.copy()
    kopyaListe.reverse()
    while (start <= end):
        step = step+1
        mid = (start + end) // 2
        
        if eleman == kopyaListe[mid]:
            return kopyaListe[mid]

        if eleman < kopyaListe[mid]:
            end = mid - 1
        else:
            start = mid + 1
    return kopyaListe[mid]

test = 3





'''       ------------------------Orjinal Kodlar------------------------
from  random import random
from random import randrange

def removeCityIfExist(citiesList, city):
    for c in citiesList:
        if c.get('name') == city:
            citiesList.remove(c)
            break

def getCandidateCities(candidatesCities, alreadyVisitedCities):
    finalList = candidatesCities.copy()
    for city in alreadyVisitedCities:
        removeCityIfExist(finalList, city)
    return finalList

def getNextCity(candidatesCities, a, b, acsParameter):
    rand = random()
    if rand <= (1- acsParameter):
        totalProbabilities = 0.0
        edegsProbabilities = []
        if len(candidatesCities) == 1 : edegsProbabilities.append(1)
        else :
            for city in candidatesCities:
                totalProbabilities += (city.get('pheromones')**a * (1/city.get('distance'))**b)
            if totalProbabilities == 0 : return candidatesCities[randrange(len(candidatesCities))]
            for city in candidatesCities:
                edegsProbabilities.append((city.get('pheromones')**a * (1/city.get('distance'))**b)/ totalProbabilities)
        cummulativeSum(edegsProbabilities)
        edegsProbabilities.append(0)
        randomNum = random()
        x = binary_search_iterative(edegsProbabilities, randomNum)
        indexX = edegsProbabilities.index(x)
        if x < randomNum:
            indexX -= 1
        return candidatesCities[indexX]
    else : 
        nextCity = candidatesCities[0]
        maxProd = (nextCity.get('pheromones') * (1/nextCity.get('distance'))**b)
        for i in range(1,len(candidatesCities)):
            prod = candidatesCities[i].get('pheromones') * (1/candidatesCities[i].get('distance'))**b
            if prod > maxProd :
                maxProd = prod
                nextCity = candidatesCities[i]
        return nextCity



def updateEdgePheromone(citiesList, city, pheromoneToAdd, fact = 1):
    for c in citiesList:
        if c.get('name') == city:
            c['pheromones'] += pheromoneToAdd*fact

def pheromoneEvaporation(graph, evaporationRate):
    for c1 in graph:
        for c2 in graph[c1]:
            c2['pheromones'] = (1 - evaporationRate)*c2['pheromones']

def globalBestReinforcement(graph, tours, reinforcementFactor = 1):
    bestTour = tours[0].get('name')
    totalDistance = tours[0].get('total distance')
    for i in range(0, len(bestTour)-1):
        updateEdgePheromone(graph.get(bestTour[i]) , bestTour[i+1], reinforcementFactor* 1/totalDistance)
        updateEdgePheromone(graph.get(bestTour[i+1]) , bestTour[i],  reinforcementFactor* 1/totalDistance)


def updatePheromones(graph, graphCopy, totalDistance, visitedCities, evaporationRate, tours, asParameter):
    tours.sort(key = lambda x: x['total distance'], reverse=False)
    graph = graphCopy.copy()

    w = asParameter if len(tours) > asParameter else len(tours)
    for j in range(0, w - 1):
        #evaporization
        pheromoneEvaporation(graph, evaporationRate)
        r = j + 1
        #deposit pheromones
        for i in range(0, len(tours[j]['name'])-1):
            updateEdgePheromone(graph.get(tours[j]['name'][i]) , tours[j]['name'][i+1], 1/tours[j]['total distance'],w - r)
            updateEdgePheromone(graph.get(tours[j]['name'][i+1]) , tours[j]['name'][i], 1/tours[j]['total distance'],w - r)
    globalBestReinforcement(graph, tours, w)
    
def cummulativeSum(probabilities):
    probabilities.reverse();
    cummulativeSum = 0
    for i in range(0,len(probabilities)):
        cummulativeSum += probabilities[i]
        probabilities[i] = cummulativeSum
    probabilities.reverse()
    probabilities[0] = round(probabilities[0]) 
    return probabilities

def binary_search_iterative(array, element):
    mid = 0
    start = 0
    end = len(array)
    step = 0
    arrayClone = array.copy()
    arrayClone.reverse()
    while (start <= end):
        step = step+1
        mid = (start + end) // 2
        
        if element == arrayClone[mid]:
            return arrayClone[mid]

        if element < arrayClone[mid]:
            end = mid - 1
        else:
            start = mid + 1
    return arrayClone[mid]

test = 3
'''
