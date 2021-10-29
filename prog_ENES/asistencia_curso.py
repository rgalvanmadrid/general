'''
Programa que cuantifica la asistencia al curso
'''

################# DEFINED BY USER  #########################
class_days = [\
'21sep20','23sep20','28sep20','30sep20',\
'05oct20','07oct20','12oct20','14oct20','19oct20','21oct20','26oct20','28oct20',\
'04nov20','09nov20','11nov20','18nov20','23nov20','25nov20','30nov20',\
'02dic20','07dic20','09dic20',\
'04ene21','06ene21','11ene21','13ene21','18ene21','20ene21','25ene21','27ene21'\
]
free_days = ['25nov20','02dic20','11ene21']

str_thr = 70
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
        assist_day = pd.read_csv('asistencia_'+day+'.csv')
        class_time = assist_day.loc[0,'Total Duration (Minutes)']

        for stud in range(len(estud)):
            name = estud.loc[stud,'Nombre'].split()
            lastname = estud.loc[stud,'Apellido'].split()
            full_name = name + lastname
            print('\n')
            print('Matching {}'.format(full_name))
            for assistant in range(len(assist_day)):
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
# 23 de septiembre:
asist_curso.loc[17,'23sep20'] = 1 # Arely Leal
# 28 de septiembre:
asist_curso.loc[9,'28sep20'] = 1 # Misael Centeno
# 28 de octubre:
asist_curso.loc[17,'28oct20'] = 1 # Arely Leal
# 11 de noviembre:
asist_curso.loc[4,'11nov20'] = 1 # Juan Carlos Bucio
asist_curso.loc[25,'11nov20'] = 1 # Luis Rea
asist_curso.loc[17,'11nov20'] = 1 # Arely Leal
asist_curso.loc[5,'11nov20'] = 1 # Dianeyra Camarena
# 18 de noviembre:
asist_curso.loc[5,'18nov20'] = 1 # Dianeyra Camarena
# 23 de noviembre:
asist_curso.loc[1,'23nov20'] = 1 # Yarco Alvarez
# 7 de diciembre:
asist_curso.loc[18,'07dic20'] = 1 # Alejandro Maldonado
asist_curso.loc[14,'07dic20'] = 1 # Ariel Hernández
asist_curso.loc[12,'07dic20'] = 1 # Azul Dueñas
# 9 de diciembre
asist_curso.loc[14,'09dic20'] = 1 # Ariel Hernández
asist_curso.loc[4,'09dic20'] = 1 # Juan Carlos Bucio
asist_curso.loc[3,'09dic20'] = 1 # Ayelen Atayde
asist_curso.loc[12,'09dic20'] = 1 # Azul Dueñas
# 4 de enero
asist_curso.loc[17,'04ene21'] = 1 # Arely Leal
asist_curso.loc[14,'04ene21'] = 1 # Ariel Hernández
# 6 de enero
asist_curso.loc[14,'06ene21'] = 1 # Ariel Hernández
# 11 de enero
asist_curso.loc[4,'11ene21'] = 1 # Juan Carlos Bucio
asist_curso.loc[10,'11ene21'] = 1 # Danlya Delgado
# 13 de enero
asist_curso.loc[16,'13ene21'] = 1 # Daniela Jurado
asist_curso.loc[14,'13ene21'] = 1 # Ariel Hernández
# 18 de enero
asist_curso.loc[28,'18ene21'] = 1 # Jessica Saldívar





n_clases = len(asist_curso.loc[0][2:2+len(class_days)])
asist_curso['Asistencias'] = np.full(estud.shape[0],0)
asist_curso['Fracción'] = np.full(estud.shape[0],0)
asist_curso['Derecho'] = np.full(estud.shape[0],True)


for stud in range(len(estud)):
    asist_curso.loc[stud,'Asistencias'] = int(sum(asist_curso.loc[stud][2:2+n_clases]))
    asist_curso.loc[stud,'Fracción'] =round(asist_curso.loc[stud,'Asistencias']/n_clases,3)
    if asist_curso.loc[stud,'Fracción'] < 0.7:
        asist_curso.loc[stud,'Derecho'] = False


asist_curso.to_csv('asistencia_curso.csv', index=False)
