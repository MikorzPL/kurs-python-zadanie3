import argparse
from typy import Miesiac, DzienTygodnia, PoraDnia, TrybPracy, FormatPliku
from sciezki import obsluguj_sciezki

OPIS_PROGRAMU = """Skrypt służy do tworzenia lub czytania plików w złożonej strukturze katalogów. 
Struktura obejmuje: Poziom 1 - miesiące; Poziom 2 - dni tygodnia; Poziom 3 - rano/wieczór; Poziom 4 - pliki csv/json.

Zasady przekazywania parametrów i działania:
- Należy podać taką samą liczbę argumentów dla zakresu dni, co dla wybranych miesięcy.
- Parametry pory dnia podaje się dla każdego z dni wynikłych z rozpisania zakresów. 
- Nie podane parametry pory dnia przyjmują wartość domyślną (rano).
- W zależności od parametrów, skrypt pozwala utworzyć pliki zadanego typu albo wczytać pliki zadanego typu i podać wynik.
- Operacja odczytu zwraca sumę wartości z kolumny 'Czas' dla wszystkich plików, gdzie w kolumnie 'Model' mamy wartość 'A'.
- Przy braku pliku zadanego do odczytu wypisze komunikat i będzie kontynuował działanie.
- Przy próbie stworzenia już istniejącego pliku program pominie ten plik."""


def rozwin_zakres(zakres: str) -> list[DzienTygodnia]:
    wszystkie_dni = list(DzienTygodnia)

    if "-" in zakres:
        elementy = zakres.split("-")

        if len(elementy) != 2:
            raise ValueError(f"Nieprawidłowy format zakresu '{zakres}'. Użyj dokładnie jednego myślnika, np. 'pn-pt'.")

        poczatek_str, koniec_str = elementy
            
        poczatek = DzienTygodnia(poczatek_str)
        koniec = DzienTygodnia(koniec_str)

        indeks_poczatku = wszystkie_dni.index(poczatek)
        indeks_konca = wszystkie_dni.index(koniec)

        if indeks_konca < indeks_poczatku:
            raise ValueError(f"Odwrotny zakres '{zakres}'. Dzień początkowy musi być przed końcowym.")
            
        return wszystkie_dni[indeks_poczatku:indeks_konca + 1]
        
    return [DzienTygodnia(zakres)]


def parsuj_argumenty():
    """
    Funkcja pobiera argumenty przekazane do programu i obsługuje polecenia użytkownika wywołując odpowiednie funkcje (jak sciezki.obsluguj_sciezki()).
    """

    parser = argparse.ArgumentParser(description=OPIS_PROGRAMU, formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("-m", "--miesiace", nargs="+", type=Miesiac, required=True, help="Wybór miesięcy których dotyczy zapytanie.")
    parser.add_argument("-d", "--dni", nargs="+", required=True, help="Wybór zakresu dni tygodnia których dotyczy zapytanie (mogą być podawane w formie przedziału). Należy podać dokładnie jeden dzień/przedział na każdy podany miesiąc.")
    parser.add_argument("-p", "--pory", nargs="*", type=PoraDnia, default=[], help="Wybór pory dnia: r (rano) albo w (wieczorem), domyślnie rano. Można dokonać wyboru dla każdego dnia wynikającego z wyboru dni.")
    parser.add_argument("-t", "--tryb", type=TrybPracy, required=True, help="Wybór opcji działania: t (tworzenie) lub o (odczyt).")
    parser.add_argument("-f", "--format", type=FormatPliku, required=True, help="Wybór formatu docelowego pliku: c (csv) lub j (json)")

    args = parser.parse_args()

    if len(args.miesiace) != len(args.dni):
        parser.error("Liczba podanych miesięcy musi być równa liczbie podanych zakresów dni.")

    lista_zapytan = []

    try:
        for miesiac, dni in zip(args.miesiace, args.dni):
            zakres_dni = rozwin_zakres(dni)

            for dzien in zakres_dni:
                if len(args.pory) > 0:
                    pora = args.pory.pop(0)
                else:
                    pora = PoraDnia.RANO
                
                lista_zapytan.append((miesiac, dzien, pora))

    except ValueError as e:
        parser.error(str(e))

    if len(args.pory) > 0:
        parser.error(f"Za dużo wartości pora dnia. Użyj maksymalnie tylu wartości, ile dni wynika z twojego zapytania.")

    return lista_zapytan, args.tryb, args.format


if __name__ == "__main__":
    lista_zapytan, tryb_pracy, format_pliku = parsuj_argumenty()
    obsluguj_sciezki(lista_zapytan, tryb_pracy, format_pliku)