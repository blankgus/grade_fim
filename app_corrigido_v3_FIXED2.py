
# ============================================
# MENU DE ABAS
# ============================================
abas = st.tabs(["🏠 Início", "📚 Disciplinas", "👩‍🏫 Professores", "🎒 Turmas", "🏫 Salas", "🗓️ Gerar Grade", "👨‍🏫 Grade por Professor", "🔧 Diagnóstico"])

# ============================================
# ABA INÍCIO
# ============================================
with abas[0]:
    st.header("Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Turmas", len(st.session_state.turmas))
    with col2:
        st.metric("Professores", len(st.session_state.professores))
    with col3:
        st.metric("Disciplinas", len(st.session_state.disciplinas))
    with col4:
        st.metric("Salas", len(st.session_state.salas))
    
    st.subheader("📊 Estatísticas por Segmento")
    
    turmas_efii = [t for t in st.session_state.turmas if obter_segmento_turma(t.nome) == "EF_II"]
    turmas_em = [t for t in st.session_state.turmas if obter_segmento_turma(t.nome) == "EM"]
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Ensino Fundamental II**")
        st.write(f"Turmas: {len(turmas_efii)}")
        st.write(f"Horário: 07:50 - 12:20")
        st.write(f"Aulas: 5 por dia + intervalo")
        st.write(f"Limite professor: {LIMITE_HORAS_EFII}h semanais")
        
    with col2:
        st.write("**Ensino Médio**")
        st.write(f"Turmas: {len(turmas_em)}")
        st.write(f"Horário: 07:00 - 13:10")
        st.write(f"Aulas: 7 por dia + intervalo")
        st.write(f"Limite professor: {LIMITE_HORAS_EM}h semanais")
    
    st.subheader("📈 Verificação de Carga de Aulas")
    
    for turma in st.session_state.turmas:
        carga_total = 0
        disciplinas_turma = []
        grupo_turma = obter_grupo_seguro(turma)
        segmento = obter_segmento_turma(turma.nome)
        
        for disc in st.session_state.disciplinas:
            if turma.nome in disc.turmas and obter_grupo_seguro(disc) == grupo_turma:
                carga_total += disc.carga_semanal
                disciplinas_turma.append(f"{disc.nome} ({disc.carga_semanal}a)")
        
        carga_maxima = calcular_carga_maxima(turma.serie)
        status = "✅" if carga_total == carga_maxima else "⚠️" if carga_total <= carga_maxima else "❌"
        
        st.write(f"**{turma.nome}** [{grupo_turma}] ({segmento}): {carga_total}/{carga_maxima} aulas {status}")
        
        if disciplinas_turma:
            st.caption(f"Disciplinas: {', '.join(disciplinas_turma[:3])}{'...' if len(disciplinas_turma) > 3 else ''}")
        else:
            st.caption("⚠️ Nenhuma disciplina atribuída")
    
    if st.button("💾 Salvar Tudo no Banco"):
        try:
            if salvar_tudo():
                st.success("✅ Todos os dados salvos!")
            else:
                st.error("❌ Erro ao salvar dados")
        except Exception as e:
            st.error(f"❌ Erro ao salvar: {str(e)}")

