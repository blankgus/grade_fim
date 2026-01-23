# 🎯 MUDANÇA CRÍTICA: Carga Horária por Turma + Disciplina

**Data:** 2026-01-22
**Versão:** v5.0 - CARGA INDIVIDUAL POR TURMA

---

## 📋 MUDANÇA IMPLEMENTADA

### ❌ ANTES (inadequado):
```
Disciplina: Matemática
Carga Semanal: 5 aulas
Turmas: [6ºA, 7ºA, 8ºA]

→ Todas as turmas recebiam 5 aulas de Matemática (fixo)
```

### ✅ AGORA (correto):
```
Disciplina: Matemática
Carga por Turma:
  - 6ºA: 5 aulas/semana
  - 7ºA: 5 aulas/semana
  - 8ºA: 4 aulas/semana  ← DIFERENTE!

→ Cada turma pode ter carga diferente
```

---

## 🔧 ARQUIVOS MODIFICADOS

### 1. `models.py` - Modelo de Dados

**Mudanças:**
```python
from typing import List, Dict  # Adicionado Dict

@dataclass
class Disciplina:
    nome: str
    carga_semanal: int  # DEPRECATED: mantido para compatibilidade
    tipo: str
    turmas: List[str]
    grupo: str
    cor_fundo: str = "#4A90E2"
    cor_fonte: str = "#FFFFFF"
    carga_por_turma: Dict[str, int] = field(default_factory=dict)  # NOVO!
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    def obter_carga_turma(self, turma_nome: str) -> int:
        """Obtém a carga semanal para uma turma específica"""
        # PRIORIDADE 1: Usar carga específica
        if self.carga_por_turma and turma_nome in self.carga_por_turma:
            return self.carga_por_turma[turma_nome]
        # PRIORIDADE 2: Fallback para carga genérica
        return self.carga_semanal
```

**Compatibilidade:**
- ✅ `carga_semanal` mantido (fallback para disciplinas antigas)
- ✅ `carga_por_turma` usado quando disponível
- ✅ Método `obter_carga_turma()` decide automaticamente

---

### 2. `app.py` - Interface do Usuário

#### 2.1 Formulário de Adicionar Disciplina

**Nova seção:**
```python
# Após selecionar turmas, aparece:
st.write("### 📊 Carga Horária Individual por Turma")

for turma in turmas_selecionadas:
    carga_turma = st.number_input(
        f"{turma}",
        min_value=1,
        max_value=10,
        value=carga_padrao,  # Valor padrão
        help=f"Aulas semanais para {turma}"
    )
    carga_por_turma[turma] = carga_turma
```

**Ao salvar:**
```python
nova_disciplina = Disciplina(
    nome=nome,
    carga_semanal=carga_padrao,  # Padrão
    carga_por_turma=carga_por_turma_temp  # Individual!
)
```

#### 2.2 Lista de Disciplinas

**Exibição melhorada:**
```python
# Antes: "Matemática [A] - Carga: 5h"
# Agora: "Matemática [A] - 15h total (3 turmas)"

# Com detalhes:
📊 Carga por Turma:
6ºA: 5h | 7ºA: 5h | 8ºA: 5h
```

#### 2.3 Editar Disciplina

**Nova seção no formulário:**
- Mostra carga atual de cada turma
- Permite ajustar individualmente
- Calcula e exibe total automático

**Função auxiliar adicionada:**
```python
def obter_carga_disciplina_turma(disciplina, turma_nome):
    """Obtém carga específica, com fallback para genérica"""
    if hasattr(disciplina, 'obter_carga_turma'):
        return disciplina.obter_carga_turma(turma_nome)
    return disciplina.carga_semanal
```

---

### 3. `simple_scheduler.py` - Algoritmo

**Mudança crítica:**
```python
# ANTES:
for _ in range(disc.carga_semanal):  # Mesma carga para todos
    disciplinas_turma.append(disc)

# AGORA:
carga = disc.obter_carga_turma(turma_nome)  # Carga específica!
for _ in range(carga):
    disciplinas_turma.append(disc)
```

**Resultado:**
- ✅ Cada turma recebe exatamente a carga definida
- ✅ 6ºA pode ter 5 aulas de Matemática
- ✅ 7ºA pode ter 4 aulas de Matemática (diferente!)

---

## 🎯 COMO USAR

### Ao Cadastrar Nova Disciplina:

1. **Preencha dados básicos:**
   - Nome: `Matemática`
   - Carga Padrão: `5` (será aplicado a todas por padrão)
   - Turmas: Selecione `[6ºA, 7ºA, 8ºA]`

2. **Nova seção aparece automaticamente:**
   ```
   📊 Carga Horária Individual por Turma
   
   6ºA: [5]  ← ajuste aqui
   7ºA: [5]  ← ajuste aqui
   8ºA: [4]  ← ajuste aqui (diferente!)
   
   Total de aulas: 14h (3 turmas)
   ```

3. **Clique em "✅ Adicionar Disciplina"**

4. **Mensagem:**
   ```
   ✅ Disciplina 'Matemática' adicionada! Total: 14 aulas (3 turmas)
   ```

---

### Ao Editar Disciplina Existente:

1. **Abra a disciplina** na lista

2. **Visualize carga atual:**
   ```
   📊 Carga por Turma:
   6ºA: 5h | 7ºA: 5h | 8ºA: 4h
   ```

3. **No formulário de edição:**
   - Seção "Carga Horária Individual por Turma"
   - Ajuste os valores conforme necessário

