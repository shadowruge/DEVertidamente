#!/bin/bash
# Script de automação para commit diário do DEVertidamente

echo "🎭 DEVertidamente - Commit Automático"
echo ""

# Registrar sentimento
python3 registrar.py

if [ $? -eq 0 ]; then
    # Atualizar gráfico e README
    echo ""
    echo "📊 Atualizando gráfico..."
    python3 gerar_grafico.py
    
    # Obter o último sentimento registrado
    ULTIMO_SENTIMENTO=$(python3 -c "
import json
from datetime import datetime

with open('registro.json', 'r') as f:
    registro = json.load(f)
    
with open('sentimentos.json', 'r') as f:
    sentimentos = json.load(f)

data_hoje = datetime.now().strftime('%Y-%m-%d')
if data_hoje in registro:
    sentimento = registro[data_hoje]['sentimento']
    emoji = sentimentos[sentimento]['emoji']
    print(f'{emoji} {sentimento.capitalize()}')
")
    
    # Git add
    git add .
    
    # Commit com mensagem automática
    MENSAGEM="Sentimento do dia: ${ULTIMO_SENTIMENTO}"
    git commit -m "${MENSAGEM}"
    
    echo ""
    echo "✅ Commit realizado: ${MENSAGEM}"
    echo ""
    read -p "Deseja fazer push? (s/n): " RESPOSTA
    
    if [ "$RESPOSTA" = "s" ] || [ "$RESPOSTA" = "S" ]; then
        git push
        echo "✅ Push realizado com sucesso!"
    else
        echo "ℹ️ Push cancelado. Você pode fazer manualmente com: git push"
    fi
else
    echo "❌ Erro ao registrar sentimento."
fi
