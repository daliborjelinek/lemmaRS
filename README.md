# Důležité odkazy
Rezervační systém je nasazený na adrese https://rs.lemma.fi.muni.cz/

Aktuální verze kódu je k dispozici v repozitáři https://gitlab.fi.muni.cz/lemma/lemmars

Portainer dashboard s monitoringem aplikace na produkčním serveru je k dispozici na https://lemma-new.ics.muni.cz/

Konfiguraci reverzního proxyserveru je možné provádět na http://lemma-new.ics.muni.cz:81/

Nasazení na produkční server lemma-new.ics.muni.cz probíhá automaticky pomocí CI/CD pipelines při commitu do master větve a ručním potvrzení v záložce pipelines.

Pro účely jednotného univerzitního přihlášení je aplikace zaregostrována na https://spreg.aai.muni.cz/spreg/

Veškeré přístupové údaje a oprávnění poskytne na vyžádání Dalibor Jelínek (487606@mail.muni.cz).


# Lokální vývoj
K vývoji jsou potřeba tyto nástroje:

- Node.js
- Python 3
- Docker
- Docker-compose


## 1. Vytvoření databáze
Nejprve je nutné vytvořit databázi.
```
docker-compose -f docker-compose.dbonly.yml up
```

## 2. Spuštění dev serveru backendu
Prerekvizitou tohoto kroku je spuštěná databáze.

Pro spuštění devserveru je potřeba nastavit systémovou proměnnou ENV_PATH která specifikuje cestu k  `.env.dev` souboru pro vývoj. Ten není součástí repozítáře, jelikož obsahuje citlivá data (API klíče, hesla...) a tudíž by se ani nikdy neměl do repozitáře dostat. Soubor je nutné vytvořit na základě souboru `.env.example` a doplnit do něj potřebné tokeny.

Do `ENV_PATH` je možné nastavit přímo `.env.example`, který je součástí repozitáře. V takovém případě ale nebude funogvat univerzitní login a odesílání emailů.

Potřebné údaje poskytne na vyžádání Dalibor Jelínek (487606@mail.muni.cz).

Před spuštěním serveru je potřeba nainstalovat knihovny definované v requirements.txt a spustit migrace databáze.


```
cd lemma_rs_be
SET ENV_PATH=.env.dev

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

Po spuštění je API k dispozici na adrese http://localhost:8000/

Dokumentace k API je k dispozici na http://localhost:8000/schema/ui

## 3. import testovacích dat
Pro účely testování je výhodné naplnit databázi testavacími daty. 

Následující příkazy vytvoří v databázi přibližně 200 zdrojů a od každé role jednoho uživatele. Za tyto uživatele je možné se přihlasit pomocí simulace jednotného přihlašení viz sekce 5.

```
cd lemma_rs_be
SET ENV_PATH=.env.dev

python manage.py loaddata sources
```

Užitečná je též možnost přihlásit se do administrace backendu. K tomu je potřeba vytvořit superuživatele pomocí následujícího příkazu.

```
python manage.py createsuperuser
```
Po vytvoření je možné se příhlásit d administrace na http://localhost:8000/admin

## 4. Spuštění dev serveru frontendu

```
cd lemma-rs-fe

npm install
npm run serve
```

Po instalaci je frontend aplikace k dispozici na adrese http://localhost:8080/


## 5 Spuštění simulátoru jednotného příhlášení

```
cd mock-oidc

docker-compose up
```

Po spuštění serveru je možné se příhlásit do rezervačního systému pomocí tlačítka "mock login" pod těmito přihlašovacími údaji:

### Admin
username: 000000\
password: pwd

### Výdejář
username: 111111\
password: pwd

### Běžný uživatel
username: 100000\
password: pwd

uživatele je možné upravovat v souboru `mock-oidc/docker-compose.yml`
Odhlásit se z autentizačního serveru je možné na http://localhost:4011/


# Lokální build & deploy
Pro otestování produkčního buildu na lokálním stoji je monžé použít následující postup:

K deploymentu na lokální stroj slouží soubor `docker-compose.test.yml`. Jedná se o mírně upravený produkční
`docker-compose.prod.yml`. Ke spuštění je potřeba vytvořit soubor `.env.test` na základě souboru `.env.example` a doplnit do něj potřebné tokeny.

Po úspěšném nasazení bude frontend k dispozici na http://localhost:8080 a api na http://localhost:8000

poslední příkaz spustí proces plánovače zasílání automatických mailových upozornění.

```
docker network create backbone
docker-compose -f docker-compose.test.yml up
docker-compose -f docker-compose.test.yml exec api python manage.py migrate
docker-compose -f docker-compose.test.yml exec api python manage.py collectstatic
docker-compose -f docker-compose.test.yml exec api python manage.py runapscheduler
```