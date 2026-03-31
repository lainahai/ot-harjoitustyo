## Tehtävä 1: Luokkakaavio

```mermaid
 classDiagram
    Monopolipeli "1" -- "2" Noppa
    Monopolipeli "1" -- "1" Pelilauta
    Pelilauta "1" -- "40" Ruutu
    Ruutu "1" -- "1" Ruutu : seuraava
    Ruutu "1" -- "0..8" Pelinappula
    Pelinappula "1" -- "1" Pelaaja
    Pelaaja "2..8" -- "1" Monopolipeli
    Raha "*" -- "1" Pelaaja
    Vankila --|> Ruutu
    Aloitusruutu --|> Ruutu
    Asema --|> Ruutu
    Laitos --|> Ruutu
    Katu --|> Ruutu
    Sattuma --|> Ruutu
    Yhteismaa --|> Ruutu
    Monopolipeli "1" -- "1" Vankila
    Monopolipeli "1" -- "1" Aloitusruutu
    Ruutu "1" -- "1" Toiminto
    Kortti "1" -- "1" Toiminto
    Yhteismaa "1" -- "*" Kortti
    Sattuma "1" -- "*" Kortti
    Katu "1" -- "0..4" Talo
    Katu "1" -- "0..1" Hotelli
    Pelaaja "1" -- "0..22" Katu
```
