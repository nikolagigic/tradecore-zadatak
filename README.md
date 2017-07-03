# tradecore-zadatak

Evo zadatka.
Nekoliko reci samo:

  Bot koji bi trebao da demonstrira funkcionalnosti sajta se zove Tyler, i smesten je u Tyler folderu.
  Python verzija: Python 3.6.1
  Django verzija: 1.11.2 final
  Ostale biblioteke koje su potrebne da bi zadatak radio su smestene u requirements.txt.
  Koriscena baza je sqlite3 s obzirom da je development mode.
  User/pass za django admina:
    -Username: djangoadmin
    -Password: Tradecore
  
  Tokom kreiranja korisnika pomocu bota, ne proverava se integritet emaila niti se radi lookup korisnika, jer su mailovi
  genericki sastavljeni, tako da je velika verovatnoca da ne postoje. Te opcije su primenjive tokom manuelne kreacije korisnika
  preko website-a.
  
  Sto se tice lookupa korisnika, postoji problem sa api.key jer je besplatan nalog, te iz nekog razloga ne radi za svaki
  lookup, iako je sve po propisima kodirano.

  Izgled website-a je krajnje prost, bez ikakvog sminkanja.
  
  REST-API URL: domain:port/api/rest/
  Filteri za REST-API: posts, lookups, <username> (npr. domain:port/api/rest/posts/; domain:post/api/rest/lookups/; domain:port/api/rest/robottyler1/)
  Profil robota/korisnika: domain:port/user/<username>
  
  U slucaju da pustate server na WAN/LAN, dodajte samo ip adresu u listu ALLOWED_HOSTS koja se nalazi u tradecore/settings.py
  
Sve u svemu to je to. Ukoliko ima bilo kakvih dodatnih pitanja, tu je mail :)
