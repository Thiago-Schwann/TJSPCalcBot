import os
import customtkinter as ctk
from threading import Thread
from tkinter.filedialog import askopenfilename
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GROQ_API_KEY')
chat = ChatGroq(model='meta-llama/llama-4-maverick-17b-128e-instruct')
messages = []
documento = ''

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def carrega_pdf():
    path = askopenfilename(title="Selecione o PDF", filetypes=[("PDF Files", "*.pdf")])
    if not path:
        return ""
    loader = PyPDFLoader(path)
    list_documents = loader.load()
    return ''.join(doc.page_content for doc in list_documents)

def answerBot(messages, documento):
    system_message = f"Você é um assistente amigável criado para ajudar a responder chamados com base nas seguintes informações: {documento}"
    prompt = ChatPromptTemplate.from_messages([("system", system_message)] + messages)
    chain = prompt | chat
    return chain.invoke({}).content

def enviar_mensagem():
    pergunta = entrada.get()
    if not pergunta.strip():
        return
    chatbox.insert("end", f"\nVocê: {pergunta}\n")
    entrada.delete(0, 'end')
    messages.append(("user", pergunta))
    resposta = answerBot(messages, documento)
    messages.append(("assistant", resposta))
    chatbox.insert("end", f"\nIA: {resposta}\n")
    chatbox.see("end")

def escolher_fonte(tipo):
    def tarefa_carregar():
        global documento
        status.configure(text="Carregando e resumindo PDF...")
        if tipo == "pdf":
            documento = carrega_pdf()
        if documento:
            status.configure(text="Fonte carregada com sucesso!")
        else:
            status.configure(text="Nenhuma informação carregada.")

    Thread(target=tarefa_carregar, daemon=True).start()

app = ctk.CTk()
app.title("Assistente de Suporte IA")
app.geometry("700x600")

titulo = ctk.CTkLabel(app, text="Assistente de Suporte IA", font=ctk.CTkFont(size=24, weight="bold"))
titulo.pack(pady=10)

status = ctk.CTkLabel(app, text="🔍 Nenhuma fonte carregada ainda.", text_color="gray")
status.pack()

frame_botoes = ctk.CTkFrame(app)
frame_botoes.pack(pady=10)

ctk.CTkButton(frame_botoes, text="Carregar PDF", command=lambda: escolher_fonte("pdf")).pack(side="left", padx=0)

chatbox = ctk.CTkTextbox(app, width=650, height=350, wrap="word")
chatbox.pack(pady=10)

entrada = ctk.CTkEntry(app, placeholder_text="Digite sua pergunta e pressione Enter...", width=500)
entrada.pack(side="left", padx=10, pady=10)
entrada.bind("<Return>", lambda e: enviar_mensagem())

btn_enviar = ctk.CTkButton(app, text="Enviar", command=enviar_mensagem)
btn_enviar.pack(side="left", padx=10)

app.mainloop()
