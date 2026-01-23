# 🚀 GUIA RÁPIDO - Novas Funcionalidades v3

## ⚡ Início Rápido

### 1️⃣ Iniciar o Sistema
```bash
streamlit run app.py
```

---

## 🎯 3 NOVAS FUNCIONALIDADES PRINCIPAIS

### ✅ 1. HORÁRIOS COMPACTADOS (SEM BURACOS)

**O que mudou:**
- Antes: Professores tinham aulas espalhadas (ex: 1º, livre, 3º, livre, 5º)
- Agora: Aulas consecutivas sempre que possível (1º, 2º, 3º...)

**Como verificar:**
1. Gere uma grade
2. Vá para aba "👨‍🏫 Grade por Professor"
3. Selecione um professor
4. **Observe**: Aulas devem estar juntas, sem buracos

**Exemplo:**
```
✅ CORRETO (compactado):
Segunda: 1º, 2º, 3º
Terça:   1º, 2º

❌ ANTES (com buracos):
Segunda: 1º, -, 3º, -, 5º
Terça:   -, 2º, -, 4º
```

---

### ✅ 2. LIMITES DE HORAS RIGOROSOS

**Limites por segmento:**
- **EF II**: 25 horas semanais
- **EM**: 35 horas semanais
- **AMBOS**: 35 horas semanais

**Como funciona:**
- O algoritmo **NÃO permite** alocar aulas se exceder o limite
- Mensagem clara ao final da geração

**Verificar limites:**
1. Após gerar grade, veja a mensagem:
   - ✅ "Grade gerada com X aulas SEM CONFLITOS e dentro dos LIMITES!"
   - ❌ "ATENÇÃO: X professores excederam limite de horas!"

2. Ou vá para aba "🔧 Diagnóstico" → Botão "📅 Analisar Conflitos e Limites"

**Se houver excesso:**
```
❌ Professor João (EM): 37h alocadas (limite: 35h) - EXCESSO: 2h

Soluções:
1. Adicionar outro professor para a disciplina
2. Aumentar disponibilidade de outros professores
3. Redistribuir aulas
```

---

### ✅ 3. SISTEMA DE MÚLTIPLAS VERSÕES

**Para que serve:**
- Salvar diferentes tentativas de grade
- Comparar versões lado a lado
- Facilitar negociação com professores
- Manter histórico de alterações

**Como usar:**

#### 📌 SALVAR UMA VERSÃO
1. Gere uma grade
2. Vá para aba "📦 Versões de Grades"
3. Digite um nome (ex: "Grade_Inicial")
4. Clique em "💾 SALVAR VERSÃO"

#### 📌 CARREGAR UMA VERSÃO
1. Na aba "📦 Versões de Grades"
2. Encontre a versão desejada
3. Clique em "📂 Carregar"
4. Vá para "🗓️ Gerar Grade" para visualizar

#### 📌 COMPARAR VERSÕES
1. Na aba "📦 Versões de Grades"
2. Role até "🔄 Comparar Versões"
3. Selecione duas versões
4. Clique em "📊 Comparar"
5. Veja qual é melhor

#### 📌 BAIXAR EM EXCEL
1. Na versão desejada
2. Clique em "📥 Excel"
3. Arquivo salvo automaticamente

---

## 🎬 CENÁRIO PRÁTICO: Negociação com Professor

**Situação:** Prof. Maria não pode na quinta-feira

### Passo 1: Grade Original
1. Gere grade normal
2. Salve como "Grade_Original"

### Passo 2: Ajustar Disponibilidade
1. Vá para aba "👩‍🏫 Professores"
2. Edite Prof. Maria
3. Remova quinta-feira da disponibilidade
4. Salve

### Passo 3: Nova Grade
1. Gere nova grade
2. Salve como "Grade_Sem_Maria_Quinta"

### Passo 4: Comparar
1. Vá para "📦 Versões de Grades"
2. Compare "Grade_Original" vs "Grade_Sem_Maria_Quinta"
3. Veja impacto da mudança

### Passo 5: Decidir
- Se nova grade está boa → Use ela
- Se nova grade ficou ruim → Volte para original e negocie com Maria

---

## 📊 ENTENDENDO OS STATUS DAS VERSÕES

