#!/usr/bin/env python3
"""
DEVertidamente API - Backend FastAPI
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict
import json
import os

app = FastAPI(
    title="DEVertidamente API",
    description="API para registro de sentimentos diários",
    version="1.0.0"
)

# CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Arquivos de dados
SENTIMENTOS_FILE = "sentimentos.json"
REGISTRO_FILE = "registro.json"

# Models
class RegistroInput(BaseModel):
    sentimento: str
    nota: Optional[str] = None
    data: Optional[str] = None
    horario: Optional[str] = None  # Formato: "HH:MM" ou período como "manhã", "tarde", "noite"

class RegistroOutput(BaseModel):
    data: str
    horario: str
    sentimento: str
    nota: Optional[str] = None

class RegistroDia(BaseModel):
    data: str
    registros: list[dict]

# Funções auxiliares
def carregar_sentimentos():
    """Carrega a configuração de sentimentos"""
    if not os.path.exists(SENTIMENTOS_FILE):
        # Criar arquivo padrão se não existir
        sentimentos_padrao = {
            "alegria": {"emoji": "😊", "cor": "#FFD700"},
            "tristeza": {"emoji": "😢", "cor": "#4A90E2"},
            "raiva": {"emoji": "😠", "cor": "#E74C3C"},
            "nojinho": {"emoji": "🤢", "cor": "#2ECC71"},
            "medo": {"emoji": "😨", "cor": "#9B59B6"},
            "ansiedade": {"emoji": "😰", "cor": "#FF6B6B"},
            "tedio": {"emoji": "😑", "cor": "#95A5A6"},
            "vergonha": {"emoji": "😳", "cor": "#FF69B4"},
            "inveja": {"emoji": "😒", "cor": "#00CED1"},
            "nostalgia": {"emoji": "🥺", "cor": "#DEB887"}
        }
        with open(SENTIMENTOS_FILE, 'w', encoding='utf-8') as f:
            json.dump(sentimentos_padrao, f, indent=2, ensure_ascii=False)
        return sentimentos_padrao
    
    with open(SENTIMENTOS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def carregar_registro():
    """Carrega o registro de sentimentos"""
    if not os.path.exists(REGISTRO_FILE):
        return {}
    
    with open(REGISTRO_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_registro(registro: Dict):
    """Salva o registro de sentimentos"""
    with open(REGISTRO_FILE, 'w', encoding='utf-8') as f:
        json.dump(registro, f, indent=2, ensure_ascii=False)

# Rotas da API

@app.get("/")
async def root():
    """Serve o frontend"""
    return FileResponse("index.html")

@app.get("/api/sentimentos")
async def get_sentimentos():
    """Retorna a lista de sentimentos disponíveis"""
    sentimentos = carregar_sentimentos()
    return {"sentimentos": sentimentos}

@app.get("/api/registro")
async def get_registro():
    """Retorna todos os registros"""
    registro = carregar_registro()
    return {"registro": registro}

@app.get("/api/registro/{data}")
async def get_registro_data(data: str):
    """Retorna o registro de uma data específica"""
    registro = carregar_registro()
    
    if data not in registro:
        raise HTTPException(status_code=404, detail="Registro não encontrado para esta data")
    
    return {
        "data": data,
        **registro[data]
    }

@app.post("/api/registro", response_model=RegistroOutput)
async def criar_registro(entrada: RegistroInput):
    """Cria ou adiciona um registro de sentimento"""
    sentimentos = carregar_sentimentos()
    
    # Validar sentimento
    if entrada.sentimento not in sentimentos:
        raise HTTPException(
            status_code=400, 
            detail=f"Sentimento inválido. Opções: {', '.join(sentimentos.keys())}"
        )
    
    # Data (hoje se não especificada)
    data = entrada.data or datetime.now().strftime("%Y-%m-%d")
    
    # Horário (agora se não especificado)
    horario = entrada.horario or datetime.now().strftime("%H:%M")
    
    # Carregar registro existente
    registro = carregar_registro()
    
    # Inicializar estrutura do dia se não existir
    if data not in registro:
        registro[data] = {"registros": []}
    elif "sentimento" in registro[data]:
        # Migrar formato antigo para novo
        registro[data] = {
            "registros": [{
                "horario": "12:00",
                "sentimento": registro[data]["sentimento"],
                "nota": registro[data].get("nota")
            }]
        }
    
    # Adicionar novo registro
    novo_registro = {
        "horario": horario,
        "sentimento": entrada.sentimento,
        "nota": entrada.nota
    }
    
    registro[data]["registros"].append(novo_registro)
    
    # Ordenar por horário
    registro[data]["registros"].sort(key=lambda x: x["horario"])
    
    # Salvar
    salvar_registro(registro)
    
    return {
        "data": data,
        "horario": horario,
        "sentimento": entrada.sentimento,
        "nota": entrada.nota
    }

@app.delete("/api/registro/{data}")
async def deletar_registro(data: str, horario: Optional[str] = None):
    """Remove um registro ou todos os registros de um dia"""
    registro = carregar_registro()
    
    if data not in registro:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    
    if horario:
        # Deletar apenas o registro específico do horário
        if "registros" in registro[data]:
            registro[data]["registros"] = [
                r for r in registro[data]["registros"] 
                if r["horario"] != horario
            ]
            if not registro[data]["registros"]:
                del registro[data]
        else:
            # Formato antigo - deletar tudo
            del registro[data]
    else:
        # Deletar o dia inteiro
        del registro[data]
    
    salvar_registro(registro)
    
    msg = f"Registro de {data}"
    if horario:
        msg += f" às {horario}"
    msg += " removido com sucesso"
    
    return {"message": msg}

@app.get("/api/estatisticas")
async def get_estatisticas():
    """Retorna estatísticas dos sentimentos"""
    registro = carregar_registro()
    sentimentos = carregar_sentimentos()
    
    if not registro:
        return {
            "total_dias": 0,
            "total_registros": 0,
            "estatisticas": []
        }
    
    # Contar sentimentos
    contador = {}
    total_registros = 0
    
    for data, info in registro.items():
        # Suportar formato antigo e novo
        if "registros" in info:
            for reg in info["registros"]:
                sentimento = reg["sentimento"]
                contador[sentimento] = contador.get(sentimento, 0) + 1
                total_registros += 1
        else:
            # Formato antigo
            sentimento = info['sentimento']
            contador[sentimento] = contador.get(sentimento, 0) + 1
            total_registros += 1
    
    # Calcular percentuais
    estatisticas = []
    
    for sentimento, count in sorted(contador.items(), key=lambda x: x[1], reverse=True):
        estatisticas.append({
            "sentimento": sentimento,
            "emoji": sentimentos[sentimento]["emoji"],
            "cor": sentimentos[sentimento]["cor"],
            "count": count,
            "percentage": round((count / total_registros) * 100, 1)
        })
    
    return {
        "total_dias": len(registro),
        "total_registros": total_registros,
        "estatisticas": estatisticas
    }

@app.get("/api/ano/{ano}")
async def get_ano(ano: int):
    """Retorna todos os registros de um ano específico"""
    registro = carregar_registro()
    
    registros_ano = {
        data: info 
        for data, info in registro.items() 
        if data.startswith(str(ano))
    }
    
    return {
        "ano": ano,
        "total_dias": len(registros_ano),
        "registro": registros_ano
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)