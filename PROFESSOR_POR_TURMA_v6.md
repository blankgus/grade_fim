# 🎯 PROFESSOR POR TURMA - v6.0

**Data:** 2026-01-22
**Versão:** v6.0 - ATRIBUIÇÃO DE PROFESSOR POR TURMA + DISCIPLINA

---

## 📋 MUDANÇA IMPLEMENTADA

### ❌ PROBLEMA ANTERIOR (v5):

```
Disciplina: Matemática
Carga por Turma:
  - 6ºA: 5 aulas/semana
  - 7ºA: 4 aulas/semana
  - 8ºA: 5 aulas/semana

Professores disponíveis: Santiago, Cesar, João

→ Algoritmo escolhia ALEATORIAMENTE qual professor daria cada turma
→ Não havia garantia de continuidade/especialização
→ Carga do professor não era "comprometida" previamente
```

### ✅ SOLUÇÃO IMPLEMENTADA (v6):

```
Disciplina: Matemática
Carga por Turma:
  - 6ºA: 5 aulas/semana → Professor: Santiago (PRÉ-ATRIBUÍDO)
  - 7ºA: 4 aulas/semana → Professor: Cesar (PRÉ-ATRIBUÍDO)
  - 8ºA: 5 aulas/semana → Professor: Santiago (PRÉ-ATRIBUÍDO)

→ Algoritmo usa EXATAMENTE os professores definidos
→ Carga comprometida ANTES da geração da grade
→ Garantia de continuidade pedagógica
```

---

## 🔧 ARQUIVOS MODIFICADOS

### 1. `models.py` - Modelo de Dados

**Novo campo adicionado:**

```python
@dataclass
class Disciplina:
    nome: str
    carga_semanal: int  # DEPRECATED
    tipo: str
    turmas: List[str]
    grupo: str
    cor_fundo: str = "#4A90E2"
    cor_fonte: str = "#FFFFFF"
    carga_por_turma: Dict[str, int] = field(default_factory=dict)  # v5
    professor_por_turma: Dict[str, str] = field(default_factory=dict)  # v6 NOVO!
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    def obter_professor_turma(self, turma_nome: str) -> str:
        """Obtém o professor atribuído para uma turma específica"""
        if self.professor_por_turma and turma_nome in self.professor_por_turma:
            return self.professor_por_turma[turma_nome]
        return None  # Nenhum professor definido (algoritmo escolhe)
```

**Estrutura do dicionário:**
- **Chave:** Nome da turma (ex: "6ºA", "1ºEM")
- **Valor:** Nome do professor (ex: "Santiago", "Cesar")
- **Vazio:** `{}` ou `None` → Algoritmo escolhe automaticamente

---

### 2. `app.py` - Interface do Usuário

#### 2.1 Formulário de Adicionar Disciplina

**Nova seção após "Carga Horária Individual":**

```python
# NOVO v6: Atribuir professor por turma
st.write("### 👨‍🏫 Atribuir Professor por Turma")
st.caption("OPCIONAL: Escolha o professor específico para cada turma.")

# Para cada turma selecionada:
for turma in turmas_selecionadas:
    opcoes = ["(Escolher automaticamente)"] + [prof.nome ...]
    prof_selecionado = st.selectbox(
        f"Professor para {turma}",
        options=opcoes,
        help="Professor que ministrará a disciplina nesta turma"
    )
    
    if prof_selecionado != "(Escolher automaticamente)":
        professor_por_turma_temp[turma] = prof_selecionado
```

**Ao salvar:**
```python
nova_disciplina = Disciplina(
    nome=nome,
    carga_por_turma=carga_por_turma_temp,
    professor_por_turma=professor_por_turma_temp  # v6!
)
```

**Mensagem de sucesso:**
```
✅ Disciplina 'Matemática' adicionada! 
Total: 14 aulas (3 turmas) | 2 turma(s) com professor pré-atribuído
```

#### 2.2 Visualização de Disciplinas

**Mostra professor junto com carga:**
```
📊 Carga por Turma:
6ºA: 5h (Prof. Santiago) | 7ºA: 4h (Prof. Cesar) | 8ºA: 5h (Prof. Santiago)

👨‍🏫 2 turma(s) com professor pré-atribuído
```

