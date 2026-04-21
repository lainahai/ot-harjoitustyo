# Vaatimusmäärittely

## Sovelluksen tarkoitus

Ystäväni tutkii proteiineja kryoelektronimikroskopialla. Analyysissä tarvitaan kahta ohjelmistoa, joiden välillä tiedon siirtäminen on hankalaa.

Sovellusta käytetään metadatan muuntamiseen kahden tomografia-analyysiohjelmiston, [Dynamon](https://www.dynamo-em.org) ja [Relionin](https://relion.readthedocs.io), välillä. Tavoitteena on vähintään saada Dynamossa valittujen partikkelien tiedot muunnettua muotoon, jossa ne voidaan viedä Relioniin jatkoanalyysiä varten. 

Dynamo tallentaa tiedot suoraan matlab-matriiseina, Relion käyttää star-tiedostoja. Lisäksi tarvitaan vll-tiedosto, jossa on absoluuttiset polut analysoitavaan tomogrammidataan. Tämä luodaan aluksi käsin, mutta ehkä jatkossa myös suoraan osana konversiota.

Dynamossa sijainnit on ilmoitettu pikseleinä, Relionissa ångströmeinä. Myös partikkeleiden asennon ilmoittamiseen käytettävät euler-kulmat on määritelty ohjelmissa eri tavoin. Konversio ei siis onnistu vain muuttamalla tietojen tallennustapaa, vaan arvot täytyy myös muuntaa esitystapojen välillä oikein.

## Alustava toiminnallisuus

* [x] Käyttäjä voi valita luettavan star-tiedoston - tehty
    * sisältää tomogrammien ja mikroskoopin metatiedot, joita tarvitaan konversiossa
* [x] Käyttäjä voi valita luettavan dynamo-taulukon -tehty
    * Dynamo-taulukko sisältää tiedot tomogrammeista valituista partikkeleista, joista tehdään analyysi
* [x] Käyttäjä voi valita luettavan vll-tiedoston -tehty
    * Tiedosto sisältää absoluuttiset polut tomogrammidataa sisältäviin tiedostoihin
* [x] Käyttäjä voi antaa nimen luotavalle star-tiedostolle - tehty
    * [x] Parametrina - tehty
    * [x] Käyttöliittymässä - tehty
* [x] Käyttäjä voi antaa tiedostonimet suoraan parametreina - tehty
    * Tällöin käyttöliittymää ei käynnistetä vaan konversio tehdään suoraan annetuilla tiedostoilla.
* [x] Käyttäjä voi luoda dynamon taulukosta star-tiedoston, joka sisältää  - tehty
    * koordinaatit
    * euler-kulmat
    * tomogrammin tunnistetiedot
    * jännitteen
* [x] Tiedostoon tallentamisen sijaan star-tiedoston sisältö voidaan tulostaa esimerkiksi putkittamista varten  - tehty
* [ ] Käyttäjä voi valita haluaako muuntaa vain keskiarvoistettujen partikkelien tiedot, vai kaikki partikkelit 
* [ ] Virheilmoitukset ja ilmoitus onnistuneesta konversiosta käyttöliittymässä

## Laajennusmahdollisuuksia
* Luettavien tiedostojen validointi, esim:
    * Dynamon table-tiedostossa on kaikki kentät
    * Tomogrammien star-tiedostossa on jännite, kuvien koot ja muut tarpeelliset tiedot
* Muunnettujen tietojen validointi, esim:
    * Koordinaatit ovat tomogrammien sisällä
    * Euler-kulmat ovat järkevissä rajoissa
* VLL-tiedoston luonti
  * Käyttäjä voisi valita projektikansiosta analysoitavaksi otettavat tomogrammit
  * Tämän voi ehkä luoda suoraan tomogrammien star-tiedoston pohjalta
* Konversio myös toiseen suuntaan, Relionista Dynamoon
