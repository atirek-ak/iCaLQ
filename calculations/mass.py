from utilities.constants import data_mass_list, mass_quarks, mass_leptons


def get_closest_mass(mass):
    """
    Find the closest mass to the input mass
    """
    closest_mass = 0
    closest_diff = 10000
    for val in data_mass_list:
        if abs(mass - val) < closest_diff:
            closest_diff = abs(mass - val)
            closest_mass = val
    return closest_mass


def make_mass_dict(ls, num_lam):
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
