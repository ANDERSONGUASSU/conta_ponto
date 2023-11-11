import sqlite3


def connect_to_database(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    return conn, cursor


def disconnect_from_database(conn):
    conn.close()


def get_table_names(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = [
        row[0] for row in cursor.fetchall() if row[0].startswith('tbl_')
    ]
    return table_names


def get_data_from_table(table_name, cursor):
    cursor.execute(f'SELECT * FROM {table_name};')
    data = cursor.fetchall()
    return data


def format_table_name(table_name):
    table_name = table_name.replace('tbl_', '')
    for i in range(len(table_name)):
        if table_name[i].isdigit() and (
            i + 1 < len(table_name) and not table_name[i + 1].isdigit()
        ):   # NOQA
            table_name = table_name[: i + 1] + ' ' + table_name[i + 1:]
    return table_name


def get_unique_address_counts(sorted_data_list):
    contagem_enderecos_unicos = {}
    for chave, valores in sorted_data_list:
        enderecos_unicos = set()
        for _, endereco in valores:
            enderecos_unicos.add(endereco)
        quantidade_enderecos_unicos = len(enderecos_unicos)
        contagem_enderecos_unicos[chave] = quantidade_enderecos_unicos
    return contagem_enderecos_unicos


def get_data_district_dict(cursor):
    cursor.execute('SELECT Distrito, Qnt_Objetos, Ar FROM dados_distritos')
    results = cursor.fetchall()
    data_district_dict = {}

    for result in results:
        distrito, qnt_objetos, ar = result
        data_district_dict[distrito] = {'Qnt_Objetos': qnt_objetos, 'AR': ar}

    return data_district_dict


def encontrar_duplicados():
    database_path = 'conta_ponto.db'
    conn, cursor = connect_to_database(database_path)
    table_names = get_table_names(cursor)
    data_list = []

    for table_name in table_names:
        data = get_data_from_table(table_name, cursor)
        data_list.append((format_table_name(table_name), data))

    # Dicionário para armazenar endereços duplicados
    enderecos_duplicados = {}

    for distrito, data in data_list:
        for codigo_objeto, endereco in data:
            # Remove espaços e converte o endereço para letras minúsculas
            endereco_limpo = endereco.strip().upper()

            if endereco_limpo in enderecos_duplicados:
                enderecos_duplicados[endereco_limpo].append(
                    (codigo_objeto, distrito)
                )
            else:
                # Crie uma nova entrada no dicionário de endereços duplicados
                enderecos_duplicados[endereco_limpo] = [
                    (codigo_objeto, distrito)
                ]

    resultados = []  # Lista para armazenar os resultados a serem retornados

    for endereco, duplicados in enderecos_duplicados.items():
        if len(duplicados) > 1:
            distritos = {}
            for codigo_objeto, distrito in duplicados:
                if distrito not in distritos:
                    distritos[distrito] = {
                        'Códigos do Objeto': [codigo_objeto]
                    }
                else:
                    distritos[distrito]['Códigos do Objeto'].append(
                        codigo_objeto
                    )

            if len(distritos) > 1:
                resultado_endereco = {
                    'Endereço Duplicado': endereco,
                    **{
                        f'Distrito{i+1}': [distrito]
                        for i, distrito in enumerate(distritos)
                    },
                    **{
                        f'Códigos do Objeto do Distrito{i+1}': data[
                            'Códigos do Objeto'
                        ]
                        for i, data in enumerate(distritos.values())
                    },
                }

                resultados.append(resultado_endereco)

    disconnect_from_database(conn)
    return resultados


def main():
    database_path = 'conta_ponto.db'
    conn, cursor = connect_to_database(database_path)
    table_names = get_table_names(cursor)
    data_list = []

    for table_name in table_names:
        data = get_data_from_table(table_name, cursor)
        data_list.append((format_table_name(table_name), data))

    # Classificar a lista de tuplas com base no critério desejado
    sorted_data_list = sorted(
        data_list,
        key=lambda x: (
            x[0].split()[1] if len(x[0].split()) > 1 else '',
            int(x[0].split()[0]) if len(x[0].split()) > 0 else 0,
        ),
    )

    contagem_enderecos_unicos = get_unique_address_counts(sorted_data_list)
    disconnect_from_database(conn)

    return contagem_enderecos_unicos


if __name__ == '__main__':
    main()
