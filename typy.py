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
    
    @property
    def pelna_nazwa(self) -> str:
        return self.value.capitalize()
    
class DzienTygodnia(StrEnum):
    PONIEDZIALEK = "pn"
    WTOREK = "wt"
    SRODA = "śr"
    CZWARTEK = "czw"
    PIATEK = "pt"
    SOBOTA = "sb"
    NIEDZIELA = "nd"

    @property
    def pelna_nazwa(self) -> str:
        nazwy = {
            DzienTygodnia.PONIEDZIALEK: "poniedziałek",
            DzienTygodnia.WTOREK: "wtorek",
            DzienTygodnia.SRODA: "środa",
            DzienTygodnia.CZWARTEK: "czwartek",
            DzienTygodnia.PIATEK: "piątek",
            DzienTygodnia.SOBOTA: "sobota",
            DzienTygodnia.NIEDZIELA: "niedziela",
        }
        return nazwy.get(self, "nieznany")

class PoraDnia(StrEnum):
    RANO = "r"
    WIECZOR = "w"

    @property
    def pelna_nazwa(self) -> Literal['rano', 'wieczorem']:
        return "rano" if self.value == "r" else "wieczorem"

class TrybPracy(StrEnum):
    TWORZENIE = "t"
    ODCZYT = "o"

class FormatPliku(StrEnum):
    CSV = "c"
    JSON = "j"

    @property
    def pelna_nazwa(self) -> Literal['csv', 'json']:
        return "json" if self.value == "j" else "csv"