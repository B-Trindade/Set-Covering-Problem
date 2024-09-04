import cplex
import requests
from pathlib import Path


def get_data(instance_url: str):
    """
    Recebe um URL para uma instância na OR-Lib e armazena os dados localmente.
    """

    # Extrai o nome da instancia do URL
    instance_name = instance_url.split('/')[-1]

    # Envia uma requisição HTTP GET para pegar os dados
    response = requests.get(instance_url)

    if response.status_code == 200:
        # Cria diretório para instâncias caso não exista
        Path("/Instancias").mkdir(parents=True, exist_ok=True)

        # Escreve o conteúdo recebido em um .txt local usando o nome da instancia
        with open(f'Instancias/{instance_name}', 'w') as file:
            file.write(response.text)
        print(f"Data saved to {instance_name}")
    else:
        print(f"Failed to fetch data from {instance_url}. Status code: {response.status_code}")


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
            Ji = data[k+1:row_len]

            J.append(Ji)
            k = row_len

        return m, n, col_costs, J

    except Exception as e:
        print(f'Instance not found or some error happened during parse.\n{e}')
        return None, None, None, None


def modelo():
    """Solve o conjunto independente máximo.
    """
    cpx = cplex.Cplex()
    cpx.objective.set_sense(cpx.objective.sense.minimize)

    instance_name = input('Escreva o nome da instância: ')
    get_data(instance_url=f'http://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/{instance_name}.txt')
    m, n, C, J = parse_instance(instance_name=instance_name)

    if m is None:
        print('Instance parsing failed.')
        return

    #create J_i
    J_i = []
    for i in range(m):
        feasible_subset_i = []
        for j in J:
            if i in j:
                feasible_subset_i.append(J.index(j))
        J_i.append(feasible_subset_i)

    x = cpx.variables.add(obj=[c_j for c_j in C],
                          lb=[0] * n, ub=[1] * n,
                          types=[cpx.variables.type.binary] * n,
                          names=[f'x_{j}' for j in range(0, n)])

    print()
    lin_exprs = [cplex.SparsePair([x[l] for l in j], [1.0]*len(j)) for j in J_i]
    cpx.linear_constraints.add(
        lin_expr=lin_exprs[1:],
        senses=['G'] * (len(J_i)-1),
        rhs=[1.0] * (len(J_i)-1),
        names=[f'c_{i}' for i in range(0, (len(J_i)-1))]
    )

    # Tweak some CPLEX parameters so that CPLEX has a harder time to
    # solve the model and our cut separators can actually kick in.
    cpx.parameters.mip.strategy.heuristicfreq.set(-1)
    cpx.parameters.mip.cuts.mircut.set(-1)
    cpx.parameters.mip.cuts.implied.set(-1)
    cpx.parameters.mip.cuts.gomory.set(-1)
    cpx.parameters.mip.cuts.flowcovers.set(-1)
    cpx.parameters.mip.cuts.pathcut.set(-1)
    cpx.parameters.mip.cuts.liftproj.set(-1)
    cpx.parameters.mip.cuts.zerohalfcut.set(-1)
    cpx.parameters.mip.cuts.cliques.set(-1)
    cpx.parameters.mip.cuts.covers.set(-1)
    cpx.parameters.threads.set(1)
    cpx.parameters.clocktype.set(1)
    cpx.parameters.timelimit.set(1800)

    cpx.write("setcover.lp")

    cpx.solve()

    print('Solution status:                   %d' % cpx.solution.get_status())
    print('Nodes processed:                   %d' %
          cpx.solution.progress.get_num_nodes_processed())
    tol = cpx.parameters.mip.tolerances.integrality.get()
    print('Optimal value:                     %f' %
          cpx.solution.get_objective_value())
    values = cpx.solution.get_values()
    for y in x:
        if values[x[y]] >= 1 - tol:
            print("x_" + str(x[y]) + "= " + str(values[x[y]]))


if __name__ == '__main__':
    modelo()
