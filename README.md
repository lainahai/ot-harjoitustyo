# Dynamo-Relion metadatakonvertteri

Sovellus muuntaa Dynamon käyttämän partikkelien metadatan Relionin vaatimaan muotoon.

## Dokumentaatio
- [Vaatimusmäärittely](dokumentaatio/vaatimusmaarittely.md)
- [Changelog](dokumentaatio/changelog.md)
- [Työaikakirjanpito](dokumentaatio/tuntikirjanpito.md)
- [Arkkitehtuuri](dokumentaatio/arkkitehtuuri.md)

## Asennus
1. Asenna riippuvuudet komennolla

```poetry install```

2. Käynnistä sovellus komennolla

```poetry run invoke start```

## Komentorivitoiminnot

### Ohjelman suorittaminen
Ohjelman suoritus

- ```poetry run invoke start``` käynnistää ohjelman käyttöliittymän. 
    - HUOM: invoken avulla suoritettaessa näppäimistökomennot eivät jostain syystä toimi. Käytä siis hiirtä.
- ```poetry run invoke print-starfile``` tulostaa testidatan konversion ilman käyttöliittymää 
- ```poetry run invoke write-starfile``` tallentaa testidatan konversion ```particles.star``` -tiedostoon

### Testit
Suorita testit komennolla

```poetry run invoke test```


### Testikattavuus
Luo testauskattavuusraportti komennolla

```poetry run invoke coverage-report```

Raportti generoidaan htmlcov-hakemistoon

### Pylint
Aja laaturaportti komennolla

```poetry run invoke lint```