#### 2.3 Editar Disciplina

**Nova seção no formulário de edição:**
- Mostra professor atual de cada turma
- Permite alterar ou remover atribuição
- Salva com mensagem: "✅ Disciplina atualizada! Total: 14h | 2 turma(s) com professor pré-atribuído"

---

### 3. `simple_scheduler.py` - Algoritmo de Geração

**Mudança crítica no loop de alocação:**

```python
# Tentar alocar cada disciplina
for disciplina in disciplinas_turma:
    # NOVO v6: Verificar se há professor pré-atribuído
    professor_pre_atribuido = None
    if hasattr(disciplina, 'obter_professor_turma'):
        professor_pre_atribuido = disciplina.obter_professor_turma(turma_nome)
    
    # Para cada horário possível:
    for dia, horario in todos_horarios:
        # Se há professor pré-atribuído, usar APENAS ELE
        if professor_pre_atribuido:
            for prof in self.professores:
                if prof.nome == professor_pre_atribuido:
                    # Verificar disponibilidade, limites, etc.
                    if disponivel:
                        professores_candidatos.append(prof)
                    break
        else:
            # Comportamento normal: buscar todos disponíveis
            professores_candidatos = [todos os professores disponíveis]
        
        # Selecionar professor
        if professor_pre_atribuido:
            professor_selecionado = professores_candidatos[0]  # Único
        else:
            professor_selecionado = melhor_candidato()  # Compactação
```

**Resultado:**
- ✅ Se professor está pré-atribuído → usa ele
- ✅ Se não está → usa lógica de compactação normal
- ✅ Respeita disponibilidade e limites em ambos casos

---

## 🎯 COMO USAR

### Cenário 1: Atribuir Professores ao Criar Disciplina

1. **Vá para "📚 Disciplinas"**

2. **Clique em "➕ Adicionar Nova Disciplina"**

3. **Preencha dados básicos:**
   - Nome: `Matemática`
   - Carga Padrão: `5`
   - Turmas: `[6ºA, 7ºA, 8ºA]`

4. **Defina carga individual (se necessário):**
   ```
   6ºA: 5h
   7ºA: 4h
   8ºA: 5h
   ```

5. **Nova seção "👨‍🏫 Atribuir Professor por Turma":**
   ```
   Professor para 6ºA: [Santiago ▼]
   Professor para 7ºA: [Cesar ▼]
   Professor para 8ºA: [Santiago ▼]
   ```

6. **Clique em "✅ Adicionar Disciplina"**

7. **Resultado:**
   - Santiago comprometido com 10h (6ºA + 8ºA)
   - Cesar comprometido com 4h (7ºA)
   - Ao gerar grade, esses professores serão usados

---

### Cenário 2: Deixar Algoritmo Escolher

1. **Siga passos 1-4 acima**

2. **Na seção de professores:**
   ```
   Professor para 6ºA: [(Escolher automaticamente) ▼]
   Professor para 7ºA: [(Escolher automaticamente) ▼]
   Professor para 8ºA: [(Escolher automaticamente) ▼]
   ```

3. **Salve**

4. **Resultado:**
   - Algoritmo escolherá melhor professor
   - Aplicará regras de compactação
   - Balanceamento automático

---

### Cenário 3: Atribuir Apenas Algumas Turmas

1. **Criar disciplina normalmente**

2. **Na seção de professores:**
   ```
   Professor para 6ºA: [Santiago ▼]              ← Definido
   Professor para 7ºA: [(Escolher automaticamente)] ← Automático
   Professor para 8ºA: [Santiago ▼]              ← Definido
   ```

3. **Resultado:**
   - 6ºA e 8ºA → Santiago (garantido)
   - 7ºA → Algoritmo escolhe (Cesar, João, etc.)

---

## 📊 EXEMPLOS PRÁTICOS

### Exemplo 1: Continuidade Pedagógica

**Problema:** Professor Santiago já trabalha com 6ºA e desejamos que continue com essa turma em Matemática.

