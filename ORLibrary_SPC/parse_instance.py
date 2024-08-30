"""

"""

def parse_instance(instance_name: str):
    """
    Lê o arquivo e interpreta a instância construindo o problema selecionado.
    """
    file_path = f'./{instance_name}.txt'

    with open(file_path, 'r') as file:
        # Passa os valores lidos para uma lista de inteiros
        data = list(map(int, file.read().split())) 

    m = data[0] # número de linhas
    n = data[1] # número de colunas
    col_costs = data[2:n+2]

    J = []
    k = n+2
    for _ in range(m):
        # print(data[k])
        row_len = k+1 + data[k]
        Ji = data[k+1:row_len]

        J.append(Ji)
        k = row_len

    return m, n, col_costs, J


if __name__ == "__main__":

    m,n,I,J = parse_instance(instance_name="scp41")

    print(f"m = {m}")
    print(f"n = {n}")
    print(f"I = {I}")
    for i in J[:2]:
        print(f"Amostra de Ji = {i}")