4. **Salve alterações**

---

## 📊 EXEMPLOS PRÁTICOS

### Exemplo 1: Disciplina com Cargas Iguais
```
Educação Física
Turmas: 6ºA, 7ºA, 8ºA, 9ºA
Carga:
  - 6ºA: 2 aulas/semana
  - 7ºA: 2 aulas/semana
  - 8ºA: 2 aulas/semana
  - 9ºA: 2 aulas/semana
Total: 8 aulas
```

### Exemplo 2: Disciplina com Cargas Diferentes
```
Química
Turmas: 1ºEM, 2ºEM, 3ºEM
Carga:
  - 1ºEM: 3 aulas/semana
  - 2ºEM: 2 aulas/semana
  - 3ºEM: 4 aulas/semana (mais aprofundado!)
Total: 9 aulas
```

### Exemplo 3: Baseado nas Imagens Fornecidas
```
Professor: Vlad - 14 aulas semanais
Disciplinas:
  - Química:
    - 1ºEMB: 2 aulas
    - 3ºEMA: 2 aulas
  - Tecnologia e Saúde:
    - 2ºEMA: 1 aula
    - 2ºEMB: 1 aula
  - Práticas Experimentais:
    - 3ºEMB: 1 aula
  - Fenômenos Biológicos:
    - 3ºEMA: 1 aula
  - Biologia:
    - 3ºEMB: 2 aulas

Total: 10 aulas ← Diferente do total de 14h especificado
(As 4h restantes devem ser de outras disciplinas/turmas)
```

---

## 🔄 MIGRAÇÃO DE DADOS ANTIGOS

### Disciplinas Antigas (sem `carga_por_turma`):

**Sistema faz automaticamente:**
```python
# Se disciplina não tem carga_por_turma:
carga = disciplina.carga_semanal  # Usa valor antigo

# Se tem carga_por_turma:
carga = disciplina.carga_por_turma[turma_nome]  # Usa específico
```

**Para atualizar manualmente:**
1. Abra disciplina antiga
2. Veja que todas turmas têm mesma carga (padrão)
3. Ajuste individualmente se necessário
4. Salve → carga_por_turma será criado automaticamente

---

## ⚠️ NOTAS IMPORTANTES

### Compatibilidade
- ✅ Disciplinas antigas continuam funcionando
- ✅ Fallback automático para `carga_semanal`
- ✅ Nenhuma quebra de funcionalidade

### Carga Padrão
- `carga_semanal` agora é usado como "padrão"
- Ao adicionar nova turma, usa esse valor
- Pode ser ajustado individualmente depois

### Validação
- Mínimo: 1 aula/semana por turma
- Máximo: 10 aulas/semana por turma
- Total calculado automaticamente

### Performance
- ✅ Não há impacto significativo
- Dicionário `{turma: carga}` é eficiente
- Lookup O(1) por turma

---

## 🧪 TESTAR A MUDANÇA

### 1. Cadastrar Nova Disciplina:
```bash
streamlit run app.py
```

1. Vá para "📚 Disciplinas"
2. Clique em "➕ Adicionar Nova Disciplina"
3. Preencha nome, tipo, etc.
4. Selecione 3+ turmas
5. **Verifique**: Seção "Carga Horária Individual" aparece
6. Ajuste valores diferentes para cada turma
7. Salve e verifique mensagem de sucesso

### 2. Verificar Lista:
1. Na lista de disciplinas
2. **Verifique**: Mostra "Xh total (Y turmas)"
3. Abra disciplina
4. **Verifique**: Seção "Carga por Turma" mostra detalhes

### 3. Gerar Grade:
1. Vá para "🗓️ Gerar Grade"
2. Gere grade
3. **Verifique**: Turmas recebem quantidade correta de aulas
4. Exemplo: Se 6ºA tem 5 aulas de Matemática, deve aparecer exatamente 5 na grade

---

## 📝 CHECKLIST DE VALIDAÇÃO

- [ ] Cadastrar disciplina com cargas iguais → funciona
- [ ] Cadastrar disciplina com cargas diferentes → funciona
- [ ] Editar disciplina existente → mantém valores
- [ ] Alterar carga de uma turma → salva corretamente
- [ ] Gerar grade → usa cargas individuais
- [ ] Disciplinas antigas → continuam funcionando (fallback)
- [ ] Total de aulas calculado corretamente

---

## 🎓 BENEFÍCIOS

### Flexibilidade
- ✅ Cada turma pode ter necessidades diferentes
- ✅ Turmas avançadas podem ter mais aulas
- ✅ Turmas com dificuldade podem ter reforço

### Precisão
- ✅ Reflete realidade da escola
- ✅ Não desperdiça tempo com aulas desnecessárias
- ✅ Não falta aulas onde é necessário

### Gestão
- ✅ Facilita ajustes finos
- ✅ Melhor controle de carga de professores
- ✅ Planejamento mais preciso

---

## 🔮 PRÓXIMOS PASSOS SUGERIDOS

1. **Importação em lote**: CSV com cargas por turma
2. **Templates**: Salvar "perfis" de carga (ex: "Perfil Intensivo", "Perfil Padrão")
3. **Análise comparativa**: Comparar carga total entre turmas
4. **Recomendações**: Sistema sugere ajustes baseado em padrões

---

**IMPORTANTE**: Esta mudança é **retrocompatível**. Disciplinas antigas continuam funcionando normalmente, usando o valor de `carga_semanal` como fallback.
