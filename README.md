# Dynamo-Relion metadatakonvertteri

Sovellus muuntaa Dynamon käyttämän partikkelien metadatan Relionin vaatimaan muotoon.

## Dokumentaatio
- [Vaatimusmäärittely](dokumentaatio/vaatimusmaarittely.md)
- [Changelog](dokumentaatio/changelog.md)
- [Työaikakirjanpito](dokumentaatio/tuntikirjanpito.md)

## Asennus
1. Asenna riippuvuudet komennolla

```poetry install```

2. Käynnistä sovellus komennolla

```poetry run invoke start```

## Komentorivitoiminnot

### Ohjelman suorittaminen
Ohjelman suoritus

- ```poetry run invoke start``` tulostaa muunnetun datan
- ```poetry run invoke write-starfile``` tallentaa datan ```converted_particles.star``` -tiedostoon

### Testit
Suorita testit komennolla

```poetry run invoke test```


### Testikattavuus
Luo testauskattavuusraportti komennolla

```poetry run invoke coverage-report```

Raportti generoidaan htmlcov-hakemistoon
