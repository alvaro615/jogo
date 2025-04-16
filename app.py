from dash import Dash, html, dcc, Input, Output, State, callback_context
import random

# Perguntas sobre fanerógamas
topics = [
    {"question": "Qual das seguintes plantas é uma fanerógama?", "options": ["Samambaia", "Pinheiro", "Musgo", "Líquens"], "answer": "Pinheiro"},
    {"question": "As fanerógamas se dividem em quais dois principais grupos?", "options": ["Briófitas e pteridófitas", "Gimnospermas e angiospermas", "Fungos e algas", "Hepáticas e musgos"], "answer": "Gimnospermas e angiospermas"},
    {"question": "Qual característica define angiospermas?", "options": ["Produzem sementes expostas", "Não possuem vasos condutores", "Produzem frutos que envolvem as sementes", "Reprodução por esporos"], "answer": "Produzem frutos que envolvem as sementes"},
    {"question": "As gimnospermas possuem sementes:", "options": ["Dentro de frutos", "Expostas em estruturas como cones", "Em cápsulas aquosas", "Em folículos"], "answer": "Expostas em estruturas como cones"},
    {"question": "Qual é o órgão reprodutivo feminino das angiospermas?", "options": ["Estame", "Pistilo", "Conífera", "Vaso do xilema"], "answer": "Pistilo"}
]
# Embaralha perguntas
random.shuffle(topics)

app = Dash(__name__)

# Layout
app.layout = html.Div(className="container", children=[
    html.H1("Jogo: Teste seus conhecimentos sobre Fanerógamas!", className="title"),
    html.P("Selecione a alternativa correta para cada pergunta sobre plantas com sementes (fanerógamas).", className="subtitle"),
    dcc.Store(id="current-index", data=0),
    dcc.Store(id="answered", data=False),
    html.Div(id="question-container", className="question-container"),
    dcc.RadioItems(id="options", className="options", labelStyle={"display": "block", "margin": "8px 0", "cursor": "pointer"}),
    html.Div([
        html.Button("Enviar", id="submit-button", n_clicks=0, className="btn"),
        html.Button("Próxima", id="next-button", n_clicks=0, className="btn")
    ], className="buttons"),
    html.Div(id="feedback", className="feedback"),
    html.Div(className="footer", children=html.P("Um jogo idealizado por Vilma, Bruna, Ssara e criado por Álvaro Vargas"))
])

# Exibe pergunta e reseta valor selecionado
@app.callback(
    Output("question-container", "children"),
    Output("options", "options"),
    Output("options", "value"),
    Input("current-index", "data")
)
def display_question(idx):
    q = topics[idx]
    opts = [{"label": opt, "value": opt} for opt in q["options"]]
    return q["question"], opts, None

# Tratamento de interações: envio e próxima (e reset do answered internamente)
@app.callback(
    Output("current-index", "data"),
    Output("feedback", "children"),
    Output("feedback", "className"),
    Output("answered", "data"),
    Input("submit-button", "n_clicks"),
    Input("next-button", "n_clicks"),
    State("options", "value"),
    State("current-index", "data"),
    State("answered", "data")
)
def handle_interactions(submit_clicks, next_clicks, selected, idx, answered):
    ctx = callback_context
    if not ctx.triggered:
        return idx, "", "feedback", answered
    btn = ctx.triggered[0]["prop_id"].split(".")[0]
    correct = topics[idx]["answer"]

    # Envio da resposta
    if btn == "submit-button":
        if not selected:
            return idx, "Selecione uma opção antes de enviar.", "feedback", False
        if selected == correct:
            return idx, "🎉 Correto!", "feedback feedback-correct", True
        return idx, f"❌ Incorreto. A resposta certa é: {correct}.", "feedback feedback-wrong", True

    # Próxima pergunta: só se já tiver respondido
    if btn == "next-button":
        if not answered:
            return idx, "Responda antes de avançar!", "feedback feedback-wrong", False
        new_idx = (idx + 1) % len(topics)
        # após avançar, reset answered
        return new_idx, "", "feedback", False

    return idx, "", "feedback", answered

if __name__ == '__main__':
    app.run(debug=True, port=8080)