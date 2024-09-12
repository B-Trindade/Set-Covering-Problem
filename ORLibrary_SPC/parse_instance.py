"""

"""
import numpy as np 

def parse_instance(instance_name: str):
    """
    Lê o arquivo e interpreta a instância construindo o problema selecionado.
    """

    try:
        file_path = f'Instancias/{instance_name}.txt'

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
            Ji = np.array(data[k+1:row_len]) - 1
            Ji = Ji.tolist()
            
            J.append(Ji)
            k = row_len
        
        return m, n, col_costs, J

    except Exception as e:
        print(f'Instance not found or some error happened during parse.\n{e}')
        return None, None, None, None

if __name__ == "__main__":

    m,n,costs,J = parse_instance(instance_name="scp41")

    print(f"m = {m}")
    print(f"n = {n}")
    print(f"Custos = {costs}")
    for i in J[:2]:
        print(f"Amostra de Ji = {i}")