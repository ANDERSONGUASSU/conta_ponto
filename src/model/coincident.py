from pyecharts import options as opts  # type: ignore
from pyecharts.charts import Tab  # type: ignore
from pyecharts.components import Table  # type: ignore
import pandas as pd
from src.utils.consult import encontrar_duplicados
from src.utils.utils import open_in_browser

resultados = encontrar_duplicados()

css_styles = """
<style>
    /* Estilização para os gráficos */
    .chart-container {
        border: 2px solid #000;
        margin: 10px; /* Adicione margem para espaçamento externo */
        text-align: center;  /* Centraliza o texto */
    }

    .title {
        font-size: 16px;
        padding-top: 10px;
    }
</style>
"""


def criar_tabela_resultados(resultados):
    df = pd.DataFrame(resultados)

    table = Table()

    table.add(
        headers=list(df.columns),
        rows=df.values.tolist()
    )

    # Defina as opções da tabela, como largura, altura, etc.
    table.set_global_opts(
        opts.TitleOpts(
            is_show=True,

        )
    )

    # Crie um objeto Tab e adicione a tabela a ele
    tab = Tab()
    tab.add(table, "Tabela de Resultados")

    return tab


def exibir_tabela_resultados(resultados):

    tabela = criar_tabela_resultados(resultados)

    tabela.render("tabela_resultados.html")

    open_in_browser("tabela_resultados.html", css_styles)
