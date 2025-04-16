from dash import Dash, html, dcc, Input, Output, State, callback_context, ALL
import random

# Configurar imagens para cada opção (substitua pelas URLs reais)
option_images = {
    "Samambaia": "https://cdn-icons-png.flaticon.com/512/5795/5795571.png",
    "Pinheiro": "https://cdn-icons-png.flaticon.com/512/415/415733.png",
    "Musgo": "https://cdn-icons-png.flaticon.com/512/4975/4975823.png",
    "Líquens": "https://cdn-icons-png.flaticon.com/512/4975/4975857.png",
    "Gimnospermas e angiospermas": "https://cdn-icons-png.flaticon.com/512/4975/4975827.png",
    "Produzem frutos que envolvem as sementes": "https://cdn-icons-png.flaticon.com/512/1019/1019680.png",
    "Expostas em estruturas como cones": "https://cdn-icons-png.flaticon.com/512/4975/4975825.png",
    "Pistilo": "https://cdn-icons-png.flaticon.com/512/4975/4975864.png",
    # Adicione outras imagens conforme necessário
}

# Perguntas sobre fanerógamas
topics = [
    {"question": "Qual das seguintes plantas é uma fanerógama?", "options": ["Samambaia", "Pinheiro", "Musgo", "Líquens"], "answer": "Pinheiro"},
    {"question": "As fanerógamas se dividem em quais dois principais grupos?", "options": ["Briófitas e pteridófitas", "Gimnospermas e angiospermas", "Fungos e algas", "Hepáticas e musgos"], "answer": "Gimnospermas e angiospermas"},
    {"question": "Qual característica define angiospermas?", "options": ["Produzem sementes expostas", "Não possuem vasos condutores", "Produzem frutos que envolvem as sementes", "Reprodução por esporos"], "answer": "Produzem frutos que envolvem as sementes"},
    {"question": "As gimnospermas possuem sementes:", "options": ["Dentro de frutos", "Expostas em estruturas como cones", "Em cápsulas aquosas", "Em folículos"], "answer": "Expostas em estruturas como cones"},
    {"question": "Qual é o órgão reprodutivo feminino das angiospermas?", "options": ["Estame", "Pistilo", "Conífera", "Vaso do xilema"], "answer": "Pistilo"}
]

random.shuffle(topics)

app = Dash(__name__, suppress_callback_exceptions=True)

# Remover título "Dash" e adicionar favicon
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Quiz de Fanerógamas</title>
        <link rel="icon" type="image/png" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAACZSURBVDhPY2CgNXj16tV/BgbGPAYqAEY0NhQYGBj6GRkZ/5MT4wzIABTg5+fHKCQk9J+UZMCAAQaQACMjI0pMkQNQYgBdG3EGurq6MgYHBzOC3DAzM8MYHh7OqKioiKIG7oYXL14w7ty5k/Hv37+M0tLSjJ6enihq4G4AAFiKIdsvW95ZAAAAAElFTkSuQmCC"/>
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = html.Div(className="container", children=[
    html.H1("Jogo: Teste seus conhecimentos sobre Fanerógamas!", className="title"),
    dcc.Store(id="current-index", data=0),
    dcc.Store(id="answered", data=False),
    dcc.Store(id="selected-option", data=None),
    
    html.Div(id="question-container", className="question-container"),
    html.Div(id="options-grid", className="options-grid"),
    
    html.Div([
        html.Button("Enviar", id="submit-button", n_clicks=0, className="btn"),
        html.Button("Próxima", id="next-button", n_clicks=0, className="btn")
    ], className="buttons"),
    
    html.Div(id="feedback", className="feedback"),
    html.Div(className="footer", children=html.P("Um jogo idealizado por Vilma, Bruna, Ssara e criado por Álvaro Vargas"))
])

@app.callback(
    Output("question-container", "children"),
    Output("options-grid", "children"),
    Input("current-index", "data")
)
def update_question(idx):
    question = topics[idx]["question"]
    options = topics[idx]["options"]
    
    buttons = []
    for opt in options:
        buttons.append(
            html.Button(
                children=[
                    html.Img(src=option_images.get(opt, "https://via.placeholder.com/150"), 
                            className="option-image"),
                    html.Div(opt, className="option-text")
                ],
                className="option-button",
                id={"type": "option", "index": opt},
                n_clicks=0
            )
        )
    
    return question, buttons

@app.callback(
    Output({"type": "option", "index": ALL}, "className"),
    Input({"type": "option", "index": ALL}, "n_clicks"),
    State("current-index", "data"),
    prevent_initial_call=True
)
def select_option(clicks, idx):
    ctx = callback_context
    if not ctx.triggered:
        return ["option-button"] * len(topics[idx]["options"])
    
    selected_id = ctx.triggered[0]["prop_id"].split(".")[0]
    selected_option = eval(selected_id)["index"]
    
    return [
        "option-button selected" if opt == selected_option else "option-button"
        for opt in topics[idx]["options"]
    ]

@app.callback(
    Output("current-index", "data"),
    Output("feedback", "children"),
    Output("feedback", "className"),
    Output("answered", "data"),
    Input("submit-button", "n_clicks"),
    Input("next-button", "n_clicks"),
    State({"type": "option", "index": ALL}, "n_clicks"),
    State("current-index", "data"),
    State("answered", "data")
)
def handle_interactions(submit_clicks, next_clicks, option_clicks, idx, answered):
    ctx = callback_context
    if not ctx.triggered:
        return idx, "", "feedback", answered
    
    btn = ctx.triggered[0]["prop_id"].split(".")[0]
    correct = topics[idx]["answer"]
    selected = topics[idx]["options"][option_clicks.index(1)] if 1 in option_clicks else None

    if btn == "submit-button":
        if not selected:
            return idx, "Selecione uma opção antes de enviar!", "feedback feedback-wrong", False
        if selected == correct:
            return idx, "🎉 Resposta Correta!", "feedback feedback-correct", True
        return idx, f"❌ Errado! A resposta correta é: {correct}", "feedback feedback-wrong", True

    if btn == "next-button":
        if not answered:
            return idx, "Responda antes de avançar!", "feedback feedback-wrong", False
        new_idx = (idx + 1) % len(topics)
        return new_idx, "", "feedback", False

    return idx, "", "feedback", answered

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)