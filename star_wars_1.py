import requests
import sqlite3

# pegar dados do SWAPI
def fetch_swapi_data(categoria):
    url = f'https://swapi.dev/api/{categoria}/'
    resposta = requests.get(url)
    return resposta.json()['results']

# cria as bases e as tabelas pra cada categoria (veiculos, pessoas etc)
def create_database_table(categoria, colunas):
    conn = sqlite3.connect(f'{categoria}.db')
    cursor = conn.cursor()
    # como cada tabela possui colunas diferentes, essa parte cria as tabelas de forma dinâmica
    create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {categoria} (
            id INTEGER PRIMARY KEY,
            {", ".join([f"{col} TEXT" for col in colunas])}
        );
    '''
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()

# alimentar as databases com as informações
def insert_data_into_database(categoria, colunas, data):
    conn = sqlite3.connect(f'{categoria}.db')
    cursor = conn.cursor()
    
    for item in data:
        # converter todas as colunas em strings (pois alguns itens em algumas colunas são listas)
        values = tuple(str(item.get(col, '')) if not isinstance(item.get(col, ''), list) else str(item.get(col, '')) for col in colunas)
        
        # entrando com as informações de forma dinâmica de acordo com a quantidade de colunas de cada tabela
        insert_query = f"INSERT INTO {categoria} ({', '.join(colunas)}) VALUES ({', '.join(['?']*len(colunas))})"
        
        cursor.execute(insert_query, values)
    
    conn.commit()
    conn.close()

# mapeamento das categorias e suas respectivas colunas
categoria_colunas = {
    'people': ['name', 'birth_year', 'eye_color', 'height', 'mass','skin_color','homeworld','films','species','starships','vehicles','url','created','edited'],
    'vehicles': ['name', 'model', 'vehicle_class', 'manufacturer','length','cost_in_credits','crew','passengers','max_atmosphering_speed','cargo_capacity','consumables','films','pilots','url','created','edited'],
    'films': ['title', 'episode_id','opening_crawl','director', 'producer','release_date','species','starships','vehicles','characters','planets','url','created','edited'],
    'starships': ['name', 'model', 'starship_class', 'manufacturer','cost_in_credits','length','crew','passengers','max_atmosphering_speed','hyperdrive_rating','MGLT','cargo_capacity','consumables','films','pilots','url','created','edited'],
    'species': ['name', 'classification','designation', 'average_height', 'average_lifespan','eye_colors','hair_colors','skin_colors','language','homeworld','people','films','url','created','edited'],
    'planets': ['name', 'diameter', 'rotation_period', 'orbital_period','gravity','population','climate','terrain','surface_water','residents','films','url','created','edited']
}


for categoria, colunas in categoria_colunas.items():
    
    data = fetch_swapi_data(categoria)

    
    create_database_table(categoria, colunas)

    
    insert_data_into_database(categoria, colunas, data)

print("Tudo certo!")