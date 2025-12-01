import subprocess
import sys
import re
import argparse
from typing import List, Optional


# --- Funções Auxiliares (Execução de Comandos Git) ---

def run_git_command(command: List[str], check_error: bool = True, capture_output: bool = True,
                    silent_success: bool = False):
    """
    Executa um comando Git e lida com erros.
    Se silent_success for True, não imprime o stdout do comando em caso de sucesso.
    """
    try:
        result = subprocess.run(
            command,
            check=check_error,
            text=True,
            capture_output=capture_output,
            encoding='utf-8'
        )
        # Imprime o output apenas se não for para ser silencioso
        if capture_output and result.stdout and not silent_success:
            print(result.stdout.strip())
        return result
    except subprocess.CalledProcessError as e:
        if not check_error and e.returncode == 1:
            if "nothing to commit" in e.stderr.lower():
                return None

        print(f"\n❌ Erro ao executar o comando: {' '.join(command)}")
        print(f"Stderr: {e.stderr.strip()}")
        sys.exit(1)
    except FileNotFoundError:
        print("\n❌ Erro: O comando 'git' não foi encontrado. Verifique se o Git está no PATH.")
        sys.exit(1)


# --- Funções de Configuração Inicial ---

def check_and_initialize_repo():
    """Verifica se o repositório Git foi inicializado e inicializa se necessário."""
    try:
        # Usa silent_success=True para suprimir o output 'true'
        run_git_command(["git", "rev-parse", "--is-inside-work-tree"], check_error=True, capture_output=True,
                        silent_success=True)
    except subprocess.CalledProcessError:
        print("⚠️ Repositório Git não encontrado. Inicializando agora...")
        run_git_command(["git", "init"], capture_output=False)


def check_and_set_remote():
    """Verifica e configura o remote 'origin'."""
    try:
        # Usa silent_success=True para suprimir o output de 'git remote -v'
        result = run_git_command(["git", "remote", "-v"], check_error=True, capture_output=True, silent_success=True)
        if re.search(r'\borigin\b', result.stdout):
            return

        print("\n⚠️ Remote 'origin' não configurado.")
        while True:
            remote_url = input("Digite o URL do repositório remoto: ")
            if remote_url:
                break

        run_git_command(["git", "remote", "add", "origin", remote_url], capture_output=False)

    except Exception as e:
        print(f"❌ Erro ao verificar/configurar o remote: {e}")
        sys.exit(1)


# --- Funções de Ação ---

def action_show_branch():
    """Exibe o branch Git ativo e o status do remote."""
    print("\n--- Branch Ativa ---")
    try:
        current_branch = run_git_command(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                                         silent_success=True).stdout.strip()
        print(f"Branch Atual: **{current_branch}**")

        remote_info = run_git_command(["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", f"@{'{'}u{'}'}"],
                                      silent_success=True).stdout.strip()
        print(f"Rastreando: {remote_info}")

    except subprocess.CalledProcessError:
        print("Não foi possível determinar o branch. Repositório vazio ou sem commits.")
    except Exception:
        print("Verificação de branch falhou.")
    print("--------------------")


def action_show_status():
    """Mostra o status atual do repositório."""
    print("\n--- Status Atual do Git ---")
    run_git_command(["git", "status"], capture_output=False)
    print("---------------------------\n")


def action_deploy(fast_message: Optional[str] = None, fast_description: Optional[str] = None):
    """Lógica principal de deploy (add, commit, push)."""

    if fast_message:
        title = fast_message
        description = fast_description
    else:
        action_show_status()
        try:
            title = input("Digite o título do commit: ")
            if not title:
                print("Título vazio. Abortando deploy.")
                return

            print("Digite a descrição longa (Enter duas vezes para finalizar): ")
            lines = []
            while True:
                line = input()
                if not line:
                    break
                lines.append(line)
            description = "\n".join(lines)

        except KeyboardInterrupt:
            print("\nOperação cancelada. Abortando deploy.")
            return

    print("\n--- Adicionando todos os arquivos (git add .) ---")
    run_git_command(["git", "add", "."])

    print(f"\n--- Criando commit ---")
    full_commit_message = title
    if description:
        full_commit_message += "\n\n" + description

    commit_command = ["git", "commit", "-m", full_commit_message]
    commit_result = run_git_command(commit_command, check_error=False)

    if commit_result is None:
        print("\n✅ Operação finalizada (Sem alterações para enviar).")
        return

    current_branch = run_git_command(["git", "rev-parse", "--abbrev-ref", "HEAD"], silent_success=True).stdout.strip()
    print(f"\n--- Enviando para o GitHub (git push origin {current_branch}) ---")
    push_command = ["git", "push", "--set-upstream", "origin", current_branch]
    run_git_command(push_command)

    print("\n✅ Projeto enviado com sucesso para o GitHub!")


# --- Modo Menu (Interativo) ---

def show_menu():
    """Exibe o menu principal."""
    print("\n" + "=" * 40)
    print(" Git Deploy CLI - Menu Principal ")
    print("=" * 40)
    print("(1) 🚀 Iniciar Deploy (add, commit, push)")
    print("(2) 🌳 Mostrar Branch Ativa")
    print("(3) 📋 Mostrar Status (git status)")
    print("(0) 🚪 Sair")
    print("-" * 40)


def menu_mode():
    """Loop do menu principal."""
    while True:
        show_menu()
        choice = input("Digite o número da opção: ").strip()

        if choice == '1':
            action_deploy()
        elif choice == '2':
            action_show_branch()
        elif choice == '3':
            action_show_status()
        elif choice == '0':
            print("👋 Fechando a ferramenta CLI. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")


# --- Função Principal e Parser de Argumentos ---

def main():
    """Gerencia a inicialização e roteia entre os modos menu e subcomando."""

    check_and_initialize_repo()
    check_and_set_remote()

    parser = argparse.ArgumentParser(
        description="Utilitário CLI para automatizar o fluxo Git.",
        epilog="Se executado sem subcomando (ex: python cli_tool.py), entra no Modo Menu Interativo."
    )

    subparsers = parser.add_subparsers(dest="command", help="Comandos de ação rápida")

    # Subcomando 'deploy'
    parser_deploy = subparsers.add_parser('deploy', help='Inicia o processo de deploy (add, commit, push).')
    parser_deploy.add_argument(
        "-m", "--message",
        type=str,
        help="Mensagem de commit curta. Se omitida, inicia o modo interativo de commit."
    )
    parser_deploy.add_argument(
        "-d", "--description",
        type=str,
        default=None,
        help="Descrição longa opcional para o commit."
    )

    # Subcomando 'branch'
    subparsers.add_parser('branch', help='Mostra o branch ativo.')

    # Subcomando 'status'
    subparsers.add_parser('status', help='Mostra o status do git (git status).')

    args = parser.parse_args()

    if args.command == 'deploy':
        action_deploy(args.message, args.description)
    elif args.command == 'branch':
        action_show_branch()
    elif args.command == 'status':
        action_show_status()
    else:
        menu_mode()


if __name__ == "__main__":
    main()
# Your code here
