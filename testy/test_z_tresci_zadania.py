from pathlib import Path
from typing import List, Tuple, Dict, Protocol
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


class ObslugujacyFormat(Protocol):
    format_pliku: FormatPliku
    format_arg: str

    def sprawdz_plik(self, sciezka: Path, liczba_rekordow: int | None = None) -> None:
        ...

    def stworz_plik(self, sciezka: Path) -> None:
        ...


class ObslugaCsv:
    format_pliku: FormatPliku = FormatPliku.CSV
    format_arg: str = "c"

    def sprawdz_plik(self, sciezka: Path, liczba_rekordow: int | None = None) -> None:
        with open(sciezka, encoding="utf-8") as plik:
            dane = csv.DictReader(plik, delimiter=";")
            pola = dane.fieldnames
            assert pola is not None, f"Brak nagłówka w {sciezka}"
            assert list(pola) == ["Model", "Wynik", "Czas"], f"Niepoprawny nagłówek w pliku {sciezka}"
            rekordy = 0
            for rekord in dane:
                rekordy += 1
                dict_assert(rekord, sciezka, rekordy)

            if liczba_rekordow is not None:
                assert rekordy == liczba_rekordow, (
                    f"Plik: {sciezka} zawiera niepoprawną liczbę rekordów, która wynosi {rekordy}"
                )
            else:
                assert rekordy > 0, f"Plik: {sciezka} nie zawiera rekordów"

    def stworz_plik(self, sciezka: Path) -> None:
        sciezka.write_text("Model;Wynik;Czas\nA;17;465s", encoding="utf-8")


class ObslugaJson:
    format_pliku: FormatPliku = FormatPliku.JSON
    format_arg: str = "j"

    def sprawdz_plik(self, sciezka: Path, liczba_rekordow: int | None = None) -> None:
        with open(sciezka, encoding="utf-8") as plik:
            rekord = json.load(plik)
            assert list(rekord) == ["Model", "Wynik", "Czas"]
            dict_assert(rekord, sciezka, 1)

    def stworz_plik(self, sciezka: Path) -> None:
        sciezka.write_text('{"Model": "A", "Wynik": 17, "Czas": "465s"}', encoding="utf-8")


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


@pytest.mark.parametrize("pomocnik_formatu", [
    ObslugaCsv(),
    ObslugaJson(),
])
def test_sciezek_tworzenie(
    fs: FakeFilesystem,
    dane_przyklad: List[Tuple[Miesiac, DzienTygodnia, PoraDnia]],
    pomocnik_formatu: ObslugujacyFormat,
    sciezki_przyklad: List[Path]
):
    tryb = TrybPracy.TWORZENIE
    format_pliku = pomocnik_formatu.format_pliku
    obsluguj_sciezki(dane_przyklad, tryb, format_pliku)
    sciezki = [sciezka / ("Dane." + format_pliku.pelna_nazwa) for sciezka in sciezki_przyklad]
    for path in sciezki:
        assert path.exists(), f"Plik {path} nie istnieje"
        pomocnik_formatu.sprawdz_plik(path)


@pytest.mark.parametrize("pomocnik_formatu", [
    ObslugaCsv(),
    ObslugaJson(),
])
def test_sciezek_odczyt(
    fs: FakeFilesystem,
    pomocnik_formatu: ObslugujacyFormat,
    sciezki_przyklad: List[Path],
    dane_przyklad: List[Tuple[Miesiac, DzienTygodnia, PoraDnia]]
):
    format_pliku = pomocnik_formatu.format_pliku
    sciezki = [sciezka / ("Dane." + format_pliku.pelna_nazwa) for sciezka in sciezki_przyklad]
    for sciezka in sciezki:
        fs.create_file(sciezka)
        pomocnik_formatu.stworz_plik(sciezka)

    mock_zapisz = Mock()
    obsluguj_sciezki(dane_przyklad, TrybPracy.ODCZYT, format_pliku, mock_zapisz)
    poprawny_wynik = 465 * len(sciezki)
    mock_zapisz.assert_called_once_with(poprawny_wynik)