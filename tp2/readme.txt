La clase Graph tiene los siguientes campos:
    x: Dict[int,List[float]]                        - diccionario con los valores de x
    y: Dict[int,List[float]]                        - diccionario con los valores de y
    row: int                                        - numero de filas
    col: int                                        - numero de columnas
    n_plots: int = None                             - numero total de plots. Por defecto el largo de x.
    joinVec: Dict[int,List[int]]                    - diccionario con el arreglo de posicionamiento
    typeGraf: Dict[int,GRAPHTYPE]                   - diccionario con los tipos: plot, stem, scatter. Plot por defecto
    xlim: Optional[Dict[int, List[float]]] = None   - diccionario con xlim (opcional)
    ylim: Optional[Dict[int, List[float]]] = None   - diccionario con ylim (opcional)
    show: bool                                      - show plot
    xlabel: Optional[Dict[int, str]] = None         - diccionario con xlabel (opcional)
    ylabel: Optional[Dict[int, str]] = None         - diccionario con ylabel (opcional)

El script ejemplo crea los datos necesarios para utilizar la clase Graph:

*N es el numero de graficos a realizar. N=7
*L es un vector aleatorio con el largo de los datos a plotear.
*y son vectores de datos aleatorios de largo L.
*row=5.
*col=3.
*Joinvec pretende mostrar de la siguiente los graficos:
    0  1  2
    3  4  2
    6  6  2
    6  6  5
    6  6  5

* xlim, ylim, xlabel, ylabel son diccionarios aleatorios que setean algunos de los graficos.
  Si no se setean los limites en algun plot usa los que vienen por defecto.
  Si no se setean los labels en algun plot no escribe nada.

* El script realiza todo tipo de verificacion sobre los datos y
  se puede setear de cualquier forma horizontal y vertical que se verifica si no hay
  overlap, agrega un print de pantalla para observar donde se encuentra el overlap.

* No hay restriccion recpecto a donde agregar los label (no se superponen)  