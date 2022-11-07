"""
Yksinkertainen ohjelma tuntien kirjaamiseen.

Ohjelmalle annetaan argumenttina polku tiedostolle mihin tunnit kirjataan
tai mistä ne luetaan (esimerkki: python tuntilaskuri.py tunnit.csv)

Validit toiminnot ovat 'k' (kirjaa), 't' (tarkastele) ja 'l' (lopeta).
"""


import sys
from csv import reader, writer
from encodings import utf_8
import datetime



def main(polku):
    while True:
        toiminto = input("Toiminto ([k]irjaa / [t]arkastele / [l]opeta): ")
        if toiminto == "k":
            paiva = pvm_kysely() 
            if paiva == False:
                continue
            tunnit = tunnit_kysely() 
            if tunnit == False: 
                continue
            syy = input("Selitys: ") 
            if not syy:
                print("Tämä ei voi olla tyhjä!")
                continue
            
            kirjoita(polku, paiva, tunnit, syy)

        if toiminto == "t":
            tulosta(polku)

        if toiminto == "l":
            print("Ohjelma lopetetaan. Kiitos ja hei!")
            break

def pvm_kysely():
    tama_paiva = datetime.datetime.now()
    while True:
        pvm = input("anna päivä: ")

        if not pvm:
            return tama_paiva

        if 1 < len(pvm) < 7:
            pvm+=str(tama_paiva.year)
        
        try:
            pvmmuotoilu = datetime.datetime.strptime(pvm, "%d.%m.%Y")
            return pvmmuotoilu
        except ValueError:
            print("Et antanut validia päivämäärää. Ohjelma alkaa alusta.")
            return False


def tunnit_kysely():
    while True:
        tunnit = input("Anna tunnit: ")
        tunnit = tunnit.replace(",", ".")
        try:
            if 0 < float(tunnit) <= 24.0:
                return tunnit
            else:
                print(f"Virhe! Päivässä on 0-24 tuntia. Ohjelma alkaa alusta.")
                return False
        except ValueError:
            print("Virhe!Päivän tunnit pitää ilmoittaa käypänä lukuna (esim. 1, 6.5 tai 3,5). Ohjelma alkaa alusta. ")
            return False



def kirjoita(polku, paiva, tunnit, syy):
    
    tiedot = [f"{paiva.day}.{paiva.month}.{paiva.year}",
    str(tunnit).replace(".", ","), syy]

    with open(polku, "a", encoding="utf_8", newline="") as tiedosto:
        kirjoitin = writer(tiedosto)
        kirjoitin.writerow(tiedot)


def tulosta(polku):
    try:
        with open (polku, encoding="utf_8") as tiedosto:
            
            x = "PÄIVÄ"
            y= "TUNNIT"
            z = "TEHTÄVÄ"
            print(f"{x:15} {y:15} {z:15}")

            lukija = reader(tiedosto)
            yhteensä = 0
            for päivä, tunnit, syy in lukija: 
                print(f"{päivä:15} {tunnit:15} {syy:15}")
                yhteensä += float(tunnit.replace(",", "."))
            yhteensä = str(round(yhteensä, 1)).replace(".", ",")
            print(f"{'YHTEENSÄ':15} {yhteensä}") 

    except FileNotFoundError:
        print("Et voi tarkastella tiedostoa jota ei ole olemassa.")
        print("Kirjaamalla jotain luot tiedoston.")

if __name__ == "__main__":
    argumentit = sys.argv[1:]
    if len(argumentit) > 2 or "--help" in argumentit:
        sys.exit(__doc__)
    try:
        main(*argumentit)
    except ValueError as err: 
            sys.exit(err) 