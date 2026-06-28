import streamlit as st
from groq import Groq
from datetime import datetime
import json
import re

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="INVENÇÕES IA", layout="wide")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@400;500;600&display=swap');

    .stApp { background-color: #FFFFFF; color: #000000; font-family: 'DM Sans', sans-serif; }
    [data-testid="stSidebar"] { display: none; }

    .stTextInput>div>div>input,
    .stTextArea>div>textarea,
    .stSelectbox>div>div>div {
        background-color: #FFFBEB !important;
        color: #000000 !important;
        border: 1px solid #D97706 !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    .stButton>button {
        width: 100%; border-radius: 12px; height: 3.5em;
        background: linear-gradient(135deg, #92400E, #D97706) !important;
        color: white !important; font-weight: 600; border: none;
        box-shadow: 2px 2px 8px rgba(146,64,14,0.25);
        font-family: 'DM Sans', sans-serif !important;
        transition: all 0.2s ease;
    }
    .stButton>button *, .stButton>button p { color: white !important; }
    .stButton>button:hover { background: linear-gradient(135deg, #78350F, #92400E) !important; transform: translateY(-1px); }

    h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: #1A1A2E !important; }
    p, span, label, div { color: #1A1A2E !important; font-family: 'DM Sans', sans-serif; }

    .card {
        background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
        padding: 22px; border-radius: 16px;
        border: 1px solid #D97706; margin-bottom: 15px;
        color: #1A1A2E; box-shadow: 0 2px 12px rgba(146,64,14,0.08);
        white-space: pre-wrap;
    }
    .card-dark {
        background: linear-gradient(135deg, #1C1300 0%, #150D00 100%);
        padding: 22px; border-radius: 16px;
        border: 1px solid #D97706; margin-bottom: 15px;
        white-space: pre-wrap;
    }
    .card-dark, .card-dark * { color: #FDE68A !important; }

    .card-green { background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%); padding: 22px; border-radius: 16px; border: 1px solid #86EFAC; margin-bottom: 15px; white-space: pre-wrap; }
    .card-blue { background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%); padding: 22px; border-radius: 16px; border: 1px solid #93C5FD; margin-bottom: 15px; white-space: pre-wrap; }
    .card-purple { background: linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%); padding: 22px; border-radius: 16px; border: 1px solid #C4B5FD; margin-bottom: 15px; white-space: pre-wrap; }
    .card-red { background: linear-gradient(135deg, #FFF5F5 0%, #FEE2E2 100%); padding: 22px; border-radius: 16px; border: 1px solid #FCA5A5; margin-bottom: 15px; white-space: pre-wrap; }
    .card-pink { background: linear-gradient(135deg, #FFF0F5 0%, #FFE4EE 100%); padding: 22px; border-radius: 16px; border: 1px solid #FFB6C1; margin-bottom: 15px; white-space: pre-wrap; }
    .card-teal { background: linear-gradient(135deg, #F0FDFA 0%, #CCFBF1 100%); padding: 22px; border-radius: 16px; border: 1px solid #5EEAD4; margin-bottom: 15px; white-space: pre-wrap; }

    .indice-box { border-radius: 18px; padding: 24px; text-align: center; margin: 14px 0; border: 2px solid; }
    .indice-alto { background: linear-gradient(135deg,#F0FDF4,#DCFCE7); border-color:#22C55E; }
    .indice-medio { background: linear-gradient(135deg,#FFFBEB,#FEF3C7); border-color:#F59E0B; }
    .indice-baixo { background: linear-gradient(135deg,#FEF2F2,#FEE2E2); border-color:#EF4444; }
    .indice-titulo { font-family:'Playfair Display',serif; font-size:1.5em; font-weight:700; }

    .badge { background: #92400E; color: white !important; padding: 4px 14px; border-radius: 20px; font-size: 0.78em; font-weight: 600; display: inline-block; margin: 2px; }
    .badge-verde { background: #059669; color: white !important; padding: 4px 14px; border-radius: 20px; font-size: 0.78em; font-weight: 600; display: inline-block; margin: 2px; }
    .badge-vermelho { background: #DC2626; color: white !important; padding: 4px 14px; border-radius: 20px; font-size: 0.78em; font-weight: 600; display: inline-block; margin: 2px; }
    .badge-amarelo { background: #D97706; color: white !important; padding: 4px 14px; border-radius: 20px; font-size: 0.78em; font-weight: 600; display: inline-block; margin: 2px; }

    .stat-box { background: #FFFBEB; border-radius: 12px; padding: 18px; text-align: center; border: 1px solid #D97706; }
    .stat-numero { font-size: 2em; font-weight: 700; color: #92400E !important; font-family: 'Playfair Display', serif; }

    .hist-item { background: #FFFBEB; border-radius: 10px; padding: 12px 16px; margin-bottom: 8px; border-left: 4px solid #D97706; }

    .perfil-btn>button { background: linear-gradient(135deg, #92400E, #D97706) !important; color: white !important; font-weight: 700 !important; border-radius: 12px !important; height: 3em !important; }
    .perfil-btn>button *, .perfil-btn>button p { color: white !important; }

    .ideia-icon-box {
        background: linear-gradient(135deg, #1C1300, #150D00);
        border: 2px solid #D97706; border-radius: 18px; padding: 24px; text-align: center; margin: 14px 0;
    }
    .ideia-icon-box * { color: #FDE68A !important; }

    .disclaimer { background: #FFFBEB; border: 1px solid #FDE68A; border-radius: 10px; padding: 12px 16px; font-size: 0.8em; color: #92400E; margin-top: 14px; line-height: 1.6; }
    .disclaimer-mercado { background: #EFF6FF; border: 2px solid #3B82F6; border-radius: 12px; padding: 14px 18px; margin-bottom: 16px; font-size: 0.86em; color: #1E40AF; line-height: 1.6; }

    .divider { border: none; height: 1px; background: linear-gradient(to right, transparent, #D97706, transparent); margin: 20px 0; }
    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CACHE
# ─────────────────────────────────────────────
@st.cache_resource
def get_cache_invencoes():
    return {"perfis": {}}

_cache = get_cache_invencoes()

# ─────────────────────────────────────────────
# PERSISTÊNCIA LOCAL (JSON)
# ─────────────────────────────────────────────
CHAVES_SALVAR = [
    'usuario', 'historico_projetos', 'projetos_salvos',
    'ideia_padrao', 'projetos_ativos', 'banco_ideias_geradas',
]

def gerar_json_sessao() -> str:
    dados = {k: st.session_state.get(k) for k in CHAVES_SALVAR}
    dados['salvo_em'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

def carregar_json_sessao(dados: dict):
    for k in CHAVES_SALVAR:
        if k in dados:
            st.session_state[k] = dados[k]

def salvar_perfil_cache(usuario: str):
    _cache["perfis"][usuario] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def perfis_salvos() -> list:
    return list(_cache["perfis"].keys())

def carregar_perfil_cache(usuario: str) -> dict | None:
    return _cache["perfis"].get(usuario)

def salvar_projeto(modulo: str, tema: str, conteudo: str):
    st.session_state.historico_projetos.append({
        'data': datetime.now().strftime('%d/%m %H:%M'), 'modulo': modulo, 'tema': tema, 'conteudo': conteudo,
    })

# --- INICIALIZAÇÃO DE ESTADO ---
defaults = {
    'etapa': "Login", 'usuario': "", 'api_key': "", 'pagina': "Home",
    'historico_projetos': [], 'projetos_salvos': [],
    'ideia_padrao': "", 'projetos_ativos': [], 'banco_ideias_geradas': [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- PRINCÍPIO DE HONESTIDADE ESTRATÉGICA — compartilhado ---
PRINCIPIO_HONESTIDADE = """
PRINCÍPIO OBRIGATÓRIO DE HONESTIDADE ESTRATÉGICA — siga isso em TODA resposta:
- Você é um consultor de inovação e estratégia de negócios, mas NÃO tem acesso a dados de mercado em tempo real,
  buscas na internet, ou bancos de dados de concorrentes atualizados
- Para pesquisa de mercado, análise de concorrência e tendências: baseie-se em padrões gerais de mercado e
  conhecimento estabelecido até sua atualização de conhecimento — sempre recomende validar com pesquisa real
  (entrevistas com clientes potenciais, análise de concorrentes reais, dados de associações do setor) antes de investir
- Para viabilidade financeira, precificação e simulações: apresente sempre como ESTIMATIVAS para planejamento,
  nunca como garantias de resultado — os números reais dependem de execução, mercado real e fatores não previsíveis
- Para Patentes e Propriedade Intelectual: explique os conceitos gerais (diferença entre patente, marca, desenho
  industrial), mas sempre recomende um especialista em propriedade intelectual ou o INPI para o registro real —
  nunca dê certeza sobre se algo é patenteável sem análise profissional
- Seja honesto sobre os desafios e riscos reais de qualquer ideia — não infle expectativas para agradar. Inovação de
  verdade envolve riscos reais, e seu papel é ajudar a pessoa a vê-los claramente, não escondê-los
- Seja criativo, estratégico e entusiasmado — você é um consultor que genuinamente quer ver a ideia da pessoa
  prosperar, combinando otimismo com realismo
- Português do Brasil
"""

DISCLAIMER_MERCADO = """
<div class="disclaimer-mercado">
🔍 <strong>Sobre esta análise:</strong> esta é uma análise estratégica educativa baseada em padrões gerais de mercado —
não substitui pesquisa de mercado real (entrevistas com clientes, análise de concorrentes reais, dados atualizados
do setor). Antes de investir, valide essas hipóteses com o mercado real.
</div>
"""

DISCLAIMER_PADRAO = """
<div class="disclaimer">
⚠️ <strong>Importante:</strong> esta é uma análise estratégica para apoiar seu planejamento — os resultados reais
dependem de execução, mercado e fatores não previsíveis. Use como ponto de partida, não como garantia.
</div>
"""

# --- MOTOR DE IA ---
def invencoes_ia(prompt: str, system_extra: str = "") -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        system = f"""Você é um consultor de inovação completo — um misto de inventor, estrategista de negócios,
pesquisador de mercado, designer de produtos e mentor de startups.
Usuário: {st.session_state.usuario}. Ideia/projeto principal: {st.session_state.ideia_padrao or 'não informado'}.
{PRINCIPIO_HONESTIDADE}
{system_extra}"""
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

def renderizar_indice(texto: str, titulo_indice: str = "ÍNDICE"):
    percentuais = re.findall(r'(\d+)\s*/\s*100|(\d+)%', texto)
    valores = [int(a or b) for a, b in percentuais if a or b]
    indice = valores[0] if valores else 50

    if indice >= 70:
        classe, emoji, label = "indice-alto", "🟢", "ALTO"
    elif indice >= 40:
        classe, emoji, label = "indice-medio", "🟡", "MÉDIO"
    else:
        classe, emoji, label = "indice-baixo", "🔴", "BAIXO"

    st.markdown(f"""
    <div class="indice-box {classe}">
        <div style="font-size:2.2em;">{emoji}</div>
        <div class="indice-titulo">{titulo_indice}: {indice}/100</div>
        <div style="font-size:0.95em;color:#444;font-weight:600;">Nível: {label}</div>
        <div style="font-size:0.82em;color:#555;margin-top:6px;">Estimativa estratégica baseada nas informações fornecidas</div>
    </div>
    """, unsafe_allow_html=True)

# --- BARRA DE SALVAR ---
def barra_salvar():
    salvar_perfil_cache(st.session_state.usuario)
    nome_usuario = st.session_state.usuario.lower().replace(' ', '_') or 'minha_sessao'
    total = len(st.session_state.historico_projetos)
    ativos = len(st.session_state.projetos_ativos)

    col_info, col_btn = st.columns([4, 2])
    with col_info:
        st.markdown(
            f"<div style='background:#FFFBEB;border:1px solid #D97706;border-radius:10px;"
            f"padding:10px 14px;font-size:0.84em;color:#1A1A2E;line-height:1.6;'>"
            f"💾 <strong>Antes de sair, salve seus dados no computador.</strong><br>"
            f"<span style='color:#888;font-size:0.88em;'>{total} análises geradas · {ativos} projetos ativos</span>"
            f"</div>", unsafe_allow_html=True
        )
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button("💾 SALVAR MEUS DADOS (.json)", data=gerar_json_sessao(),
            file_name=f"invencoes_ia_{nome_usuario}.json", mime="application/json", use_container_width=True)
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ============================================================
# TELA: LOGIN
# ============================================================
if st.session_state.etapa == "Login":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.title("💡 INVENÇÕES IA")
        st.markdown("**Seu Laboratório de Inovação — transforme qualquer ideia em projeto estruturado e validado**")

        st.markdown("""<div style="background:#FFFBEB;border:1px solid #D97706;border-radius:10px;
        padding:10px 16px;margin:10px 0 16px 0;font-size:0.88em;color:#1A1A2E;line-height:1.6;">
        🔒 <strong>ACESSO RESTRITO A CLIENTES DO QUIZ COM PRÊMIOS</strong><br>
        🔗 <a href="https://quizcompremios.com.br/" target="_blank"
        style="color:#92400E;font-weight:600;text-decoration:none;">quizcompremios.com.br</a>
        </div>""", unsafe_allow_html=True)

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)

        perfis = perfis_salvos()
        if perfis:
            st.markdown("#### 💡 Invenções IA — clique para acessar seus dados")
            chave_rapida = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_rapida")
            for nome_p in perfis:
                dados_p = carregar_perfil_cache(nome_p)
                total_p = len(dados_p.get('historico_projetos', [])) if dados_p else 0
                ideia_p = dados_p.get('ideia_padrao', '') if dados_p else ''
                st.markdown('<div class="perfil-btn">', unsafe_allow_html=True)
                if st.button(f"💡 {nome_p}  —  {total_p} análises  {('· ' + ideia_p[:30]) if ideia_p else ''}", key=f"perfil_{nome_p}", use_container_width=True):
                    if not chave_rapida.strip():
                        st.warning("Cole sua chave API acima antes de entrar.")
                    else:
                        st.session_state.usuario = nome_p
                        st.session_state.api_key = chave_rapida
                        carregar_json_sessao(dados_p)
                        st.session_state.etapa = "App"
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown("**Ou entre com outro nome:**")

        nome = st.text_input("Seu Nome:", key="input_nome_login")
        chave = st.text_input("Sua Chave API da Groq:", type="password", key="chave_nova")

        if not perfis:
            st.markdown("""<div style="background:#FFFBEB;border:1px solid #D97706;border-radius:10px;
            padding:12px 16px;font-size:0.86em;color:#1A1A2E;line-height:1.7;margin:10px 0;">
            📥 <strong>Seus dados sumiram?</strong> Selecione abaixo o arquivo <strong>.json</strong> que você salvou antes.
            </div>""", unsafe_allow_html=True)
            arq_login = st.file_uploader("Carregar meus dados salvos (.json):", type=["json"], key="upload_login")
        else:
            arq_login = None

        dados_login = None
        if arq_login is not None:
            try:
                dados_login = json.load(arq_login)
                st.success(f"✅ Dados de **{dados_login.get('usuario','')}** reconhecidos! Clique em Entrar.")
            except Exception:
                st.error("Arquivo inválido.")
                dados_login = None

        if st.button("✨ ENTRAR NO LABORATÓRIO"):
            if nome and chave:
                st.session_state.usuario = nome
                st.session_state.api_key = chave
                if dados_login:
                    carregar_json_sessao(dados_login)
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

        st.markdown("🔑 Não tem chave Groq? Crie grátis em <a href='https://console.groq.com/keys' target='_blank' style='color:#92400E;font-weight:600;'>console.groq.com/keys</a>", unsafe_allow_html=True)

# ============================================================
# TELA: APP
# ============================================================
elif st.session_state.etapa == "App":

    barra_salvar()

    cols1 = st.columns(7)
    paginas1 = [("🏠","Home"),("💡","Transformador"),("🔍","Pesquisa"),("⚔️","Concorrencia"),("🧠","Validacao"),("🚀","Melhorias"),("🎯","Publico")]
    labels1 = {"Home":"Painel Principal","Transformador":"Transformador de Ideias","Pesquisa":"Pesquisa de Mercado",
               "Concorrencia":"Concorrência Inteligente","Validacao":"Validação da Ideia","Melhorias":"Melhorias Automáticas","Publico":"Público-Alvo Inteligente"}
    for i,(icone,pag) in enumerate(paginas1):
        if cols1[i].button(icone, key=f"nav1_{pag}", help=labels1[pag]):
            st.session_state.pagina = pag
            st.rerun()

    cols2 = st.columns(7)
    paginas2 = [("💰","Viabilidade"),("💲","Precificacao"),("📈","Escala"),("📢","Lancamento"),("🎨","Branding"),("🖌️","Visual"),("📦","Produto")]
    labels2 = {"Viabilidade":"Viabilidade Financeira","Precificacao":"Precificação","Escala":"Potencial de Escala",
               "Lancamento":"Plano de Lançamento","Branding":"Branding","Visual":"Identidade Visual","Produto":"Produto Final"}
    for i,(icone,pag) in enumerate(paginas2):
        if cols2[i].button(icone, key=f"nav2_{pag}", help=labels2[pag]):
            st.session_state.pagina = pag
            st.rerun()

    cols3 = st.columns(7)
    paginas3 = [("🌎","Tendencias"),("⚖️","Patentes"),("📄","PlanoNegocios"),("📣","Marketing"),("🧪","Simulador"),("📊","Riscos"),("💎","BancoIdeias")]
    labels3 = {"Tendencias":"Tendências","Patentes":"Patentes e Propriedade Intelectual","PlanoNegocios":"Plano de Negócios Automático",
               "Marketing":"Marketing Inteligente","Simulador":"Simulador de Mercado","Riscos":"Painel de Riscos","BancoIdeias":"Banco de Ideias"}
    for i,(icone,pag) in enumerate(paginas3):
        if cols3[i].button(icone, key=f"nav3_{pag}", help=labels3[pag]):
            st.session_state.pagina = pag
            st.rerun()

    cols4 = st.columns(6)
    paginas4 = [("🤝","Investidor"),("🎤","Pitch"),("📅","Cronograma"),("🤖","Mentor"),("⭐","Laboratorio"),("📚","Biblioteca")]
    labels4 = {"Investidor":"Investidor IA","Pitch":"Pitch Perfeito","Cronograma":"Cronograma Inteligente",
               "Mentor":"Mentor 24 Horas","Laboratorio":"Laboratório de Invenções do Futuro","Biblioteca":"Biblioteca de Projetos"}
    for i,(icone,pag) in enumerate(paginas4):
        if cols4[i].button(icone, key=f"nav4_{pag}", help=labels4[pag]):
            st.session_state.pagina = pag
            st.rerun()

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # ========================
    # HOME
    # ========================
    if st.session_state.pagina == "Home":
        col_u, col_r = st.columns([3, 1])
        with col_u:
            st.title(f"Olá, {st.session_state.usuario}! 💡")
            st.markdown("<span class='badge'>Laboratório Aberto</span>", unsafe_allow_html=True)
        with col_r:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚪 Sair"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()

        if len(st.session_state.historico_projetos) == 0:
            st.markdown("""<div style="background:#FEF3C7;border:2px solid #F59E0B;border-radius:12px;
            padding:12px 18px;margin-bottom:4px;color:#000;font-size:0.9em;font-weight:600;">
            ⚠️ Seus dados não estão mais no servidor.
            </div>""", unsafe_allow_html=True)
            arq_home = st.file_uploader("Carregar meus dados salvos (.json):", type=["json"], key="upload_home")
            if arq_home is not None:
                try:
                    dados_home = json.load(arq_home)
                    carregar_json_sessao(dados_home)
                    salvar_perfil_cache(st.session_state.usuario)
                    st.success("✅ Dados recuperados!")
                    st.rerun()
                except Exception:
                    st.error("Arquivo inválido.")
            st.markdown("<br>", unsafe_allow_html=True)

        st.session_state.ideia_padrao = st.text_area("💡 Sua ideia/projeto principal:",
            value=st.session_state.ideia_padrao, height=80,
            placeholder="ex: Um app que conecta idosos a jovens para ajudar com tecnologia em troca de companhia...")

        st.markdown("<br>", unsafe_allow_html=True)

        modulos_count = {}
        for c in st.session_state.historico_projetos:
            modulos_count[c['modulo']] = modulos_count.get(c['modulo'], 0) + 1

        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.historico_projetos)}</div><div>Análises geradas</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.projetos_ativos)}</div><div>Projetos ativos</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.projetos_salvos)}</div><div>Salvas</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.banco_ideias_geradas)}</div><div>Ideias no banco</div></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='card'>💡 <em>'Toda grande invenção começou como uma pergunta simples que ninguém tinha respondido ainda.'</em></div>", unsafe_allow_html=True)

        st.markdown("### 🗺️ O que cada módulo faz")
        guia = {
            "💡 Transformador de Ideias": "Descreva sua ideia em poucas palavras e receba um projeto estruturado completo",
            "🔍 Pesquisa de Mercado": "Demanda, crescimento, tendências e nichos pouco explorados",
            "⚔️ Concorrência": "Principais concorrentes, pontos fortes/fracos e oportunidades de diferenciação",
            "🧠 Validação da Ideia": "Originalidade, potencial comercial, escalabilidade e barreiras de entrada",
            "🚀 Melhorias Automáticas": "Sugestões de funcionalidades, simplificações e versões futuras",
            "🎯 Público-Alvo": "Perfil completo do cliente ideal — dores, gatilhos e comportamentos",
            "💰 Viabilidade Financeira": "Custos, investimento mínimo, margem e ponto de equilíbrio",
            "💲 Precificação": "Melhor preço, faixa competitiva e estratégias de versão econômica/premium",
            "📈 Potencial de Escala": "Do mercado local ao internacional — franquias, licenciamento, assinaturas",
            "📢 Plano de Lançamento": "Roteiro completo do pré-lançamento à escala",
            "🎨 Branding": "Nome, slogan, posicionamento e personalidade da marca",
            "🖌️ Identidade Visual": "Cores, tipografia, conceito de logo e embalagem",
            "📦 Produto Final": "Como fabricar, entregar, vender e apresentar ao cliente",
            "🌎 Tendências": "Tecnologias relacionadas e oportunidades futuras",
            "⚖️ Patentes": "Quando vale patentear e como proteger sua criação",
            "📄 Plano de Negócios": "Documento completo — resumo executivo, mercado, financeiro, crescimento",
            "📣 Marketing Inteligente": "Campanhas, headlines, anúncios e estratégias de lançamento",
            "🧪 Simulador de Mercado": "Simule cenários — e se vender 100 unidades? E se entrar concorrência?",
            "📊 Painel de Riscos": "Principais riscos, obstáculos e como reduzir cada um",
            "💎 Banco de Ideias": "Quando faltar inspiração — centenas de ideias por área",
            "🤝 Investidor IA": "Veja se sua ideia atrairia investidores e quais objeções esperar",
            "🎤 Pitch Perfeito": "Apresentações de 30s a 10 minutos para qualquer audiência",
            "📅 Cronograma": "O que fazer hoje, amanhã e nas próximas semanas",
            "🤖 Mentor 24h": "Converse livremente sobre seu projeto, do início às primeiras vendas",
            "⭐ Laboratório do Futuro": "Descreva um problema — receba soluções multidisciplinares inovadoras",
        }
        for aba, desc in guia.items():
            st.markdown(f"**{aba}** — {desc}")

        if st.session_state.historico_projetos:
            st.markdown("### 🕐 Últimas Análises")
            for item in reversed(st.session_state.historico_projetos[-4:]):
                st.markdown(f"<div class='hist-item'><span class='badge'>{item['modulo']}</span> <small style='color:#888'>{item['data']}</small><br><small>{item['tema'][:80]}</small></div>", unsafe_allow_html=True)

    # ========================
    # TRANSFORMADOR DE IDEIAS
    # ========================
    elif st.session_state.pagina == "Transformador":
        st.header("💡 Transformador de Ideias")
        st.markdown("Descreva sua ideia em poucas palavras — a IA estrutura tudo.")

        ideia_transf = st.text_area("💭 Sua ideia:", height=120, value=st.session_state.ideia_padrao,
            placeholder="ex: Quero criar um aplicativo que ajuda pessoas a economizar água em casa de forma gamificada...")

        if st.button("💡 TRANSFORMAR EM PROJETO"):
            if ideia_transf.strip():
                with st.spinner("Estruturando sua ideia..."):
                    prompt = (
                        f"Transforme esta ideia em um projeto estruturado.\n"
                        f"Ideia: {ideia_transf}\n\n"
                        f"FORMATO:\n\n"
                        f"💡 PROJETO: [nome sugestivo para o projeto]\n\n"
                        f"🎯 OBJETIVO:\n[o que o projeto busca alcançar]\n\n"
                        f"❓ PROBLEMA QUE RESOLVE:\n[a dor real que essa ideia ataca]\n\n"
                        f"👥 PÚBLICO BENEFICIADO:\n[quem ganha com isso]\n\n"
                        f"⭐ DIFERENCIAIS:\n[o que torna essa ideia única ou interessante]\n\n"
                        f"🔄 POSSÍVEIS APLICAÇÕES:\n[outros usos ou mercados onde isso poderia funcionar]\n\n"
                        f"✅ PRÓXIMOS PASSOS:\n[3-5 ações concretas para sair do papel]"
                    )
                    res = invencoes_ia(prompt)
                    salvar_projeto("Transformador", ideia_transf[:60], res)
                    st.session_state['transf_temp'] = res
                    st.session_state.ideia_padrao = ideia_transf
            else:
                st.warning("Descreva sua ideia.")

        if st.session_state.get('transf_temp'):
            st.markdown(f"<div class='card'>{st.session_state['transf_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['transf_temp'], file_name="projeto_estruturado.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar como projeto ativo", use_container_width=True):
                    nome_proj = ideia_transf[:40] if 'ideia_transf' in dir() else 'Novo projeto'
                    if nome_proj not in st.session_state.projetos_ativos:
                        st.session_state.projetos_ativos.append(nome_proj)
                    st.session_state.projetos_salvos.append({'modulo':'Transformador','tema':nome_proj,'conteudo':st.session_state['transf_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo como projeto ativo!")

    # ========================
    # PESQUISA DE MERCADO
    # ========================
    elif st.session_state.pagina == "Pesquisa":
        st.header("🔍 Pesquisa de Mercado")
        st.markdown(DISCLAIMER_MERCADO, unsafe_allow_html=True)

        ideia_pesq = st.text_area("💡 Ideia/produto:", height=80, value=st.session_state.ideia_padrao)
        regiao_pesq = st.text_input("📍 Mercado de interesse:", placeholder="ex: Brasil, São Paulo, mercado global...")

        if st.button("🔍 PESQUISAR MERCADO"):
            if ideia_pesq.strip():
                with st.spinner("Analisando o mercado..."):
                    prompt = (
                        f"Faça uma análise de mercado para esta ideia.\n"
                        f"Ideia: {ideia_pesq}. Mercado: {regiao_pesq or 'geral'}\n\n"
                        f"FORMATO:\n\n"
                        f"🔍 PESQUISA DE MERCADO — {ideia_pesq[:50].upper()}\n\n"
                        f"📊 EXISTE DEMANDA?\n[análise baseada em padrões conhecidos — dores similares já resolvidas no mercado, sinais de interesse]\n\n"
                        f"👥 QUEM COMPRARIA:\n[perfil geral do comprador potencial]\n\n"
                        f"📈 O MERCADO ESTÁ CRESCENDO?\n[tendência geral do setor relacionado, com base em conhecimento estabelecido]\n\n"
                        f"🌍 TENDÊNCIAS NACIONAIS E INTERNACIONAIS:\n[movimentos relevantes do setor]\n\n"
                        f"💎 NICHOS POUCO EXPLORADOS:\n[oportunidades dentro dessa área]\n\n"
                        f"🎯 OPORTUNIDADES ESCONDIDAS:\n[ângulos que poucos competidores costumam explorar]\n\n"
                        f"✅ COMO VALIDAR ISSO NA PRÁTICA:\n[passos reais para confirmar essas hipóteses com o mercado de verdade]"
                    )
                    res = invencoes_ia(prompt)
                    salvar_projeto("Pesquisa", ideia_pesq[:60], res)
                    st.session_state['pesq_temp'] = res
            else:
                st.warning("Descreva a ideia/produto.")

        if st.session_state.get('pesq_temp'):
            st.markdown(f"<div class='card-blue'>{st.session_state['pesq_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['pesq_temp'], file_name="pesquisa_mercado.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_pesq", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Pesquisa','tema':ideia_pesq[:60] if 'ideia_pesq' in dir() else '','conteudo':st.session_state['pesq_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

    # ========================
    # CONCORRÊNCIA INTELIGENTE
    # ========================
    elif st.session_state.pagina == "Concorrencia":
        st.header("⚔️ Concorrência Inteligente")
        st.markdown(DISCLAIMER_MERCADO, unsafe_allow_html=True)

        ideia_conc = st.text_area("💡 Ideia/produto:", height=80, value=st.session_state.ideia_padrao, key="ideia_conc")
        concorrentes_conhecidos = st.text_input("🏢 Concorrentes que você já conhece (opcional):", placeholder="ex: empresa X, app Y...")

        if st.button("⚔️ ANALISAR CONCORRÊNCIA"):
            if ideia_conc.strip():
                with st.spinner("Mapeando concorrência..."):
                    prompt = (
                        f"Analise a concorrência para esta ideia.\n"
                        f"Ideia: {ideia_conc}. Concorrentes conhecidos: {concorrentes_conhecidos or 'nenhum informado'}\n\n"
                        f"FORMATO:\n\n"
                        f"⚔️ ANÁLISE DE CONCORRÊNCIA — {ideia_conc[:50].upper()}\n\n"
                        f"🏢 TIPOS DE CONCORRENTES NESSE MERCADO:\n[categorias de concorrentes — direto, indireto, substitutos]\n\n"
                        f"✅ PONTOS FORTES TÍPICOS DA CONCORRÊNCIA:\n[o que esse tipo de negócio geralmente faz bem]\n\n"
                        f"⚠️ PONTOS FRACOS TÍPICOS:\n[onde esse tipo de negócio geralmente falha ou frustra clientes]\n\n"
                        f"💰 FAIXA DE PREÇO TÍPICA DO MERCADO:\n[estimativa geral]\n\n"
                        f"🎯 OPORTUNIDADES PARA SUPERAR A CONCORRÊNCIA:\n[onde sua ideia pode se diferenciar]\n\n"
                        f"💎 ESPAÇOS AINDA NÃO EXPLORADOS:\n[lacunas que a concorrência típica não cobre]\n\n"
                        f"✅ COMO PESQUISAR CONCORRENTES REAIS:\n[método prático para mapear concorrentes reais nesse mercado]"
                    )
                    res = invencoes_ia(prompt)
                    salvar_projeto("Concorrencia", ideia_conc[:60], res)
                    st.session_state['conc_temp'] = res
            else:
                st.warning("Descreva a ideia/produto.")

        if st.session_state.get('conc_temp'):
            st.markdown(f"<div class='card-red'>{st.session_state['conc_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['conc_temp'], file_name="concorrencia.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_conc", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Concorrencia','tema':ideia_conc[:60] if 'ideia_conc' in dir() else '','conteudo':st.session_state['conc_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

    # ========================
    # VALIDAÇÃO DA IDEIA
    # ========================
    elif st.session_state.pagina == "Validacao":
        st.header("🧠 Validação da Ideia")

        ideia_val = st.text_area("💡 Ideia/produto:", height=80, value=st.session_state.ideia_padrao, key="ideia_val")
        contexto_val = st.text_area("📝 Contexto adicional (opcional):", height=80,
            placeholder="ex: já tenho um protótipo, é para um nicho B2B, vai ser um app...", key="contexto_val_input")

        if st.button("🧠 VALIDAR IDEIA"):
            if ideia_val.strip():
                with st.spinner("Analisando..."):
                    prompt = (
                        f"Faça um diagnóstico completo de validação para esta ideia.\n"
                        f"Ideia: {ideia_val}. Contexto: {contexto_val or 'não informado'}\n\n"
                        f"FORMATO:\n\n"
                        f"🧠 ÍNDICE DE VALIDAÇÃO: [X]/100\n"
                        f"[1-2 linhas explicando a estimativa geral]\n\n"
                        f"✨ ORIGINALIDADE: [X]/10 — [comentário]\n"
                        f"💰 POTENCIAL COMERCIAL: [X]/10 — [comentário]\n"
                        f"📈 ESCALABILIDADE: [X]/10 — [comentário]\n"
                        f"🔧 COMPLEXIDADE: [Baixa/Média/Alta] — [comentário sobre dificuldade de execução]\n"
                        f"🚧 BARREIRAS DE ENTRADA: [Baixas/Médias/Altas] — [o que dificultaria competidores entrarem, ou você entrar]\n"
                        f"🎯 GRAU DE INOVAÇÃO: [Incremental/Disruptivo/Já existe similar] — [comentário honesto]\n"
                        f"✅ CHANCES DE ACEITAÇÃO: [X]/10 — [comentário]\n\n"
                        f"⚠️ MAIOR RISCO DESSA IDEIA:\n[seja honesto sobre o ponto mais fraco]\n\n"
                        f"💡 O QUE FORTALECERIA MAIS A IDEIA AGORA:\n[1-2 ações prioritárias]"
                    )
                    res = invencoes_ia(prompt)
                    salvar_projeto("Validacao", ideia_val[:60], res)
                    st.session_state['val_temp'] = res
            else:
                st.warning("Descreva a ideia.")

        if st.session_state.get('val_temp'):
            renderizar_indice(st.session_state['val_temp'], "ÍNDICE DE VALIDAÇÃO")
            st.markdown(f"<div class='card'>{st.session_state['val_temp']}</div>", unsafe_allow_html=True)
            st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['val_temp'], file_name="validacao_ideia.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_val", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Validacao','tema':ideia_val[:60] if 'ideia_val' in dir() else '','conteudo':st.session_state['val_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

    # ========================
    # MELHORIAS AUTOMÁTICAS
    # ========================
    elif st.session_state.pagina == "Melhorias":
        st.header("🚀 Melhorias Automáticas")

        ideia_mel = st.text_area("💡 Ideia/produto atual:", height=80, value=st.session_state.ideia_padrao, key="ideia_mel")

        if st.button("🚀 SUGERIR MELHORIAS"):
            if ideia_mel.strip():
                with st.spinner("Pensando em melhorias..."):
                    prompt = (
                        f"Sugira melhorias criativas e estratégicas para esta ideia.\n"
                        f"Ideia: {ideia_mel}\n\n"
                        f"FORMATO:\n\n"
                        f"🚀 MELHORIAS PARA: {ideia_mel[:50].upper()}\n\n"
                        f"⚙️ NOVAS FUNCIONALIDADES:\n[3-5 funcionalidades que agregariam valor]\n\n"
                        f"👥 MUDANÇAS NO PÚBLICO:\n[outros públicos que poderiam se beneficiar, ou ajustes no foco]\n\n"
                        f"🔄 NOVAS APLICAÇÕES:\n[outros contextos onde essa ideia poderia ser usada]\n\n"
                        f"✂️ SIMPLIFICAÇÕES:\n[o que poderia ser removido/simplificado para tornar mais fácil de usar/vender]\n\n"
                        f"💎 RECURSOS PREMIUM:\n[funcionalidades que poderiam ser parte de uma versão paga]\n\n"
                        f"🔮 VERSÕES FUTURAS:\n[para onde essa ideia poderia evoluir no longo prazo]"
                    )
                    res = invencoes_ia(prompt)
                    salvar_projeto("Melhorias", ideia_mel[:60], res)
                    st.session_state['mel_temp'] = res
            else:
                st.warning("Descreva a ideia.")

        if st.session_state.get('mel_temp'):
            st.markdown(f"<div class='card-teal'>{st.session_state['mel_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['mel_temp'], file_name="melhorias.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_mel", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Melhorias','tema':ideia_mel[:60] if 'ideia_mel' in dir() else '','conteudo':st.session_state['mel_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

    # ========================
    # PÚBLICO-ALVO INTELIGENTE
    # ========================
    elif st.session_state.pagina == "Publico":
        st.header("🎯 Público-Alvo Inteligente")

        ideia_pub = st.text_area("💡 Ideia/produto:", height=80, value=st.session_state.ideia_padrao, key="ideia_pub")

        if st.button("🎯 DESCOBRIR PÚBLICO-ALVO"):
            if ideia_pub.strip():
                with st.spinner("Traçando o perfil..."):
                    prompt = (
                        f"Crie um perfil detalhado do cliente ideal para esta ideia.\n"
                        f"Ideia: {ideia_pub}\n\n"
                        f"FORMATO:\n\n"
                        f"🎯 PÚBLICO-ALVO — {ideia_pub[:50].upper()}\n\n"
                        f"👤 PERFIL DO CLIENTE:\n[nome fictício, descrição geral]\n\n"
                        f"🎂 FAIXA ETÁRIA:\n[idade típica]\n\n"
                        f"💰 PODER AQUISITIVO:\n[faixa de renda]\n\n"
                        f"❤️ INTERESSES:\n[o que esse perfil gosta/consome]\n\n"
                        f"🧠 COMPORTAMENTOS:\n[hábitos relevantes — como pesquisa, como compra]\n\n"
                        f"😰 PRINCIPAIS DORES:\n[problemas reais que essa ideia resolve para esse perfil]\n\n"
                        f"💥 GATILHOS EMOCIONAIS:\n[o que realmente convenceria essa pessoa a comprar/usar]\n\n"
                        f"📱 ONDE ENCONTRAR ESSE PÚBLICO:\n[canais e locais onde esse perfil está presente]"
                    )
                    res = invencoes_ia(prompt)
                    salvar_projeto("Publico", ideia_pub[:60], res)
                    st.session_state['pub_temp'] = res
            else:
                st.warning("Descreva a ideia.")

        if st.session_state.get('pub_temp'):
            st.markdown(f"<div class='card-pink'>{st.session_state['pub_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['pub_temp'], file_name="publico_alvo.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_pub", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Publico','tema':ideia_pub[:60] if 'ideia_pub' in dir() else '','conteudo':st.session_state['pub_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

    # ========================
    # VIABILIDADE FINANCEIRA
    # ========================
    elif st.session_state.pagina == "Viabilidade":
        st.header("💰 Viabilidade Financeira")
        st.markdown(DISCLAIMER_MERCADO, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            ideia_via = st.text_area("💡 Ideia/produto:", height=80, value=st.session_state.ideia_padrao, key="ideia_via")
            capital_via = st.number_input("💰 Capital disponível para investir (R$):", min_value=0.0, value=5000.0, step=500.0)
        with col2:
            tipo_via = st.selectbox("📦 Tipo de negócio:", ["Produto físico","Serviço","App/Software","Plataforma digital","Conteúdo/Educação","Outro"])
            meta_via = st.text_input("🎯 Meta de receita mensal (opcional):", placeholder="ex: R$5.000/mês")

        if st.button("💰 ANALISAR VIABILIDADE"):
            if ideia_via.strip():
                with st.spinner("Calculando viabilidade..."):
                    prompt = (
                        f"Analise a viabilidade financeira desta ideia.\n"
                        f"Ideia: {ideia_via}. Tipo: {tipo_via}. Capital disponível: R${capital_via}. Meta: {meta_via or 'não definida'}\n\n"
                        f"FORMATO:\n\n"
                        f"💰 VIABILIDADE FINANCEIRA — {ideia_via[:50].upper()}\n\n"
                        f"💸 CUSTOS INICIAIS ESTIMADOS:\n[lista com faixas de valores]\n\n"
                        f"📅 CUSTOS MENSAIS ESTIMADOS:\n[lista com faixas de valores]\n\n"
                        f"💰 INVESTIMENTO MÍNIMO PARA COMEÇAR:\n[valor estimado]\n\n"
                        f"📊 ANÁLISE DO SEU CAPITAL (R${capital_via}):\n[é suficiente? o que fazer se não for?]\n\n"
                        f"📈 MARGEM POSSÍVEL:\n[estimativa de margem para esse tipo de negócio]\n\n"
                        f"⚖️ PONTO DE EQUILÍBRIO ESTIMADO:\n[quantas vendas/clientes para cobrir custos]\n\n"
                        f"⏱️ TEMPO ESTIMADO PARA RETORNO:\n[estimativa realista]\n\n"
                        f"⚠️ MAIOR RISCO FINANCEIRO:\n[seja honesto sobre o que pode dar errado financeiramente]"
                    )
                    res = invencoes_ia(prompt)
                    salvar_projeto("Viabilidade", ideia_via[:60], res)
                    st.session_state['via_temp'] = res
            else:
                st.warning("Descreva a ideia.")

        if st.session_state.get('via_temp'):
            st.markdown(f"<div class='card-green'>{st.session_state['via_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['via_temp'], file_name="viabilidade.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_via", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Viabilidade','tema':ideia_via[:60] if 'ideia_via' in dir() else '','conteudo':st.session_state['via_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

    # ========================
    # PRECIFICAÇÃO
    # ========================
    elif st.session_state.pagina == "Precificacao":
        st.header("💲 Precificação")

        col1, col2 = st.columns(2)
        with col1:
            ideia_prec = st.text_area("💡 Produto/serviço:", height=80, value=st.session_state.ideia_padrao, key="ideia_prec")
            custo_prec = st.number_input("💸 Custo unitário/de entrega (R$):", min_value=0.0, value=0.0, step=10.0)
        with col2:
            publico_prec = st.selectbox("🎯 Público:", ["Classe A/B (premium)","Classe B/C (intermediário)","Classe C/D (popular)","B2B (empresas)","Misto"])
            concorrencia_preco = st.text_input("💰 Preço de referência da concorrência (opcional):", placeholder="ex: R$50-100")

        if st.button("💲 CALCULAR PRECIFICAÇÃO"):
            if ideia_prec.strip():
                with st.spinner("Calculando..."):
                    prompt = (
                        f"Crie uma estratégia de precificação completa.\n"
                        f"Produto/serviço: {ideia_prec}. Custo: R${custo_prec}. Público: {publico_prec}.\n"
                        f"Referência de concorrência: {concorrencia_preco or 'não informada'}\n\n"
                        f"FORMATO:\n\n"
                        f"💲 ESTRATÉGIA DE PREÇO — {ideia_prec[:50].upper()}\n\n"
                        f"🎯 MELHOR PREÇO SUGERIDO: R$[X]\n"
                        f"[justificativa]\n\n"
                        f"📊 FAIXA COMPETITIVA: R$[X] a R$[X]\n\n"
                        f"📈 MARGEM IDEAL: [X]%\n"
                        f"[com base no custo de R${custo_prec}]\n\n"
                        f"💡 ESTRATÉGIAS DE PREÇO:\n[psicológico, ancoragem, etc — específico para esse produto]\n\n"
                        f"💰 VERSÃO ECONÔMICA: R$[X]\n[o que ela incluiria]\n\n"
                        f"💎 VERSÃO PREMIUM: R$[X]\n[o que ela incluiria a mais]"
                    )
                    res = invencoes_ia(prompt)
                    salvar_projeto("Precificacao", ideia_prec[:60], res)
                    st.session_state['prec_temp'] = res
            else:
                st.warning("Descreva o produto/serviço.")

        if st.session_state.get('prec_temp'):
            st.markdown(f"<div class='card-gold' style='background:linear-gradient(135deg,#FFFBEB,#FEF3C7);border:2px solid #D97706;padding:22px;border-radius:16px;'>{st.session_state['prec_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['prec_temp'], file_name="precificacao.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_prec", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Precificacao','tema':ideia_prec[:60] if 'ideia_prec' in dir() else '','conteudo':st.session_state['prec_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

    # ========================
    # POTENCIAL DE ESCALA
    # ========================
    elif st.session_state.pagina == "Escala":
        st.header("📈 Potencial de Escala")

        ideia_esc = st.text_area("💡 Ideia/produto:", height=80, value=st.session_state.ideia_padrao, key="ideia_esc")

        if st.button("📈 ANALISAR POTENCIAL DE ESCALA"):
            if ideia_esc.strip():
                with st.spinner("Analisando escala..."):
                    prompt = (
                        f"Analise até onde esta ideia pode crescer.\n"
                        f"Ideia: {ideia_esc}\n\n"
                        f"FORMATO:\n\n"
                        f"📈 POTENCIAL DE ESCALA — {ideia_esc[:50].upper()}\n\n"
                        f"🏘️ MERCADO LOCAL:\n[viabilidade e tamanho aproximado]\n\n"
                        f"🇧🇷 MERCADO NACIONAL:\n[o que seria necessário para expandir]\n\n"
                        f"🌍 MERCADO INTERNACIONAL:\n[viabilidade e desafios — idioma, regulação, logística]\n\n"
                        f"🏪 POSSIBILIDADE DE FRANQUIAS:\n[faz sentido para esse tipo de negócio?]\n\n"
                        f"📜 LICENCIAMENTO:\n[a ideia poderia ser licenciada para terceiros?]\n\n"
                        f"🔄 MODELO DE ASSINATURA:\n[seria viável transformar em recorrência?]\n\n"
                        f"💻 EXPANSÃO DIGITAL:\n[como a digitalização poderia acelerar o crescimento]\n\n"
                        f"🎯 TETO REALISTA DE CRESCIMENTO:\n[seja honesto sobre limitações reais dessa ideia]"
                    )
                    res = invencoes_ia(prompt)
                    salvar_projeto("Escala", ideia_esc[:60], res)
                    st.session_state['esc_temp'] = res
            else:
                st.warning("Descreva a ideia.")

        if st.session_state.get('esc_temp'):
            st.markdown(f"<div class='card-blue'>{st.session_state['esc_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['esc_temp'], file_name="potencial_escala.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_esc", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Escala','tema':ideia_esc[:60] if 'ideia_esc' in dir() else '','conteudo':st.session_state['esc_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

    # ========================
    # PLANO DE LANÇAMENTO
    # ========================
    elif st.session_state.pagina == "Lancamento":
        st.header("📢 Plano de Lançamento")

        col1, col2 = st.columns(2)
        with col1:
            ideia_lanc = st.text_area("💡 Ideia/produto:", height=80, value=st.session_state.ideia_padrao, key="ideia_lanc")
        with col2:
            prazo_lanc = st.text_input("📅 Prazo desejado para lançar:", placeholder="ex: 2 meses, 6 meses...")
            orcamento_lanc = st.number_input("💰 Orçamento para lançamento (R$):", min_value=0.0, value=1000.0, step=200.0)

        if st.button("📢 CRIAR PLANO DE LANÇAMENTO"):
            if ideia_lanc.strip():
                with st.spinner("Montando o roteiro..."):
                    prompt = (
                        f"Crie um plano completo de lançamento.\n"
                        f"Ideia: {ideia_lanc}. Prazo: {prazo_lanc or 'flexível'}. Orçamento: R${orcamento_lanc}\n\n"
                        f"FORMATO:\n\n"
                        f"📢 PLANO DE LANÇAMENTO — {ideia_lanc[:50].upper()}\n\n"
                        f"📋 FASE 1 — PRÉ-LANÇAMENTO:\n[ações antes de lançar — construir audiência, validar, preparar]\n\n"
                        f"🧪 FASE 2 — VALIDAÇÃO:\n[como testar com público real antes de escalar]\n\n"
                        f"🚀 FASE 3 — PRIMEIRAS VENDAS:\n[estratégia para as primeiras conversões]\n\n"
                        f"📣 FASE 4 — DIVULGAÇÃO:\n[canais e táticas considerando o orçamento de R${orcamento_lanc}]\n\n"
                        f"📈 FASE 5 — CRESCIMENTO:\n[como ganhar tração após a validação inicial]\n\n"
                        f"🏆 FASE 6 — ESCALA:\n[próximos passos quando o modelo estiver funcionando]\n\n"
                        f"📅 CRONOGRAMA RESUMIDO:\n[timeline considerando o prazo de {prazo_lanc or 'médio prazo'}]"
                    )
                    res = invencoes_ia(prompt)
                    salvar_projeto("Lancamento", ideia_lanc[:60], res)
                    st.session_state['lanc_temp'] = res
            else:
                st.warning("Descreva a ideia.")

        if st.session_state.get('lanc_temp'):
            st.markdown(f"<div class='card-purple'>{st.session_state['lanc_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['lanc_temp'], file_name="plano_lancamento.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_lanc", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Lancamento','tema':ideia_lanc[:60] if 'ideia_lanc' in dir() else '','conteudo':st.session_state['lanc_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

    # ========================
    # BRANDING
    # ========================
    elif st.session_state.pagina == "Branding":
        st.header("🎨 Branding")

        ideia_brand = st.text_area("💡 Ideia/produto:", height=80, value=st.session_state.ideia_padrao, key="ideia_brand")
        valores_brand = st.text_input("💎 Valores que você quer transmitir (opcional):", placeholder="ex: sustentabilidade, inovação, acessibilidade...")

        if st.button("🎨 CRIAR BRANDING"):
            if ideia_brand.strip():
                with st.spinner("Criando a marca..."):
                    prompt = (
                        f"Crie um branding completo para esta ideia.\n"
                        f"Ideia: {ideia_brand}. Valores desejados: {valores_brand or 'a definir'}\n\n"
                        f"FORMATO:\n\n"
                        f"🎨 BRANDING — {ideia_brand[:50].upper()}\n\n"
                        f"🏷️ OPÇÕES DE NOME (5):\n[nome — significado/por que funciona]\n\n"
                        f"🎯 SLOGAN (3 opções):\n[slogan 1]\n[slogan 2]\n[slogan 3]\n\n"
                        f"📍 POSICIONAMENTO:\n[frase: Para [público], a [marca] é a [categoria] que [benefício único]]\n\n"
                        f"🗣️ PERSONALIDADE DA MARCA:\n[como a marca se comporta — adjetivos]\n\n"
                        f"💬 IDENTIDADE VERBAL:\n[como a marca fala — tom de voz, vocabulário]\n\n"
                        f"💎 VALORES DA MARCA:\n[3-5 valores centrais]"
                    )
                    res = invencoes_ia(prompt)
                    salvar_projeto("Branding", ideia_brand[:60], res)
                    st.session_state['brand_temp'] = res
            else:
                st.warning("Descreva a ideia.")

        if st.session_state.get('brand_temp'):
            st.markdown(f"<div class='card-pink'>{st.session_state['brand_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['brand_temp'], file_name="branding.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_brand", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Branding','tema':ideia_brand[:60] if 'ideia_brand' in dir() else '','conteudo':st.session_state['brand_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

    # ========================
    # IDENTIDADE VISUAL
    # ========================
    elif st.session_state.pagina == "Visual":
        st.header("🖌️ Identidade Visual")

        ideia_vis = st.text_area("💡 Ideia/produto:", height=80, value=st.session_state.ideia_padrao, key="ideia_vis")
        estilo_vis = st.selectbox("🎨 Estilo desejado:", ["Moderno/minimalista","Divertido/colorido","Sofisticado/premium","Rústico/artesanal","Tecnológico/futurista","Não sei, sugira"])

        if st.button("🖌️ SUGERIR IDENTIDADE VISUAL"):
            if ideia_vis.strip():
                with st.spinner("Criando conceito visual..."):
                    prompt = (
                        f"Sugira uma identidade visual completa.\n"
                        f"Ideia: {ideia_vis}. Estilo desejado: {estilo_vis}\n\n"
                        f"FORMATO:\n\n"
                        f"🖌️ IDENTIDADE VISUAL — {ideia_vis[:50].upper()}\n\n"
                        f"🎨 PALETA DE CORES:\n[2-3 cores principais com código hex sugerido + o que cada uma transmite]\n\n"
                        f"🔤 TIPOGRAFIA:\n[estilo de fonte recomendado — serifada/sem serifa, e por quê]\n\n"
                        f"💡 CONCEITO DO LOGOTIPO:\n[ideia de símbolo/conceito visual que represente a marca]\n\n"
                        f"📦 EMBALAGEM/APRESENTAÇÃO:\n[se aplicável, como deveria parecer fisicamente ou digitalmente]\n\n"
                        f"🎭 REFERÊNCIAS DE ESTILO:\n[tipo de marcas/design que servem de inspiração visual, sem citar marcas registradas específicas]"
                    )
                    res = invencoes_ia(prompt)
                    salvar_projeto("Visual", ideia_vis[:60], res)
                    st.session_state['vis_temp'] = res
            else:
                st.warning("Descreva a ideia.")

        if st.session_state.get('vis_temp'):
            st.markdown(f"<div class='card-purple'>{st.session_state['vis_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['vis_temp'], file_name="identidade_visual.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_vis", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Visual','tema':ideia_vis[:60] if 'ideia_vis' in dir() else '','conteudo':st.session_state['vis_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

    # ========================
    # PRODUTO FINAL
    # ========================
    elif st.session_state.pagina == "Produto":
        st.header("📦 Produto Final")

        ideia_prod = st.text_area("💡 Ideia/produto:", height=80, value=st.session_state.ideia_padrao, key="ideia_prod")

        if st.button("📦 TRANSFORMAR EM PRODUTO REAL"):
            if ideia_prod.strip():
                with st.spinner("Estruturando o produto final..."):
                    prompt = (
                        f"Mostre como transformar esta ideia em um produto real e entregável.\n"
                        f"Ideia: {ideia_prod}\n\n"
                        f"FORMATO:\n\n"
                        f"📦 PRODUTO FINAL — {ideia_prod[:50].upper()}\n\n"
                        f"🏭 COMO FABRICAR/CRIAR:\n[processo geral de produção/desenvolvimento]\n\n"
                        f"🚚 COMO ENTREGAR:\n[logística — física ou digital]\n\n"
                        f"💰 COMO VENDER:\n[canais de venda recomendados]\n\n"
                        f"🎤 COMO APRESENTAR AO CLIENTE:\n[script ou estrutura de apresentação do produto]\n\n"
                        f"✅ CHECKLIST PARA O PRODUTO ESTAR PRONTO:\n[itens essenciais antes de vender]"
                    )
                    res = invencoes_ia(prompt)
                    salvar_projeto("Produto", ideia_prod[:60], res)
                    st.session_state['prod_temp'] = res
            else:
                st.warning("Descreva a ideia.")

        if st.session_state.get('prod_temp'):
            st.markdown(f"<div class='card-teal'>{st.session_state['prod_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['prod_temp'], file_name="produto_final.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_prod", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Produto','tema':ideia_prod[:60] if 'ideia_prod' in dir() else '','conteudo':st.session_state['prod_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

    # ========================
    # TENDÊNCIAS
    # ========================
    elif st.session_state.pagina == "Tendencias":
        st.header("🌎 Tendências")
        st.markdown(DISCLAIMER_MERCADO, unsafe_allow_html=True)

        area_tend = st.selectbox("Área de interesse:", [
            "Tecnologia e IA", "Saúde e bem-estar", "Educação", "Sustentabilidade",
            "Alimentação", "Serviços financeiros", "Mobilidade", "Entretenimento", "Outra (descrever)",
        ])
        area_custom = ""
        if area_tend == "Outra (descrever)":
            area_custom = st.text_input("Descreva a área:")

        if st.button("🌎 EXPLORAR TENDÊNCIAS"):
            area_final = area_custom if area_tend == "Outra (descrever)" and area_custom.strip() else area_tend
            if area_final.strip():
                with st.spinner("Explorando tendências..."):
                    prompt = (
                        f"Explore as tendências da área: {area_final}\n\n"
                        f"FORMATO:\n\n"
                        f"🌎 TENDÊNCIAS — {area_final.upper()}\n\n"
                        f"💻 TECNOLOGIAS RELACIONADAS:\n[tecnologias relevantes para essa área]\n\n"
                        f"✨ INOVAÇÕES RECENTES:\n[movimentos recentes conhecidos nessa área]\n\n"
                        f"📈 MERCADOS EM CRESCIMENTO:\n[sub-segmentos em expansão]\n\n"
                        f"🔄 MUDANÇAS DE COMPORTAMENTO:\n[como o consumidor está mudando nessa área]\n\n"
                        f"🚀 OPORTUNIDADES FUTURAS:\n[onde os próximos movimentos provavelmente estarão]"
                    )
                    res = invencoes_ia(prompt)
                    salvar_projeto("Tendencias", area_final, res)
                    st.session_state['tend_temp'] = res
            else:
                st.warning("Escolha ou descreva a área.")

        if st.session_state.get('tend_temp'):
            st.markdown(f"<div class='card-blue'>{st.session_state['tend_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['tend_temp'], file_name="tendencias.txt", mime="text/plain")

    # ========================
    # PATENTES E PROPRIEDADE INTELECTUAL
    # ========================
    elif st.session_state.pagina == "Patentes":
        st.header("⚖️ Patentes e Propriedade Intelectual")

        st.markdown("""<div class="disclaimer-mercado">
        ⚖️ <strong>Importante:</strong> esta seção é educativa. Para registro real de patente, marca ou desenho
        industrial, consulte um especialista em propriedade intelectual ou o INPI (Instituto Nacional da Propriedade Industrial).
        </div>""", unsafe_allow_html=True)

        tema_pat = st.selectbox("Tema:", [
            "Quando vale a pena patentear", "Diferença entre patente, marca e desenho industrial",
            "Como proteger minha ideia antes de divulgar", "Como funciona o registro de marca",
            "Direitos de autor vs patente", "Cuidados ao buscar investidores/parceiros",
        ])

        if st.button("⚖️ EXPLICAR"):
            with st.spinner("Preparando explicação..."):
                prompt = (
                    f"Explique de forma clara e prática: {tema_pat}, no contexto de proteção de ideias e inovação no Brasil.\n\n"
                    f"FORMATO:\n\n"
                    f"⚖️ {tema_pat.upper()}\n\n"
                    f"📖 EXPLICAÇÃO:\n[explicação didática]\n\n"
                    f"✅ QUANDO ISSO SE APLICA:\n[situações práticas]\n\n"
                    f"📋 PASSO A PASSO GERAL:\n[processo típico, sempre indicando que detalhes devem ser confirmados com especialista/INPI]\n\n"
                    f"⚠️ CUIDADOS COMUNS:\n[erros frequentes que pessoas cometem nessa área]\n\n"
                    f"💡 DICA PRÁTICA:\n[1 dica de proteção imediata e de baixo custo]"
                )
                res = invencoes_ia(prompt)
                salvar_projeto("Patentes", tema_pat, res)
                st.session_state['pat_temp'] = res

        if st.session_state.get('pat_temp'):
            st.markdown(f"<div class='card'>{st.session_state['pat_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['pat_temp'], file_name="patentes.txt", mime="text/plain")

    # ========================
    # PLANO DE NEGÓCIOS AUTOMÁTICO
    # ========================
    elif st.session_state.pagina == "PlanoNegocios":
        st.header("📄 Plano de Negócios Automático")

        ideia_plano = st.text_area("💡 Ideia/produto:", height=100, value=st.session_state.ideia_padrao, key="ideia_plano")
        contexto_plano = st.text_area("📝 Contexto adicional (opcional):", height=80,
            placeholder="ex: capital disponível, experiência prévia, equipe...", key="contexto_plano_input")

        if st.button("📄 GERAR PLANO DE NEGÓCIOS COMPLETO"):
            if ideia_plano.strip():
                with st.spinner("Montando o plano de negócios..."):
                    prompt = (
                        f"Crie um plano de negócios completo.\n"
                        f"Ideia: {ideia_plano}. Contexto: {contexto_plano or 'não informado'}\n\n"
                        f"FORMATO:\n\n"
                        f"📄 PLANO DE NEGÓCIOS — {ideia_plano[:50].upper()}\n\n"
                        f"📋 RESUMO EXECUTIVO:\n[visão geral em 3-4 linhas]\n\n"
                        f"💼 MODELO DE NEGÓCIO:\n[como o negócio gera valor e receita]\n\n"
                        f"📊 MERCADO:\n[tamanho e características gerais do mercado-alvo]\n\n"
                        f"📣 MARKETING:\n[estratégia geral de aquisição de clientes]\n\n"
                        f"⚙️ OPERAÇÃO:\n[como o negócio funciona no dia a dia]\n\n"
                        f"💰 FINANCEIRO:\n[estrutura de custos e receita esperada]\n\n"
                        f"📈 CRESCIMENTO:\n[plano para os próximos passos de expansão]"
                    )
                    res = invencoes_ia(prompt)
                    salvar_projeto("PlanoNegocios", ideia_plano[:60], res)
                    st.session_state['plano_neg_temp'] = res
            else:
                st.warning("Descreva a ideia.")

        if st.session_state.get('plano_neg_temp'):
            st.markdown(f"<div class='card-dark'>{st.session_state['plano_neg_temp']}</div>", unsafe_allow_html=True)
            st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar plano completo (.txt)", data=st.session_state['plano_neg_temp'], file_name="plano_de_negocios.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_plano_neg", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'PlanoNegocios','tema':ideia_plano[:60] if 'ideia_plano' in dir() else '','conteudo':st.session_state['plano_neg_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

    # ========================
    # MARKETING INTELIGENTE
    # ========================
    elif st.session_state.pagina == "Marketing":
        st.header("📣 Marketing Inteligente")

        ideia_mkt = st.text_area("💡 Ideia/produto:", height=80, value=st.session_state.ideia_padrao, key="ideia_mkt")
        canal_mkt = st.multiselect("📱 Canais de interesse:", ["Instagram","TikTok","Facebook","Google Ads","E-mail","WhatsApp"], default=["Instagram"])

        if st.button("📣 CRIAR MATERIAL DE MARKETING"):
            if ideia_mkt.strip():
                with st.spinner("Criando materiais..."):
                    canais_txt = ", ".join(canal_mkt) if canal_mkt else "redes sociais em geral"
                    prompt = (
                        f"Crie materiais de marketing para esta ideia.\n"
                        f"Ideia: {ideia_mkt}. Canais: {canais_txt}\n\n"
                        f"FORMATO:\n\n"
                        f"📣 MARKETING — {ideia_mkt[:50].upper()}\n\n"
                        f"🎯 CAMPANHA PRINCIPAL (conceito):\n[ideia central da campanha de lançamento]\n\n"
                        f"📰 3 HEADLINES PARA TESTAR:\n[headline 1]\n[headline 2]\n[headline 3]\n\n"
                        f"📢 IDEIA DE ANÚNCIO PAGO:\n[estrutura de anúncio — gancho, corpo, CTA]\n\n"
                        f"📱 3 IDEIAS DE POSTS:\n[post 1]\n[post 2]\n[post 3]\n\n"
                        f"🎥 IDEIA DE VÍDEO CURTO:\n[roteiro resumido para Reels/TikTok]\n\n"
                        f"🚀 ESTRATÉGIA DE LANÇAMENTO NOS CANAIS ({canais_txt}):\n[como sequenciar o conteúdo nos primeiros 30 dias]"
                    )
                    res = invencoes_ia(prompt)
                    salvar_projeto("Marketing", ideia_mkt[:60], res)
                    st.session_state['mkt_temp'] = res
            else:
                st.warning("Descreva a ideia.")

        if st.session_state.get('mkt_temp'):
            st.markdown(f"<div class='card-pink'>{st.session_state['mkt_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['mkt_temp'], file_name="marketing.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_mkt", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Marketing','tema':ideia_mkt[:60] if 'ideia_mkt' in dir() else '','conteudo':st.session_state['mkt_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

    # ========================
    # SIMULADOR DE MERCADO
    # ========================
    elif st.session_state.pagina == "Simulador":
        st.header("🧪 Simulador de Mercado")
        st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            ideia_sim = st.text_area("💡 Ideia/produto:", height=80, value=st.session_state.ideia_padrao, key="ideia_sim")
            preco_sim = st.number_input("💰 Preço de venda (R$):", min_value=0.0, value=50.0, step=5.0)
        with col2:
            custo_sim = st.number_input("💸 Custo unitário (R$):", min_value=0.0, value=20.0, step=5.0)
            cenario_sim = st.selectbox("🧪 Cenário a simular:", [
                "Vender 100 unidades/mês", "Vender 1.000 unidades/mês", "Dobrar o preço",
                "Reduzir o preço em 30%", "Entrada de um concorrente forte", "Reduzir custos em 20%",
                "Cenário customizado (descrever)",
            ])
            cenario_custom = ""
            if cenario_sim == "Cenário customizado (descrever)":
                cenario_custom = st.text_input("Descreva o cenário:")

        if st.button("🧪 SIMULAR CENÁRIO"):
            if ideia_sim.strip():
                with st.spinner("Simulando..."):
                    cenario_final = cenario_custom if cenario_sim == "Cenário customizado (descrever)" and cenario_custom.strip() else cenario_sim
                    margem_unit = preco_sim - custo_sim
                    prompt = (
                        f"Simule este cenário de mercado.\n"
                        f"Ideia: {ideia_sim}. Preço: R${preco_sim}. Custo: R${custo_sim}. Margem unitária: R${margem_unit:.2f}\n"
                        f"Cenário a simular: {cenario_final}\n\n"
                        f"FORMATO:\n\n"
                        f"🧪 SIMULAÇÃO: {cenario_final.upper()}\n\n"
                        f"📊 PROJEÇÃO NUMÉRICA:\n[calcule receita, custo total e lucro estimado para esse cenário]\n\n"
                        f"📈 IMPACTO NO NEGÓCIO:\n[o que isso significa na prática]\n\n"
                        f"⚠️ RISCOS DESSE CENÁRIO:\n[o que pode dar errado]\n\n"
                        f"✅ COMO SE PREPARAR:\n[ações para aproveitar ou se proteger desse cenário]"
                    )
                    res = invencoes_ia(prompt)
                    salvar_projeto("Simulador", cenario_final, res)
                    st.session_state['sim_temp'] = res
            else:
                st.warning("Descreva a ideia.")

        if st.session_state.get('sim_temp'):
            st.markdown(f"<div class='card-dark'>{st.session_state['sim_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['sim_temp'], file_name="simulacao.txt", mime="text/plain")

    # ========================
    # PAINEL DE RISCOS
    # ========================
    elif st.session_state.pagina == "Riscos":
        st.header("📊 Painel de Riscos")

        ideia_risco = st.text_area("💡 Ideia/produto:", height=80, value=st.session_state.ideia_padrao, key="ideia_risco")

        if st.button("📊 MAPEAR RISCOS"):
            if ideia_risco.strip():
                with st.spinner("Mapeando riscos..."):
                    prompt = (
                        f"Mapeie os riscos completos desta ideia, com honestidade.\n"
                        f"Ideia: {ideia_risco}\n\n"
                        f"FORMATO:\n\n"
                        f"📊 PAINEL DE RISCOS — {ideia_risco[:50].upper()}\n\n"
                        f"⚠️ PRINCIPAIS RISCOS:\n[liste 4-6 riscos reais, do mais para o menos crítico]\n\n"
                        f"🚧 OBSTÁCULOS:\n[barreiras práticas para executar essa ideia]\n\n"
                        f"🎯 PONTOS CRÍTICOS:\n[os momentos/decisões que mais podem fazer a ideia falhar]\n\n"
                        f"🛡️ COMO REDUZIR CADA RISCO:\n[para cada risco listado, uma ação de mitigação]"
                    )
                    res = invencoes_ia(prompt)
                    salvar_projeto("Riscos", ideia_risco[:60], res)
                    st.session_state['risco_temp'] = res
            else:
                st.warning("Descreva a ideia.")

        if st.session_state.get('risco_temp'):
            st.markdown(f"<div class='card-red'>{st.session_state['risco_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['risco_temp'], file_name="painel_riscos.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_risco", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Riscos','tema':ideia_risco[:60] if 'ideia_risco' in dir() else '','conteudo':st.session_state['risco_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

    # ========================
    # BANCO DE IDEIAS
    # ========================
    elif st.session_state.pagina == "BancoIdeias":
        st.header("💎 Banco de Ideias")
        st.markdown("Quando faltar inspiração, gere ideias novas em qualquer área.")

        area_banco = st.selectbox("Área:", [
            "Tecnologia","Saúde","Educação","Agricultura","Indústria","Alimentação",
            "Meio Ambiente","Serviços","Aplicativos","Inteligência Artificial","Qualquer área (surpreenda-me)",
        ])
        qtd_ideias = st.slider("Quantas ideias gerar:", 3, 15, 5)

        if st.button("💎 GERAR IDEIAS"):
            with st.spinner("Gerando ideias..."):
                prompt = (
                    f"Gere {qtd_ideias} ideias de produtos/negócios/invenções na área: {area_banco}\n\n"
                    f"FORMATO — para cada ideia:\n\n"
                    f"💡 [NOME DA IDEIA]\n"
                    f"[Descrição em 2-3 linhas: o que é e que problema resolve]\n"
                    f"Potencial: [Baixo/Médio/Alto]\n\n"
                    f"[Repita para as {qtd_ideias} ideias, todas diferentes entre si]"
                )
                res = invencoes_ia(prompt)
                salvar_projeto("BancoIdeias", area_banco, res)
                st.session_state['banco_temp'] = res
                st.session_state.banco_ideias_geradas.append({'area': area_banco, 'data': datetime.now().strftime('%d/%m/%Y')})

        if st.session_state.get('banco_temp'):
            st.markdown(f"<div class='card'>{st.session_state['banco_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar ideias (.txt)", data=st.session_state['banco_temp'], file_name="banco_de_ideias.txt", mime="text/plain")

    # ========================
    # INVESTIDOR IA
    # ========================
    elif st.session_state.pagina == "Investidor":
        st.header("🤝 Investidor IA")
        st.markdown("Veja como sua ideia seria avaliada por um investidor.")

        ideia_inv = st.text_area("💡 Ideia/produto:", height=100, value=st.session_state.ideia_padrao, key="ideia_inv")
        estagio_inv = st.selectbox("📊 Estágio atual:", ["Apenas ideia","Protótipo","MVP funcionando","Já vendendo","Negócio estabelecido buscando expansão"])

        if st.button("🤝 ANALISAR COMO INVESTIDOR"):
            if ideia_inv.strip():
                with st.spinner("Analisando como investidor..."):
                    prompt = (
                        f"Analise esta ideia do ponto de vista de um investidor.\n"
                        f"Ideia: {ideia_inv}. Estágio: {estagio_inv}\n\n"
                        f"FORMATO:\n\n"
                        f"🤝 ANÁLISE DO INVESTIDOR — {ideia_inv[:50].upper()}\n\n"
                        f"📈 POTENCIAL DE CRESCIMENTO: [Baixo/Médio/Alto] — [justificativa honesta]\n\n"
                        f"📊 ESCALABILIDADE: [Baixa/Média/Alta] — [justificativa]\n\n"
                        f"⭐ DIFERENCIAL COMPETITIVO: [comentário honesto sobre o quão defensável é a ideia]\n\n"
                        f"🎯 ATRATIVIDADE PARA INVESTIMENTO: [Baixa/Média/Alta] — [no estágio atual: {estagio_inv}]\n\n"
                        f"❓ PRINCIPAIS OBJEÇÕES QUE UM INVESTIDOR FARIA:\n[3-4 perguntas difíceis reais]\n\n"
                        f"✅ O QUE FORTALECERIA A IDEIA PARA INVESTIDORES:\n[1-2 ações prioritárias antes de buscar investimento]"
                    )
                    res = invencoes_ia(prompt, "Seja honesto como um investidor real seria — investidores fazem perguntas difíceis e não se impressionam facilmente. Não infle a avaliação para agradar.")
                    salvar_projeto("Investidor", ideia_inv[:60], res)
                    st.session_state['investidor_temp'] = res
            else:
                st.warning("Descreva a ideia.")

        if st.session_state.get('investidor_temp'):
            st.markdown(f"<div class='card-dark'>{st.session_state['investidor_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['investidor_temp'], file_name="analise_investidor.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_investidor", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Investidor','tema':ideia_inv[:60] if 'ideia_inv' in dir() else '','conteudo':st.session_state['investidor_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

    # ========================
    # PITCH PERFEITO
    # ========================
    elif st.session_state.pagina == "Pitch":
        st.header("🎤 Pitch Perfeito")

        col1, col2 = st.columns(2)
        with col1:
            ideia_pitch = st.text_area("💡 Ideia/produto:", height=80, value=st.session_state.ideia_padrao, key="ideia_pitch")
        with col2:
            duracao_pitch = st.selectbox("⏱️ Duração:", ["30 segundos","1 minuto","3 minutos","10 minutos"])
            audiencia_pitch = st.selectbox("🎯 Audiência:", ["Investidores","Clientes","Parceiros/Sócios","Banco/Crédito"])

        if st.button("🎤 CRIAR PITCH"):
            if ideia_pitch.strip():
                with st.spinner("Criando o pitch..."):
                    prompt = (
                        f"Crie um pitch de {duracao_pitch} para {audiencia_pitch}.\n"
                        f"Ideia: {ideia_pitch}\n\n"
                        f"FORMATO:\n\n"
                        f"🎤 PITCH DE {duracao_pitch.upper()} — PARA {audiencia_pitch.upper()}\n\n"
                        f"[Script completo, palavra por palavra, adequado à duração e à audiência — "
                        f"para investidores foque em números/escala, para clientes foque no benefício, "
                        f"para parceiros foque na visão compartilhada, para banco foque em solidez/garantias]\n\n"
                        f"🎯 GANCHO DE ABERTURA:\n[a frase que precisa capturar atenção nos primeiros segundos]\n\n"
                        f"💡 DICA DE ENTREGA:\n[como falar — tom, postura, ritmo para essa duração e audiência]"
                    )
                    res = invencoes_ia(prompt)
                    salvar_projeto("Pitch", f"{duracao_pitch} — {audiencia_pitch}", res)
                    st.session_state['pitch_temp'] = res
            else:
                st.warning("Descreva a ideia.")

        if st.session_state.get('pitch_temp'):
            st.markdown(f"<div class='card-green'>{st.session_state['pitch_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['pitch_temp'], file_name="pitch.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_pitch", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Pitch','tema':ideia_pitch[:60] if 'ideia_pitch' in dir() else '','conteudo':st.session_state['pitch_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

    # ========================
    # CRONOGRAMA INTELIGENTE
    # ========================
    elif st.session_state.pagina == "Cronograma":
        st.header("📅 Cronograma Inteligente")

        ideia_cron = st.text_area("💡 Ideia/produto:", height=80, value=st.session_state.ideia_padrao, key="ideia_cron")
        prazo_cron = st.text_input("📅 Prazo total do projeto:", placeholder="ex: 3 meses, 1 ano...")

        if st.button("📅 GERAR CRONOGRAMA"):
            if ideia_cron.strip():
                with st.spinner("Montando cronograma..."):
                    prompt = (
                        f"Crie um cronograma detalhado para este projeto.\n"
                        f"Ideia: {ideia_cron}. Prazo total: {prazo_cron or 'a definir'}\n\n"
                        f"FORMATO:\n\n"
                        f"📅 CRONOGRAMA — {ideia_cron[:50].upper()}\n\n"
                        f"☀️ HOJE (próximas 24h):\n[ação imediata e concreta]\n\n"
                        f"📆 ESTA SEMANA:\n[3-5 ações]\n\n"
                        f"📅 PRÓXIMO MÊS:\n[principais marcos]\n\n"
                        f"🗓️ PRÓXIMOS {prazo_cron or '3 meses'}:\n[etapas principais até o prazo final]\n\n"
                        f"🏁 MARCO FINAL:\n[o que define que o projeto atingiu esse objetivo de prazo]"
                    )
                    res = invencoes_ia(prompt)
                    salvar_projeto("Cronograma", ideia_cron[:60], res)
                    st.session_state['cron_temp'] = res
            else:
                st.warning("Descreva a ideia.")

        if st.session_state.get('cron_temp'):
            st.markdown(f"<div class='card-teal'>{st.session_state['cron_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['cron_temp'], file_name="cronograma.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_cron", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Cronograma','tema':ideia_cron[:60] if 'ideia_cron' in dir() else '','conteudo':st.session_state['cron_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

    # ========================
    # MENTOR 24 HORAS
    # ========================
    elif st.session_state.pagina == "Mentor":
        st.header("🤖 Mentor 24 Horas")
        st.markdown("Converse livremente sobre seu projeto.")

        if 'chat_mentor' not in st.session_state:
            st.session_state.chat_mentor = []
        if 'mentor_key' not in st.session_state:
            st.session_state.mentor_key = 0

        if st.session_state.chat_mentor:
            for msg in st.session_state.chat_mentor:
                if msg['role'] == 'user':
                    st.markdown(f"<div style='background:#FFFBEB;border:1px solid #D97706;border-radius:12px 12px 4px 12px;padding:12px 16px;margin:8px 0;'><b>Você:</b> {msg['content']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='card-dark' style='margin:8px 0;'><b>💡 Mentor:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown("""<div style="background:#FFFBEB;border:1px dashed #D97706;border-radius:12px;padding:16px;text-align:center;">
            🤖 <strong>Pergunte qualquer coisa sobre seu projeto!</strong> Ex: "Devo focar em B2B ou B2C primeiro?",
            "Como conseguir os primeiros 10 clientes sem dinheiro para anúncios?"
            </div>""", unsafe_allow_html=True)

        pergunta_mentor = st.text_input("Sua pergunta:", key=f"mentor_input_{st.session_state.mentor_key}", placeholder="Pergunte qualquer coisa sobre seu projeto...")

        col_env, col_limpar = st.columns([3, 1])
        with col_env:
            if st.button("📤 PERGUNTAR"):
                if pergunta_mentor.strip():
                    with st.spinner("Pensando..."):
                        historico_msgs = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_mentor[-10:]]
                        resp = invencoes_ia(pergunta_mentor, "Você é um mentor de startups e inovação experiente, direto e estratégico. Responda com profundidade mas sem rodeios.")
                    st.session_state.chat_mentor.append({"role": "user", "content": pergunta_mentor})
                    st.session_state.chat_mentor.append({"role": "assistant", "content": resp})
                    st.session_state.mentor_key += 1
                    salvar_projeto("Mentor", pergunta_mentor[:60], resp)
                    st.rerun()
                else:
                    st.warning("Digite sua pergunta.")
        with col_limpar:
            if st.button("🗑️ Limpar"):
                st.session_state.chat_mentor = []
                st.rerun()

    # ========================
    # LABORATÓRIO DE INVENÇÕES DO FUTURO
    # ========================
    elif st.session_state.pagina == "Laboratorio":
        st.header("⭐ Laboratório de Invenções do Futuro")
        st.markdown("Informe um problema real — a IA combina múltiplas áreas para propor soluções inovadoras.")

        st.markdown("""<div class="ideia-icon-box">
        <div style="font-size:2.5em;">⭐</div>
        <div style="font-size:1.1em;font-weight:600;">Equipe Multidisciplinar de Inovação</div>
        <div style="font-size:0.85em;margin-top:6px;">Engenharia · Tecnologia · Design · Psicologia · Logística · Negócios</div>
        </div>""", unsafe_allow_html=True)

        problema_lab = st.text_area("❓ Qual problema você quer resolver?", height=100,
            placeholder="ex: Como reduzir acidentes de bicicleta? Como economizar água em casa? Como diminuir filas em hospitais?")

        if st.button("⭐ GERAR SOLUÇÕES MULTIDISCIPLINARES"):
            if problema_lab.strip():
                with st.spinner("Combinando conhecimentos de múltiplas áreas..."):
                    prompt = (
                        f"Combine conhecimentos de engenharia, tecnologia, design, psicologia, logística e negócios "
                        f"para propor soluções inovadoras para este problema.\n"
                        f"Problema: {problema_lab}\n\n"
                        f"FORMATO:\n\n"
                        f"⭐ SOLUÇÕES PARA: {problema_lab.upper()}\n\n"
                        f"💡 SOLUÇÃO 1 — [nome]:\n"
                        f"[Descrição da solução]\n"
                        f"Áreas combinadas: [quais disciplinas essa solução usa]\n"
                        f"Por que funciona: [lógica por trás]\n\n"
                        f"💡 SOLUÇÃO 2 — [nome]:\n"
                        f"[mesma estrutura]\n\n"
                        f"💡 SOLUÇÃO 3 — [nome, mais não-convencional/criativa]:\n"
                        f"[mesma estrutura]\n\n"
                        f"🔧 SOLUÇÃO 4 — [adaptação de tecnologia existente]:\n"
                        f"[uma tecnologia que já existe em outro contexto, adaptada para esse problema]\n\n"
                        f"🚀 CONCEITO MAIS PROMISSOR:\n"
                        f"[qual das soluções acima parece ter mais potencial e por quê]\n\n"
                        f"⚠️ MAIOR DESAFIO PARA IMPLEMENTAR:\n"
                        f"[seja honesto sobre a dificuldade real de execução]"
                    )
                    res = invencoes_ia(prompt, "Seja genuinamente criativo e multidisciplinar. Combine perspectivas de diferentes áreas de forma real, não superficial. Inclua pelo menos uma ideia pouco convencional.")
                    salvar_projeto("Laboratorio", problema_lab[:60], res)
                    st.session_state['lab_temp'] = res
            else:
                st.warning("Descreva o problema que você quer resolver.")

        if st.session_state.get('lab_temp'):
            st.markdown(f"<div class='card-dark'>{st.session_state['lab_temp']}</div>", unsafe_allow_html=True)
            st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['lab_temp'], file_name="laboratorio_invencoes.txt", mime="text/plain", use_container_width=True)
            with col_sv:
                if st.button("❤️ Salvar", key="sv_lab", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Laboratorio','tema':problema_lab[:60] if 'problema_lab' in dir() else '','conteudo':st.session_state['lab_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

    # ========================
    # BIBLIOTECA
    # ========================
    elif st.session_state.pagina == "Biblioteca":
        st.header("📚 Biblioteca de Projetos")

        if not st.session_state.projetos_salvos:
            st.info("Biblioteca vazia. Gere análises nos módulos e salve as importantes aqui!")
        else:
            modulos_bib = list(set(c['modulo'] for c in st.session_state.projetos_salvos))
            filtro = st.selectbox("Filtrar por módulo:", ["Todos"] + modulos_bib, key="select_filtro_bib")
            consultas_f = [c for c in st.session_state.projetos_salvos if filtro == "Todos" or c['modulo'] == filtro]

            st.markdown(f"**{len(consultas_f)} análise(s) encontrada(s)**")
            for i, item in enumerate(reversed(consultas_f)):
                idx_real = len(st.session_state.projetos_salvos) - 1 - i
                with st.expander(f"[{item['modulo']}] {item['tema'][:60]} — {item['data']}"):
                    st.markdown(f"<div class='card'>{item['conteudo']}</div>", unsafe_allow_html=True)
                    col_dl, col_del = st.columns([3, 1])
                    with col_dl:
                        st.download_button("📋 Baixar", data=item['conteudo'], file_name=f"{item['modulo'].lower()}.txt", mime="text/plain", key=f"dl_bib_{i}")
                    with col_del:
                        if st.button("🗑️ Remover", key=f"del_bib_{i}"):
                            st.session_state.projetos_salvos.pop(idx_real)
                            st.rerun()

        if st.session_state.projetos_ativos:
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown("### 📂 Seus Projetos Ativos")
            for p in st.session_state.projetos_ativos:
                st.markdown(f"<span class='badge'>💡 {p}</span>", unsafe_allow_html=True)

        if st.session_state.historico_projetos:
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            historico_txt = "\n\n".join(f"[{c['data']}] {c['modulo']} — {c['tema']}\n{c['conteudo']}\n{'─'*40}" for c in st.session_state.historico_projetos)
            st.download_button("⬇️ Exportar todo o histórico (.txt)", data=historico_txt, file_name="historico_invencoes.txt", mime="text/plain")
            if st.button("🗑️ Limpar Todo o Histórico"):
                st.session_state.historico_projetos = []
                st.rerun()

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "© 2026 Invenções IA — Laboratório de Inovação com IA · Quiz Com Prêmios"
    "</div>", unsafe_allow_html=True
)
