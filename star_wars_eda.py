import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# carregar os dados das bases de dados
def fetch_data_into_dataframe(categorias):
    
    conn = sqlite3.connect(f'{categorias}.db')
    query = f"SELECT * FROM {categorias}"
    
    df = pd.read_sql_query(query, conn)

    conn.close()
    
    return df

# lista de bases
bases = ['people', 'vehicles', 'films', 'starships', 'species','planets']

# dicionário para guardar as bases e poder acessá-las posteriormente no formato dataframes['bases']
dataframes = {}

# carregar os dados para os dataframes
for categorias in bases:
    dataframes[categorias] = fetch_data_into_dataframe(categorias)

# análises iniciais para entender o formato das bases
for categorias in bases:
    print(categorias)
    print(dataframes[categorias].dtypes)
    print(dataframes[categorias].shape)
    print(dataframes[categorias].describe)
    print(dataframes[categorias].isnull().sum())
    print(dataframes[categorias].info())


# insights

# verificando qual personagem aparece em mais filmes
# nesse caso, como a quantidade de filmes está em formato string, é preciso transformar essa coluna de volta em lista e abrir cada item em uma linha
dataframes['people']['films'] = dataframes['people']['films'].apply(lambda x: eval(x) if pd.notnull(x) else [])
exploded_df = dataframes['people'].explode('films')
print(exploded_df.describe)

# contando a quantidade de itens por nome e colocando em ordem decrescente
films_counts = exploded_df.groupby(['name']).size().reset_index(name='count')
films_counts = films_counts.sort_values(by='count', ascending=False)

print("Personagens e Filmes:")
print(films_counts)

# verificando veículo é o mais rápido
# como salvamos todas as colunas como string, também foi necessário ter o cuidado de passar a coluna que traz a velocidade pra número antes de começar a mexer
dataframes['vehicles']['max_atmosphering_speed'] = pd.to_numeric(dataframes['vehicles']['max_atmosphering_speed'], errors='coerce')

# verificando o maior valor da coluna, agrupando pelo nome do veículo e colocando em ordem decrescente
max_speed_df = dataframes['vehicles'].groupby('name')['max_atmosphering_speed'].max().reset_index(name='max_atmosphering_speed')
max_speed_df = max_speed_df.sort_values(by='max_atmosphering_speed', ascending=False)


print("Veículo mas rápido:")
print(max_speed_df['name'].iloc[0])


# verificando os climas dos planetas em busca de algum planeta árido (considerado o clima mais quente)
print(dataframes['planets'][['name','climate','surface_water']])

# verificando qual classificação de especies que mais aparece
# nesse caso, contei a quantidade de vezes que cada classificação aparece e joguei em um histograma pra verificar num gráfico
classification_counts = dataframes['species']['classification'].value_counts()

plt.figure(figsize=(10, 6))
classification_counts.plot(kind='bar', color='skyblue')
plt.title('Distribution of Species by Classification')
plt.xlabel('Classification')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.show()








