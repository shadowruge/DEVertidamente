# 🚀 Guia de Instalação e Uso - DEVertidamente

## 📋 Pré-requisitos

- Python 3.6 ou superior
- Git instalado
- Conta no GitHub

## 🔧 Instalação

### 1. Criar o repositório no GitHub

1. Acesse [GitHub](https://github.com) e faça login
2. Clique em "New repository"
3. Nome do repositório: `DEVertidamente`
4. Adicione uma descrição: "Registro diário dos meus sentimentos inspirado no filme Divertidamente"
5. Escolha se será público ou privado
6. **NÃO** marque "Add a README file"
7. Clique em "Create repository"

### 2. Configurar o projeto localmente

```bash
# Clone ou baixe os arquivos do projeto
cd /caminho/para/seus/projetos
git clone <url-deste-repo-temporario>
cd DEVertidamente

# Ou crie a pasta e adicione os arquivos manualmente
mkdir DEVertidamente
cd DEVertidamente
# [Copie todos os arquivos para esta pasta]

# Inicializar repositório Git
git init
git add .
git commit -m "🎭 Commit inicial: DEVertidamente"

# Conectar ao seu repositório GitHub
git remote add origin https://github.com/SEU_USUARIO/DEVertidamente.git
git branch -M main
git push -u origin main
```

## 📝 Como usar diariamente

### Método 1: Script Automático (Recomendado)

```bash
./commit_diario.sh
```

Este script irá:
1. Pedir para você escolher seu sentimento do dia
2. Atualizar o gráfico automaticamente
3. Criar um commit com mensagem formatada
4. Perguntar se você quer fazer push

### Método 2: Passo a passo manual

```bash
# 1. Registrar seu sentimento
python3 registrar.py

# 2. Atualizar o gráfico e README
python3 gerar_grafico.py

# 3. Fazer commit
git add .
git commit -m "Sentimento do dia: 😊 Alegria"
git push
```

## 🎨 Sentimentos disponíveis

| Sentimento | Emoji | Cor Hex |
|------------|-------|---------|
| Alegria    | 😊    | #F7D917 |
| Tristeza   | 😢    | #5B9BD5 |
| Raiva      | 😠    | #C00000 |
| Nojo       | 🤢    | #70AD47 |
| Medo       | 😨    | #7030A0 |
| Ansiedade  | 😰    | #FFA500 |
| Vergonha   | 😳    | #FF69B4 |
| Tédio      | 😑    | #808080 |
| Nostalgia  | 🥺    | #D2691E |
| Inveja     | 😒    | #00CED1 |

## 💡 Dicas

1. **Seja consistente**: Tente registrar todos os dias, de preferência no mesmo horário
2. **Adicione notas**: Use o campo de nota para contextualizar seu sentimento
3. **Revise periodicamente**: Olhe as estatísticas para identificar padrões
4. **Privacidade**: Considere deixar o repositório privado se for compartilhar informações sensíveis

## 🔄 Automatização (Opcional)

### Lembrete diário no Linux/Mac

Adicione ao seu crontab:

```bash
# Editar crontab
crontab -e

# Adicionar linha (exemplo: todo dia às 20h)
0 20 * * * cd /caminho/para/DEVertidamente && /caminho/para/DEVertidamente/commit_diario.sh
```

### Lembrete no Windows

Use o Agendador de Tarefas do Windows para executar o script diariamente.

## 🐛 Solução de Problemas

### Erro: "python3 not found"
- No Windows, tente usar `python` ao invés de `python3`
- Certifique-se de que o Python está instalado e no PATH

### Erro: "permission denied"
```bash
chmod +x registrar.py gerar_grafico.py commit_diario.sh
```

### O gráfico não aparece no GitHub
- Verifique se o arquivo `grafico.svg` foi commitado
- O GitHub pode levar alguns minutos para atualizar a visualização

## 📊 Estrutura do Projeto

```
DEVertidamente/
├── sentimentos.json      # Configuração dos sentimentos e cores
├── registro.json         # Seu histórico de sentimentos
├── registrar.py          # Script para registrar sentimento
├── gerar_grafico.py      # Script para gerar gráfico e README
├── commit_diario.sh      # Script de automação
├── grafico.svg           # Gráfico visual (atualizado automaticamente)
├── README.md             # Documentação (atualizada automaticamente)
└── .gitignore           # Arquivos ignorados pelo Git
```

## 🎯 Próximos passos

- [ ] Configurar seu repositório no GitHub
- [ ] Fazer o primeiro registro
- [ ] Estabelecer uma rotina diária
- [ ] Revisar suas estatísticas semanalmente

---

**Lembre-se**: Este projeto é sobre autoconsciência emocional. Não há respostas certas ou erradas! 💙
