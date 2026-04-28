# Dynamo-Relion metadatakonvertteri

Sovellus muuntaa Dynamon käyttämän partikkelien metadatan Relionin vaatimaan muotoon.

## Dokumentaatio
- [Vaatimusmäärittely](dokumentaatio/vaatimusmaarittely.md)
- [Changelog](dokumentaatio/changelog.md)
- [Työaikakirjanpito](dokumentaatio/tuntikirjanpito.md)
- [Arkkitehtuuri](dokumentaatio/arkkitehtuuri.md)
- [Käyttöohje](dokumentaatio/kayttoohje.md)

## Release

[Viikko 5 Release](https://github.com/lainahai/ot-harjoitustyo/releases/tag/viikko5)

## Asennus

1. Asenna riippuvuudet komennolla

```poetry install```

2. Käynnistä sovellus komennolla

```poetry run invoke start```

## Komentorivitoiminnot

### Ohjelman suorittaminen
Ohjelman suoritus

- ```poetry run invoke start``` käynnistää ohjelman käyttöliittymän. 
    - HUOM: invoken avulla suoritettaessa enter-näppäin ei jostain syystä toimi. Käytä siis hiirtä.
- ```poetry run invoke print-starfile``` tulostaa konversion ilman käyttöliittymää 
- ```poetry run invoke write-starfile``` tallentaa konversion ```particles.star``` -tiedostoon

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

## Esimerkkidata

```test_data```-kansiossa on esimerkkidataa:
- ```test_table.tbl```: Dynamon tuottamaa parikkelidataa. [Linkki kenttien selitteeseen](https://www.dynamo-em.org/w/index.php?title=Table_convention)
- ```test_vll.vll```: Dynamon käyttämä lista tomogrammeista, joista partikkelit on poimittu
- ```test_tomograms.star```: Relionin tuottama tomogrammien metadatatiedosto