**✅ Verde (Perfeita):**
- Completude: 100%
- Conflitos: 0
- Limites: Todos OK
- **Pronta para usar!**

**⚠️ Laranja (Quase):**
- Completude: ≥ 90%
- Pode ter pequenos problemas
- **Revisar antes de usar**

**❌ Vermelho (Incompleta):**
- Completude: < 90%
- Muitos problemas
- **Precisa melhorias**

---

## 🛠️ SOLUÇÃO DE PROBLEMAS

### Problema: Grade incompleta
**Sintomas:** Completude < 100%

**Soluções:**
1. Adicionar mais professores
2. Aumentar disponibilidade dos professores existentes
3. Verificar se todas disciplinas têm professores
4. Usar botão "🔧 TENTAR COMPLETAR GRADE"

### Problema: Professor excede limite
**Sintomas:** "❌ ATENÇÃO: X professores excederam limite"

**Soluções:**
1. Adicionar outro professor para a disciplina
2. Redistribuir aulas entre professores
3. Verificar segmento do professor (EF II = 25h, EM = 35h)

### Problema: Aulas com buracos
**Sintomas:** Professor tem horários livres entre aulas

**Nota:** A compactação é tentativa de melhor esforço
- Nem sempre 100% possível devido a restrições
- Prioriza conflitos e limites sobre compactação

**Se muito crítico:**
- Ajuste manualmente na grade gerada
- Ou aumente disponibilidade do professor

---

## ⚠️ AVISOS IMPORTANTES

### 🔴 Versões em Memória
- Versões salvas ficam apenas na sessão atual
- **Ao fechar o navegador, versões são perdidas**
- **SOLUÇÃO**: Sempre baixe em Excel as versões importantes

### 🔴 Limites são Rigorosos
- Se não houver professores suficientes, grade ficará incompleta
- Algoritmo **NÃO vai** exceder limites contratuais

### 🔴 Compactação é Heurística
- Nem sempre consegue compactar 100%
- Prioridade: sem conflitos > limites OK > compactação

---

## 📞 FLUXO COMPLETO RECOMENDADO

```
1. Configure professores com disponibilidades corretas
   ↓
2. Configure disciplinas com cargas semanais
   ↓
3. Configure turmas
   ↓
4. Vá para "🔧 Diagnóstico" → Verifique capacidade
   ↓
5. Gere grade em "🗓️ Gerar Grade"
   ↓
6. Salve como "Grade_v1" em "📦 Versões"
   ↓
7. Se houver problemas:
   - Ajuste professores/disponibilidades
   - Gere nova grade
   - Salve como "Grade_v2"
   - Compare versões
   ↓
8. Escolha melhor versão e baixe em Excel
```

---

## 🎓 DICAS PRO

### Dica 1: Nomear Versões Descritivamente
❌ Ruim: "Grade_1", "Grade_2"
✅ Bom: "Grade_Inicial", "Grade_Sem_ProfMaria_Quinta", "Grade_Final_Aprovada"

### Dica 2: Salvar Antes de Grandes Mudanças
Sempre salve versão atual antes de:
- Mudar disponibilidade de professores
- Adicionar/remover disciplinas
- Fazer ajustes manuais

### Dica 3: Usar Comparação para Convencer
- Mostre versões lado a lado
- Demonstre impacto de mudanças
- Facilita aprovação da direção

### Dica 4: Backup em Excel
- Baixe versão final em Excel
- Guarde em local seguro
- Não dependa apenas da memória do sistema

---

## 📋 CHECKLIST FINAL

Antes de aprovar uma grade:

- [ ] ✅ Completude = 100%
- [ ] ✅ Conflitos = 0
- [ ] ✅ Limites OK para todos professores
- [ ] ✅ Horários compactados (maioria dos casos)
- [ ] ✅ Versão salva com nome descritivo
- [ ] ✅ Download em Excel feito
- [ ] ✅ Grade revisada por coordenador
- [ ] ✅ Professores consultados sobre horários

---

**Para mais detalhes técnicos, veja:**
- `MELHORIAS_v3.md` - Explicação técnica completa
- `GUIA_DE_TESTE.md` - Testes detalhados
