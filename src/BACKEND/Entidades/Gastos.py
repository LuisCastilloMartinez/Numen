from dataclasses import dataclass 
import datetime
from time import strftime


@dataclass
class Gastos:
    id_usuaio:int
    id_ingreso:int
    monto:float
    fecha: datetime.now().strftime("%Y-%m-%d")
    tipo_enum:str