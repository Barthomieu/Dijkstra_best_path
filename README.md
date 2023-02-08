# Dijkstra_best_path

## Opis projektu
Problem: Wytyczanie najszybszej drogi z punktu A do punktu B w mieście zakładając, że
niektóre ulicę są tymczasowo zamknięte.
Opis: Wykorzystanie algorytmu Dijkstry w modelowaniu samochodowego ruchu miejskiego,
z uwzględnieniem czasowego wyłączenia ulic. Problem projektu sprowadza się do
wyznaczania optymalnych obwodnic/ tras alternatywnych w mieście. Założono
niejednorodność gęstości sieci ulic oraz prędkości samochodów.

## Realizacja
Projekt został zrealizowany wykorzystując:
- Python
- Dash - to platforma typu open source do budowania interfejsów wizualizacji danych.
- OSMNX - pakiet Pythona, który umożliwia pobieranie danych geoprzestrzennych z
OpenStreetMap oraz modelowanie, projektowanie, wizualizowanie i analizowanie
rzeczywistych sieci ulic i wszelkich innych geometrii geoprzestrzennych.
do wyznaczania najkrótszej trasy wykorzystaliśmy algorytm Dijkstry który
zaimplementowano w funkcji Dijkstras_Shortest_Path klasy Graph:

Kod projektu znajduje się w repozytorium github:
https://github.com/Barthomieu/Dijkstra_best_path.git

## Instrukcja
Strona startowa projektu prezentuje się następująco,
![mainpage](https://user-images.githubusercontent.com/92340031/217549716-24fa7fb0-5485-485c-a11b-1900cb329160.jpg)

domyślnie pola Północ, Wschód, Południe, Zachód są ustalone na współrzędne Katowic
jednak można je zmienić wchodząc na stronę https://www.openstreetmap.org/ jest to
interfejs który współpracuje z biblioteką OSMNX. Po ustaleniu wycinka mapy który nas
interesuje, klikamy Eksport, który pokaże nam potrzebne współrzędne(pola zaznaczone na
zielono):
![map](https://user-images.githubusercontent.com/92340031/217549925-f5f27512-0f06-48eb-9c8e-d99380a03b4e.jpg)

w podobny sposób należy określić punkt startowy i punkt końcowy. Współrzędne punktów
również można określić przy pomocy portalu https://www.openstreetmap.org/ klikając PPM-
&gt;pokaż adres w określonym punkcie

Po uzupełnieniu wszystkich pól i kliknięciu przycisku “Szukaj najkrótszej trasy” przy pomocy
pakietu OSMNX zostanie wygenerowany graf którego wierzchołkami będa miejsca
przecięcie ulic:
![graf](https://user-images.githubusercontent.com/92340031/217550575-e2c42ad0-805e-4fb2-8f25-c096b401c872.jpg)

dodatkowo w pliku json zwracane są dane wierzchołków oraz odcinków które je łączą.
Poniżej fragment zwracanego pliku JSON w którym każdy wierzchołek jest opisany w
następujący sposób:
{&quot;type&quot;: &quot;node&quot;, &quot;id&quot;: 26310253, &quot;lat&quot;: 50.2500417, &quot;lon&quot;:
19.0022881},
natomiast każda krawędź będąca połączeniem wierzchołków w następujący sposób

{&quot;type&quot;: &quot;way&quot;, &quot;id&quot;: 29729269, &quot;nodes&quot;: [3109781806, 2003201137,
2137893310, 3109781794, 327480519], &quot;tags&quot;: {&quot;highway&quot;:
&quot;residential&quot;, &quot;lanes&quot;: &quot;1&quot;, &quot;name&quot;: &quot;1 Maja&quot;, &quot;oneway&quot;: &quot;yes&quot;,
&quot;surface&quot;: &quot;asphalt&quot;}}

Przy pomocy algorytmu Dijkstry zostaje wytyczona najkrótsza trasa
jako początkowy ustalona Budynek CNTI a jako punkt końcowy ustalono Budynek N.
w efekcie otrzymujemy najkrótszą trasę która wynosi 3990m
![trasa1](https://user-images.githubusercontent.com/92340031/217550631-4fa8d8eb-6489-4ad7-99b7-e850f4f12c6e.jpg)

aby zaznaczyć zamkniętą ulicę, należy wpisać jej nazwę w polu “wprowadź nazwę
zamkniętej ulicy” a następnie kliknąć przycisk “Szukaj nowej trasy”
na poniższym screenie występuje trasa przy założeniu zamknięcia ulicy 1 Maja, trasa
wydłużyła sie do 4449 metrów
![trasa2](https://user-images.githubusercontent.com/92340031/217550738-1a8583f1-7813-4afc-b404-cd7f33a06259.jpg)

Fragment pierwotnej trasy

Fragment nowej trasy:
