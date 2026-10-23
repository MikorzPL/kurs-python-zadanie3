from pathlib import Path
from typy import FormatPliku
from typy import TrybPracy
from typy import PoraDnia
from typy import DzienTygodnia
from typy import Miesiac
import csv
from sciezki import obsluguj_sciezki

def csv_tester(file: Path, liczba_rekordow: int | None = None):
    with open(file, encoding="utf-8") as plik:
        dane = csv.DictReader(plik, delimiter=";")
        pola = dane.fieldnames
        assert pola is not None, f"Brak nagłówka w {file}"
        assert set(pola) == {"Model", "Wynik", "Czas"}, (f"Niepoprawny nagłówek w pliku {file}")
        rekordy = 0
        for rekord in dane:
            rekordy += 1
            assert rekord["Model"] in {"A", "B", "C"}, (
                f"Zły format kolumny 'Model' w {file} w rekordzie nr {rekordy}"
            )
            wynik = int(rekord["Wynik"]) 
            assert 0 <= wynik <= 1000, (
                f"Zły format kolumny 'Wynik' w {file} w rekordzie nr {rekordy}"
            )
            czas_str = rekord["Czas"]
            assert czas_str.endswith("s"), (
                f"Zły format kolumny 'Czas' w {file} w rekordzie nr {rekordy}. Czas nie kończy się 's'"
            )
            czas = int(czas_str[:-1])
            assert 0 <= czas <= 1000, (
                f"Zły format kolumny 'Czas' w {file} w rekordzie nr {rekordy}. Czas jest poza zakresem"
            )
        
        if liczba_rekordow is not None:
            assert rekordy == liczba_rekordow, f"Plik: {file} zawiera niepoprawną liczbę rekordów, która wynosi {rekordy}"
        else:
            assert rekordy > 0, f"Plik: {file} nie zawiera rekordów"
        
def test_sciezek(fs):
    dane = [
        (Miesiac.STYCZEN, DzienTygodnia.PONIEDZIALEK, PoraDnia.RANO),
        (Miesiac.STYCZEN, DzienTygodnia.WTOREK, PoraDnia.WIECZOR),
        (Miesiac.LUTY, DzienTygodnia.PIATEK, PoraDnia.RANO),
    ]
    tryb = TrybPracy.TWORZENIE
    format = FormatPliku.CSV
    obsluguj_sciezki(dane, tryb, format)
    sciezki = [
        Path(".") / "Styczeń" / "poniedziałek" / "rano" / "Dane.csv",
        Path(".") / "Styczeń" / "wtorek" / "wieczorem" / "Dane.csv",
        Path(".") / "Luty" / "piątek" / "rano" / "Dane.csv",
    ]

    for path in sciezki:
        assert path.exists(), f"Plik {path} nie istnieje"
        csv_tester(path, liczba_rekordow=1)