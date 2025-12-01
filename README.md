# GitHub Deployer CLI

`github-deployer` é uma ferramenta de linha de comando (CLI) para automatizar o fluxo de trabalho básico do Git: adicionar, commitar e enviar alterações para um repositório remoto.

## Funcionalidades

- **Modo Interativo**: Um menu fácil de usar para iniciantes.
- **Modo de Comando Rápido**: Argumentos de linha de comando para automação e usuários experientes.
- **Inicialização Automática**: Detecta e inicializa um repositório Git se necessário.
- **Configuração de Remote**: Ajuda a configurar o remote `origin` se ele não existir.

## Instalação

Você pode instalar a ferramenta diretamente do PyPI:

```bash
pip install github-deployer-cli
```

## Como Usar

Após a instalação, o comando `github-deployer` estará disponível no seu terminal.

### Modo Interativo (Menu)

Para uma experiência guiada, simplesmente execute o comando sem argumentos:

```bash
github-deployer
```

Você verá um menu com as seguintes opções:
- **Iniciar Deploy**: Guia você através do processo de adicionar, commitar e enviar seus arquivos.
- **Mostrar Branch Ativa**: Exibe o branch atual e seu status de rastreamento.
- **Mostrar Status**: Executa `git status` para mostrar o estado do seu repositório.

### Comandos Rápidos

Para um fluxo de trabalho mais rápido, você pode usar subcomandos:

#### Deploy Rápido

Para fazer um deploy com uma mensagem de commit curta:

```bash
github-deployer deploy -m "Sua mensagem de commit"
```

Para adicionar também uma descrição longa:

```bash
github-deployer deploy -m "Título do Commit" -d "Descrição mais detalhada sobre as alterações."
```

#### Outros Comandos

```bash
# Mostrar o branch atual
github-deployer branch

# Mostrar o status do Git
github-deployer status
```

## Licença

Este projeto é licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
