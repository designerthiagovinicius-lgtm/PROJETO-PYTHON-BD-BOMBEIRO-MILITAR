import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

#comentario: Este código é responsável por enviar e-mails relacionados à segurança de contas, 
#como recuperação de senha, notificações de alteração de senha, alertas de bloqueio de conta
#e relatórios para administradores. Ele utiliza as configurações de e-mail definidas em variáveis 
#de ambiente e inclui uma função interna para reduzir a repetição de código no envio de e-mails.




load_dotenv()

def _enviar_email(to_email: str, subject: str, body: str) -> bool:
    """Função interna para reduzir repetição de código de envio."""
    sender_email = os.getenv("MAIL_USERNAME")
    sender_password = os.getenv("MAIL_PASSWORD")
    smtp_server = os.getenv("MAIL_SERVER")
    smtp_port = int(os.getenv("MAIL_PORT", 587))

    if not all([sender_email, sender_password, smtp_server]):
        return False

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail para {to_email}: {e}")
        return False

def send_password_reset_email(recipient_email: str, new_password: str) -> bool:
    subject = "Recuperação de Senha - Novo Acesso"
    body = f"Olá!\n\nSua nova senha temporária é: {new_password}\n\nRecomendamos alterar após o primeiro login.\n\nAtenciosamente, admin"
    return _enviar_email(recipient_email, subject, body)

def send_password_change_notification(recipient_email: str) -> bool:
    subject = "Segurança: Sua senha foi alterada"
    body = f"Olá!\n\nSua senha foi alterada recentemente. Se não foi você, contate o administrador."
    return _enviar_email(recipient_email, subject, body)

def send_account_blocked_email(recipient_email: str) -> bool:
    subject = "ALERTA: Sua conta foi bloqueada"
    body = f"Olá!\n\nSua conta ({recipient_email}) foi bloqueada após 3 erros de senha. Contate um admin."
    return _enviar_email(recipient_email, subject, body)

def send_unlocked_notification(recipient_email: str, admin_nome: str) -> bool:
    """Notifica o usuário que ele foi desbloqueado."""
    subject = "Conta Desbloqueada - Acesso Restaurado"
    body = f"Olá!\n\nBoas notícias! Sua conta foi desbloqueada pelo administrador {admin_nome}.\n\nVocê já pode realizar o login normalmente."
    return _enviar_email(recipient_email, subject, body)

def send_admin_blocked_report(admin_email: str, usuario_bloqueado: str, lista_bloqueados: list) -> bool:
    """Envia relatório de usuários bloqueados para os administradores."""
    subject = "RELATÓRIO: Novo Usuário Bloqueado no Sistema"
    
    lista_str = "\n".join([f"- {u[1]} ({u[2]}) - {u[3]}" for u in lista_bloqueados])
    
    body = f"Olá Administrador,\n\nO usuário {usuario_bloqueado} acabou de ser bloqueado por excesso de tentativas.\n\nLista atual de usuários bloqueados:\n{lista_str}\n\nPor favor, verifique o painel administrativo ."
    return _enviar_email(admin_email, subject, body)