from enum import Enum
from typing import Dict, List
from pydantic import BaseModel,field_validator
import numpy as np

class UserRole(Enum):
    STEM = "stem"
    PLOT = "plot"
    
class Graph(BaseModel): 
    x: Dict[int,List[float]]
    y: Dict[int,List[float]]
    row: int
    col: int
    n_plots: int = None
    #joinVec: Dict[int,List[int,int]]
    # numplot: int
    # show: bool
    # typeGraf: UserRole
    # xlim: Dict[int, tuple]
    # ylim: Dict[int, tuple]
    # xlabel: Dict[str, tuple]
    # ylabel: Dict[str, tuple]

    @field_validator('row', 'col')
    def validate_integers(cls, value):
        if value <= 0:
            raise ValueError("Col and Row have to be integers >0")
        return value
    
    def validate_vectors(cls, x,y):
        if not(x.keys() == y.keys()):
            raise ValueError("x and y have to have the same keys")
        
        for index,arr in enumerate(x.keys()):
            if not(len(x[index]) == len(y[index])):
                raise ValueError("x and y have to have the same vectors length")

    def validate_n_plots(cls,self):
        if self.n_plots > self.col*self.row:
            raise ValueError("there are more vectors than possible position to plot")
    
    def __init__(self, **data):
        super().__init__(**data)  
        self.validate_vectors(self.x,self.y)
        self.n_plots = len(self.x.keys())
        self.validate_n_plots(self)



x = {}
a = [1,2,3]
for i in range(10):
    x[i] = (np.array(a)) 

y = {}
a = [1,2,3]
for i in range(10):
    y[i] = (np.array(a)) 


obj_in = {'x': x,'y': y, 'row':5, 'col':3}
try:
    a = Graph(**obj_in)
except ValueError as e:
    print(e)



# figPlot(x, y, row, col, joinVec, numplot, show=False, typeGraf, xlim, ylim, xlabel,
# ylabel)
# • x, y : Rango de valores a graficar. Se ingresan tantos vectores como gráficos a
# realizar.
# • row, col : Filas y columnas de la figura.
# • joinVec : Vector que especifica como se agrupan los gráficos. Ej. row,col: 3,3.
# joinVec:(1,3),4,5,6,(7,9).
# • numplot : Nombre del plot en número, el cual se incluye en figure(numplot).
# • show : Habilita el gráfico.
# • typeGraf : Selecciona el tipo de gráfico en plot o stem y se deben ingresar tantos
# tipos como gráficos a realizar.
# • xlim, ylim : Lı́mites de los ejes y se deben pasar tantos lı́mites como gráficos a
# realizar.
# • xlabel, ylabel : Nombre de los ejes X e Y pero s


    # id: int = Field(..., description="The unique identifier for the user")
    # username: str = Field(..., max_length=50, description="The username of the user")
    # email: EmailStr = Field(..., description="The email address of the user")
    # full_name: Optional[str] = Field(None, max_length=100, description="The full name of the user")
    # is_active: bool = Field(True, description="Indicates if the user is active")

