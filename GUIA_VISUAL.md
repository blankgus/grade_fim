# 🎯 GUIA VISUAL RÁPIDO - Como Verificar se Está Funcionando

## ✅ SUCESSO - Como deve aparecer

### 1. **Ao Gerar a Grade:**
```
🎯 Iniciando geração de grade horária (algoritmo corrigido)...
⚠️ Não foi possível alocar Vida Pratica B para 9anoB
✅ Grade gerada com 245 aulas SEM CONFLITOS!
✅ Grade Todas as Turmas gerada com Algoritmo Simples! (245 aulas)
```
**O QUE OBSERVAR:**
- ✅ Mensagem "SEM CONFLITOS!" (verde)
- ✅ Número de aulas geradas (exemplo: 245)
- ⚠️ Avisos amarelos são OK (disciplinas que não couberam)

---

### 2. **Visualização da Grade (por Turma):**
```
              Segunda     Terça       Quarta      Quinta      Sexta
1º 07:00      Matemática  Português   História    Geografia   Inglês
              (Tatiane)   (Heliana)   (Laís)      (Rene)      (Maria)

2º 07:50      Português   Matemática  Geografia   Português   Matemática
              (Heliana)   (Ricardo)   (Gisele)    (Deise)     (Tatiane)
```
**O QUE OBSERVAR:**
- ✅ UMA disciplina por célula
- ✅ UMA professor por célula
- ✅ Células vazias marcadas "LIVRE"
- ❌ NUNCA duas disciplinas na mesma célula

---

### 3. **Grade por Professor (Exemplo: Tatiane):**
```
Dia       | Horário          | Turma  | Disciplina
----------|------------------|--------|------------
Segunda   | 1º (07:00-07:50) | 6anoA  | Matemática
Segunda   | 3º (08:40-09:30) | 7anoA  | Matemática
Segunda   | 5º (10:40-11:30) | 8anoA  | Matemática
Terca     | 2º (07:50-08:40) | 6anoA  | Matemática
Terca     | 4º (09:50-10:40) | 9anoA  | Matemática
```
**O QUE OBSERVAR:**
- ✅ Cada linha = horário DIFERENTE
- ✅ NUNCA repetir: Segunda + 1º (duas vezes)
- ✅ Total de linhas ≤ limite do professor

---

### 4. **Diagnóstico:**
```
Status        Completude    Aulas
✅ COMPLETA   100.0%        245/245

📋 PROBLEMAS DETECTADOS
(vazio - nenhum problema)

💡 SUGESTÕES PARA COMPLETAR
(vazio - grade completa)
```
**O QUE OBSERVAR:**
- ✅ Status verde "COMPLETA" ou "QUASE COMPLETA"
- ✅ Completude ≥ 90%
- ✅ Seção de problemas vazia ou com poucos itens

---

### 5. **Análise de Conflitos (Diagnóstico):**
```
✅ Nenhum problema encontrado!
```
**O QUE OBSERVAR:**
- ✅ Mensagem verde única
- ❌ Se aparecer lista de conflitos, há problema

---

## ❌ PROBLEMAS - Como NÃO deve aparecer

### 1. **Conflito de Professor:**
```
❌ ATENÇÃO: 3 conflitos de professores detectados!
  - Professor Tatiane em 6anoA, 7anoA no segunda às 1h
  - Professor Ricardo em 8anoA, 9anoA no terca às 2h
```
**AÇÃO:** Clique em "Corrigir Conflitos Automaticamente"

---

### 2. **Grade com Sobreposição:**
```
              Segunda
1º 07:00      Matemática (Tatiane) + Português (Heliana)
              ❌ DUAS DISCIPLINAS NA MESMA CÉLULA!
```
**AÇÃO:** Regenere a grade

---

### 3. **Professor Duplicado:**
```
Dia       | Horário          | Turma  | Disciplina
----------|------------------|--------|------------
Segunda   | 1º (07:00-07:50) | 6anoA  | Matemática  ✅
Segunda   | 1º (07:00-07:50) | 7anoA  | Matemática  ❌ CONFLITO!
```
**AÇÃO:** Use "Corrigir Conflitos" no Diagnóstico

---

### 4. **Limite Excedido:**
```
❌ Problemas encontrados:
- Limites excedidos: 2 professores
  - Tatiane: 40h > 35h (EM)
  - Ricardo: 30h > 25h (EF_II)
```
**AÇÃO:** Redistribua aulas ou adicione professores

---

## 🔍 VERIFICAÇÃO MANUAL RÁPIDA

### **TESTE 1: Escolha um professor aleatório**
1. Vá para "Grade por Professor"
2. Selecione qualquer professor
3. Verifique se a coluna **"Dia + Horário"** NÃO tem duplicatas

