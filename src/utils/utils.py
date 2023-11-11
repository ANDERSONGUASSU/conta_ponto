import os
import webbrowser


def open_in_browser(chart_path, css_styles, title):
    current_directory = os.getcwd()
    chart_full_path = os.path.join(current_directory, chart_path)

    # Leia o conteúdo do arquivo HTML
    with open(chart_full_path, 'r') as file:
        html_content = file.read()

    # Insira os estilos CSS e o título no HTML
    modified_html_content = html_content.replace(
        '</head>', f'{css_styles}</head>'
    )
    modified_html_content = modified_html_content.replace(
        'Awesome-pyecharts</title>', f'{title}</title>'
    )

    # Salve o arquivo HTML atualizado
    with open(chart_full_path, 'w') as file:
        file.write(modified_html_content)

    # Abra o arquivo HTML no navegador
    webbrowser.open(f'file://{chart_full_path}', new=2)
