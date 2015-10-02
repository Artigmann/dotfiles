## Struktur
Oppgaven er spredd ut over hovedsakelig fire filer jeg skal beskrive her:
* weather.py: Inneholder funksjoner for å hente og tolke data fra yr.no
* weatherbuf.py: Inneholder en klasse for å gjøre buffering.
* extreme.py: Raskt python-script for å hente høyeste og laveste temperatur neste 13:00.
* tests/test_weather.py: Inneholder tester skrevet ved hjelp av py.test.

## Bruk
* For å kjøre tester kan du kjøre "py.test" i mappen week4, dette forutsetter at du har installert py.test.
* For å gjøre et oppslag på sted og tid det neste døgnet kan du kjøre, denne kommandoen støtter også wildcard i stedsnavn (husk å putt stedsnavn i anførselstegn hvis du har med wildcard):
``` bash
python weather.py STEDSNAVN TIME MINUTT
```

* For å få ekstreme verdier kan du kjøre følgende, merk at dette kun tester 100 linker for ikke å bombardere yr.no. Dette gjør at extreme.py IKKE er representativt for hele landet.
``` bash
python extreme.py
```
