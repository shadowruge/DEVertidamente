#!/usr/bin/env python3
"""
DEVertidamente - Registro de Sentimentos Diários
Inspirado no filme Divertidamente (Inside Out)
"""

import json
import os
from datetime import datetime

SENTIMENTOS_FILE = "sentimentos.json"
REGISTRO_FILE = "registro.json"

def carregar_sentimentos():
    """Carrega a configuração de sentimentos"""
    with open(SENTIMENTOS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def carregar_registro():
    """Carrega o registro histórico de sentimentos"""
    if os.path.exists(REGISTRO_FILE):
        with open(REGISTRO_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def salvar_registro(registro):
    """Salva o registro de sentimentos"""
    with open(REGISTRO_FILE, 'w', encoding='utf-8') as f:
        json.dump(registro, f, indent=2, ensure_ascii=False)

def registrar_sentimento():
    """Registra o sentimento do dia"""
    sentimentos = carregar_sentimentos()
    registro = carregar_registro()
    
    print("\n🎭 DEVertidamente - Como você está se sentindo hoje?\n")
    
    # Listar sentimentos disponíveis
    sentimentos_lista = list(sentimentos.keys())
    for i, sentimento in enumerate(sentimentos_lista, 1):
        emoji = sentimentos[sentimento]['emoji']
        print(f"{i}. {emoji} {sentimento.capitalize()}")
    
    # Obter escolha do usuário
    while True:
        try:
            escolha = int(input("\nEscolha o número do sentimento (1-10): "))
            if 1 <= escolha <= len(sentimentos_lista):
                sentimento_escolhido = sentimentos_lista[escolha - 1]
                break
            else:
                print("❌ Número inválido. Tente novamente.")
        except ValueError:
            print("❌ Por favor, digite um número válido.")
    
    # Opcional: adicionar nota
    nota = input("\n📝 Quer adicionar uma nota? (Enter para pular): ").strip()
    
    # Registrar
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    registro[data_hoje] = {
        "sentimento": sentimento_escolhido,
        "nota": nota if nota else None
    }
    
    salvar_registro(registro)
    
    emoji = sentimentos[sentimento_escolhido]['emoji']
    print(f"\n✅ Sentimento registrado: {emoji} {sentimento_escolhido.capitalize()}")
    print(f"📅 Data: {data_hoje}")
    
    return data_hoje, sentimento_escolhido

if __name__ == "__main__":
    registrar_sentimento()
