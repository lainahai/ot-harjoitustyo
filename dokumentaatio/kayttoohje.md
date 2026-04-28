# Käyttöohje

Lataa ohjelman viimeisin [release](https://github.com/lainahai/ot-harjoitustyo/releases) Assets-osion Source code -linkistä ja pura koodi haluamaasi kansioon.

## Ohjelman käynnistäminen

Asenna ohjelman riippuvuudet suorittamalla

```poetry install```

Käynnistä ohjelma käyttöliittymässä suorittamalla

```poetry run invoke start```

Jos haluat kokeilla tehdä konversion testidatasta (kansiossa `test_data`) ilman käyttöliittymää, aja komento

```poetry run invoke print_starfile```

## Käyttöliittymä

Käyttöliittymään käynnistettäessä aukeaa näkymä, jossa tarvittavat metadatatiedosto voidaan valita.

Käyttöliittymä toimii hiirellä, mutta myös näppäinkomennoista voi olla hyötyä:

Tärkeimmät näppäinkomennot:

 - ```tab``` siirtyy elementtien välillä
 - Liiku tiedostojen valinnassa nuolinäppäimillä
 - ```enter``` hyväksyy 

 Valittujen tiedostojen polut näkyvät näppäimien yläpuolella.

Painikkeet:

 - __Convert and save__: suorittaa konversion ja tallentaa tulokset _Output file name_ -kentässä annettuun tiedostoon
 - __Convert and show__: suorittaa konversion ja tulostaa tulokset alaosan lokinäkymään.
 - __Quit__: Sulkee ohjelman.

![Käyttöliittymä](./kuvat/howto_ui.png)
