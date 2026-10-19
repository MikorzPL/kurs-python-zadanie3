from enum import Enum

class Miesiac(Enum):
    STYCZEN = 1
    LUTY = 2
    MARZEC = 3
    KWIECIEN = 4
    MAJ = 5
    CZERWIEC = 6
    LIPIEC = 7
    SIERPIEN = 8
    WRZESIEN = 9
    PAZDZIERNIK = 10
    LISTOPAD = 11
    GRUDZIEN =  12
    
class DzienTygodnia(Enum):
    PONIEDZIALEK = 1
    WTOREK = 2
    SRODA = 3
    CZWARTEK = 4
    PIATEK = 5
    SOBOTA = 6
    NIEDZIELA = 7

class PoraDnia(Enum):
    RANO = 1
    WIECZOR = 2