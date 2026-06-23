import os
import re


def escrever(arquivo, texto):
    with open(arquivo, 'w', encoding='utf-8') as arq:
        arq.write(texto)


def ler(arquivo):
    with open(arquivo, 'r', encoding='utf-8') as arq:
        return arq.read()


def caminhos():
    todos_arquivos = []
    
    # os.walk percorre a pasta e todas as subpastas
    for raiz, subpastas, arquivos in os.walk("WorkSPACE"):
        for arquivo in arquivos:
            # Cria o caminho completo do arquivo
            caminho_completo = os.path.join(raiz, arquivo)
            todos_arquivos.append(caminho_completo)
    
    return todos_arquivos


def codigos():
    contexto = "---------------------Estado atual da pasta WorkSPACE---------------------\n"
    for arq in caminhos():
        contexto += f"""{arq}
{ler(arq)}\n"""
    return contexto[:-1]


def AIsWriter(texto):
    texto = re.split(r'WorkSPACE/|_-_-_-_-_-_-_', texto)[1:]
    newtexto = []
    
    for i in texto:
        if i[-1:] == "\n":
            i = i[:-1]
        
        if i[0] == "\n":
            i = i[1:]
        
        newtexto.append(i)

    for i in range(0, int(len(newtexto)/2)):
        escrever(f"WorkSPACE/{newtexto[i*2]}", newtexto[i*2+1])
