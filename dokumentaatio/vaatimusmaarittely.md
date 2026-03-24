# Vaatimusmäärittely

## Sovelluksen tarkoitus

Ystäväni tutkii proteiineja kryoelektronimikroskopialla. Analyysissä tarvitaan kahta ohjelmistoa, joiden välillä tiedon siirtäminen on hankalaa.

Sovellusta käytetään metadatan muuntamiseen kahden tomografia-analyysiohjelmiston, [Dynamon](https://www.dynamo-em.org) ja [Relionin](https://relion.readthedocs.io), välillä. Tavoitteena on vähintään saada Dynamossa valittujen partikkelien tiedot muunnettua muotoon, jossa ne voidaan viedä Relioniin jatkoanalyysiä varten. 

Dynamo tallentaa tiedot suoraan matlab-matriiseina, Relion käyttää star-tiedostoja. Lisäksi tarvitaan vll-tiedosto, jossa on absoluuttiset polut analysoitavaan tomogrammidataan. Tämä luodaan aluksi käsin, mutta ehkä jatkossa myös suoraan osana konversiota.

Dynamossa sijainnit on ilmoitettu pikseleinä, Relionissa ångströmeinä. Myös partikkeleiden asennon ilmoittamiseen käytettävät euler-kulmat on määritelty ohjelmissa eri tavoin. Konversio ei siis onnistu vain muuttamalla tietojen tallennustapaa, vaan arvot täytyy myös muuntaa esitystapojen välillä oikein.

## Alustava toiminnallisuus

* Käyttäjä voi valita luettavan star-tiedoston
  * sisältää tomogrammien ja mikroskoopin metatiedot, joita tarvitaan konversiossa
* Käyttäjä voi valita luettavan dynamo-taulukon
  * Dynamo-taulukko sisältää tiedot tomogrammeista valituista partikkeleista, joista tehdään analyysi
* Käyttäjä voi valita luettavan vll-tiedoston
  * Tiedosto sisältää absoluuttiset polut tomogrammidataa sisältäviin tiedostoihin
* Käyttäjä voi antaa nimen luotavalle star-tiedostolle
* Käyttäjä voi antaa tiedostonimet suoraan parametreina
  * Tällöin käyttöliittymää ei käynnistetä vaan konversio tehdään suoraan annetuilla tiedostoilla.
* Käyttäjä voi luoda dynamon taulukosta star-tiedoston, joka sisältää
  * koordinaatit
  * euler-kulmat
  * tomogrammin tunnistetiedot
  * jännitteen

## Laajennusmahdollisuuksia
* VLL-tiedoston luonti
  * Käyttäjä voisi valita projektikansiosta analysoitavaksi otettavat tomogrammit
* Konversio myös toiseen suuntaan, Relionista Dynamoon
