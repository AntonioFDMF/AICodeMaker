from openai import OpenAI
from google import genai
from telebot import TeleBot
from Gerendirs import codigos, ler, AIsWriter, escrever
from subprocess import Popen

global IA
IA = "IA"

bot = TeleBot(CHAVE_API_TeleBot)
clientgpt = OpenAI(api_key=CHAVE_API_OpenAI)
clientgemini = genai.Client(api_key=CHAVE_API_Genai)


def runcode(code):
    Popen([r"...\AppData\Local\Programs\Python\Python312\python.exe"] + [f"{code[0]}"], cwd=fr"{code[1]}")


@bot.message_handler(commands=['start'])
def comando_start(message):
    if message.from_user.id != SUA_CHAVE_USER_ID:
        bot.reply_to(message, "Desculpe, este bot é privado e você não tem permissão para usá-lo.")
        return
    
    boas_vindas = """🤖 Olá, Fulano! Bem vindo ao codemaker!

✨ Envie solicitações para que eu altere ou crie códigos (ainda não consigo ler imagens e não salvo nosso histórico de conversa).
📌 Comandos:
/start - Iniciar
/help - Ajuda
/ping - Verifica se estou online
/chatgpt - Seleciona a IA ChatGPT como editor de código
/gemini - Seleciona a IA Gemini como editor de código
/return - Volta à central do S.P.A.C.E."""
    
    bot.reply_to(message, boas_vindas)


@bot.message_handler(commands=['help'])
def comando_help(message):
    if message.from_user.id != SUA_CHAVE_USER_ID:
        bot.reply_to(message, "Desculpe, este bot é privado e você não tem permissão para usá-lo.")
        return
    bot.reply_to(message, """📌 Comandos:
/start - Iniciar
/help - Ajuda
/ping - Verifica se estou online
/chatgpt - Seleciona a IA ChatGPT como editor de código
/gemini - Seleciona a IA Gemini como editor de código
/return - Volta à central do S.P.A.C.E.""")


@bot.message_handler(commands=['ping'])
def comando_ping(message):
    if message.from_user.id != SUA_CHAVE_USER_ID:
        bot.reply_to(message, "Desculpe, este bot é privado e você não tem permissão para usá-lo.")
        return
    bot.reply_to(message, "🏓 Pong!")


@bot.message_handler(commands=['chatgpt'])
def comando_chatgpt(message):
    global IA
    if message.from_user.id != SUA_CHAVE_USER_ID:
        bot.reply_to(message, "Desculpe, este bot é privado e você não tem permissão para usá-lo.")
        return
    
    IA = "ChatGPT"
    
    bot.reply_to(message, "ChatGPT foi selecionado como editor de código.")


@bot.message_handler(commands=['gemini'])
def comando_gemini(message):
    global IA
    if message.from_user.id != SUA_CHAVE_USER_ID:
        bot.reply_to(message, "Desculpe, este bot é privado e você não tem permissão para usá-lo.")
        return
    
    IA = "Gemini"
    
    bot.reply_to(message, "Gemini foi selecionado como editor de código.")


# Handler principal CORRIGIDO - usa contexto do histórico
@bot.message_handler(func=lambda message: True)
def responder_mensagem(message):
    if message.from_user.id != SUA_CHAVE_USER_ID or message.text.startswith('/'):
        bot.reply_to(message, "Desculpe, este bot é privado e você não tem permissão para usá-lo.")
        return
    
    mensagem_usuario = message.text
    
    mensagem = f"{ler("Contexto/Apoio.txt")}{mensagem_usuario}\n{codigos()}"
    print(mensagem)

    print(f"💬 Usuário {message.from_user.username}: {mensagem_usuario}...")

    try:
        bot.send_chat_action(message.chat.id, 'typing')
        if IA == "ChatGPT":
            response = clientgpt.responses.create(model="gpt-5.4-mini", input=mensagem, store=True,).output_text

        elif IA == "Gemini":
            response = clientgemini.models.generate_content(model="gemini-3.5-flash", contents=mensagem).text
        
        else:
            bot.reply_to(message, """Antes, selecione uma IA para gerar seu código:
/chatgpt - Seleciona a IA ChatGPT como editor de código
/gemini - Seleciona a IA Gemini como editor de código""")
            return
        
        AIsWriter(response)
        bot.reply_to(message, "Concluído! Verifique na sua pasta WorkSPACE")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        bot.reply_to(message, "❌ Ocorreu um erro. Tente novamente.")
    escrever("ultimamensagem.txt", response)


try:
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
except KeyboardInterrupt:
    print("\n👋 Bot encerrado.")
