import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd

# Inicialização
app = dash.Dash(__name__)
server = app.server

# Dados das partidas
partidas = pd.DataFrame(columns=["TimeCasa", "GolsCasa", "TempoVisitante", "GolsVisitante"])

# Layout
app.layout = html.Div([
    html.Div([
        dcc.Input(id="time-casa", type="text", placeholder="Time da Casa"),
        dcc.Input(id="gols-casa", type="number", placeholder="Gols da Casa"),
        dcc.Input(id="time-visitante", type="text", placeholder="Tempo Visitante"),
        dcc.Input(id="gols-visitante", type="number", placeholder="Gols do Visitante"),
        html.Button("Registrador Partida", id="registrar", n_clicks=0)
    ]),
    html.H2("🏟️ Tabela de Partidas", style={"marginTop": "30px"}),
    html.Div(id="tabela-partidas"),

    html.H2("🏆 Estatísticas dos Times", style={"marginTop": "30px"}),
    dcc.Graph(id="grafico-estatisticas")
])

# Callback
@app.callback(
    [Output("tabela-partidas", "children"),
     Output("grafico-estatisticas", "figure")],
    [Input("registrar", "n_clicks")],
    [State("time-casa", "value"),
     State("gols-casa", "value"),
     State("time-visitante", "value"),
     State("gols-visitante", "value")]
)
def atualizar_tabela(n_clicks, time_casa, gols_casa, time_visitante, gols_visitante):
    global partidas
    if n_clicks > 0 and None not in (time_casa, gols_casa, time_visitante, gols_visitante):
        nova_partida = {
            "TimeCasa": time_casa,
            "GolsCasa": gols_casa,
            "TempoVisitante": time_visitante,
            "GolsVisitante": gols_visitante
        }
        partidas = pd.concat([partidas, pd.DataFrame([nova_partida])], ignore_index=True)

    tabela = html.Table([
        html.Thead(html.Tr([html.Th(col) for col in partidas.columns])),
        html.Tbody([
            html.Tr([html.Td(partidas.iloc[i][col]) for col in partidas.columns])
            for i in range(len(partidas))
        ])
    ]) if not partidas.empty else html.Div("Nenhuma partida registrada ainda.")

    # Estatísticas
    df_estatisticas = pd.DataFrame(columns=["Time", "Gols"])
    if not partidas.empty:
        gols_por_time = pd.concat([
            partidas[["TimeCasa", "GolsCasa"]].rename(columns={"TimeCasa": "Time", "GolsCasa": "Gols"}),
            partidas[["TempoVisitante", "GolsVisitante"]].rename(columns={"TempoVisitante": "Time", "GolsVisitante": "Gols"})
        ])
        df_estatisticas = gols_por_time.groupby("Time").sum().reset_index()

    fig = px.bar(df_estatisticas, x="Time", y="Gols", title="Total de Gols por Time") if not df_estatisticas.empty else px.bar()

    return tabela, fig

# Execução
if __name__ == "__main__":
    app.run(debug=True)



