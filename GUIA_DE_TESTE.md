# 🧪 GUIA DE TESTE - Sistema de Grade Horária

## 🎯 OBJETIVO
Verificar se as correções eliminaram completamente o problema de **professores em múltiplas salas ao mesmo tempo**.

---

## 📋 CHECKLIST DE TESTE

### ✅ **TESTE 1: Geração Básica**

1. Execute: `streamlit run app.py`
2. Vá para **"Gerar Grade"**
3. Configure:
   - Tipo: **Grade Completa - Todas as Turmas**
   - Algoritmo: **Simples (Rápido)**
4. Clique em **"Gerar Grade"**
5. **RESULTADO ESPERADO:**
   - ✅ Mensagem: "Grade gerada com X aulas SEM CONFLITOS!"
   - ✅ Nenhuma mensagem de erro vermelha sobre conflitos

---

### ✅ **TESTE 2: Verificação Visual - Grade por Turma**

1. Após gerar a grade, role para baixo até **"Visualização da Grade Horária"**
2. Para cada turma, verifique a tabela:

**VERIFICAR:**
```
Segunda | Terça | Quarta | Quinta | Sexta
--------|-------|--------|--------|-------
Matemática (Prof. A) | Português (Prof. B) | ...
```

**❌ NUNCA DEVE ACONTECER:**
- Duas disciplinas na mesma célula
- Horário vazio quando deveria ter aula

**✅ DEVE ACONTECER:**
- Uma disciplina por célula
- Células vazias marcadas como "LIVRE"
- Intervalo claramente marcado

---

### ✅ **TESTE 3: Verificação por Professor**

1. Vá para a aba **"Grade por Professor"**
2. Selecione um professor (ex: "Tatiane")
3. Verifique a tabela:

**VERIFICAR:**
```
Dia       | Horário     | Turma  | Disciplina
----------|-------------|--------|------------
Segunda   | 1º (07:50)  | 6anoA  | Matemática
Segunda   | 2º (08:40)  | 7anoA  | Matemática
Segunda   | 3º (08:40)  | 8anoA  | Matemática  ❌ ERRO!
```

**❌ NUNCA DEVE ACONTECER:**
- Mesmo **Dia + Horário** aparecer duas vezes
- Exemplo: Segunda 2º em 6anoA E 7anoA ao mesmo tempo

**✅ DEVE ACONTECER:**
- Cada combinação Dia + Horário é ÚNICA
- Professor pode ter várias aulas por dia, mas em horários DIFERENTES

---

### ✅ **TESTE 4: Diagnóstico Automático**

1. Vá para a aba **"Diagnóstico"**
2. Clique em **"Analisar Conflitos e Limites"**

**RESULTADO ESPERADO:**
```
✅ Nenhum problema encontrado!
```

**SE APARECER ERRO:**
```
❌ Problemas encontrados:
- Conflitos: 3 horários sobrepostos
- Limites excedidos: 2 professores
```

**AÇÃO:**
1. Clique em **"Corrigir Todos os Problemas"**
2. Verifique novamente

---

### ✅ **TESTE 5: Verificação Manual Detalhada**

1. Após gerar a grade, vá para **"Lista Detalhada das Aulas"**
2. Baixe o Excel/CSV
3. Abra no Excel
4. Aplique filtro na coluna **Professor**
5. Selecione um professor
6. Ordene por **Dia** e **Horário**

**VERIFICAR:**
```
Professor | Dia     | Horário | Turma
----------|---------|---------|-------
Tatiane   | Segunda | 1º      | 6anoA   ✅
Tatiane   | Segunda | 1º      | 7anoA   ❌ CONFLITO!
Tatiane   | Segunda | 2º      | 8anoA   ✅
```

**❌ SE ENCONTRAR CONFLITO:**
- Copie as linhas problemáticas
- Anote: Professor, Dia, Horário, Turmas
- Reporte o bug

---

## 🔍 CASOS DE TESTE ESPECÍFICOS

### **CASO 1: Professor com Múltiplas Disciplinas**

**Cenário:**
- Professor "Marina" ministra: Biologia A, Biologia B, Ciências A, Ciências B
- Pode dar aula para Grupo A E Grupo B

**TESTE:**
1. Gere a grade
2. Vá para **"Grade por Professor"** → Selecione "Marina"
3. Verifique se não há conflitos entre turmas de grupos diferentes

**RESULTADO ESPERADO:**
```
Segunda | 1º | 6anoA | Ciências A  ✅
Segunda | 2º | 6anoB | Ciências B  ✅
Segunda | 3º | 1emA  | Biologia A  ✅
```

**❌ NUNCA:**
```
Segunda | 1º | 6anoA | Ciências A
Segunda | 1º | 6anoB | Ciências B  ❌ CONFLITO!
```

---

### **CASO 2: Professor de Matemática (Várias Instâncias)**

**Cenário:**
- Tatiane, Ricardo, Tatiane II, Santiago, Andréia Lucia (todos Matemática)
- Devem ser distribuídos entre as turmas

**TESTE:**
1. Gere a grade
2. Para cada professor de Matemática, verifique a grade individual
3. Verifique se estão balanceados (cargas similares)

**VERIFICAR:**
```
Tatiane: 20 aulas
Ricardo: 18 aulas
Santiago: 22 aulas
```

