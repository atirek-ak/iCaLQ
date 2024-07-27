import math


def momentum(mlq: float, mq: float, ml: float):
    """
    mlq: mass of leptoquark
    mq: mass of quark
    ml: mass pf lepton
    """
    a = math.pow(mlq + ml, 2) - math.pow(mq, 2)
    b = math.pow(mlq - ml, 2) - math.pow(mq, 2)
    return math.sqrt(a * b) / (2 * mlq)


def abseffcoupl_massfactor(mlq: float, mq: float, ml: float):
    """
    mlq: mass of leptoquark
    ml: mass pf lepton
    mq: mass of quark
    """
    return (
        math.pow(mlq, 2)
        - (math.pow(ml, 2) + math.pow(mq, 2))
        - math.pow((math.pow(ml, 2) - math.pow(mq, 2)), 2) / math.pow(mlq, 2)
        - (6 * ml * mq)
    )


def U1_decay_width_massfactor(mlq: float, M: list):
    """
    mlq: mass of leptoquark
    M:  list with [mlq, mq, ml]
    """
    return (
        momentum(mlq, M[0], M[1])
        * abseffcoupl_massfactor(mlq, M[0], M[1])
        / (8 * math.pow(math.pi, 2) * math.pow(mlq, 2))
    )

def S1_decay_width(mlq: float, M: list):
    mq = M[0]
    ml= M[1]
    return (math.pow(mlq, 2) - math.pow(ml + mq, 2)) * (math.sqrt((math.pow(mlq, 2) - math.pow(ml + mq, 2)) * (math.pow(mlq, 2) - math.pow(ml - mq, 2)))) / (8 * math.pi * math.pow(mlq, 3))
    


# Calculate branching fraction of dielectron, dimuon an ditau using decay_width
def branching_fraction(leptoquark_model, all_ls, all_lam, md, Mlq, width_const: float=0):
    
    denom = width_const
    numer = [0, 0, 0]
    for i in range(len(all_ls)):
        for j in range(len(all_ls[i])):
            if leptoquark_model == "U1":
                denom += all_lam[i][j] ** 2 * U1_decay_width_massfactor(
                    Mlq, md[all_ls[i][j]][0]
                )
                numer[i] += all_lam[i][j] ** 2 * U1_decay_width_massfactor(
                    Mlq, md[all_ls[i][j]][0]
                )
                if all_ls[i][j][4] == "L":
                    denom += all_lam[i][j] ** 2 * U1_decay_width_massfactor(
                        Mlq, md[all_ls[i][j]][1]
                    )
            elif leptoquark_model == "S1":
                denom += all_lam[i][j] ** 2 * S1_decay_width(
                    Mlq, md[all_ls[i][j]][0]
                )
                numer[i] += all_lam[i][j] ** 2 * S1_decay_width(
                    Mlq, md[all_ls[i][j]][0]
                )
                if all_ls[i][j][4] == "L":
                    denom += all_lam[i][j] ** 2 * S1_decay_width(
                        Mlq, md[all_ls[i][j]][1]
                    )



    return [nu / denom for nu in numer]
