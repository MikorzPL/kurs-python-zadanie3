from pathlib import Path
import sys
from typing import List
from unittest.mock import Mock
from pyfakefs.fake_filesystem import FakeFilesystem
import pytest
from testy.test_z_tresci_zadania import ObslugaCsv, ObslugaJson, ObslugujacyFormat, sciezki_przyklad
from main import main

@pytest.mark.parametrize("pomocnik_formatu", [
    ObslugaCsv(),
    ObslugaJson(),
])
def test_calosc_tworzenie(
    fs: FakeFilesystem,
    monkeypatch: pytest.MonkeyPatch,
    pomocnik_formatu: ObslugujacyFormat,
    sciezki_przyklad: List[Path]
):
    format_pliku = pomocnik_formatu.format_pliku
    format_arg = pomocnik_formatu.format_arg
    sciezki = [sciezka / ("Dane." + format_pliku.pelna_nazwa) for sciezka in sciezki_przyklad]

    argumenty = [
        "main.py",
        "-m", "styczeń", "luty",
        "-d", "pn-wt", "pt",
        "-p", "r", "w",
        "-t", "t",
        "-f", format_arg
    ]
    monkeypatch.setattr(sys, "argv", argumenty)
    main()
    for sciezka in sciezki:
        assert sciezka.exists(), f"Plik {sciezka} nie istnieje"
        pomocnik_formatu.sprawdz_plik(sciezka)

@pytest.mark.parametrize("pomocnik_formatu", [
    ObslugaCsv(),
    ObslugaJson(),
])
def test_calosc_odczyt(
    fs: FakeFilesystem,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    pomocnik_formatu: ObslugujacyFormat,
    sciezki_przyklad: List[Path]
):
    format_pliku = pomocnik_formatu.format_pliku
    format_arg = pomocnik_formatu.format_arg
    sciezki = [sciezka / ("Dane." + format_pliku.pelna_nazwa) for sciezka in sciezki_przyklad]
    for sciezka in sciezki:
        fs.create_file(sciezka)
        pomocnik_formatu.stworz_plik(sciezka)

    argumenty = [
        "main.py",
        "-m", "styczeń", "luty",
        "-d", "pn-wt", "pt",
        "-p", "r", "w",
        "-t", "o",
        "-f", format_arg
    ]
    monkeypatch.setattr(sys, "argv", argumenty)
    main()
    out = capsys.readouterr()
    poprawny_wynik = 465 * len(sciezki)
    # test będzie błędny jeśli zmienimy schemat printowania wyniku
    assert out.out == f'Suma czasu modeli "A": wynik={poprawny_wynik}\n'
    assert out.err == ""
