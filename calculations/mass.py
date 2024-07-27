from utilities.constants import mass_quarks, mass_leptons


def make_leptoquark_mass_dict(ls, num_lam):
    md = {}
    for i in range(num_lam):
        if ls[i][4] == "L":
            md[ls[i]] = [
                [mass_quarks[ls[i][6]][1], mass_leptons[ls[i][8]][0]],
                [mass_quarks[ls[i][6]][0], mass_leptons[ls[i][8]][1]],
            ]
        elif ls[i][4] == "R":
            md[ls[i]] = [[mass_quarks[ls[i][6]][1], mass_leptons[ls[i][8]][0]]]
    return md
