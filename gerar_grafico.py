#!/usr/bin/env python3
"""
Gerador de gráfico de sentimentos - estilo GitHub contributions
"""

import json
from datetime import datetime, timedelta
from collections import defaultdict

SENTIMENTOS_FILE = "sentimentos.json"
REGISTRO_FILE = "registro.json"

def carregar_dados():
    """Carrega sentimentos e registro"""
    with open(SENTIMENTOS_FILE, 'r', encoding='utf-8') as f:
        sentimentos = json.load(f)
    
    try:
        with open(REGISTRO_FILE, 'r', encoding='utf-8') as f:
            registro = json.load(f)
    except FileNotFoundError:
        registro = {}
    
    return sentimentos, registro

def gerar_grafico_svg(registro, sentimentos, num_semanas=52):
    """Gera um SVG com o gráfico de sentimentos estilo GitHub"""
    
    # Configurações
    tamanho_celula = 12
    espacamento = 2
    margem_esquerda = 40
    margem_topo = 20
    
    # Calcular dimensões
    largura = margem_esquerda + (num_semanas * (tamanho_celula + espacamento))
    altura = margem_topo + (7 * (tamanho_celula + espacamento)) + 30
    
    # Data final (hoje) e inicial
    data_final = datetime.now()
    data_inicial = data_final - timedelta(weeks=num_semanas)
    
    # Começar SVG
    svg = [f'<svg width="{largura}" height="{altura}" xmlns="http://www.w3.org/2000/svg">']
    svg.append('<style>')
    svg.append('.dia { rx: 2; }')
    svg.append('.dia:hover { stroke: #000; stroke-width: 1; }')
    svg.append('.mes-label { font-size: 10px; fill: #767676; }')
    svg.append('.dia-label { font-size: 9px; fill: #767676; }')
    svg.append('</style>')
    
    # Título
    svg.append(f'<text x="{largura/2}" y="15" text-anchor="middle" style="font-size: 14px; font-weight: bold; fill: #333;">DEVertidamente - Mapa de Sentimentos</text>')
    
    # Labels dos dias da semana
    dias_semana = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
    for i, dia in enumerate(['Seg', 'Qua', 'Sex']):  # Apenas alguns para não poluir
        y = margem_topo + (dias_semana.index(dia) * (tamanho_celula + espacamento)) + tamanho_celula/2 + 3
        svg.append(f'<text x="5" y="{y}" class="dia-label" text-anchor="start">{dia}</text>')
    
    # Gerar células
    data_atual = data_inicial
    semana = 0
    mes_anterior = None
    
    while data_atual <= data_final:
        dia_semana = data_atual.weekday()  # 0 = segunda
        
        # Adicionar label do mês
        if data_atual.day <= 7 and data_atual.month != mes_anterior:
            x = margem_esquerda + (semana * (tamanho_celula + espacamento))
            svg.append(f'<text x="{x}" y="{margem_topo - 5}" class="mes-label">{data_atual.strftime("%b")}</text>')
            mes_anterior = data_atual.month
        
        # Posição da célula
        x = margem_esquerda + (semana * (tamanho_celula + espacamento))
        y = margem_topo + (dia_semana * (tamanho_celula + espacamento))
        
        # Verificar se há registro para esse dia
        data_str = data_atual.strftime("%Y-%m-%d")
        if data_str in registro:
            sentimento = registro[data_str]['sentimento']
            cor = sentimentos[sentimento]['cor']
            emoji = sentimentos[sentimento]['emoji']
            nota = registro[data_str].get('nota', '')
            
            tooltip = f"{data_str}: {emoji} {sentimento.capitalize()}"
            if nota:
                tooltip += f" - {nota}"
            
            svg.append(f'<rect x="{x}" y="{y}" width="{tamanho_celula}" height="{tamanho_celula}" '
                      f'fill="{cor}" class="dia">')
            svg.append(f'<title>{tooltip}</title>')
            svg.append('</rect>')
        else:
            # Dia sem registro
            svg.append(f'<rect x="{x}" y="{y}" width="{tamanho_celula}" height="{tamanho_celula}" '
                      f'fill="#ebedf0" class="dia">')
            svg.append(f'<title>{data_str}: Sem registro</title>')
            svg.append('</rect>')
        
        # Avançar para próximo dia
        data_atual += timedelta(days=1)
        if dia_semana == 6:  # Domingo, próxima semana
            semana += 1
    
    svg.append('</svg>')
    
    return '\n'.join(svg)

def gerar_estatisticas(registro, sentimentos):
    """Gera estatísticas dos sentimentos"""
    if not registro:
        return "Nenhum registro ainda."
    
    contador = defaultdict(int)
    for data, info in registro.items():
        contador[info['sentimento']] += 1
    
    total = len(registro)
    
    # Ordenar por frequência
    ranking = sorted(contador.items(), key=lambda x: x[1], reverse=True)
    
    stats = [f"\n📊 **Estatísticas** ({total} dias registrados)\n"]
    
    for sentimento, count in ranking:
        emoji = sentimentos[sentimento]['emoji']
        porcentagem = (count / total) * 100
        barra = "█" * int(porcentagem / 5)
        stats.append(f"- {emoji} **{sentimento.capitalize()}**: {count} dias ({porcentagem:.1f}%) {barra}")
    
    return '\n'.join(stats)

def atualizar_readme():
    """Atualiza o README.md com o gráfico e estatísticas"""
    sentimentos, registro = carregar_dados()
    
    # Gerar SVG
    svg_content = gerar_grafico_svg(registro, sentimentos)
    
    # Salvar SVG
    with open('grafico.svg', 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    # Gerar estatísticas
    stats = gerar_estatisticas(registro, sentimentos)
    
    # Legenda
    legenda = ["\n## 🎨 Legenda de Sentimentos\n"]
    for sentimento, config in sentimentos.items():
        cor = config['cor']
        emoji = config['emoji']
        legenda.append(f"- {emoji} **{sentimento.capitalize()}** `{cor}`")
    
    # Criar README
    readme = f"""# 🎭 DEVertidamente

> Inspirado no filme **Divertidamente (Inside Out)**, este projeto registra meu sentimento predominante a cada dia.

## 📅 Mapa de Sentimentos

![Mapa de Sentimentos](grafico.svg)

{''.join(legenda)}

{stats}

---

## 🚀 Como usar

1. **Registrar sentimento do dia:**
   ```bash
   python registrar.py
   ```

2. **Atualizar o gráfico:**
   ```bash
   python gerar_grafico.py
   ```

3. **Fazer commit:**
   ```bash
   git add .
   git commit -m "Sentimento do dia: [EMOJI] [SENTIMENTO]"
   git push
   ```

## 💡 Sobre o projeto

Este projeto é uma forma de acompanhar minha saúde emocional ao longo do tempo, identificando padrões e tendências nos meus sentimentos predominantes.

Última atualização: {datetime.now().strftime("%d/%m/%Y")}
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme)
    
    print("✅ README.md e grafico.svg atualizados!")

if __name__ == "__main__":
    atualizar_readme()