**❌ PROBLEMAS:**
```
Tatiane: 40 aulas  ❌ Excede limite de 35h
Ricardo: 5 aulas   ⚠️ Desbalanceado
```

---

### **CASO 3: Ensino Médio vs Ensino Fundamental II**

**Cenário:**
- EM: 7 períodos (07:00-13:10)
- EF II: 5 períodos (07:50-12:20)

**TESTE:**
1. Gere a grade para **Grade Completa**
2. Verifique turmas de EM:
   - Devem ter aulas nos períodos 1-7
3. Verifique turmas de EF II:
   - Devem ter aulas nos períodos 1-5 (mas horários diferentes!)

**VERIFICAR:**
```
1emA (EM):
- Período 1: 07:00-07:50  ✅
- Período 7: 12:20-13:10  ✅

6anoA (EF II):
- Período 1: 07:50-08:40  ✅
- Período 5: 11:30-12:20  ✅
- Período 6: N/A          ✅
- Período 7: N/A          ✅
```

---

## 📊 MÉTRICAS DE SUCESSO

Após os testes, a grade deve ter:

| Métrica | Meta | Como Verificar |
|---------|------|----------------|
| **Conflitos de Professor** | 0 | Diagnóstico → Analisar Conflitos |
| **Conflitos de Turma** | 0 | Visualização da Grade (células únicas) |
| **Completude** | ≥ 90% | Diagnóstico → Completude |
| **Limites Respeitados** | 100% | Nenhum prof > 25h (EF II) ou 35h (EM) |
| **Aulas Não Alocadas** | < 10 | Avisos amarelos durante geração |

---

## 🐛 COMO REPORTAR BUGS

Se encontrar um problema:

### 1. **Capture as Informações:**
```
PROBLEMA: Professor X em duas salas ao mesmo tempo

DETALHES:
- Professor: Tatiane
- Dia: Segunda
- Horário: 2º período
- Turmas: 6anoA e 7anoA
- Disciplinas: Matemática em ambas
```

### 2. **Capture o Screenshot:**
- Tire print da tabela "Grade por Professor"
- Marque as linhas conflitantes

### 3. **Verifique os Logs:**
- Veja o terminal onde rodou `streamlit run app.py`
- Copie qualquer mensagem de erro

### 4. **Teste a Correção Automática:**
- Vá para Diagnóstico → Clique "Corrigir Todos os Problemas"
- Anote se funcionou ou não

---

## 🎯 TESTES RÁPIDOS (5 minutos)

### **TESTE EXPRESSO:**

1. ✅ `streamlit run app.py`
2. ✅ Gerar Grade → Grade Completa → Gerar
3. ✅ Verificar mensagem: "SEM CONFLITOS!"
4. ✅ Diagnóstico → Analisar Conflitos → "Nenhum problema!"
5. ✅ Grade por Professor → Selecionar 3 professores aleatórios → Verificar duplicatas

**TEMPO:** ~5 minutos  
**RESULTADO:** Se tudo ✅, o sistema está funcionando!

---

## 📞 TROUBLESHOOTING

### **PROBLEMA: "Grade gerada, mas com conflitos"**

**SOLUÇÃO 1:**
```
Diagnóstico → Corrigir Todos os Problemas → Recarregar página
```

**SOLUÇÃO 2:**
```
Início → Resetar Banco de Dados → Recarregar → Gerar Grade novamente
```

**SOLUÇÃO 3:**
```
Verifique se tem professores suficientes:
- Cada disciplina precisa de pelo menos 1 professor
- Professores devem estar disponíveis nos dias corretos
- Grupos (A/B) devem estar corretos
```

---

### **PROBLEMA: "Grade incompleta (< 100%)"**

**CAUSAS COMUNS:**
1. ❌ Poucos professores para a demanda
2. ❌ Professores com pouca disponibilidade (< 3 dias)
3. ❌ Carga horária excede capacidade

**SOLUÇÃO:**
```
1. Diagnóstico → Ver "SUGESTÕES PARA COMPLETAR"
2. Adicionar mais professores nas disciplinas faltantes
3. Aumentar disponibilidade dos professores existentes
4. Usar "TENTAR COMPLETAR GRADE" (Completador Avançado)
```

---

### **PROBLEMA: "Erro ao gerar grade"**

**SOLUÇÃO:**
```
1. Veja o erro no terminal
2. Verifique se todos os campos obrigatórios estão preenchidos:
   - Turmas têm Grupo (A ou B)
   - Disciplinas têm Turmas vinculadas
   - Professores têm Disciplinas e Disponibilidade
3. Resetar Banco de Dados se necessário
```

---

## ✅ CHECKLIST FINAL

Antes de considerar o teste completo, verifique:

- [ ] Grade gerada sem mensagens de erro
- [ ] Diagnóstico mostra "Nenhum problema encontrado"
- [ ] Pelo menos 3 professores verificados manualmente (sem duplicatas)
- [ ] Completude ≥ 90%
- [ ] Visualização das turmas mostra células únicas
- [ ] Exportação para Excel funciona

**SE TODOS ✅ → SISTEMA FUNCIONANDO CORRETAMENTE!**

---

**Última Atualização:** 2026-01-15  
**Versão do Teste:** 1.0  
**Tempo Estimado:** 10-15 minutos (teste completo) | 5 minutos (teste rápido)
