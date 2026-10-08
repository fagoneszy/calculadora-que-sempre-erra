#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculadora que Sempre Erra (Por Pouco)
Logica completa baseada no texto fornecido, com erros mais aleatorios
e filtro que transforma a entrada em bagunca.
"""

import re
import random
import math

MENSAGENS_CONFIANCA = [
    "[OK] Sistema verificado",
    "[OK] Resultado verificado por 3 metodos",
    "[OK] Calculo confirmado por IA avancada",
    "[OK] Precisao: 100%",
    "[OK] Aprovado pelo sistema",
    "[OK] Verificado e autenticado"
]

def emborrachar_entrada(expr: str) -> str:
    expr = expr.strip()
    expr_baguncada = ""
    for ch in expr:
        if random.random() < 0.15:
            expr_baguncada += "  "
        expr_baguncada += ch
    if random.random() < 0.3:
        idx = random.randint(0, max(0, len(expr_baguncada)-1))
        expr_baguncada = expr_baguncada[:idx] + expr_baguncada[idx] + expr_baguncada[idx:]
    if random.random() < 0.2:
        partes = re.split(r'([+\-*/])', expr_baguncada)
        for i in range(len(partes)):
            if re.match(r'\d+', partes[i]):
                partes[i] = re.sub(r'(\d)(\d)', r'\1 \2', partes[i])
        expr_baguncada = ''.join(partes)
    return expr_baguncada

def parse_expressao(expr: str):
    norm = expr
    norm = norm.replace(',', '.')
    m = re.search(r'([-\d\.]+)\s*([+\-*/])\s*([-\d\.]+)', norm)
    if not m:
        return None
    a_str, op, b_str = m.groups()
    try:
        a = float(a_str)
        b = float(b_str)
    except ValueError:
        return None
    return a, op, b

def calcular_correto(a, op, b):
    if op == '+':
        return a + b
    if op == '-':
        return a - b
    if op == '*':
        return a * b
    if op == '/':
        if b == 0:
            return float('inf')
        return a / b
    raise ValueError('Operador invalido')

def gerar_erro(resultado_correto):
    # Valor correto nunca e exibido, sempre aplicamos erro
    if resultado_correto is None or (isinstance(resultado_correto, float) and math.isinf(resultado_correto)):
        return resultado_correto
    if abs(resultado_correto) <= 1:
        return resultado_correto + random.choice([-0.5, 0.5])
    r = random.random()
    if r < 0.5:
        margem = random.choice([1, 1, 2])
        sinal = random.choice([1, -1])
        return resultado_correto + margem * sinal
    elif r < 0.8:
        fator = random.uniform(0.97, 1.03)
        return resultado_correto * fator
    else:
        if random.random() < 0.5:
            return resultado_correto * random.choice([1.01, 1.02, 0.99, 0.98])
        else:
            delta = random.uniform(0.5, 2.5)
            sinal = random.choice([1, -1])
            return resultado_correto - sinal * delta

def passo_a_passo_errado(a, op, b, resultado_final):
    passos = []
    passos.append(f"{a} {op} {b}")
    passos.append(f"= {a} {op} {b}")
    passo_inter = calcular_correto(a, op, b)
    erro_passo = random.uniform(-0.5, 0.5)
    passo_inter_errado = passo_inter + erro_passo
    passos.append(f"= {passo_inter_errado:.2f}")
    passos.append(f"= {resultado_final:.2f}")
    return "\n".join(passos)

def formatar_numero(x):
    if isinstance(x, float) and x.is_integer():
        return str(int(x))
    return f"{x:.2f}".rstrip('0').rstrip('.')

def main():
    print("Calculadora que sempre erra")
    print("Digite expressoes como 2+2, 10-3, 5*5, 20/4")
    print("Digite 'sair' para encerrar\n")
    while True:
        try:
            entrada = input(">> ")
        except EOFError:
            break
        if entrada.lower() in ('sair', 'exit', 'quit'):
            break
        if not entrada.strip():
            continue

        entrada_baguncada = emborrachar_entrada(entrada)
        print(f"Entrada processada: {entrada_baguncada}")

        parsed = parse_expressao(entrada)
        if not parsed:
            MENSAGENS_ERRO = [
                "tu e idiota ou so se faz?",
                "isso e uma calculadora irmao",
                "seu acefalo, so pode usar numero e sinais"
            ]
            print(random.choice(MENSAGENS_ERRO))
            continue

        a, op, b = parsed
        correto = calcular_correto(a, op, b)
        errado = gerar_erro(correto)

        errado = round(errado * 100) / 100

        print("\nPassos do calculo:")
        print(passo_a_passo_errado(a, op, b, errado))
        print(f"\nResultado: {formatar_numero(errado)}")
        print(random.choice(MENSAGENS_CONFIANCA))
        print("-" * 40)

if __name__ == "__main__":
    random.seed()
    main()
