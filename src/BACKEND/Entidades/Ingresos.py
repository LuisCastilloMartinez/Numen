from dataclasses import dataclass 
import datetime
from time import strftime

@dataclass
class Ingresos:
    id_usuarios:int
    monto:float
    fecha: datetime.now().strftime("%Y-%m-%d")
    tipo_enum:str