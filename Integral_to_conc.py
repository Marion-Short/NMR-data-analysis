#!/usr/bin/env python
# coding: utf-8
# Integrals to concentration (mM)

def Integral_to_conc(df, weight_TSP):

    # Create tuples of the metabolites and the number of protons
    metabolite_protons = [('TSP', 9), ('formate', 1), ('MES', 2), ('fructose', 1), ('glycerol', 1), ('ethylene_glycol', 4), ('propanoate', 2),
                      ('acetate', 3), ('acetaldehyde', 3), ('ethanol', 3)]

    # TSP number of moles in NMR tube
    gfm = 172.27 # g/mol
    D2O_density = 1.11 # g/mL
    volume_of_TSP_solution = 0.03 # mL
    mass_of_TSP_solution = volume_of_TSP_solution * D2O_density # g
    weight_percent_of_TSP_in_solution = weight_TSP / 100 # =0.75% 0.0075
    mass_of_TSP = weight_percent_of_TSP_in_solution * mass_of_TSP_solution # g
    moles_of_TSP = mass_of_TSP / gfm # mol

    df_mol = df.copy()

    for col in df.columns:
        for m, p in metabolite_protons:
            if m in col:
                protons = p
        df_mol[col] = df[col] * 9 * moles_of_TSP * 1000 / protons # mmol

    df_conc = df_mol / 0.00057
    return df_conc
