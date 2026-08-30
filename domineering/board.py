import math


class Board:
    """Clase base que representa una matriz bidimensional para tableros."""

    __places: list[list[str]]  # Tablero en sí.
    __size: int  # Tamaño del tablero.
    
    EMPTY_SPACE = "."  # Constante de clase que marca los espacios vacíos.
    
    def __init__(self, n: int = 3):
        """Inicializa un tablero cuadrado de tamaño n x n."""
        # Define la lista de listas para almacenar las posiciones.
        self.__places = [
            [Board.EMPTY_SPACE] * n for _ in range(n)
        ]
        self.__size = n

    def __str__(self) -> str:
        """Genera la representación en cadena del tablero para impresión."""
        # Cantidad de caracteres para la columna con número de fila.
        offset = math.ceil(math.log10(self.__size))
        
        # Asegura un ancho mínimo para que las letras no queden pegadas.
        ancho_columna = max(offset, 2)
        
        # Primera línea: espacio inicial para cuadrar los encabezados.
        board = " " * ancho_columna
        
        # Toma el número i y lo obliga a ocupar el espacio definido.
        for i in range(1, self.__size + 1):
            board += f" {i:>{ancho_columna}}"
        board += "\n"
        
        # Itera sobre las filas para generar el contenido de la matriz.
        for i, line in enumerate(self.__places, 1):
            # Alinea el número de la fila a la derecha.
            board += f"{i:>{ancho_columna}}"
            
            # Alinea cada celda (letras o puntos) con el mismo ancho exacto.
            for elemento in line:
                board += f" {elemento:>{ancho_columna}}"
            board += '\n'
            
        return board

    def __repr__(self) -> str:
        """Devuelve la representación formal del objeto (útil para depurar)."""
        return f"Board({self.__size})"

    def __len__(self) -> int:
        """Permite usar len() para obtener la dimensión del tablero."""
        return self.__size

    def __check_valid_range(self, r: int) -> bool:
        """
        Valida que el índice provisto esté dentro del rango del tablero.
        
        Considera que las posiciones del tablero van de 1 a n.
        """
        # Los nombres con doble guion bajo inicial sufren 'name mangling'
        # para emular el comportamiento de métodos o atributos privados.
        if 1 > r or r > self.__size:
            return False
        return True

    def __getitem__(self, subscript: int | tuple):
        """
        Permite el acceso a los elementos usando indexación (self[subscript]).
        
        El parámetro `subscript` puede ser un entero (fila) o una tupla de
        coordenadas. Levanta excepciones si los índices no son correctos.
        """
        if isinstance(subscript, tuple):
            # Lógica para cuando el índice es una tupla de coordenadas.
            
            # Verifica que no haya más ni menos dimensiones que filas y columnas.
            if len(subscript) != 2:
                raise ValueError("Cooordinates with too many dimensions")
                
            # Valida que la fila solicitada no esté fuera del rango.
            if not self.__check_valid_range(subscript[0]):
                raise LookupError(f"Row out of range: {subscript[0]}")
                
            # Valida que la columna solicitada no esté fuera del rango.
            if not self.__check_valid_range(subscript[1]):
                raise LookupError(f"Column out of range: {subscript[1]}")
                
            # Retorna el valor (ajustando índices de base-1 a base-0).
            return self.__places[subscript[0] - 1][subscript[1] - 1]
            
        elif isinstance(subscript, int):
            # Lógica para cuando el índice es un entero (petición de fila).
            
            if not self.__check_valid_range(subscript):
                raise LookupError(f"Row out of range: {subscript}")
                
            # Retorna la fila completa (ajustando el índice a base-0).
            return self.__places[subscript - 1]
            
        else:
            # Si el tipo de dato del índice no es soportado.
            raise TypeError("Subscript must be integer or coordinates")
    
    def __setitem__(self, key: tuple, value: str) -> None:
        """
        Permite la asignación de valores usando coordenadas (self[key] = value).
        
        La `key` ingresada debe ser estrictamente un par de coordenadas.
        """
        if not isinstance(key, tuple):
            raise TypeError(
                f"Subscript must be coordinates (tuple), not {type(key)}"
            )
            
        if len(key) != 2:
            raise ValueError("Cooordinates with too many dimensions")
            
        # Valida que la fila solicitada no esté fuera del rango.
        if not self.__check_valid_range(key[0]):
            raise LookupError(f"Row out of range: {key[0]}")
            
        # Valida que la columna solicitada no esté fuera del rango.
        if not self.__check_valid_range(key[1]):
            raise LookupError(f"Column out of range: {key[1]}")
            
        # Asigna el valor en la matriz (ajustando índices de base-1 a base-0).
        self.__places[key[0] - 1][key[1] - 1] = value

    def valid_move(self, r: int, c: int):
        """
        Valida que un movimiento se realice hacia una casilla desocupada.
        
        Este método está diseñado para ser sobrecargado por clases hijas
        que requieran reglas de validación adicionales.
        """
        return self[r, c] == Board.EMPTY_SPACE