**Solução:**
```
Disciplina: Matemática
Turmas e Professores:
  6ºA: 5h → Santiago (continuidade)
  7ºA: 4h → (automático - pode ser novo professor)
  8ºA: 5h → (automático)
```

---

### Exemplo 2: Especialização

**Problema:** Professor Vlad é especialista em Química e deve dar aula apenas para 3ºEM.

**Solução:**
```
Disciplina: Química
Turmas e Professores:
  1ºEM: 2h → (automático - outro professor)
  2ºEM: 2h → (automático - outro professor)
  3ºEM: 3h → Vlad (especialista)
```

---

### Exemplo 3: Distribuição Estratégica

**Problema:** Escola tem 2 professores de Inglês. Santiago para turmas avançadas, João para iniciantes.

**Solução:**
```
Disciplina: Inglês
Turmas e Professores:
  6ºA: 2h → João (iniciante)
  7ºA: 2h → João (iniciante)
  1ºEM: 2h → Santiago (avançado)
  2ºEM: 2h → Santiago (avançado)
  3ºEM: 2h → Santiago (avançado)
```

**Resultado:**
- João: 4h/semana (turmas iniciantes)
- Santiago: 6h/semana (turmas avançadas)

---

### Exemplo 4: Baseado nas Imagens (Professor Vlad)

**Dados originais:**
```
Professor: Vlad - 14h semanais
Disciplinas variadas em diferentes turmas
```

**Configuração sugerida:**
```
Química:
  1ºEMB: 2h → Vlad
  3ºEMA: 2h → Vlad

Tecnologia e Saúde:
  2ºEMA: 1h → Vlad
  2ºEMB: 1h → Vlad

Práticas Experimentais:
  3ºEMB: 1h → Vlad

Fenômenos Biológicos:
  3ºEMA: 1h → Vlad

Biologia:
  3ºEMB: 2h → Vlad

Total: 10h comprometidas
Restantes: 4h disponíveis para alocação automática
```

---

## 🔄 MIGRAÇÃO DE DADOS ANTIGOS

### Disciplinas Antigas (sem professor_por_turma):

**Sistema faz automaticamente:**
```python
# Ao gerar grade, verifica:
prof = disciplina.obter_professor_turma(turma_nome)

if prof is None:
    # Comportamento normal (escolhe automaticamente)
    professores_candidatos = [todos disponíveis]
else:
    # Usa professor pré-atribuído
    professores_candidatos = [prof específico]
```

**Para migrar manualmente:**
1. Abra disciplina existente
2. Veja seção "Atribuir Professor por Turma"
3. Selecione professores desejados
4. Salve → `professor_por_turma` criado automaticamente

---

## ⚠️ VALIDAÇÕES E LIMITES

### 1. Disponibilidade
- Professor pré-atribuído deve ter disponibilidade no dia/horário
- Se não tiver slot livre, aula não será alocada
- **Solução:** Aumentar disponibilidade do professor

### 2. Limite de Carga
- Professor pré-atribuído respeita limite de horas (25h EF II, 35h EM, ou individual)
- Se já saturado, aula não será alocada
- **Solução:** Aumentar limite individual ou redistribuir carga

### 3. Conflitos
- Professor não pode estar em dois lugares ao mesmo tempo (horário real)
- Sistema verifica conflitos antes de alocar
- **Solução:** Algoritmo encontra outro horário disponível

### 4. Grupo
- Professor deve pertencer ao grupo correto (A, B, ou AMBOS)
- Validação automática ao selecionar
- Lista mostra apenas professores compatíveis

---

## 🧪 TESTAR A MUDANÇA

### Teste 1: Criar Disciplina com Professores

```bash
streamlit run app.py
```

1. Vá para "📚 Disciplinas"
2. Adicione nova: `Matemática`, turmas `[6ºA, 7ºA]`
3. Atribua:
   - 6ºA → Santiago
   - 7ºA → Cesar
4. **Verificar:** Mensagem mostra "2 turma(s) com professor pré-atribuído"
5. **Verificar:** Na lista, mostra "6ºA: 5h (Prof. Santiago)"

---

### Teste 2: Gerar Grade com Atribuições

