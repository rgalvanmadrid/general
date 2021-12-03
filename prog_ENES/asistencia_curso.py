'''
Programa que cuantifica la asistencia al curso
'''

################# DEFINED BY USER  #########################
class_days = [\
'22sep21','27sep21','29sep21',\
'04oct21','06oct21','11oct21','13oct21','18oct21','20oct21','25oct21','27oct21',\
'03nov21'\
]
# Nota: la primera clase fue 20sep21, pero empezamos a pasar lista en la segunda.

free_days = ['29sep21','18oct21']

str_thr = 72
time_thr = 0.66
############################################################

import pandas as pd
from fuzzywuzzy import fuzz
import numpy as np

estud = pd.read_csv('lista_estudiantes.csv',skipinitialspace=True)
asist_curso = estud.copy()


for day in class_days:
    day_attendance = np.full(estud.shape[0],0)
    if day in free_days:
        day_attendance = np.full(estud.shape[0],1)
        asist_curso[day] = day_attendance
    else:
        print('\n')
        print('Day: {}'.format(day))
        assist_day = pd.read_csv('asistencia_'+day+'.csv')
        class_time = assist_day.loc[0,'Total Duration (Minutes)']
        assist_day = assist_day.drop(0)

        for stud in range(len(estud)):
            name = estud.loc[stud,'Nombre'].split()
            lastname = estud.loc[stud,'Apellido'].split()
            full_name = name + lastname
            print('\n')
            print('Matching {}'.format(full_name))
            for assistant in range(1,len(assist_day)+1):
                counter = 0
                assistant_time = assist_day.loc[assistant,'Total Duration (Minutes)']
                name_parts = assist_day.loc[assistant,'Name (Original Name)'].split()
                #print(name_parts)
                for j in range(len(full_name)):
                    for i in range(len(name_parts)):
                        ratio = fuzz.ratio(full_name[j].lower(),name_parts[i].lower())
                        if ratio > str_thr:
                            counter += 1
                            #print('{0} vs {1} = {2}'.format(full_name[j].lower(),name_parts[i].lower(),ratio))
                if counter > 1 and assistant_time/class_time > time_thr:
                    day_attendance[stud]=1
                    print('{0} has {1} parts with string threshold > {2} and was present {3:.3f} of the class time'\
                    .format(name_parts,counter,str_thr,assistant_time/class_time))
        asist_curso[day] = day_attendance


# Poner justificaciónes a mano, ver justificaciones.txt
asist_curso.at[4,'06oct21'] = 1 #Abril Iraís Castañeda Suárez
asist_curso.at[5,'27sep21'] = 1 #Misael Centeno
asist_curso.at[8,'27oct21'] = 1 #Erick Darío Garibay

# Otros errores corregidos a mano:
asist_curso.at[5,'22sep21'] = 1 #Misael Centeno
asist_curso.at[6,'22sep21'] = 1 #Jose Eduardo Cerda Dueñas
asist_curso.at[7,'22sep21'] = 1 #GALVAN RUIZ,RAMIRO ISAAC


####################################################################################################

n_clases = len(asist_curso.loc[0][2:2+len(class_days)])
asist_curso['Asistencias'] = np.full(estud.shape[0],0)
asist_curso['Fracción'] = np.full(estud.shape[0],0)
asist_curso['Derecho'] = np.full(estud.shape[0],True)


for stud in range(len(estud)):
    asist_curso.loc[stud,'Asistencias'] = int(sum(asist_curso.loc[stud][3:3+n_clases]))
    asist_curso.loc[stud,'Fracción'] =round(asist_curso.loc[stud,'Asistencias']/n_clases,3)
    if asist_curso.loc[stud,'Fracción'] < 0.7:
        asist_curso.loc[stud,'Derecho'] = False


asist_curso.to_csv('asistencia_curso.csv', index=False)
