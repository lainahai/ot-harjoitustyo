## Tehtävä 2: Sekvenssikaavio

```mermaid
sequenceDiagram
    create participant laitehallinto
    main->>laitehallinto: HKLLaitehallinto()
    create participant rautatientori
    main->>rautatientori: Lataajalaite()
    create participant ratikka6
    main->>ratikka6: Lukijalaite()
    create participant bussi244
    main->>bussi244: Lukijalaite()
    
    main->>laitehallinto: lisaa_lataaja(rautatientori)
    main->>laitehallinto: lisaa_lukija(ratikka6)
    main->>laitehallinto: lisaa_lukija(bussi244)
    
    create participant lippu_luukku
    main->>lippu_luukku: Kioski()
    
    main->>+lippu_luukku: osta_matkakortti("Kalle")
    create participant kallen_kortti
    lippu_luukku->>kallen_kortti: Matkakortti("Kalle")
    lippu_luukku-->>-main: kallen_kortti
    
    main->>+rautatientori: lataa_arvoa(kallen_kortti, 3)
    rautatientori->>kallen_kortti: kasvata_arvoa(3)
    deactivate rautatientori
    
    main->>+ratikka6: osta_lippu(kallen_kortti, 0)
    ratikka6->>+kallen_kortti: arvo()
    kallen_kortti-->>-ratikka6: 3
    ratikka6->>kallen_kortti: vahenna_arvoa(1.5)
    ratikka6-->>-main: True
    
    main->>+bussi244: osta_lippu(kallen_kortti, 2)
    bussi244->>+kallen_kortti: arvo()
    kallen_kortti-->>-bussi244: 1.5
    bussi244-->>-main: False
```
