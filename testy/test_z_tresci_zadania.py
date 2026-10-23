from pathlib import Path
from typing import Callable, List, Tuple, Dict
from pyfakefs.fake_filesystem import FakeFilesystem
import pytest
from typy import Miesiac, DzienTygodnia, PoraDnia, TrybPracy, FormatPliku
import csv
import json
from sciezki import obsluguj_sciezki
from unittest.mock import Mock

def dict_assert(rekord: Dict[str, str], file: Path, nr_rekordu: int) -> None:
        assert rekord["Model"] in {"A", "B", "C"}, (
            f"Zły format kolumny 'Model' w {file} w rekordzie nr {nr_rekordu}"
        )
        try:
            wynik = int(rekord["Wynik"])
            assert 0 <= wynik <= 1000
        except (ValueError, AssertionError):
            pytest.fail(f"Zły format kolumny 'Wynik' w {file} w rekordzie nr {nr_rekordu}")

        try:
            czas_str = rekord["Czas"]
            assert czas_str.endswith("s")
            czas = int(czas_str[:-1])
            assert 0 <= czas <= 1000
        except (ValueError, AssertionError):
            pytest.fail(f"Zły format kolumny 'Czas' w {file} w rekordzie nr {nr_rekordu}. Czas nie kończy się 's'")

def csv_assert(file: Path, liczba_rekordow: int | None = None) -> None:
    with open(file, encoding="utf-8") as plik:
        dane = csv.DictReader(plik, delimiter=";")
        pola = dane.fieldnames
        assert pola is not None, f"Brak nagłówka w {file}"
        assert list(pola) == ["Model", "Wynik", "Czas"], (f"Niepoprawny nagłówek w pliku {file}")
        rekordy = 0
        for rekord in dane:
            rekordy += 1
            dict_assert(rekord, file, rekordy)

        if liczba_rekordow is not None:
            assert rekordy == liczba_rekordow, f"Plik: {file} zawiera niepoprawną liczbę rekordów, która wynosi {rekordy}"
        else:
            assert rekordy > 0, f"Plik: {file} nie zawiera rekordów"

def json_assert(file: Path) -> None:
    with open(file, encoding="utf-8") as plik:
        rekord = json.load(plik)
        assert list(rekord) == ["Model", "Wynik", "Czas"]
        dict_assert(rekord, file, 1)

def stworz_json(file: Path) -> None:
    file.write_text('{"Model": "A", "Wynik": 17, "Czas": "465s"}', encoding="utf-8")

def stworz_csv(file: Path) -> None:
    file.write_text("Model;Wynik;Czas\nA;17;465s", encoding="utf-8")

@pytest.fixture
def dane_przyklad() -> List[Tuple[Miesiac, DzienTygodnia, PoraDnia]]:
    return [
        (Miesiac.STYCZEN, DzienTygodnia.PONIEDZIALEK, PoraDnia.RANO),
        (Miesiac.STYCZEN, DzienTygodnia.WTOREK, PoraDnia.WIECZOR),
        (Miesiac.LUTY, DzienTygodnia.PIATEK, PoraDnia.RANO),
    ]


@pytest.fixture
def sciezki_przyklad() -> List[Path]:
    return [
        Path(".") / "Styczeń" / "poniedziałek" / "rano",
        Path(".") / "Styczeń" / "wtorek" / "wieczorem",
        Path(".") / "Luty" / "piątek" / "rano",
    ]


@pytest.mark.parametrize("assert_formatu, format", [
    (csv_assert, FormatPliku.CSV),
    (json_assert, FormatPliku.JSON),
])
def test_sciezek_tworzenie(
    fs: FakeFilesystem,
    dane_przyklad: List[Tuple[Miesiac, DzienTygodnia, PoraDnia]],
    assert_formatu: Callable[[Path], None],
    format: FormatPliku,
    sciezki_przyklad: List[Path]
    ):
    tryb = TrybPracy.TWORZENIE
    obsluguj_sciezki(dane_przyklad, tryb, format)
    sciezki = [sciezka / ("Dane." + format.pelna_nazwa) for sciezka in sciezki_przyklad]
    for path in sciezki:
        assert path.exists(), f"Plik {path} nie istnieje"
        assert_formatu(path)

@pytest.mark.parametrize("funkcja_tworzaca_format, format", [
    (stworz_csv, FormatPliku.CSV),
    (stworz_json, FormatPliku.JSON),
])
def test_sciezek_odczyt(
    fs: FakeFilesystem,
    funkcja_tworzaca_format: Callable[[Path], None],
    format: FormatPliku,
    sciezki_przyklad: List[Path],
    dane_przyklad: List[Tuple[Miesiac, DzienTygodnia, PoraDnia]]
    ):
    sciezki = [sciezka / ("Dane." + format.pelna_nazwa) for sciezka in sciezki_przyklad]
    for sciezka in sciezki:
        fs.create_file(sciezka)
        funkcja_tworzaca_format(sciezka)
    
    mock_zapisz = Mock()
    obsluguj_sciezki(dane_przyklad, TrybPracy.ODCZYT, format, mock_zapisz)
    poprawny_wynik = 465 * len(sciezki)
    mock_zapisz.assert_called_once_with(poprawny_wynik)