## Struktur
Oppgaven er spredd ut over hovedsakelig fire filer jeg skal beskrive her:
* weather.py: Inneholder funksjoner for å hente og tolke data fra yr.no
* weatherbuf.py: Inneholder en klasse for å gjøre buffering.
* extreme.py: Raskt python-script for å hente høyeste og laveste temperatur neste 13:00.
* tests/test_weather.py: Inneholder tester skrevet ved hjelp av py.test.

## Bruk
* For å kjøre tester kan du kjøre `py.test` i mappen week4, dette forutsetter at du har installert py.test.
* For å gjøre et oppslag på sted og tid det neste døgnet kan du kjøre `python weather.py STEDSNAVN TIME MINUTT`, denne kommandoen støtter også wildcard i stedsnavn (husk å putt stedsnavn i anførselstegn hvis du har med wildcard).
* For å få ekstreme hente ut de mest ekstreme verdiene neste klokken 1300 kan du kjøre `python extreme.py`, merk at dette kun tester 100 linker for ikke å bombardere yr.no. Dette gjør at extreme.py IKKE er representativt for hele landet.

## Bruk av API
API i weather.py skal være OK dokumentert og mulig å bruke til hva enn man ønsker, innenfor rimelighetens grenser.
