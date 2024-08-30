import cplex
from maxi import get_SS


print('SS: ', get_SS())


def modelo(S, SS):
    """Solve o conjunto independente máximo.
    """

    def get_Ji(m, SS):
        J_i = []
        for i in range(m):
            a = []
            for k, clique in enumerate(SS):
                if i in clique:
                    a.append(k)
            J_i.append(a)

        while [] in J_i:
            J_i.remove([])

        return J_i

    cpx = cplex.Cplex()
    cpx.objective.set_sense(cpx.objective.sense.minimize)


    m = len(S)
    J_i = get_Ji(m, SS)
    n = len(J_i)
    C = [len(j) for j in J_i]
    print('J_i: ', J_i)
    print('C: ', C)

    x = cpx.variables.add(obj=[c_j for c_j in C],
                          lb=[0] * n, ub=[1] * n,
                          types=[cpx.variables.type.binary] * n,
                          names=['x_%d' % (j) for j in range(n)])

    # Para cada aresta só pode haver um (HL)
    sparse_pairs = []
    active = 0
    # for j in J_i:
    #     if j:
    #         print(j)
    #         sparse_pair = cplex.SparsePair([x[J_i.index(j)]], [1.0]*len(j))
    #         print(sparse_pair)
    #         sparse_pairs.append(sparse_pair)
    #         active += 1

    #print(sparse_pairs)
    #print(active)
    # cpx.linear_constraints.add(
    #     lin_expr=[cplex.SparsePair([x[1]], [1.0]), cplex.SparsePair([x[1], x[2]], [1.0]*2)],
    #     senses=['G'] * 2,
    #     rhs=[1.0] * 2,
    #     names=['%d' % (i) for i in range(2)]
    # )
    print()
    cpx.linear_constraints.add(
        lin_expr=[cplex.SparsePair([x[l] for l in j], [1.0]*len(j)) for j in J_i],
        senses=['G'] * n,
        rhs=[1.0] * n,
        names=['%d' % (i) for i in range(0, n)]
    )#'Edge_' + str(i) + '_' + str(j) for i, j in E])

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

    cpx.write("conjind.lp")

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
            print("y_" + str(x) + "= " + str(values[x[y]]))


modelo([0,1,2,3,4], get_SS())