# ============================================
# ABA DISCIPLINAS
# ============================================
with abas[1]:
    st.header("📚 Disciplinas")
    
    grupo_filtro = st.selectbox("Filtrar por Grupo", ["Todos", "A", "B"], key="filtro_disc")
    
    with st.expander("➕ Adicionar Nova Disciplina", expanded=False):
        with st.form("add_disc"):
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("Nome da Disciplina*")
                carga = st.number_input("Carga Semanal*", 1, 10, 3)
                tipo = st.selectbox("Tipo*", ["pesada", "media", "leve", "pratica"])
            with col2:
                turmas_opcoes = [t.nome for t in st.session_state.turmas]
                turmas_selecionadas = st.multiselect("Turmas*", turmas_opcoes)
                grupo = st.selectbox("Grupo*", ["A", "B"])
                cor_fundo = st.color_picker("Cor de Fundo", "#4A90E2")
                cor_fonte = st.color_picker("Cor da Fonte", "#FFFFFF")
            
            # Mostrar professores disponíveis para esta disciplina
            if nome and turmas_selecionadas:
                st.subheader("👨‍🏫 Professores Disponíveis")
                
                # Determinar grupo para filtragem
                grupo_filtro_prof = grupo
                
                professores_disponiveis = []
                for prof in st.session_state.professores:
                    # Verificar se professor ministra alguma disciplina
                    # (não podemos verificar ainda se ministra esta disciplina específica)
                    prof_grupo = obter_grupo_seguro(prof)
                    if prof_grupo in [grupo_filtro_prof, "AMBOS"]:
                        professores_disponiveis.append(prof)
                
                if professores_disponiveis:
                    st.write(f"**{len(professores_disponiveis)} professores disponíveis no grupo {grupo}:**")
                    for prof in professores_disponiveis[:5]:  # Mostrar apenas 5
                        st.write(f"- {prof.nome} ({obter_segmento_professor(prof)})")
                    if len(professores_disponiveis) > 5:
                        st.write(f"... e mais {len(professores_disponiveis) - 5}")
                else:
                    st.warning(f"⚠️ Nenhum professor disponível no grupo {grupo}")
            
            if st.form_submit_button("✅ Adicionar Disciplina"):
                if nome and turmas_selecionadas:
                    try:
                        nova_disciplina = Disciplina(
                            nome, carga, tipo, turmas_selecionadas, grupo, cor_fundo, cor_fonte
                        )
                        st.session_state.disciplinas.append(nova_disciplina)
                        if salvar_tudo():
                            st.success(f"✅ Disciplina '{nome}' adicionada!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao adicionar disciplina: {str(e)}")
                else:
                    st.error("❌ Preencha todos os campos obrigatórios (*)")
    
    st.subheader("📋 Lista de Disciplinas")
    
    disciplinas_exibir = st.session_state.disciplinas
    if grupo_filtro != "Todos":
        disciplinas_exibir = [d for d in st.session_state.disciplinas if obter_grupo_seguro(d) == grupo_filtro]
    
    if not disciplinas_exibir:
        st.info("📝 Nenhuma disciplina cadastrada.")
    
    for disc in disciplinas_exibir:
        with st.expander(f"📖 {disc.nome} [{obter_grupo_seguro(disc)}] - Carga: {disc.carga_semanal}h", expanded=False):
            
            # SEÇÃO 1: INFORMAÇÕES DA DISCIPLINA
            st.write("### 📋 Informações da Disciplina")
            with st.form(f"edit_disc_{disc.id}"):
                col1, col2 = st.columns(2)
                with col1:
                    novo_nome = st.text_input("Nome", disc.nome, key=f"nome_{disc.id}")
                    nova_carga = st.number_input("Carga Semanal", 1, 10, disc.carga_semanal, key=f"carga_{disc.id}")
                    novo_tipo = st.selectbox(
                        "Tipo", 
                        ["pesada", "media", "leve", "pratica"],
                        index=["pesada", "media", "leve", "pratica"].index(disc.tipo),
                        key=f"tipo_{disc.id}"
                    )
                with col2:
                    turmas_opcoes = [t.nome for t in st.session_state.turmas]
                    turmas_selecionadas = st.multiselect(
                        "Turmas", 
                        turmas_opcoes,
                        default=disc.turmas,
                        key=f"turmas_{disc.id}"
                    )
                    novo_grupo = st.selectbox(
                        "Grupo", 
                        ["A", "B"],
                        index=0 if obter_grupo_seguro(disc) == "A" else 1,
                        key=f"grupo_{disc.id}"
                    )
                    nova_cor_fundo = st.color_picker("Cor de Fundo", disc.cor_fundo, key=f"cor_fundo_{disc.id}")
                    nova_cor_fonte = st.color_picker("Cor da Fonte", disc.cor_fonte, key=f"cor_fonte_{disc.id}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("💾 Salvar Alterações"):
                        if novo_nome and turmas_selecionadas:
                            try:
                                disc.nome = novo_nome
                                disc.carga_semanal = nova_carga
                                disc.tipo = novo_tipo
                                disc.turmas = turmas_selecionadas
                                disc.grupo = novo_grupo
                                disc.cor_fundo = nova_cor_fundo
                                disc.cor_fonte = nova_cor_fonte
                                
                                if salvar_tudo():
                                    st.success("✅ Disciplina atualizada!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erro ao atualizar: {str(e)}")
                        else:
                            st.error("❌ Preencha todos os campos obrigatórios")
                
                with col2:
                    if st.form_submit_button("🗑️ Excluir Disciplina", type="secondary"):
                        try:
                            st.session_state.disciplinas.remove(disc)
                            if salvar_tudo():
                                st.success("✅ Disciplina excluída!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erro ao excluir: {str(e)}")
            
            # SEÇÃO 2: PROFESSORES DISPONÍVEIS
            st.write("### 👨‍🏫 Professores Disponíveis")
            
            grupo_disc = obter_grupo_seguro(disc)
            
            # Obter professores que podem ministrar esta disciplina
            professores_disponiveis = obter_professores_para_disciplina(disc.nome, grupo_disc)
            
            if professores_disponiveis:
                # Dividir em professores livres e comprometidos
                professores_livres = []
                professores_comprometidos = []
                
                for prof in professores_disponiveis:
                    if verificar_professor_comprometido(prof, disc.nome, grupo_disc):
                        professores_comprometidos.append(prof)
                    else:
                        professores_livres.append(prof)
                
                # Mostrar estatísticas
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total", len(professores_disponiveis))
                with col2:
                    st.metric("Livres", len(professores_livres))
                with col3:
                    st.metric("Comprometidos", len(professores_comprometidos))
                
                # Mostrar professores livres
                if professores_livres:
                    st.write("#### ✅ Professores Livres (Podem ministrar):")
                    for prof in professores_livres:
                        segmento = obter_segmento_professor(prof)
                        limite = obter_limite_horas_professor(prof)
                        disponibilidade = calcular_disponibilidade_professor(prof)
                        
                        # Calcular carga atual (se houver aulas na grade)
                        carga_atual = 0
                        if hasattr(st.session_state, 'aulas') and st.session_state.aulas:
                            carga_atual = calcular_horas_professor(prof, st.session_state.aulas)
                        
                        status = "✅" if carga_atual < limite else "⚠️" if carga_atual == limite else "❌"
                        
                        st.write(f"- **{prof.nome}** ({segmento}): {carga_atual}/{limite}h {status}")
                        st.caption(f"  Disponibilidade: {disponibilidade} períodos/semana | Grupo: {obter_grupo_seguro(prof)}")
                
                # Mostrar professores comprometidos
                if professores_comprometidos:
                    st.write("#### ⚠️ Professores Comprometidos:")
                    for prof in professores_comprometidos:
                        # Descobrir com quais outras disciplinas está comprometido
                        outras_disciplinas = []
                        for outra_disc_nome in prof.disciplinas:
                            if outra_disc_nome != disc.nome:
                                # Verificar se é do mesmo grupo
                                for d in st.session_state.disciplinas:
                                    if d.nome == outra_disc_nome:
                                        if obter_grupo_seguro(d) == grupo_disc:
                                            outras_disciplinas.append(outra_disc_nome)
                                            break
                        
                        st.write(f"- **{prof.nome}**: Comprometido com {', '.join(outras_disciplinas[:2])}{'...' if len(outras_disciplinas) > 2 else ''}")
            else:
                st.warning(f"⚠️ Nenhum professor pode ministrar **{disc.nome}** no grupo **{grupo_disc}**")
                st.write("**Sugestões:**")
                st.write("1. Adicione professores que ministrem esta disciplina")
                st.write("2. Mude professores existentes para o grupo correto")
                st.write("3. Adicione a disciplina à lista de disciplinas dos professores")
            
            # SEÇÃO 3: TURMAS QUE CURSAM ESTA DISCIPLINA
            st.write("### 🎒 Turmas que Cursam esta Disciplina")
            
            if disc.turmas:
                for turma_nome in disc.turmas:
                    # Encontrar turma
                    turma_obj = next((t for t in st.session_state.turmas if t.nome == turma_nome), None)
                    if turma_obj:
                        segmento = obter_segmento_turma(turma_nome)
                        grupo_turma = obter_grupo_seguro(turma_obj)
                        
                        # Verificar compatibilidade de grupos
                        grupo_compativel = (grupo_disc == grupo_turma)
                        
                        st.write(f"- **{turma_nome}** ({segmento}, Grupo {grupo_turma}) {'✅' if grupo_compativel else '❌'}")
                        
                        if not grupo_compativel:
                            st.caption(f"  ⚠️ A disciplina é do grupo {grupo_disc}, mas a turma é do grupo {grupo_turma}")
            else:
                st.info("📝 Nenhuma turma atribuída a esta disciplina")

# ============================================
# ABA PROFESSORES
# ============================================
with abas[2]:
    st.header("👩‍🏫 Professores")
    
    grupo_filtro = st.selectbox("Filtrar por Grupo", ["Todos", "A", "B", "AMBOS"], key="filtro_prof")
    disc_nomes = [d.nome for d in st.session_state.disciplinas]
    
    with st.expander("➕ Adicionar Novo Professor", expanded=False):
        with st.form("add_prof"):
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("Nome do Professor*")
                disciplinas = st.multiselect("Disciplinas*", disc_nomes)
                grupo = st.selectbox("Grupo*", ["A", "B", "AMBOS"])
            with col2:
                disponibilidade = st.multiselect("Dias Disponíveis*", DIAS_SEMANA, default=DIAS_SEMANA)
                st.write("**Horários Indisponíveis:**")
                
                horarios_indisponiveis = []
                for dia in DIAS_SEMANA:
                    with st.container():
                        st.write(f"**{dia.upper()}:**")
                        horarios_cols = st.columns(4)
                        horarios_todos = list(range(1, 8))
                        for i, horario in enumerate(horarios_todos):
                            with horarios_cols[i % 4]:
                                if st.checkbox(f"{horario}º", key=f"add_{dia}_{horario}"):
                                    horarios_indisponiveis.append(f"{dia}_{horario}")
            
            # Mostrar limites de horas baseado nas disciplinas
            if disciplinas:
                # Determinar segmento do professor
                segmento = "AMBOS"
                tem_efii = False
                tem_em = False
                
                for disc_nome in disciplinas:
                    # Verificar turmas desta disciplina
                    for disc in st.session_state.disciplinas:
                        if disc.nome == disc_nome:
                            for turma_nome in disc.turmas:
                                if obter_segmento_turma(turma_nome) == "EF_II":
                                    tem_efii = True
                                elif obter_segmento_turma(turma_nome) == "EM":
                                    tem_em = True
                
                if tem_efii and not tem_em:
                    segmento = "EF_II"
                    limite = LIMITE_HORAS_EFII
                elif tem_em and not tem_efii:
                    segmento = "EM"
                    limite = LIMITE_HORAS_EM
                else:
                    segmento = "AMBOS"
                    limite = LIMITE_HORAS_EM  # Usar limite maior
                
                st.info(f"💡 Este professor será do segmento **{segmento}** com limite de **{limite}h** semanais")
            
            if st.form_submit_button("✅ Adicionar Professor"):
                if nome and disciplinas and disponibilidade:
                    try:
                        disponibilidade_completa = converter_disponibilidade_para_completo(disponibilidade)
                        
                        novo_professor = Professor(
                            nome, 
                            disciplinas, 
                            disponibilidade_completa,
                            grupo,
                            horarios_indisponiveis
                        )
                        st.session_state.professores.append(novo_professor)
                        if salvar_tudo():
                            st.success(f"✅ Professor '{nome}' adicionado!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao adicionar professor: {str(e)}")
                else:
                    st.error("❌ Preencha todos os campos obrigatórios (*)")
    
    st.subheader("📋 Lista de Professores")
    
    professores_exibir = st.session_state.professores
    if grupo_filtro != "Todos":
        professores_exibir = [p for p in st.session_state.professores if obter_grupo_seguro(p) == grupo_filtro]
    
    if not professores_exibir:
        st.info("📝 Nenhum professor cadastrado.")
    
    for prof in professores_exibir:
        with st.expander(f"👨‍🏫 {prof.nome} [{obter_grupo_seguro(prof)}]", expanded=False):
            disciplinas_validas = [d for d in prof.disciplinas if d in disc_nomes]
            
            # Calcular informações do professor
            segmento = obter_segmento_professor(prof)
            limite = obter_limite_horas_professor(prof)
            disponibilidade_horas = calcular_disponibilidade_professor(prof)
            
            # Calcular carga atual (se houver aulas na grade)
            carga_atual = 0
            if hasattr(st.session_state, 'aulas') and st.session_state.aulas:
                carga_atual = calcular_horas_professor(prof, st.session_state.aulas)
            
            # Mostrar informações
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Segmento", segmento)
            with col2:
                st.metric("Carga Atual", f"{carga_atual}/{limite}h")
            with col3:
                st.metric("Disponibilidade", f"{disponibilidade_horas} períodos")
            
            with st.form(f"edit_prof_{prof.id}"):
                col1, col2 = st.columns(2)
                with col1:
                    novo_nome = st.text_input("Nome", prof.nome, key=f"nome_prof_{prof.id}")
                    novas_disciplinas = st.multiselect(
                        "Disciplinas", 
                        disc_nomes, 
                        default=disciplinas_validas,
                        key=f"disc_prof_{prof.id}"
                    )
                    novo_grupo = st.selectbox(
                        "Grupo", 
                        ["A", "B", "AMBOS"],
                        index=["A", "B", "AMBOS"].index(obter_grupo_seguro(prof)),
                        key=f"grupo_prof_{prof.id}"
                    )
                with col2:
                    disponibilidade_convertida = converter_disponibilidade_para_semana(prof.disponibilidade)
                    
                    nova_disponibilidade = st.multiselect(
                        "Dias Disponíveis", 
                        DIAS_SEMANA, 
                        default=disponibilidade_convertida,
                        key=f"disp_prof_{prof.id}"
                    )
                    
                    st.write("**Horários Indisponíveis:**")
                    novos_horarios_indisponiveis = []
                    horarios_todos = list(range(1, 8))
                    for dia in DIAS_SEMANA:
                        with st.container():
                            st.write(f"**{dia.upper()}:**")
                            horarios_cols = st.columns(4)
                            for i, horario in enumerate(horarios_todos):
                                with horarios_cols[i % 4]:
                                    checked = False
                                    horario_str = f"{dia}_{horario}"
                                    if hasattr(prof, 'horarios_indisponiveis'):
                                        if isinstance(prof.horarios_indisponiveis, (list, set)):
                                            checked = horario_str in prof.horarios_indisponiveis
                                    
                                    if st.checkbox(
                                        f"{horario}º", 
                                        value=checked,
                                        key=f"edit_{prof.id}_{dia}_{horario}"
                                    ):
                                        novos_horarios_indisponiveis.append(horario_str)
                
                # Mostrar novo segmento se disciplinas mudarem
                if novas_disciplinas != disciplinas_validas:
                    # Recalcular segmento
                    novo_segmento = "AMBOS"
                    tem_efii = False
                    tem_em = False
                    
                    for disc_nome in novas_disciplinas:
                        for disc in st.session_state.disciplinas:
                            if disc.nome == disc_nome:
                                for turma_nome in disc.turmas:
                                    if obter_segmento_turma(turma_nome) == "EF_II":
                                        tem_efii = True
                                    elif obter_segmento_turma(turma_nome) == "EM":
                                        tem_em = True
                    
                    if tem_efii and not tem_em:
                        novo_segmento = "EF_II"
                        novo_limite = LIMITE_HORAS_EFII
                    elif tem_em and not tem_efii:
                        novo_segmento = "EM"
                        novo_limite = LIMITE_HORAS_EM
                    else:
                        novo_segmento = "AMBOS"
                        novo_limite = LIMITE_HORAS_EM
                    
                    st.info(f"💡 Novo segmento: **{novo_segmento}** com limite de **{novo_limite}h**")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("💾 Salvar Alterações"):
                        if novo_nome and novas_disciplinas and nova_disponibilidade:
                            try:
                                prof.nome = novo_nome
                                prof.disciplinas = novas_disciplinas
                                prof.grupo = novo_grupo
                                
                                disponibilidade_completa = converter_disponibilidade_para_completo(nova_disponibilidade)
                                
                                prof.disponibilidade = disponibilidade_completa
                                prof.horarios_indisponiveis = novos_horarios_indisponiveis
                                
                                if salvar_tudo():
                                    st.success("✅ Professor atualizado!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erro ao atualizar: {str(e)}")
                        else:
                            st.error("❌ Preencha todos os campos obrigatórios")
                
                with col2:
                    if st.form_submit_button("🗑️ Excluir Professor", type="secondary"):
                        try:
                            st.session_state.professores.remove(prof)
                            if salvar_tudo():
                                st.success("✅ Professor excluído!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erro ao excluir: {str(e)}")

# ============================================
# ABA TURMAS
# ============================================
with abas[3]:
    st.header("🎒 Turmas")
    
    grupo_filtro = st.selectbox("Filtrar por Grupo", ["Todos", "A", "B"], key="filtro_turma")
    
    with st.expander("➕ Adicionar Nova Turma", expanded=False):
        with st.form("add_turma"):
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("Nome da Turma* (ex: 8anoA)")
                serie = st.text_input("Série* (ex: 8ano)")
            with col2:
                turno = st.selectbox("Turno*", ["manha"], disabled=True)
                grupo = st.selectbox("Grupo*", ["A", "B"])
            
            segmento = "EM" if serie and 'em' in serie.lower() else "EF_II"
            st.info(f"💡 Segmento: {segmento} - {calcular_carga_maxima(serie)}h semanais máximas")
            
            if st.form_submit_button("✅ Adicionar Turma"):
                if nome and serie:
                    try:
                        nova_turma = Turma(nome, serie, "manha", grupo, segmento)
                        st.session_state.turmas.append(nova_turma)
                        if salvar_tudo():
                            st.success(f"✅ Turma '{nome}' adicionada!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao adicionar turma: {str(e)}")
                else:
                    st.error("❌ Preencha todos os campos obrigatórios (*)")
    
    st.subheader("📋 Lista de Turmas")
    
    turmas_exibir = st.session_state.turmas
    if grupo_filtro != "Todos":
        turmas_exibir = [t for t in st.session_state.turmas if obter_grupo_seguro(t) == grupo_filtro]
    
    if not turmas_exibir:
        st.info("📝 Nenhuma turma cadastrada.")
    
    for turma in turmas_exibir:
        with st.expander(f"🎒 {turma.nome} [{obter_grupo_seguro(turma)}]", expanded=False):
            with st.form(f"edit_turma_{turma.id}"):
                col1, col2 = st.columns(2)
                with col1:
                    novo_nome = st.text_input("Nome", turma.nome, key=f"nome_turma_{turma.id}")
                    nova_serie = st.text_input("Série", turma.serie, key=f"serie_turma_{turma.id}")
                with col2:
                    st.text_input("Turno", "manha", disabled=True, key=f"turno_turma_{turma.id}")
                    novo_grupo = st.selectbox(
                        "Grupo", 
                        ["A", "B"],
                        index=0 if obter_grupo_seguro(turma) == "A" else 1,
                        key=f"grupo_turma_{turma.id}"
                    )
                
                segmento = obter_segmento_turma(turma.nome)
                horarios = obter_horarios_turma(turma.nome)
                st.write(f"**Segmento:** {segmento}")
                st.write(f"**Horários disponíveis:** {len(horarios)} períodos")
                
                grupo_turma = obter_grupo_seguro(turma)
                carga_atual = 0
                disciplinas_turma = []
                
                for disc in st.session_state.disciplinas:
                    if turma.nome in disc.turmas and obter_grupo_seguro(disc) == grupo_turma:
                        carga_atual += disc.carga_semanal
                        disciplinas_turma.append(disc.nome)
                
                carga_maxima = calcular_carga_maxima(turma.serie)
                st.write(f"**Carga horária atual:** {carga_atual}/{carga_maxima}h")
                if disciplinas_turma:
                    st.caption(f"Disciplinas: {', '.join(disciplinas_turma[:3])}{'...' if len(disciplinas_turma) > 3 else ''}")
                else:
                    st.caption("⚠️ Nenhuma disciplina atribuída")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("💾 Salvar Alterações"):
                        if novo_nome and nova_serie:
                            try:
                                turma.nome = novo_nome
                                turma.serie = nova_serie
                                turma.grupo = novo_grupo
                                
                                if salvar_tudo():
                                    st.success("✅ Turma atualizada!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erro ao atualizar: {str(e)}")
                        else:
                            st.error("❌ Preencha todos os campos obrigatórios")
                
                with col2:
                    if st.form_submit_button("🗑️ Excluir Turma", type="secondary"):
                        try:
                            st.session_state.turmas.remove(turma)
                            if salvar_tudo():
                                st.success("✅ Turma excluída!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erro ao excluir: {str(e)}")

# ============================================
# ABA SALAS
# ============================================
with abas[4]:
    st.header("🏫 Salas")
    
    with st.expander("➕ Adicionar Nova Sala", expanded=False):
        with st.form("add_sala"):
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("Nome da Sala*")
                capacidade = st.number_input("Capacidade*", 1, 100, 30)
            with col2:
                tipo = st.selectbox("Tipo*", ["normal", "laboratório", "auditório"])
            
            if st.form_submit_button("✅ Adicionar Sala"):
                if nome:
                    try:
                        nova_sala = Sala(nome, capacidade, tipo)
                        st.session_state.salas.append(nova_sala)
                        if salvar_tudo():
                            st.success(f"✅ Sala '{nome}' adicionada!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro ao adicionar sala: {str(e)}")
                else:
                    st.error("❌ Preencha todos os campos obrigatórios (*)")
    
    st.subheader("📋 Lista de Salas")
    
    if not st.session_state.salas:
        st.info("📝 Nenhuma sala cadastrada.")
    
    for sala in st.session_state.salas:
        with st.expander(f"🏫 {sala.nome}", expanded=False):
            with st.form(f"edit_sala_{sala.id}"):
                col1, col2 = st.columns(2)
                with col1:
                    novo_nome = st.text_input("Nome", sala.nome, key=f"nome_sala_{sala.id}")
                    nova_capacidade = st.number_input("Capacidade", 1, 100, sala.capacidade, key=f"cap_sala_{sala.id}")
                with col2:
                    novo_tipo = st.selectbox(
                        "Tipo", 
                        ["normal", "laboratório", "auditório"],
                        index=["normal", "laboratório", "auditório"].index(sala.tipo),
                        key=f"tipo_sala_{sala.id}"
                    )
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("💾 Salvar Alterações"):
                        if novo_nome:
                            try:
                                sala.nome = novo_nome
                                sala.capacidade = nova_capacidade
                                sala.tipo = novo_tipo
                                
                                if salvar_tudo():
                                    st.success("✅ Sala atualizada!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Erro ao atualizar: {str(e)}")
                        else:
                            st.error("❌ Preencha todos os campos obrigatórios")
                
                with col2:
                    if st.form_submit_button("🗑️ Excluir Sala", type="secondary"):
                        try:
                            st.session_state.salas.remove(sala)
                            if salvar_tudo():
                                st.success("✅ Sala excluída!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erro ao excluir: {str(e)}")

# ============================================
# ABA GERAR GRADE (VERSÃO CORRIGIDA)
# ============================================
with abas[5]:
    st.header("🗓️ Gerar Grade Horária")
    
    st.subheader("🎯 Configurações da Grade")
    
    col1, col2 = st.columns(2)
    with col1:
        tipo_grade = st.selectbox(
            "Tipo de Grade",
            [
                "Grade Completa - Todas as Turmas",
                "Grade por Grupo A",
                "Grade por Grupo B", 
                "Grade por Turma Específica"
            ],
            key="tipo_grade_select"
        )
        
        if tipo_grade == "Grade por Turma Específica":
            turmas_opcoes = [t.nome for t in st.session_state.turmas]
            if turmas_opcoes:
                turma_selecionada = st.selectbox("Selecionar Turma", turmas_opcoes, key="turma_especifica_select")
            else:
                turma_selecionada = None
    
    with col2:
        tipo_algoritmo = st.selectbox(
            "Algoritmo de Geração",
            ["Algoritmo Simples (Rápido)", "Algoritmo Corrigido (Recomendado)"],
            key="algoritmo_select"
        )
        
        tipo_completador = st.selectbox(
            "Algoritmo de Completude",
            ["Completador Básico", "Completador Avançado (Recomendado)"],
            help="O completador avançado usa múltiplas estratégias para tentar completar grades incompletas",
            key="completador_select"
        )
        
        st.info("📅 **EM: 07:00-13:10 (7 períodos)**")
        st.info("📅 **EF II: 07:50-12:20 (5 períodos)**")
        st.info("📊 **Limites:** EF II: 25h | EM: 35h")
    
    st.subheader("📊 Pré-análise de Viabilidade")
    
    # Determinar turmas filtradas
    if tipo_grade == "Grade por Grupo A":
        turmas_filtradas = [t for t in st.session_state.turmas if obter_grupo_seguro(t) == "A"]
        grupo_texto = "Grupo A"
    elif tipo_grade == "Grade por Grupo B":
        turmas_filtradas = [t for t in st.session_state.turmas if obter_grupo_seguro(t) == "B"]
        grupo_texto = "Grupo B"
    elif tipo_grade == "Grade por Turma Específica" and turma_selecionada:
        turmas_filtradas = [t for t in st.session_state.turmas if t.nome == turma_selecionada]
        grupo_texto = f"Turma {turma_selecionada}"
    else:
        turmas_filtradas = st.session_state.turmas
        grupo_texto = "Todas as Turmas"
    
    # Determinar disciplinas filtradas
    if tipo_grade == "Grade por Grupo A":
        disciplinas_filtradas = [d for d in st.session_state.disciplinas if obter_grupo_seguro(d) == "A"]
    elif tipo_grade == "Grade por Grupo B":
        disciplinas_filtradas = [d for d in st.session_state.disciplinas if obter_grupo_seguro(d) == "B"]
    else:
        disciplinas_filtradas = st.session_state.disciplinas
    
    # Determinar professores filtrados
    if tipo_grade == "Grade por Grupo A":
        professores_filtrados = [p for p in st.session_state.professores 
                               if obter_grupo_seguro(p) in ["A", "AMBOS"]]
    elif tipo_grade == "Grade por Grupo B":
        professores_filtrados = [p for p in st.session_state.professores 
                               if obter_grupo_seguro(p) in ["B", "AMBOS"]]
    else:
        professores_filtrados = st.session_state.professores
    
    # Cálculos de capacidade
    total_aulas = 0
    aulas_por_turma = {}
    problemas_carga = []
    
    for turma in turmas_filtradas:
        aulas_turma = 0
        grupo_turma = obter_grupo_seguro(turma)
        
        for disc in disciplinas_filtradas:
            disc_grupo = obter_grupo_seguro(disc)
            if turma.nome in disc.turmas and disc_grupo == grupo_turma:
                aulas_turma += disc.carga_semanal
                total_aulas += disc.carga_semanal
        
        aulas_por_turma[turma.nome] = aulas_turma
        
        carga_maxima = calcular_carga_maxima(turma.serie)
        if aulas_turma != carga_maxima:
            status = "✅" if aulas_turma == carga_maxima else "⚠️" if aulas_turma <= carga_maxima else "❌"
            problemas_carga.append(f"{turma.nome} [{grupo_turma}]: {aulas_turma}h {status} {carga_maxima}h máximo")
    
    capacidade_total = 0
    for turma in turmas_filtradas:
        horarios_turma = obter_horarios_turma(turma.nome)
        capacidade_total += len(DIAS_SEMANA) * len(horarios_turma)
    
    # Calcular capacidade dos professores
    capacidade_professores = 0
    for prof in professores_filtrados:
        limite = obter_limite_horas_professor(prof)
        capacidade_professores += limite
    
    # Mostrar métricas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Turmas", len(turmas_filtradas))
    with col2:
        st.metric("Aulas Necessárias", total_aulas)
    with col3:
        st.metric("Capacidade Horários", capacidade_total)
    with col4:
        st.metric("Capacidade Professores", capacidade_professores)
    
    # Mostrar problemas de carga
    if problemas_carga:
        st.warning("⚠️ Observações sobre carga horária:")
        for problema in problemas_carga:
            st.write(f"- {problema}")
    
    # Validação de viabilidade
    viabilidade_ok = True
    mensagens_erro = []
    
    if total_aulas == 0:
        mensagens_erro.append("❌ Nenhuma aula para alocar! Verifique as disciplinas.")
        viabilidade_ok = False
    elif total_aulas > capacidade_total:
        mensagens_erro.append(f"❌ Capacidade de horários insuficiente! Reduza a carga horária em {total_aulas - capacidade_total} aulas.")
        viabilidade_ok = False
    elif total_aulas > capacidade_professores:
        mensagens_erro.append(f"❌ Capacidade dos professores insuficiente! Adicione mais professores ou aumente limites.")
        viabilidade_ok = False
    
    for mensagem in mensagens_erro:
        st.error(mensagem)
    
    # Botão de geração (só habilitado se viável)
    if viabilidade_ok:
        st.success("✅ Pronto para gerar grade!")
        
        if st.button("🚀 Gerar Grade Horária", type="primary", disabled=not viabilidade_ok):
            if not turmas_filtradas:
                st.error("❌ Nenhuma turma selecionada!")
            elif not disciplinas_filtradas:
                st.error("❌ Nenhuma disciplina disponível!")
            else:
                # BLOCO TRY CORRETAMENTE ESTRUTURADO
                try:
                    with st.spinner(f"Gerando grade para {grupo_texto}..."):
                        # Escolher algoritmo
                        if tipo_algoritmo == "Algoritmo Corrigido (Recomendado)":
                            try:
                                from simple_scheduler_final import SimpleGradeHoraria
                            except ImportError:
                                st.error("❌ Algoritmo corrigido não disponível! Usando algoritmo simples.")
                                from simple_scheduler import SimpleGradeHoraria
                        else:
                            from simple_scheduler import SimpleGradeHoraria
                        
                        # Criar scheduler
                        simple_grade = SimpleGradeHoraria(
                            turmas=turmas_filtradas,
                            professores=professores_filtrados,
                            disciplinas=disciplinas_filtradas,
                            salas=st.session_state.salas
                        )
                        
                        # Gerar grade
                        aulas = simple_grade.gerar_grade()
                        
                        # Filtrar por turma específica se necessário
                        if tipo_grade == "Grade por Turma Específica" and turma_selecionada:
                            aulas = [a for a in aulas if obter_turma_aula(a) == turma_selecionada]
                        
                        # Salvar no estado da sessão
                        st.session_state.aulas = aulas
                        
                        if salvar_tudo():
                            st.success(f"✅ Grade {grupo_texto} gerada com sucesso! ({len(aulas)} aulas)")
                        
                        # ============================================
                        # ANÁLISE DA GRADE GERADA
                        # ============================================
                        
                        if aulas:
                            # Análise de qualidade
                            st.subheader("📊 Análise da Grade Gerada")
                            
                            # Verificar conflitos
                            conflitos = verificar_conflitos_horarios(aulas)
                            superposicoes = verificar_professor_superposto(aulas)
                            limites_excedidos = verificar_limites_professores(aulas)
                            
                            # Mostrar métricas
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Aulas", len(aulas))
                            with col2:
                                st.metric("Conflitos", len(conflitos))
                            with col3:
                                st.metric("Superposições", len(superposicoes))
                            with col4:
                                st.metric("Limites Excedidos", len(limites_excedidos))
                            
                            # Mostrar problemas
                            if superposicoes:
                                st.error(f"❌ **{len(superposicoes)} SUPERPOSIÇÕES DE PROFESSOR**")
                                with st.expander("Ver detalhes", expanded=False):
                                    for sup in superposicoes[:3]:
                                        st.write(f"- Professor {sup['professor']}: {len(sup['aulas'])} aulas às {sup['dia']}, {sup['horario_real']}")
                            
                            if conflitos:
                                st.warning(f"⚠️ **{len(conflitos)} conflitos de horário**")
                            
                            if limites_excedidos:
                                st.warning(f"⚠️ **{len(limites_excedidos)} professores com limite excedido**")
                            
                            # Botões de correção
                            if superposicoes or conflitos or limites_excedidos:
                                st.subheader("🔧 Correções Necessárias")
                                
                                col1, col2 = st.columns(2)
                                with col1:
                                    if superposicoes:
                                        if st.button("🚨 Corrigir Superposições", type="primary", key="corrigir_sup"):
                                            with st.spinner("Corrigindo superposições..."):
                                                aulas_corrigidas = corrigir_superposicoes_professor(aulas, superposicoes)
                                                st.session_state.aulas = aulas_corrigidas
                                                salvar_tudo()
                                                st.success("✅ Superposições corrigidas!")
                                                st.rerun()
                                
                                with col2:
                                    if conflitos:
                                        if st.button("🔄 Corrigir Conflitos", type="secondary", key="corrigir_conf"):
                                            with st.spinner("Corrigindo conflitos..."):
                                                aulas_corrigidas = corrigir_conflitos_automaticamente(aulas, conflitos)
                                                st.session_state.aulas = aulas_corrigidas
                                                salvar_tudo()
                                                st.success("✅ Conflitos corrigidos!")
                                                st.rerun()
                            
                            # Visualização da grade
                            st.subheader("📅 Visualização da Grade")
                            
                            # Mostrar por turma
                            turmas_na_grade = set()
                            for aula in aulas:
                                turma = obter_turma_aula(aula)
                                if turma:
                                    turmas_na_grade.add(turma)
                            
                            for turma_nome in sorted(turmas_na_grade):
                                with st.expander(f"🎒 Turma {turma_nome}", expanded=False):
                                    # Filtrar aulas da turma
                                    aulas_turma = [a for a in aulas if obter_turma_aula(a) == turma_nome]
                                    
                                    # Criar tabela simples
                                    dias = ["segunda", "terca", "quarta", "quinta", "sexta"]
                                    periodos = obter_horarios_turma(turma_nome)
                                    
                                    # Dataframe
                                    dados = []
                                    for aula in aulas_turma:
                                        dados.append({
                                            "Dia": obter_dia_aula(aula).capitalize(),
                                            "Período": f"{obter_horario_aula(aula)}º",
                                            "Horário": obter_horario_real(turma_nome, obter_horario_aula(aula)),
                                            "Disciplina": obter_disciplina_aula(aula),
                                            "Professor": obter_professor_aula(aula)
                                        })
                                    
                                    if dados:
                                        df_turma = pd.DataFrame(dados)
                                        df_turma = df_turma.sort_values(["Dia", "Período"])
                                        st.dataframe(df_turma, use_container_width=True)
                                    else:
                                        st.info("Nenhuma aula para esta turma")
                        
                        else:
                            st.warning("⚠️ Nenhuma aula foi gerada. Verifique a configuração.")
                    
                except Exception as e:
                    st.error(f"❌ Erro ao gerar grade: {str(e)}")
                    st.code(traceback.format_exc())
    
    # Se não é viável, mostrar botão desabilitado
    else:
        st.button("🚀 Gerar Grade Horária", type="primary", disabled=True, 
                 help="Corrija os problemas de viabilidade primeiro")

# ============================================
# ABA GRADE POR PROFESSOR
# ============================================
with abas[6]:
    st.header("👨‍🏫 Grade Horária por Professor")
    
    if not st.session_state.get('aulas'):
        st.info("ℹ️ Gere uma grade horária primeiro na aba 'Gerar Grade'.")
    else:
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            options_set = set()
            for a in st.session_state.aulas:
                prof = obter_professor_aula(a)
                if prof:
                    options_set.add(prof)
            options = list(sorted(options_set))
            
            professor_selecionado = st.selectbox(
                "Selecionar Professor",
                options=options,
                key="filtro_professor_grade_1"
            )
        
        if professor_selecionado:
            # Filtrar aulas do professor
            aulas_professor = [a for a in st.session_state.aulas if obter_professor_aula(a) == professor_selecionado]
            
            if not aulas_professor:
                st.warning(f"ℹ️ Professor {professor_selecionado} não tem aulas alocadas.")
            else:
                # Calcular informações do professor
                professor_obj = next((p for p in st.session_state.professores if p.nome == professor_selecionado), None)
                segmento = obter_segmento_professor(professor_obj)
                limite = obter_limite_horas_professor(professor_obj)
                
                # Mostrar estatísticas
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total de Aulas", len(aulas_professor))
                with col2:
                    st.metric("Limite Horas", limite)
                with col3:
                    st.metric("Segmento", segmento)
                with col4:
                    disponibilidade = calcular_disponibilidade_professor(professor_obj) if professor_obj else 0
                    st.metric("Disponibilidade", f"{disponibilidade} períodos")
                
                st.success(f"📊 Professor {professor_selecionado} ({segmento}): {len(aulas_professor)}/{limite}h")
                
                # Criar dataframe COM HORÁRIOS REAIS
                df_professor = pd.DataFrame([
                    {
                        "Dia": (obter_dia_aula(a) or "").capitalize(),
                        "Período": f"{obter_horario_aula(a)}º",
                        "Horário REAL": obter_horario_real(obter_turma_aula(a), obter_horario_aula(a)),
                        "Turma": obter_turma_aula(a),
                        "Disciplina": obter_disciplina_aula(a),
                        "Segmento": obter_segmento_aula(a) or obter_segmento_turma(obter_turma_aula(a))
                    }
                    for a in aulas_professor
                ])
                
                # Ordenar por horário REAL
                ordem_dias = {"Segunda": 1, "Terca": 2, "Quarta": 3, "Quinta": 4, "Sexta": 5}
                df_professor['Ordem_Dia'] = df_professor['Dia'].map(ordem_dias)
                
                # Extrair hora inicial para ordenação
                def extrair_hora_inicio(horario_real):
                    try:
                        return int(horario_real.split(':')[0])
                    except:
                        return 0
                
                df_professor['Hora_Inicio'] = df_professor['Horário REAL'].apply(extrair_hora_inicio)
                df_professor = df_professor.sort_values(['Ordem_Dia', 'Hora_Inicio']).drop(['Ordem_Dia', 'Hora_Inicio'], axis=1)
                
                st.dataframe(df_professor, width='stretch')

# ============================================
# ABA DIAGNÓSTICO
# ============================================
with abas[7]:
    st.header("🔧 DIAGNÓSTICO AVANÇADO DO SISTEMA")
    
    st.subheader("📊 Análise de Capacidade")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_necessario = 0
        for turma in st.session_state.turmas:
            grupo_turma = obter_grupo_seguro(turma)
            for disc in st.session_state.disciplinas:
                if turma.nome in disc.turmas and obter_grupo_seguro(disc) == grupo_turma:
                    total_necessario += disc.carga_semanal
        st.metric("Aulas Necessárias", total_necessario)
    
    with col2:
        capacidade_total = 0
        for turma in st.session_state.turmas:
            horarios = obter_horarios_turma(turma.nome)
            capacidade_total += len(horarios) * 5
        st.metric("Capacidade Horários", capacidade_total)
    
    with col3:
        capacidade_professores = 0
        for professor in st.session_state.professores:
            capacidade_professores += obter_limite_horas_professor(professor)
        st.metric("Capacidade Professores", capacidade_professores)
    
    with col4:
        if capacidade_total >= total_necessario and capacidade_professores >= total_necessario:
            st.success("✅ Capacidade OK")
        else:
            problemas = []
            if capacidade_total < total_necessario:
                problemas.append(f"Horários: -{total_necessario - capacidade_total}")
            if capacidade_professores < total_necessario:
                problemas.append(f"Professores: -{total_necessario - capacidade_professores}")
            st.error(f"❌ Déficit: {', '.join(problemas)}")
    
    # Análise de professores
    st.subheader("👨‍🏫 Análise de Professores")
    
    professores_problema = []
    for prof in st.session_state.professores:
        dias_disponiveis = len(prof.disponibilidade) if hasattr(prof, 'disponibilidade') else 0
        segmento = obter_segmento_professor(prof)
        limite = obter_limite_horas_professor(prof)
        
        if dias_disponiveis < 3:
            professores_problema.append(f"**{prof.nome}** ({segmento}): Apenas {dias_disponiveis} dia(s) | Limite: {limite}h")
    
    if professores_problema:
        st.warning("⚠️ Professores com pouca disponibilidade:")
        for problema in professores_problema[:3]:
            st.markdown(f"- {problema}")
        if len(professores_problema) > 3:
            st.caption(f"... e mais {len(professores_problema) - 3}")
    else:
        st.success("✅ Todos professores têm disponibilidade razoável")
    
    # Botões para correção de problemas
    st.subheader("🔄 Ferramentas de Correção")
    
    if st.session_state.get('aulas'):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔧 Remover Aulas Repetidas", use_container_width=True):
                with st.spinner("Removendo aulas repetidas..."):
                    aulas_original = len(st.session_state.aulas)
                    st.session_state.aulas = remover_aulas_repetidas(st.session_state.aulas)
                    aulas_final = len(st.session_state.aulas)
                    
                    if aulas_final < aulas_original:
                        st.success(f"✅ Removidas {aulas_original - aulas_final} aulas repetidas!")
                        st.success(f"✅ Total de aulas agora: {aulas_final}")
                        if salvar_tudo():
                            st.success("✅ Grade atualizada no banco de dados!")
                        st.rerun()
                    else:
                        st.info("ℹ️ Não foram encontradas aulas repetidas para remover.")
        
        with col2:
            if st.button("🚨 Corrigir Superposições (Horários REAIS)", use_container_width=True):
                with st.spinner("Verificando superposições..."):
                    superposicoes = verificar_professor_superposto(st.session_state.aulas)
                    
                    if superposicoes:
                        st.error(f"❌ Encontradas {len(superposicoes)} superposições de professor!")
                        
                        # Mostrar exemplos com horários REAIS
                        with st.expander("📋 Ver Superposições (Horários REAIS)", expanded=True):
                            for i, sup in enumerate(superposicoes[:3]):
                                st.write(f"**Professor {sup['professor']}**: {len(sup['aulas'])} aulas às {sup['dia']}, {sup['horario_real']}")
                                st.write(f"**Segmentos**: {', '.join(sup['segmentos'])}")
                                for aula in sup['aulas']:
                                    st.write(f"  - Turma: {obter_turma_aula(aula)}, Disciplina: {obter_disciplina_aula(aula)}")
                        
                        if st.button("✅ Corrigir Agora", type="primary"):
                            with st.spinner("Corrigindo superposições..."):
                                aulas_corrigidas = corrigir_superposicoes_professor(st.session_state.aulas, superposicoes)
                                st.session_state.aulas = aulas_corrigidas
                                st.success("✅ Superposições corrigidas!")
                                st.rerun()
                    else:
                        st.success("✅ Nenhuma superposição encontrada!")
        
        with col3:
            if st.button("📊 Verificar Conflitos (Horários REAIS)", use_container_width=True):
                # Executar diagnóstico completo
                diagnostico = diagnosticar_grade(
                    st.session_state.turmas,
                    st.session_state.professores,
                    st.session_state.disciplinas,
                    st.session_state.aulas
                )
                
                # Mostrar resultados
                st.subheader("📋 Resultado da Verificação (Horários REAIS)")
                
                st.metric("Status", diagnostico['status'])
                st.metric("Completude", f"{diagnostico['completude']}%")
                
                if diagnostico['problemas']:
                    st.error("❌ Problemas encontrados:")
                    for problema in diagnostico['problemas'][:5]:
                        st.write(f"- {problema}")
                else:
                    st.success("✅ Nenhum problema encontrado!")
    
    # Botão para otimização manual
    st.subheader("⚙️ Otimização Avançada")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Rebalancear Professores", use_container_width=True):
            st.info("""
            **Sugestões de rebalanceamento:**
            
            1. Verifique professores com muitas disciplinas
            2. Distribua disciplinas entre professores do mesmo grupo
            3. Considere professores 'AMBOS' para cobrir falta
            4. Respeite limites: EF II (25h) | EM (35h)
            5. **EVITE** que professores tenham aulas no mesmo horário REAL
            """)
    
    with col2:
        if st.button("📅 Analisar Grade Completa", use_container_width=True):
            if st.session_state.get('aulas'):
                # Executar todas as verificações
                conflitos = verificar_conflitos_horarios(st.session_state.aulas)
                superposicoes = verificar_professor_superposto(st.session_state.aulas)
                limites_excedidos = verificar_limites_professores(st.session_state.aulas)
                
                st.subheader("📊 Resultado da Análise (Horários REAIS)")
                
                problemas_totais = len(conflitos) + len(superposicoes) + len(limites_excedidos)
                
                if problemas_totais == 0:
                    st.success("✅ Grade perfeita! Nenhum problema encontrado.")
                else:
                    st.error(f"❌ Encontrados {problemas_totais} problemas:")
                    
                    if superposicoes:
                        st.write(f"🚨 **SUPERPOSIÇÕES CRÍTICAS**: {len(superposicoes)}")
                        for sup in superposicoes[:2]:
                            st.write(f"  - Professor {sup['professor']}: {len(sup['aulas'])} aulas às {sup['dia']}, {sup['horario_real']}")
                            st.write(f"    Segmentos: {', '.join(sup['segmentos'])}")
                    
                    if conflitos:
                        st.write(f"⚠️ **Conflitos de horário REAL**: {len(conflitos)}")
                        for conf in conflitos[:2]:
                            if conf.get('horario_real'):
                                st.write(f"  - Turma {conf['turma']}: {conf['horario_real']} - {', '.join(conf.get('disciplinas', []))}")
                    
                    if limites_excedidos:
                        st.write(f"❌ **Limites excedidos**: {len(limites_excedidos)}")
                        for problema in limites_excedidos[:2]:
                            st.write(f"  - {problema['professor']}: {problema['horas_atual']}h > {problema['limite']}h")
                    
                    # Botão para corrigir tudo
                    if st.button("🔧 Corrigir Todos os Problemas", type="primary"):
                        aulas_corrigidas = st.session_state.aulas.copy()
                        
                        # 1. Corrigir superposições (mais crítico)
                        if superposicoes:
                            aulas_corrigidas = corrigir_superposicoes_professor(aulas_corrigidas, superposicoes)
                        
                        # 2. Corrigir conflitos
                        if conflitos:
                            aulas_corrigidas = corrigir_conflitos_automaticamente(aulas_corrigidas, conflitos)
                        
                        # 3. Para limites, usar completador
                        if limites_excedidos:
                            completador = CompletadorDeGradeAvancado(
                                st.session_state.turmas,
                                st.session_state.professores,
                                st.session_state.disciplinas
                            )
                            aulas_corrigidas = completador.completar_grade(aulas_corrigidas)
                        
                        st.session_state.aulas = aulas_corrigidas
                        st.success("✅ Problemas corrigidos! Recarregue a página.")
                        st.rerun()
            else:
                st.info("ℹ️ Gere uma grade primeiro para usar esta ferramenta.")
    
    # Grades salvas
    if hasattr(st.session_state, 'grades_salvas') and st.session_state.grades_salvas:
        st.subheader("💾 Grades Salvas")
        
        for nome_grade, dados_grade in st.session_state.grades_salvas.items():
            with st.expander(f"📁 {nome_grade} ({dados_grade['total_aulas']} aulas)"):
                st.write(f"**Data:** {dados_grade['data']}")
                st.write(f"**Configuração:** {dados_grade['config']}")
                
                if st.button(f"Carregar Grade '{nome_grade}'", key=f"load_{nome_grade}"):
                    st.session_state.aulas = dados_grade['aulas']
                    st.success(f"✅ Grade '{nome_grade}' carregada!")
                    st.rerun()

# ============================================
# SIDEBAR (ATUALIZADO COM INFORMAÇÕES CLARAS)
# ============================================
st.sidebar.title("⚙️ Configurações")
if st.sidebar.button("🔄 Resetar Banco de Dados"):
    try:
        database.resetar_banco()
        st.sidebar.success("✅ Banco resetado! Recarregue a página.")
    except Exception as e:
        st.sidebar.error(f"❌ Erro ao resetar: {str(e)}")

st.sidebar.write("### Status do Sistema:")
st.sidebar.write(f"**Turmas:** {len(st.session_state.turmas)}")
st.sidebar.write(f"**Professores:** {len(st.session_state.professores)}")
st.sidebar.write(f"**Disciplinas:** {len(st.session_state.disciplinas)}")
st.sidebar.write(f"**Salas:** {len(st.session_state.salas)}")
st.sidebar.write(f"**Aulas na Grade:** {len(st.session_state.get('aulas', []))}")

st.sidebar.write("### 💡 IMPORTANTE - Horários DIFERENTES por Segmento:")
st.sidebar.write("**EF II:** 07:50-12:20 (5 períodos)")
st.sidebar.write("**EM:** 07:00-13:10 (7 períodos)")
st.sidebar.write(f"**Limites:** EF II: {LIMITE_HORAS_EFII}h | EM: {LIMITE_HORAS_EM}h")

st.sidebar.write("### 🕒 Horários REAIS por Segmento:")
st.sidebar.write("**EM (7 períodos):**")
st.sidebar.write("1º: 07:00-07:50")
st.sidebar.write("2º: 07:50-08:40")
st.sidebar.write("3º: 08:40-09:30")
st.sidebar.write("🕛 INTERVALO: 09:30-09:50")
st.sidebar.write("4º: 09:50-10:40")
st.sidebar.write("5º: 10:40-11:30")
st.sidebar.write("6º: 11:30-12:20")
st.sidebar.write("7º: 12:20-13:10")

st.sidebar.write("**EF II (5 períodos):**")
st.sidebar.write("1º: 07:50-08:40")
st.sidebar.write("2º: 08:40-09:30")
st.sidebar.write("🕛 INTERVALO: 09:30-09:50")
st.sidebar.write("3º: 09:50-10:40")
st.sidebar.write("4º: 10:40-11:30")
st.sidebar.write("5º: 11:30-12:20")

st.sidebar.write("### ⚠️ OBSERVAÇÃO CRÍTICA:")
st.sidebar.write("**08:40-09:30 =**")
st.sidebar.write("- 2º período para EF II")
st.sidebar.write("- 3º período para EM")
st.sidebar.write("**São o MESMO horário REAL!**")