import pandas as pd
import sqlite3
import os


def sanitize_table_name(table_name):
    table_name = table_name.replace(' ', '_')
    table_name = ''.join(filter(str.isalnum, table_name))
    return f'tbl_{table_name}'


def remove_bank():
    if os.path.exists('conta_ponto.db'):
        os.remove('conta_ponto.db')


def processing_district_data(data, data1):
    remove_bank()
    conn = sqlite3.connect('conta_ponto.db')
    cursor = conn.cursor()
    district_line = data.split('\n')
    district_columns = [line.split('\t') for line in district_line]

    df_district = pd.DataFrame(
        district_columns,
        columns=[
            'Distrito',
            'Mat/Carteiro',
            'Qnt_Objetos',
            'Vazia',
            'Ar',
            'Vazia1',
            'Num_lista',
            'Impressão',
        ],
    )
    df_district = df_district.drop(['Vazia', 'Vazia1', 'Impressão'], axis=1)
    df_district = df_district.dropna(how='any')

    df_district = df_district.fillna(0)

    df_district.to_sql(
        'dados_distritos', conn, if_exists='replace', index=False
    )

    object_line = data1.split('\n')
    object_columns = [line.split('\t') for line in object_line]

    df_object = pd.DataFrame(
        object_columns,
        columns=[
            'Num_lista',
            'objeto',
            'false',
            'endereço',
            'ar',
            'cep',
            'zero',
        ],
    )

    df_object = df_object.drop(['false', 'ar', 'cep', 'zero'], axis=1)
    df_object = df_object.dropna(how='any')

    df_object = df_object.fillna(0)

    object_dict = {}
    current_key = None

    for index, row in df_object.iterrows():
        num_lista = row['Num_lista']
        object_cod = row['objeto']
        address = row['endereço']

        if num_lista.strip():
            current_key = num_lista

        if current_key not in object_dict:
            object_dict[current_key] = []

        if object_cod.strip() or address.strip():
            object_dict[current_key].append([object_cod, address])

    distrito_dict = dict(
        zip(df_district['Num_lista'], df_district['Distrito'])
    )

    object_dict = {
        distrito_dict.get(key_dict, 'Distrito não encontrado'): values
        for key_dict, values in object_dict.items()
    }

    for key, values in object_dict.items():
        # Sanitize o nome da tabela
        table_name = sanitize_table_name(key)

        cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {table_name} (objeto TEXT,endereco TEXT)'
        )   # noqa

        for value in values:
            cursor.execute(
                f'INSERT INTO {table_name} (objeto, endereco) VALUES (?, ?)',
                (value[0], value[1]),
            )   # noqa
    conn.commit()