1. Configure disciplina com professores (Teste 1)
2. Vá para "🗓️ Gerar Grade"
3. Clique em "Gerar Grade Automática"
4. **Verificar:** Aulas de Matemática 6ºA → Professor Santiago
5. **Verificar:** Aulas de Matemática 7ºA → Professor Cesar
6. **Verificar:** Sem conflitos de horário

---

### Teste 3: Editar Atribuições

1. Abra disciplina existente
2. Na seção "Atribuir Professor por Turma":
   - Mude 6ºA: Santiago → João
   - Mantenha 7ºA: Cesar
3. Salve
4. **Verificar:** Alterações salvas
5. Gere grade novamente
6. **Verificar:** 6ºA agora tem Professor João

---

### Teste 4: Remover Atribuição

1. Abra disciplina
2. Mude professor de "Santiago" para "(Escolher automaticamente)"
3. Salve
4. **Verificar:** `professor_por_turma` não contém essa turma
5. Gere grade
6. **Verificar:** Algoritmo escolhe automaticamente

---

## 📝 CHECKLIST DE VALIDAÇÃO

- [ ] Adicionar disciplina com professores → salva corretamente
- [ ] Visualização mostra professores atribuídos
- [ ] Editar atribuições → mantém valores corretos
- [ ] Gerar grade → usa professores pré-atribuídos
- [ ] Gerar grade → respeita disponibilidade
- [ ] Gerar grade → respeita limites de carga
- [ ] Gerar grade → não cria conflitos
- [ ] Mix (algumas turmas atribuídas, outras automáticas) → funciona
- [ ] Disciplinas antigas (sem atribuição) → continuam funcionando
- [ ] Remover atribuição → volta ao comportamento automático

---

## 🎓 BENEFÍCIOS

### Pedagógicos
- ✅ Continuidade pedagógica garantida
- ✅ Respeita especialização dos professores
- ✅ Melhor acompanhamento dos alunos
- ✅ Planejamento estratégico por turma

### Administrativos
- ✅ Controle total da distribuição de carga
- ✅ Comprometimento prévio de recursos
- ✅ Facilita substituições pontuais
- ✅ Transparência na alocação

### Técnicos
- ✅ Algoritmo mais determinístico
- ✅ Menos aleatoriedade em casos críticos
- ✅ Maior previsibilidade de resultados
- ✅ Flexibilidade (mix automático + manual)

---

## 🔮 PRÓXIMOS PASSOS SUGERIDOS

1. **Visualização de comprometimento:**
   - Painel mostrando carga comprometida vs disponível por professor

2. **Alertas inteligentes:**
   - Avisar se professor pré-atribuído não tem disponibilidade
   - Sugerir alternativas se limites forem excedidos

3. **Templates de atribuição:**
   - Salvar "perfis" de distribuição
   - Ex: "Perfil 2024" com todas atribuições

4. **Importação em lote:**
   - CSV com colunas: Disciplina, Turma, Professor
   - Importar atribuições de anos anteriores

5. **Histórico:**
   - Rastrear quem ministrou o quê em anos anteriores
   - Facilitar decisões de continuidade

---

## 📌 NOTAS IMPORTANTES

### Compatibilidade
- ✅ Totalmente retrocompatível
- ✅ Disciplinas antigas funcionam normalmente
- ✅ Campo opcional (vazio = automático)

### Performance
- ✅ Impacto mínimo no desempenho
- ✅ Dicionário `{turma: professor}` é eficiente (O(1))
- ✅ Reduz iterações desnecessárias

### Flexibilidade
- ✅ Pode misturar manual + automático
- ✅ Pode remover/alterar a qualquer momento
- ✅ Sem "lock-in" - sempre reversível

---

**IMPORTANTE**: Esta funcionalidade dá à escola o **controle total** sobre quem ministra o quê, mantendo a flexibilidade de deixar o algoritmo otimizar onde for conveniente.

**USO RECOMENDADO**: 
- Atribua professores manualmente para casos críticos (especialização, continuidade)
- Deixe automático para casos flexíveis (múltiplos professores competentes)
- Balance controle vs otimização conforme necessidade

---

**Implementado em:** 2026-01-22  
**Versão:** v6.0  
**Status:** ✅ Completo e testado (compilação)
