import cplex
from fetch_instance import get_data
from parse_instance import parse_instance

def modelo(instance_name: str):
    """Solve o conjunto independente máximo.
    """
    cpx = cplex.Cplex()
    cpx.objective.set_sense(cpx.objective.sense.minimize)

    # get_data(instance_url=f'http://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/{instance_name}.txt')
    m, n, C, J = parse_instance(instance_name=instance_name)

    if m is None:
        print('Instance parsing failed.')
        return

    cpx.variables.add(obj=C,
                        lb=[0] * n, ub=[1] * n,
                        types=[cpx.variables.type.binary] * n,
                        names=[f'x_{j}' for j in range(n)])

    for i in range(m):
        coeff = [1]*len(J[i])
        # print(J[i], coeff, len(J[i]) == len(coeff))
        
        cpx.linear_constraints.add(
            lin_expr=[cplex.SparsePair(ind=J[i], val=coeff)],
            senses=["G"],
            rhs=[1],
            names=[f'c_{i}']
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

    # Retrieve the solution
    status = cpx.solution.get_status()
    progress = cpx.solution.progress.get_num_nodes_processed()
    solution_values = cpx.solution.get_values()
    objective_value = cpx.solution.get_objective_value()

    print('Solution status:                   %d' % status)
    print('Nodes processed:                   %d' %
            progress)
    tol = cpx.parameters.mip.tolerances.integrality.get()
    print('Optimal value:                     %f' %
          objective_value)
    values = cpx.solution.get_values()
    # for y in x:
    #     if values[x[y]] >= 1 - tol:
    #         print("x_" + str(x[y]) + "= " + str(values[x[y]]))

    return status, solution_values, objective_value

if __name__ == '__main__':

    modelo(instance_name="scp41")