from typing import Literal
from enum import StrEnum

class Miesiac(StrEnum):
    STYCZEN = "styczeń"
    LUTY = "luty"
    MARZEC = "marzec"
    KWIECIEN = "kwiecień"
    MAJ = "maj"
    CZERWIEC = "czerwiec"
    LIPIEC = "lipiec"
    SIERPIEN = "sierpień"
    WRZESIEN = "wrzesień"
    PAZDZIERNIK = "październik"
    LISTOPAD = "listopad"
    GRUDZIEN =  "grudzień"
    
class DzienTygodnia(StrEnum):
    PONIEDZIALEK = "pn"
    WTOREK = "wt"
    SRODA = "śr"
    CZWARTEK = "czw"
    PIATEK = "pt"
    SOBOTA = "sb"
    NIEDZIELA = "nd"


class PoraDnia(StrEnum):
    RANO = "r"
    WIECZOR = "w"

class TrybPracy(StrEnum):
    TWORZENIE = "t"
    ODCZYT = "o"

class FormatPliku(StrEnum):
    CSV = "c"
    JSON = "j"

    @property
    def pelna_nazwa(self) -> Literal['csv', 'json']:
        return "json" if self.value == "json" else "csv"