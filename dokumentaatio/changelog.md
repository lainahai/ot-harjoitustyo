## Viikko 3

- Projektin alustus ja testien konfigurointi
- Kokeiluun kelpaavat tbl- ja vll-tiedostot luotu
- Lisätty ParticleService-luokka, joka lukee dynamo-tiedostot (pitää vielä refaktoroida urakalla)
- Dynamo-tiedostojen luku ja tomogrammien nimen yhdistäminen taulukkodataan toimii

## Viikko 4

- Siirretty tiedostojen käsittely FileRepository -luokkaan
- Koordinaattien konversio toimii
- Euler-kulmien konversio toimii
- Muunnettujen tietojen tallennus star-muodossa toimii
- Jännite ja binning-parametri luetaan tomogrammien star-tiedostosta
- Käyttäjä voi antaa luettavat tiedostot ja tallennettavan tiedoston nimen parametreina.
- Käyttäjä voi myös tulostaa tiedoston sisällön tiedostoon kirjoittamisen sijaan.

## Viikko 5

- Käyttöliittymän kehitys Textual-kirjastolla aloitettu 
- Käyttäjä voi valita tiedostot käyttöliittymästä
- Käyttäjä voi nimetä tallennettavan tiedoston käyttöliittymässä
- Jos käyttäjä antaa kaikki tiedostot parametreina, käyttöliittymä ei käynnisty
- Siirretty tulostusten ohjaus LogServiceen
- Konversion tuloksen voi tulostaa käyttöliittymään

## Viikko 6

- Virhetilanteiden käsittelyä parannettu
  - Ohjelma ei kaadu jos tiedostoa ei ole olemassa  tai sitä ei voi lukea.
  - Ohjelma ei kaadu jos sille antaa kuvatiedoston.
- Virhetilanteessa käyttäjälle tulostuu siisti virheilmoitus.
- Testattu ettei ohjelma kaadu jos tiedostopolku on virheellinen.
