import pandas as pd
import numpy as np
from plaguedoctor.models import SEIRDrm
from plaguedoctor.datamanager import access

initial_month = input('Insira o nome do primeiro mês que deseja analisar e que conste na tabela: ').lower()
last_month = input('Insira o nome do último mês que deseja analisar e que conste na tabela: ').lower()
period_predict = int(input('Insira o número de dias que deseja que o modelo preveja a partir da última'
                           'data que consta na base de dados: '))


local_archive = 'C:/Users/weime/Documents/Estudo/Engenharia Biomédica/Modelo COVID/POA.xlsx'

census = pd.read_excel(access.states_sheets(0, 2), usecols=[0, 7])
census['Código do município'] = pd.to_numeric(census['Código do município'])
census['Total da população 2010'] = pd.to_numeric(census['Total da população 2010'])

month1 = initial_month.upper()
month2 = last_month.upper()

sheet = pd.ExcelFile(local_archive)

data1 = pd.read_excel(sheet, month1, usecols=[0,1,3,4,5,6,7,8])
data2 = pd.read_excel(sheet, month2, usecols=[0,1,3,4,5,6,7,8])

if initial_month != last_month:
    
    data_POA = pd.concat([data1, data2])
    
else:
    data_POA = data1


ibgeID_POA = pd.Series(data_POA['ibgeID']).unique()
ibgeID_POA = ibgeID_POA[0]

date_POA = pd.DatetimeIndex(data_POA['Data'])
MONTH = date_POA.month
DAY = date_POA.day
last_day = DAY[len(DAY)-1]

infected = np.array(data_POA['totalCases'])
exposed = 4 * infected
dead = np.array(data_POA['óbitos'])
recovered = np.array(data_POA['recuperados'])


census_POA = census.loc[census['Código do município'] == ibgeID_POA]
census_array = np.array(census_POA)
population = census_array[0][1]

cases = infected
exposed_0, infected_0, recovered_0, dead_0 = exposed[0], infected[0], recovered[0], dead[0]

t_i = 10

beta, alfa, f = SEIRDrm.trainer(t_i, cases, population, exposed_0, infected_0, recovered_0, dead_0)

point = beta, alfa, f

erro = SEIRDrm.error_model(point, t_i, cases, population, exposed_0, infected_0, recovered_0, dead_0)

print(f'O erro do modelo é de {erro}')

time_predict = np.arange(1, period_predict + 1)

E0, I0, R0, D0 = exposed[len(exposed) - 1], infected[len(infected) - 1], recovered[len(recovered) - 1], dead[len(dead) - 1]

S, E, I, R, D = SEIRDrm.prediction(beta, alfa, f, t_i, population, E0, I0, R0, D0, time_predict)

SEIRDrm.plot(S, E, I, R, D, 'RS', 'Rio Grande do Sul', 'Porto Alegre', period_predict, time_predict, population, date_POA, initial_month, last_month, last_day)
