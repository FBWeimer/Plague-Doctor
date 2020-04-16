import pandas as pd
import numpy as np
from plaguedoctor.models import SIR
from plaguedoctor.datamanager import access, get_data

initial_month = input('Insira o nome do primeiro mês que deseja analisar e que conste na tabela: ').lower()
last_month = input('Insira o nome do último mês que deseja analisar e que conste na tabela: ').lower()
period_predict = int(input('Insira o número de dias que deseja que o modelo preveja a partir da última'
                           'data que consta na base de dados: '))
local = 'C:/Users/weime/Documents/Estudo/Engenharia Biomédica/Modelo COVID/'
client = access.dataframe()

for states in range(0, 1):  # or in range(0,len(state)) if you want simulate to all states
    data_city, date_cities, infected, dead, recovered, census_city, N_pop = {}, {}, {}, {}, {}, {}, {}
    Suscepted, Infected, Recovered = {}, {}, {}

    state_name = access.states_sheets(states, 0)
    census = pd.read_excel(access.states_sheets(states, 2), usecols=[0, 7])
    census['Código do município'] = pd.to_numeric(census['Código do município'])
    census['Total da população 2010'] = pd.to_numeric(census['Total da população 2010'])

    data = get_data.data_concatenate(initial_month, last_month, access.states_sheets(states, 1),client)
    data = data[['Data', 'ibgeID', 'state', 'city', 'newCases', 'totalCases', 'óbitos', 'recuperados']]
    ibgeID_list = pd.Series(data['ibgeID']).unique()

    cities_names = pd.Series(data['city']).unique()
    initials_state = pd.Series(data['state']).unique()[0]

    for cities in range(0, 2):  # len(ibgeID_list)):
        city_name = cities_names[cities]

        data_city[city_name] = data.loc[data['ibgeID'] == ibgeID_list[cities]]

        date_cities[city_name] = pd.DatetimeIndex(data_city[city_name]['Data'])
        date_city = date_cities[city_name]
        MONTH = date_city.month
        DAY = date_city.day

        infected[city_name] = np.array(data_city[city_name]['totalCases'])
        dead[city_name] = np.array(data_city[city_name]['óbitos'])
        recovered[city_name] = np.array(data_city[city_name]['recuperados'])

        census_city[city_name] = census.loc[census['Código do município'] == ibgeID_list[cities]]
        census_array = np.array(census_city[city_name])
        N_pop[city_name] = census_array[0][1]
        population = N_pop[city_name]

        cases = infected[city_name]
        infected_0, recovered_0, dead_0 = infected[city_name][0], recovered[city_name][0], dead[city_name][0]

        beta, gamma = SIR.trainer(cases, population, infected_0, recovered_0, dead_0)

        time_predict = np.arange(1, period_predict + 1)

        I0, R0 = infected[city_name][len(infected[city_name]) - 1], recovered[city_name][len(recovered[city_name]) - 1]
        D0 = dead[city_name][len(dead[city_name]) - 1]

        Suscepted[city_name], Infected[city_name], \
            Recovered[city_name] = SIR.prediction(beta, gamma, population, I0, R0, D0, time_predict)

        S, I, R = Suscepted[city_name], Infected[city_name], Recovered[city_name]

        SIR.plot(S, I, R, initials_state, state_name, city_name, period_predict, time_predict, population, date_city, last_month)