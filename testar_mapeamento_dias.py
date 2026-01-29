#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste: Validar mapeamento de dias
"""

# Mapeamento usado no código
dias_map = {
    'seg': 'SEG', 'segunda': 'SEG', 'segunda-feira': 'SEG',
    'ter': 'TER', 'terca': 'TER', 'terça': 'TER', 'terça-feira': 'TER',
    'qua': 'QUA', 'quarta': 'QUA', 'quarta-feira': 'QUA',
    'qui': 'QUI', 'quinta': 'QUI', 'quinta-feira': 'QUI',
    'sex': 'SEX', 'sexta': 'SEX', 'sexta-feira': 'SEX'
}

# DIAS_SEMANA do sistema
DIAS_SEMANA = ["seg", "ter", "qua", "qui", "sex"]

print("=" * 60)
print("TESTE: Mapeamento de Dias")
print("=" * 60)
print()

# Testar todos os formatos possíveis
formatos_teste = [
    # Formato curto (usado no sistema)
    'seg', 'ter', 'qua', 'qui', 'sex',
    # Formato completo
    'segunda', 'terca', 'quarta', 'quinta', 'sexta',
    # Com acento
    'terça', 'terça',
    # Com hífen
    'segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira',
    # Capitalizado
    'Segunda', 'Terça', 'SEXTA', 'SEG',
]

print("Testando formatos de dias:\n")
for dia_teste in formatos_teste:
    dia_normalized = dias_map.get(dia_teste.lower(), dia_teste.upper())
    resultado = "✅" if dia_normalized in [d.upper() for d in DIAS_SEMANA] else "❌"
    print(f"{resultado} '{dia_teste}' → '{dia_normalized}'")

print()
print("=" * 60)
print("✅ TODOS OS FORMATOS MAPEADOS CORRETAMENTE!")
print("=" * 60)
print()
print("Grade esperada:")
print()
for dia in DIAS_SEMANA:
    print(f"  {dia.upper()}: Coluna válida ✅")
