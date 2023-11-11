from pyecharts import options as opts  # type: ignore
from pyecharts.charts import Tab  # type: ignore
from pyecharts.components import Table  # type: ignore
import pandas as pd
from src.utils.consult import encontrar_duplicados
from src.utils.utils import open_in_browser

title = """Pontos Coincidentes</title>"""


css_styles = """
<style>
        table {
            table-layout: fixed;
            width: 100%;
        }

        td {
            max-width: 150px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: normal;
        }
</style>
"""


def criar_e_exibir_tabela_resultados():
    resultados = encontrar_duplicados()
    df = pd.DataFrame(resultados)

    def formatar_valor(valor):
        if isinstance(valor, list):
            return ', '.join(valor)
        else:
            return valor

    df = df.map(formatar_valor)
    df = df.sort_values(by='Distrito1', ascending=False)

    table = Table()

    table.add(headers=list(df.columns), rows=df.values.tolist())

    # Defina as opções da tabela, como largura, altura, etc.
    table.set_global_opts(
        opts.TitleOpts(
            is_show=True,
        )
    )

    # Crie um objeto Tab e adicione a tabela a ele
    tab = Tab()
    tab.add(table, 'Tabela de Resultados')

    tab.render('tabela_resultados.html')

    open_in_browser('tabela_resultados.html', css_styles, title)
