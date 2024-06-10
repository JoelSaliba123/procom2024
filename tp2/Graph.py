from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel,field_validator
import matplotlib.pyplot as plt
import numpy as np

class GRAPHTYPE(Enum):
    STEM = "stem"
    PLOT = "plot"
    SCATTER = 'scatter'
    
class Graph(BaseModel): 
    x: Dict[int,List[float]]
    y: Dict[int,List[float]]
    row: int
    col: int
    n_plots: int = None
    joinVec: Dict[int,List[int]]
    typeGraf: Dict[int,GRAPHTYPE] 
    xlim: Optional[Dict[int, List[float]]] = None
    ylim: Optional[Dict[int, List[float]]] = None
    show: bool
    xlabel: Optional[Dict[int, str]] = None
    ylabel: Optional[Dict[int, str]] = None

    @field_validator('row', 'col')
    def validate_integers(cls, value):
        if value <= 0:
            raise ValueError("Col and Row have to be integers >0")
        return value
    
    @field_validator('xlim', 'ylim')
    def check_limits(cls, v):
        if v is not None:
            for key, val in v.items():
                if len(val) != 2:
                    raise ValueError(f"List for key {key} must contain exactly two floats.")
                if val[0] >= val[1]:
                    raise ValueError(f"First value must be less than the second value for key {key}.")
        return v

    def check_keys(cls,self):
        if not(self.x.keys() == self.y.keys() == self.joinVec.keys() ):
            raise ValueError("JoinVec, typeGraf, x and y have to have the same keys")
        
        if self.xlim is not None:
            invalid_keys = [key for key in self.xlim.keys() if key not in self.x.keys()]
            if invalid_keys:
                raise ValueError(f"The following keys in xlim are not present in x: {invalid_keys}")
        
        if self.ylim is not None:
            invalid_keys = [key for key in self.ylim.keys() if key not in self.y.keys()]
            if invalid_keys:
                raise ValueError(f"The following keys in ylim are not present in y: {invalid_keys}")
        
        if self.typeGraf is not None:
            invalid_keys = [key for key in self.typeGraf.keys() if key not in self.y.keys()]
            if invalid_keys:
                raise ValueError(f"The following keys in typeGraf are not present in y: {invalid_keys}")
        

        if self.xlabel is not None:
            invalid_keys = [key for key in self.xlabel.keys() if key not in self.x.keys()]
            if invalid_keys:
                raise ValueError(f"The following keys in xlabel are not present in x: {invalid_keys}")
        
        if self.ylabel is not None:
            invalid_keys = [key for key in self.ylabel.keys() if key not in self.y.keys()]
            if invalid_keys:
                raise ValueError(f"The following keys in ylabel are not present in y: {invalid_keys}")

    def validate_vectors(cls, x,y):
        for index,arr in enumerate(x.keys()):
            if not(len(x[index]) == len(y[index])):
                raise ValueError("x and y have to have the same vectors length")
            
    def validate_joinVec(cls,self):
        matrix_validation = np.zeros((self.row*self.col,1))
        for index,dump in enumerate(self.joinVec.keys()):
            pos_len = len(self.joinVec[index])
           
            if pos_len==1:
                arr=self.joinVec[index][0]
                if 0<arr<self.row*self.col:
                    matrix_validation[arr-1] = (matrix_validation[arr-1])+1
                else:
                    raise ValueError('Index cannot be <0 or >{}'.format(self.row*self.col))
            elif pos_len==2:

                position = self.joinVec[index]

                if position[0]>position[1]:
                    raise ValueError('Wrong agrupation')

                row_index1 = np.ceil(position[0]/self.col)
                row_index2 = np.ceil(position[1]/self.col)
                
                if row_index1==row_index2:
                
                    distance = position[1]-position[0] 
                    for i in range(distance+1):
                        matrix_validation[position[0]+i-1] = (matrix_validation[position[0]+i-1])+1
                else:
                    col_pos1 = (position[0]%(self.col))
                    col_pos2 = (position[1]%(self.col))

                    if col_pos1>col_pos2 and col_pos2!=0:
                        raise ValueError('Wrong agrupation')
                        
                    if col_pos2==0 and col_pos1==0:
                        row_distance = 1
                    elif col_pos2==0:
                        row_distance=self.col-(col_pos1-1)
                    else:
                        row_distance=col_pos2-(col_pos1-1)

                    col_distance = int(row_index2 - row_index1)+1

                    for i in range(col_distance):
                        for j in range(row_distance):
                            matrix_validation[position[0]+i*self.col+j-1] = (matrix_validation[position[0]+i*self.col+j-1])+1

            else:
                raise ValueError("Plot agrupations cannot have more than 2 dimensions")
        
        for i in matrix_validation: 
            if i>1:
                matrix_validation = matrix_validation.reshape((self.row,self.col))
                raise ValueError("OVERLAP!!!\n\n{}".format((matrix_validation)))
        
        matrix_validation = matrix_validation.reshape((self.row,self.col))
        print(matrix_validation)

    def validate_n_plots(cls,self):
        if self.n_plots > self.col*self.row:
            raise ValueError("there are more vectors than possible position to plot")

    def create_figure(self):
        plt.figure(figsize=[14,14])
        for arr in self.joinVec.keys():
            if len(self.joinVec[arr])>1:
                plt.subplot(self.row,self.col,(self.joinVec[arr][0],self.joinVec[arr][1]))
            else:
                plt.subplot(self.row,self.col,self.joinVec[arr][0])

            try:
                if self.typeGraf[arr] == GRAPHTYPE.PLOT:
                    plt.plot(self.x[arr],self.y[arr])
                elif self.typeGraf[arr] == GRAPHTYPE.STEM:
                    plt.stem(self.x[arr],self.y[arr])
                elif self.typeGraf[arr] == GRAPHTYPE.SCATTER:
                    plt.scatter(self.x[arr],self.y[arr])
            except:
                plt.plot(self.x[arr],self.y[arr])
            
            try:
                if self.xlim is not None:
                    plt.xlim(self.xlim[arr])
            except:
                pass

            try:
                if self.ylim is not None:
                    plt.ylim(self.ylim[arr]) 
            except:
                pass

            try:
                if self.xlabel is not None:
                    plt.xlabel(self.xlabel[arr])
            except:
                pass
            
            try:
                if self.ylabel is not None:
                    plt.ylabel(self.ylabel[arr])
            except:
                pass

            plt.grid()

        plt.tight_layout(pad=4.0)
            
        if self.show:
            plt.show()


    def __init__(self, **data):
        super().__init__(**data)  
        self.validate_vectors(self.x,self.y)
        self.n_plots = len(self.x.keys())
        self.validate_n_plots(self)
        self.check_keys(self)
        self.validate_joinVec(self)
