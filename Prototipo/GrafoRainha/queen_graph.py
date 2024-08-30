import math

def generate_queen_graph(board_size: int) -> dict:
    vertices: list = list(range(0, board_size**2+1))

    def generate_board_matrix() -> list[list]:
        matrix: list[list] = []
        row = []
        for v in vertices:
            if len(row) < board_size:
                row.append(v)
            else:
                matrix.append(row)
                row = [v]

        return matrix

    board_matrix: list[list] = generate_board_matrix()

    def get_vertice_position(vertice: int) -> tuple | bool:
        for row in board_matrix:
            if vertice in row:
                position: tuple = (board_matrix.index(row), row.index(vertice))
                return position

        return False

    def get_vertice_from_position(position: tuple) -> int:
        return board_matrix[position[0]][position[1]]

    def generate_edges() -> list[tuple]:
        edges: list[tuple] = []

        def generate_row(vertice: int) -> list[int]:
            row: list[int] = [i for i in range(vertice + 1, board_size + math.floor(vertice/board_size)*board_size)]
            #print(row)
            return row

        def generate_column(vertice: int) -> list[int]:
            column: list[int] = [i for i in range(vertice + board_size, board_size**2, board_size)]
            #print(column)
            return column

        def generate_right_diagonal(vertice: int) -> list[int]:
            right_diagonal: list[int] = [i for i in range(vertice + board_size + 1, board_size ** 2, board_size + 1)]
            #print(right_diagonal)
            return right_diagonal

        def generate_left_diagonal(vertice: int) -> list[int]:
            left_diagonal: list[int] = []
            for i in range(vertice + board_size - 1, board_size ** 2, board_size - 1):
                if board_matrix.index(board_matrix[get_vertice_position(i)[0]]) == board_matrix.index(board_matrix[get_vertice_position(vertice)[0]]):
                    break

                left_diagonal.append(i)
                #print(get_vertice_position(i))
                if board_matrix[get_vertice_position(i)[0]].index(i) == 0:
                    break

            #print(left_diagonal)
            return left_diagonal

        for v in vertices[0:-1]:
            #print(f'{v}')
            edges_row: list[tuple] = [(v, i) for i in generate_row(v)]
            #print(edges_row)
            edges_right_diagonal: list[tuple] = [(v, i) for i in generate_right_diagonal(v)]
            #print(edges_right_diagonal)
            edges_column: list[tuple] = [(v, i) for i in generate_column(v)]
            #print(edges_column)
            edges_left_diagonal: list[tuple] = [(v, i) for i in generate_left_diagonal(v)]
            #print(edges_left_diagonal)

            #print('\n\n')

            for edge in edges_row:
                edges.append(edge)

            for edge in edges_right_diagonal:
                edges.append(edge)

            for edge in edges_column:
                edges.append(edge)

            for edge in edges_left_diagonal:
                edges.append(edge)

        return edges

    def format_edges(edges: list[tuple]) -> list[list]:
        formatted_edges: list[list] = []
        for v in vertices[0:-1]:
            current_edge_list: list = []
            for edge in edges:
                if v == edge[0]:
                    current_edge_list.append(edge[1])
            formatted_edges.append(current_edge_list)

        return formatted_edges

    a = generate_board_matrix()
    for i in a:
        print(i)
    print('\n\n')

    edges: list[tuple] = generate_edges()
    formatted_edges: list[list] = format_edges(edges=edges)

    return {'V': vertices[0:-1], 'E': edges, 'E_formatted': formatted_edges}

    # def generate_edges() -> list[tuple]:
    #     for v in vertices:
    #         for i in range(board_size):


