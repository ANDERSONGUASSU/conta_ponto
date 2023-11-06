from pyecharts.charts import Gauge, Page, Pie, Grid   # type: ignore
from pyecharts import options as opts   # type: ignore
from pyecharts.commons.utils import JsCode   # type: ignore
from src.utils.utils import open_in_browser
from src.utils.consult import main, get_data_district_dict, connect_to_database, disconnect_from_database # NOQA

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
fn_object = """
    function(params) {
        if(params.name == 'Objetos')
            return '\\nObjetos: ' + params.value;
        return params.name + ' : ' + params.value;
    }
    """
fn_ar = """
    function(params) {
        if(params.name == 'AR')
            return '\\nAR: ' + params.value;
        return params.name + ' : ' + params.value;
    }
    """
fn_qnt = """
    function(params) {
        if(params.name == 'Pontos')
            return '\\nPontos: ' + params.value;
        return params.name + ' : ' + params.value;
    }
    """


def new_label_opts_object():
    return opts.LabelOpts(
        formatter=JsCode(fn_object),
        position="center", font_size=16, font_weight="bold")


def new_label_opts_ar():
    return opts.LabelOpts(
        formatter=JsCode(fn_ar),
        position="center", font_size=16, font_weight="bold")


def new_label_opts_qnt():
    return opts.LabelOpts(
        formatter=JsCode(fn_qnt),
        position="center", font_size=16, font_weight="bold")


class GaugeChart:
    def create_chart(self):
        contagem_enderecos_unicos = main()
        page = Page(layout=Page.SimplePageLayout)

        database_path = 'conta_ponto.db'
        conn, cursor = connect_to_database(database_path)

        for chave, quantidade in contagem_enderecos_unicos.items():
            data_district_dict = get_data_district_dict(cursor)

            if chave in data_district_dict:
                qnt_objetos = data_district_dict[chave]['Qnt_Objetos']
                ar = data_district_dict[chave]['AR']
            else:
                qnt_objetos = 0
                ar = 0

            gauge = self.create_gauge(chave, quantidade, qnt_objetos, ar)

            # Criar gráfico Pie (donut) para "Qnt_Objetos"
            pie_objetos = self.create_pie_object("Objetos", qnt_objetos)

            # Criar gráfico Pie (donut) para "AR"
            pie_ar = self.create_pie_ar("AR", ar)

            # Criar gráfico Pie (donut) para "Quantidade"
            pie_quantidade = self.create_pie_qnt("Pontos", quantidade)

            # Posicionar os gráficos Pie em uma grade
            grid = (
                Grid()
                .add(pie_objetos,
                     grid_opts=opts.GridOpts(
                         pos_left="10%", pos_top="10%",
                         width="25%", height="25%"))
                .add(pie_ar,
                     grid_opts=opts.GridOpts(
                         pos_left="40%", pos_top="10%",
                         width="25%", height="25%"))
                .add(pie_quantidade,
                     grid_opts=opts.GridOpts(
                         pos_left="70%", pos_top="10%",
                         width="25%", height="25%"))
                .add(gauge,
                     grid_opts=opts.GridOpts(
                         pos_left="70%", pos_top="10%",
                         width="25%", height="25%"))
            )

            page.add(grid)

        disconnect_from_database(conn)

        chart_path = "temp_chart.html"
        page.render(chart_path)

        open_in_browser(chart_path, css_styles)

    def create_gauge(self, title, quantidade, qnt_objetos, ar):
        gauge = (
            Gauge()
            .add(
                "",
                [((-120 + quantidade), quantidade)],
                radius="50%",
                center=["50%", "75%"],
                split_number=10,
                min_=0,
                max_=200,
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(
                        color=[
                            (0.5, "#37a2da"),
                            (0.6, "#47B23B"),
                            (1, "#fd666d"),
                        ],
                        width=10
                    )
                ),
                detail_label_opts=opts.LabelOpts(formatter="{value}"),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(title=f"Distrito {title}"),
                legend_opts=opts.LegendOpts(is_show=False),
            )
        )
        return gauge

    def create_pie_object(self, category, value):
        pie = (
            Pie()
            .add(
                "",
                [(category, value)],
                radius=["20%", "30%"],
                center=["15%", "25%"],
                label_opts=new_label_opts_object()
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(is_show=False),
                legend_opts=opts.LegendOpts(is_show=False),
            )
        )
        return pie

    def create_pie_ar(self, category, value):
        pie = (
            Pie()
            .add(
                "",
                [(category, value)],
                radius=["20%", "30%"],
                center=["50%", "25%"],
                label_opts=new_label_opts_ar(),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(is_show=False),
                legend_opts=opts.LegendOpts(is_show=False),
            )
        )
        return pie

    def create_pie_qnt(self, category, value):
        pie = (
            Pie()
            .add(
                "",
                [(category, value)],
                radius=["20%", "30%"],
                center=["85%", "25%"],
                label_opts=new_label_opts_qnt(),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(is_show=False),
                legend_opts=opts.LegendOpts(is_show=False),
            )
        )
        return pie