**EXEMPLO OK:**
```
Segunda 1º
Segunda 2º  ✅ Todos diferentes
Terca 1º
```

**EXEMPLO PROBLEMA:**
```
Segunda 1º
Segunda 1º  ❌ DUPLICADO!
```

---

### **TESTE 2: Escolha uma turma aleatória**
1. Visualize a grade da turma
2. Passe o mouse sobre cada célula
3. Verifique se tem APENAS UMA disciplina

**EXEMPLO OK:**
```
[Matemática - Tatiane]  ✅
```

**EXEMPLO PROBLEMA:**
```
[Matemática - Tatiane + Português - Heliana]  ❌
```

---

## 🎯 CHECKLIST DE 1 MINUTO

Execute este teste rápido após gerar a grade:

### ✅ **VISUAL (30 segundos):**
- [ ] Mensagem "SEM CONFLITOS!" apareceu?
- [ ] Tabela da grade mostra células únicas (não empilhadas)?
- [ ] Diagnóstico mostra ✅ verde?

### ✅ **MANUAL (30 segundos):**
- [ ] Selecione 1 professor → Sem duplicatas de horário?
- [ ] Selecione 1 turma → Sem células sobrepostas?

**SE TODOS ✅ → FUNCIONANDO!**  
**SE ALGUM ❌ → Veja "AÇÃO" na seção de problemas**

---

## 📊 INTERPRETAÇÃO DE MENSAGENS

### **Mensagens BOAS (pode ignorar):**
```
⚠️ Não foi possível alocar Dinâmica A para 9anoA
```
- Significa: Essa disciplina não coube no horário disponível
- OK se completude ≥ 90%

### **Mensagens RUINS (precisa corrigir):**
```
❌ ATENÇÃO: 5 conflitos de professores detectados!
```
- Significa: Há professores em 2+ salas ao mesmo tempo
- AÇÃO: Corrigir conflitos

```
❌ LIMITE EXCEDIDO: Professor X tem 40h (limite: 35h)
```
- Significa: Professor tem aulas demais
- AÇÃO: Redistribuir ou adicionar professores

---

## 🚦 SEMÁFORO DE STATUS

### 🟢 **VERDE - Tudo OK**
```
✅ Grade gerada SEM CONFLITOS!
✅ Nenhum problema encontrado!
Status: ✅ COMPLETA
Completude: 100%
```
**AÇÃO:** Pode usar a grade!

---

### 🟡 **AMARELO - Quase OK**
```
✅ Grade gerada SEM CONFLITOS!
Status: ⚠️ QUASE COMPLETA
Completude: 92%
Faltam: 15 aulas
```
**AÇÃO:** Use "Tentar Completar Grade" (opcional)

---

### 🔴 **VERMELHO - Precisa Corrigir**
```
❌ ATENÇÃO: 8 conflitos detectados!
Status: ❌ INCOMPLETA
Completude: 65%
```
**AÇÃO:** Clique "Corrigir Conflitos" e regenere

---

## 🎓 EXEMPLO REAL DE SUCESSO

```
🎯 Iniciando geração de grade horária (algoritmo corrigido)...
✅ Grade gerada com 238 aulas SEM CONFLITOS!
✅ Grade Todas as Turmas gerada com Algoritmo Simples! (238 aulas)

🔍 DIAGNÓSTICO DA GRADE
Status: ✅ COMPLETA
Completude: 98.3%
Aulas: 238/242

📋 PROBLEMAS DETECTADOS
(vazio)

💡 SUGESTÕES PARA COMPLETAR
- Faltam 4 aulas no total. Verifique disponibilidade de professores.

📊 DETALHES POR TURMA
✅ 6anoA (EF_II): 25/25 aulas (100.0%)
✅ 6anoB (EF_II): 24/25 aulas (96.0%)
  Faltam: Vida Pratica B (1/2)
...

VERIFICAÇÃO FINAL:
✅ Nenhum problema encontrado!
```

**INTERPRETAÇÃO:**
- ✅ SEM conflitos de professor
- ✅ 98% completa (excelente!)
- ⚠️ Faltam 4 aulas (aceitável)
- ✅ Pode usar a grade

---

## 📞 QUANDO PEDIR AJUDA

Se após seguir este guia você ainda ver:

1. ❌ "ATENÇÃO: X conflitos detectados!" persistente
2. ❌ Professores duplicados na grade individual
3. ❌ Células com múltiplas disciplinas

**FAÇA:**
1. Execute `python verificar_conflitos.py`
2. Copie o resultado completo
3. Verifique se seguiu TODOS os passos do guia
4. Reporte o problema com:
   - Screenshot do erro
   - Resultado do verificar_conflitos.py
   - Completude da grade (%)

---

**Última Atualização:** 2026-01-15  
**Tempo de Leitura:** 5 minutos  
**Nível:** Iniciante
