from typing import NamedTuple
import re
from tkinter import *
from tkinter import ttk

raiz = Tk()
raiz.title("Gabriel Hashtable")

Num_tokens_validos = 0
Num_tokens_invalidos = 0

def Nvalidos():
    global Num_tokens_validos
    Num_tokens_validos = Num_tokens_validos + 1


def NinValidos():
    global Num_tokens_invalidos
    Num_tokens_invalidos = Num_tokens_invalidos + 1

hashtable = { 'ID':         { 'IDENT_TOKEN': 27, 'LEXEMA': 'LETRA_MAS_NUMERO', 'CANTIDAD': 0},
              'CONSTANTE':  {'IDENT_TOKEN': 28, 'LEXEMA': 'N_L_CONS', 'CANTIDAD': 0},
              'IF':         {'IDENT_TOKEN': 59, 'LEXEMA': 'IF', 'CANTIDAD': 0},
              'THEN':       {'IDENT_TOKEN': 60, 'LEXEMA': 'THEN', 'CANTIDAD': 0},
              'ELSE':       {'IDENT_TOKEN': 61, 'LEXEMA': 'ELSE', 'CANTIDAD': 0},
              'SUMA':       {'IDENT_TOKEN': 70, 'LEXEMA': '+', 'CANTIDAD': 0},
              'DIV':        {'IDENT_TOKEN': 73, 'LEXEMA': '/', 'CANTIDAD': 0},
              'MAYORQ':     {'IDENT_TOKEN': 80, 'LEXEMA': '>=', 'CANTIDAD': 0},
              'ASIGNACION': {'IDENT_TOKEN': 85, 'LEXEMA': ':=', 'CANTIDAD': 0},
              }

class Token(NamedTuple):
    type: str
    value: str

def tokenize(code):
    keywords = {'IF', 'THEN', 'ELSE'}
    token_specification = [
        ('CONSTANTE',   r'CONS [A-Za-z0-9]+'),
        ('ID',          r'[A-Za-z]+[A-Za-z0-9]*'),
        ('SUMA',          r'[+]'),
        ('DIV',          r'/'),
        ('MAYORQ',      r'>='),
        ('ASIGNACION',  r':='),
        ('SKIP',        r'[ \t]+'),
        ('INVALIDO',    r'.'),
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        
        if kind == 'NUMBER':
            value = float(value) if '.' in value else int(value)
        elif kind == 'ID' and value in keywords:
            kind = value
        elif kind == 'SKIP':
            continue
        if kind == 'INVALIDO':
            NinValidos()
        else:
            Nvalidos()
            hashtable[kind]['CANTIDAD'] = hashtable[kind]['CANTIDAD'] + 1
        yield Token(kind, value)

f = open("archivo.txt")
info = f.read()

statements = info

token = []
token.extend(tokenize(statements))

#hash table
hashT = Label(raiz, text="HASHTABLE", padx=20, pady=5, font="Verdana 11")
hashT.pack()

tabla = ttk.Treeview(raiz, columns=(0,1,2,3), show='headings', height=8)
tabla.pack()

for i in range(0,4):
    tabla.column(i, anchor=CENTER, width=130)

columnas = ['TOKEN','IDENT_TOKEN', 'LEXEMA','CANTIDAD']

index = 0
for i in columnas:
    tabla.heading(index, text=i)
    index = index + 1

index = 0
for i in hashtable:
    tabla.insert(parent='', index=index, iid=index, text='', values=(
        i,
        hashtable[i]['IDENT_TOKEN'],
        hashtable[i]['LEXEMA'],
        hashtable[i]['CANTIDAD']))
    index = index + 1

#tabla de tokens validos

Tvalidos = Label(raiz, text="TOKENS VALIDOS", padx=20, pady=5, font="Verdana 11")
Tvalidos.pack()

tablatokens = ttk.Treeview(raiz, columns=(0,1,2), show='headings', height=8)
tablatokens.pack()

for i in range(0,3):
    tablatokens.column(i, anchor=CENTER,width=100)


columnastokens = ['NUM','TOKEN','LEXEMA']

index = 0
for i in columnastokens:
    tablatokens.heading(index, text=i)
    index = index + 1



index = 0
for i in token:
    if i.type != 'INVALIDO':
        tablatokens.insert(parent='', index=index, iid=index, text='', values=(
            index,
            i.type,
            i.value,
            ))
        index = index + 1


#tabla de tokens invalidos

Tivalidos = Label(raiz, text="TOKENS INVALIDOS", padx=20, pady=5, font="Verdana 11")
Tivalidos.pack()

tablatokensINV = ttk.Treeview(raiz, columns=(0,1), show='headings', height=8)
tablatokensINV.pack()

for i in range(0,2):
    tablatokensINV.column(i, anchor=CENTER, width=100)


columnastokensINV = ['NUM','INVALIDOS']

index = 0
for i in columnastokensINV:
    tablatokensINV.heading(index, text=i)
    index = index + 1



index = 0
for i in token:
    if i.type == 'INVALIDO':
        tablatokensINV.insert(parent='', index=index, iid=index, text='', values=(
            index,
            i.value,
            ))
        index = index + 1


#NUMERO DE VALIDOS E INVALIDOS
validos = Label(raiz, text="número de tokens validos: "+"\t"+str(Num_tokens_validos), padx=20, pady=5, font="Verdana 11")
validos.pack(anchor=NW)

invalidos = Label(raiz, text="número de tokens invalidos: "+"\t"+str(Num_tokens_invalidos),padx=20, pady=2, font="Verdana 11")
invalidos.pack(anchor=NW)
raiz.mainloop()