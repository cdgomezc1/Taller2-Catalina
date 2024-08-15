import pulp as lp
import pandas as pd

file_name = './data.xlsx'

#-----------------
#Conjuntos
#-----------------

conjuntos = pd.read_excel(io=file_name,sheet_name='Tabla 1.1')
dataframe = pd.read_excel(io=file_name, sheet_name='Tabla 1.1')

# Conjunto de Proteínas
P =pd.unique([i for i in conjuntos['Tipo de proteína'] if not pd.isna(i)]).tolist()

# Conjunto de Cortes
M = [j for j in conjuntos['Corte'] if not pd.isna(j)]


#Subconjunto 
P_i = {i:[dataframe['Corte'][j]for j in range (len(dataframe)) if dataframe['Tipo de proteína'][j] == i] for i in P}

# Parámetro costos 
# Como se recorren los costos 

costos = pd.read_excel(file_name,sheet_name='Tabla 1.1', index_col=1)

costo_por_corte= {m:costos["viviana"][m] for m in M}


# -------------------------------------
# Creación del objeto problema en PuLP
# -------------------------------------
prob = lp.LpProblem('Punto_1',sense = lp.LpMinimize)

# -----------------------------
# Variable de Decisión
# -----------------------------
# Variable de decisión
# Indica si el corte se compra o no

corte = pd.read_excel(file_name,sheet_name='Tabla 1.1', index_col=1)

x = {m:lp.LpVariable(f'realiza_{m}', lowBound=0, cat= lp.LpBinary) for m in M }

# -----------------------------
# Restricciones
# -----------------------------

#Pedir al menos un corte por cada tipo de proteína

for i in P:
    prob += lp.lpSum(x[m] for m in P_i[i]) >= 1
 

#Pedir al menos un corte entre Rib Eye, New York Stake o Tomahawk.
prob += x["New York Steak"] + x["Rib Eye"] + x["Tomahawk"]>= 1
 
# Si se pide New York Steak  no se puede pedir ni Rib Eye ni Tomahawk
prob += 2*(1-x["New York Steak"])>= x["Rib Eye"] + x["Tomahawk"]


#	Asegurar un corte especial entre Picanha, Brisket y Asado de Tira
prob += x["Picanha"] + x["Brisket"] + x["Asado de tira"]>= 1

#Mínimo 3 tipo de mariscos
prob += sum(x[m] for m in P_i["Mariscos"]) >= 3

#Si se piden muslos o alas hay que pedir Magret de pato
prob += x["Muslo y contramuslo de pollo"] + x["Alas"] <=  x["Magret de pato"]

#No se pueden pedir muslos y alas
prob += x["Muslo y contramuslo de pollo"] + x["Alas"] <= 1

#Si no se piden ostras se debe pedir langosta, gambas y pulpo 
prob += 3*(1-x["Ostras"]) <= x["Langosta"] + x["Gamba"] + x["Pulpo"]

#No se puede pedir corvina y tilapia contemporáneamente
prob += x["Corvina"] + x["Tilapia"] <= 1



