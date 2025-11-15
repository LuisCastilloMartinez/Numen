from dataclasses import dataclass 
import datetime
from time import strftime

@dataclass
class Categoria_Gastos:
    id_categoria:int
    nombre:int
    tipo_sugerido: str
    icono:str