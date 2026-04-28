# Arkkitehtuurikuvaus

## Rakenne

![Pakkauskaavio](./kuvat/pakkauskaavio.png)

Pakkaus _ui_ sisältää ohjelman käyttöliittymän, _services_ sovelluslogiikasta vastaavan koodin ja _repositories_ tallennuksesta vastaavan koodin.

## Sovelluslogiikka

Luokka [ParticleService](https://github.com/lainahai/ot-harjoitustyo/blob/main/src/services/particle_service.py) toteuttaa partikkelimetadatan konversion metodin ```convert_dynamo_star(table_file, vll_file, tomograms_file, output_file)``` kautta.

Tiedostojen lukemisesta ja kirjoittamisesta vastaa luokka [FileRepository](https://github.com/lainahai/ot-harjoitustyo/blob/main/src/repositories/file_repository.py).

Luokka [LogService](https://github.com/lainahai/ot-harjoitustyo/blob/main/src/services/log_service.py) vastaa ohjelman tulosteiden ohjaamisesta joko terminaaliin tai käyttöliittymään rippuen siitä, suoritetaanko ohjelmaa käyttöliittymän kanssa vai ilman sitä.

Käyttöliittymästä vastaa luokka [ConverterApp](https://github.com/lainahai/ot-harjoitustyo/blob/main/src/ui/converter_app.py).
Käyttöliittymän avulla käyttäjä voi valita konversiossa käytettävät metadatatiedostot, nimetä tallennettavan tiedoston ja tarkastella muunnettua dataa tallentamatta sitä. 

### Luokkakaavio
```mermaid
 classDiagram
    ParticleService --> "1" FileRepository
    ParticleService --> "1" LogService
    FileRepository --> "1" LogService
    LogService --> "0..1" ConverterApp
    ConverterApp --> "1" ParticleService
    class ParticleService{
        convert_dynamo_star()
    }
    class FileRepository{
        read_dynamotable()
        read_starfile()
        read_vllfile()
        write_starfile()
    }
    class LogService{
        log()
    }
    class ConverterApp{
        run()
        print_log()
    }
```


### Konversion sekvenssikaavio

Kun käyttöliittymässä on valittu käsiteltävät tiedostot tai ne on annettu parametreina 
ja tulokset tallennetaan tiedostoon, suoritus etenee seuraavasti:

```mermaid
sequenceDiagram
    participant UI
    participant ParticleService
    participant FileRepository
    participant LogService
    UI -->>+ParticleService: convert_dynamo_star(tbl, vll, tomo, of)
    ParticleService-->>ParticleService: _validate_input_paths(tbl, vll, tomo)
    ParticleService-->>ParticleService: _validate_file_path(tbl)
    ParticleService-->>ParticleService: _validate_file_path(vll)
    ParticleService-->>ParticleService: _validate_file_path(tomo)
    ParticleService-->>ParticleService: _read_dynamo_particles(tbl, vll)
    ParticleService-->>+FileRepository: read_dynamotable(tbl)
    FileRepository-->>-ParticleService: particles_df
    ParticleService-->>+FileRepository: read_vll(vll)
    FileRepository-->>-ParticleService: vll_contents
    ParticleService-->>ParticleService: _filter_unaveraged_particles(particles_dynamo_df)
    ParticleService -->>+FileRepository: read_starfile(tomo)
    FileRepository -->>-ParticleService: tomograms_star_df
    ParticleService-->>ParticleService: _convert_eulers_dynamo_relion(eulers_dynamo_df)
    ParticleService-->>ParticleService: _convert_coordinates_dynamo_relion(coordinates_dynamo_df)
    ParticleService -->>FileRepository: write_starfile(converted_particles_dict)
    ParticleService -->>LogService: log(f"Wrote {of}", ui_only=True)
      
```
