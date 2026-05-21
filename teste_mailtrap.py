import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText

def testar_conexao():
    print("--- TESTE DE CONEXÃO MAILTRAP ---")
    
    # Tenta carregar o .env
    if os.path.exists(".env"):
        load_dotenv()
        print("[OK] Arquivo .env encontrado.")
    else:
        print("[ERRO] Arquivo .env NÃO encontrado na raiz do projeto!")
        return

    user = os.getenv("MAIL_USERNAME")
    password = os.getenv("MAIL_PASSWORD")
    server_host = os.getenv("MAIL_SERVER")
    port = os.getenv("MAIL_PORT")

    print(f"Dados carregados do .env:")
    print(f"  Servidor: {server_host}")
    print(f"  Porta: {port}")
    print(f"  Usuário: {user}")
    print(f"  Senha: {'*' * len(password) if password else 'VAZIA'}")

    if not all([user, password, server_host, port]):
        print("\n[ERRO] Algumas variáveis estão faltando no seu arquivo .env!")
        return

    try:
        port = int(port)
        print(f"\nTentando conectar a {server_host}:{port}...")
        
        server = smtplib.SMTP(server_host, port, timeout=10)
        print("[OK] Conectado ao servidor.")
        
        print("Iniciando STARTTLS...")
        server.starttls()
        print("[OK] STARTTLS ativado.")
        
        print("Tentando fazer login...")
        server.login(user, password)
        print("[OK] Login realizado com sucesso!")
        
        print("Enviando e-mail de teste...")
        msg = MIMEText("Este é um teste do sistema de bombeiros.")
        msg["Subject"] = "Teste de Conexão Mailtrap"
        msg["From"] = "teste@bombeiros.com"
        msg["To"] = "seu-email@teste.com"
        
        server.send_message(msg)
        print("[SUCESSO] E-mail de teste enviado! Verifique sua caixa de entrada no Mailtrap.")
        
        server.quit()
        
    except Exception as e:
        print(f"\n[FALHA] Ocorreu um erro: {e}")
        print("\nDica: Verifique se o seu antivírus ou firewall não está bloqueando a porta 2525 ou 587.")

if __name__ == "__main__":
    testar_conexao()