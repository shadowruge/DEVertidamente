#!/bin/bash

echo "🎭 DEVertidamente - Iniciando..."
echo ""

# Verificar se uvicorn está instalado
if ! command -v uvicorn &> /dev/null
then
    echo "❌ Uvicorn não encontrado. Instalando dependências..."
    pip install -r requirements.txt
    echo "✅ Dependências instaladas!"
    echo ""
fi

echo "🚀 Iniciando servidor FastAPI..."
echo "📍 Acesse: http://localhost:8000"
echo ""
echo "💡 Pressione Ctrl+C para parar o servidor"
echo ""

uvicorn main:app --reload --host 0.0.0.0 --port 8000