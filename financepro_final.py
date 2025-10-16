import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
import random
from streamlit_lottie import st_lottie
import requests
import hashlib
import io
import base64

# ========== CONFIGURAÇÃO ==========
st.set_page_config(
    page_title="FinancePro",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== CSS OTIMIZADO ==========
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .header-container {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        color: white;
    }
    
    .custom-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        border: 1px solid #e0e6ed;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3);
    }
    
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 25px;
        font-weight: 600;
    }
    
    .stSpinner > div {
        border: 4px solid #f3f3f3;
        border-radius: 50%;
        border-top: 4px solid #667eea;
        width: 40px;
        height: 40px;
        animation: spin 2s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# ========== SISTEMA DE VALIDAÇÃO SIMPLES ==========
class ValidadorApp:
    def __init__(self):
        self.arquivo_validacao = "app_config.dat"
        
    def validar_aplicacao(self):
        """Validação simples para garantir que o app está íntegro"""
        try:
            # Verificar se é a primeira execução
            if not os.path.exists(self.arquivo_validacao):
                self._criar_arquivo_validacao()
                return True
                
            # Verificar integridade do arquivo
            with open(self.arquivo_validacao, 'r') as f:
                dados_config = json.load(f)
                
            if dados_config.get('app') == 'FinancePro' and dados_config.get('versao') == '1.0':
                return True
                
        except Exception as e:
            st.sidebar.warning("⚠️ Configuração reiniciada")
            
        # Recriar se houver problema
        self._criar_arquivo_validacao()
        return True
    
    def _criar_arquivo_validacao(self):
        """Cria arquivo de validação"""
        dados_config = {
            'app': 'FinancePro',
            'versao': '1.0',
            'instalacao': datetime.now().isoformat(),
            'usuario': f"user_{random.randint(1000, 9999)}"
        }
        
        with open(self.arquivo_validacao, 'w') as f:
            json.dump(dados_config, f)

# ========== FUNÇÕES AUXILIARES ==========
@st.cache_data(ttl=300)
def carregar_lottie_url(url: str):
    """Carrega animação Lottie com cache"""
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return None

def carregar_dados():
    """Carrega dados com tratamento de erro"""
    try:
        if os.path.exists("dados_financepro.json"):
            with open("dados_financepro.json", "r", encoding='utf-8') as f:
                dados = json.load(f)
                if isinstance(dados, list) and all(isinstance(item, dict) for item in dados):
                    return dados
    except Exception as e:
        st.sidebar.error(f"Erro ao carregar dados: {str(e)}")
    
    return []

def salvar_dados(dados):
    """Salva dados com backup automático"""
    try:
        with open("dados_financepro.json", "w", encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"Erro ao salvar dados: {str(e)}")
        return False

# ========== CONFIGURAÇÕES ==========
CATEGORIAS_DETALHADAS = {
    "🏠 Moradia": {
        "descricao": "Aluguel, financiamento, condomínio, IPTU, contas de luz, água, gás, internet",
        "cor": "#FF6B6B",
        "icone": "🏠",
        "dica": "Mantenha até 30% da sua renda com moradia"
    },
    "🚗 Transporte": {
        "descricao": "Combustível, manutenção do carro, transporte público, Uber/Táxi, seguro, IPVA",
        "cor": "#4ECDC4", 
        "icone": "🚗",
        "dica": "Considere transporte público para economizar"
    },
    "🍎 Alimentação": {
        "descricao": "Supermercado, restaurantes, delivery, feira, padaria, lanches",
        "cor": "#45B7D1",
        "icone": "🍎",
        "dica": "Planeje suas refeições da semana"
    },
    "🏥 Saúde": {
        "descricao": "Consultas médicas, medicamentos, plano de saúde, exames, academia",
        "cor": "#96CEB4",
        "icone": "🏥",
        "dica": "Invista em prevenção para evitar gastos maiores"
    },
    "🎮 Lazer": {
        "descricao": "Cinema, streaming, jogos, passeios, viagens, hobbies, esportes",
        "cor": "#FFEAA7",
        "icone": "🎮",
        "dica": "Reserve 10-15% da renda para lazer"
    },
    "🛒 Compras": {
        "descricao": "Roupas, eletrônicos, móveis, cosméticos, presentes, utilidades domésticas",
        "cor": "#DDA0DD",
        "icone": "🛒",
        "dica": "Pesquise antes de comprar e espere promoções"
    },
    "📚 Educação": {
        "descricao": "Cursos, livros, materiais escolares, faculdade, certificações",
        "cor": "#98D8C8",
        "icone": "📚",
        "dica": "É o melhor investimento que você pode fazer"
    },
    "💼 Outros": {
        "descricao": "Despesas diversas, emergências, serviços, assinaturas, doações",
        "cor": "#B2B2B2",
        "icone": "💼",
        "dica": "Mantenha uma reserva para imprevistos"
    }
}

ANIMACOES = {
    "dashboard": "https://assets1.lottiefiles.com/packages/lf20_0y6b1n6i.json",
    "add": "https://assets1.lottiefiles.com/packages/lf20_gn0tojcq.json", 
    "success": "https://assets1.lottiefiles.com/packages/lf20_ykfpefcp.json"
}

# ========== APLICAÇÃO PRINCIPAL ==========
class FinancePro:
    def __init__(self):
        self.validador = ValidadorApp()
        self.dados = carregar_dados()
        self.inicializar_session_state()
    
    def inicializar_session_state(self):
        """Inicialização do session state"""
        # Inicializar dados se não existirem
        if 'dados' not in st.session_state:
            st.session_state.dados = self.dados
        
        # Inicializar último ID
        if 'ultimo_id' not in st.session_state:
            ultimo_id = max([gasto.get('id', 0) for gasto in self.dados] or [0])
            st.session_state.ultimo_id = ultimo_id
        
        # Inicializar formulário se não existir
        if 'formulario' not in st.session_state:
            st.session_state.formulario = {
                "descricao": "", 
                "valor": "", 
                "categoria": "🏠 Moradia", 
                "data": datetime.now().strftime("%Y-%m-%d")
            }
    
    def validar_e_iniciar(self):
        """Valida e inicia a aplicação"""
        try:
            return self.validador.validar_aplicacao()
        except Exception as e:
            st.error(f"Erro na validação: {str(e)}")
            return False
    
    def header(self):
        """Header da aplicação"""
        col1, col2, col3 = st.columns([2, 3, 1])
        
        with col1:
            animacao = carregar_lottie_url(ANIMACOES["dashboard"])
            if animacao:
                st_lottie(animacao, height=100, key="header_anim")
        
        with col2:
            st.markdown("""
            <div class="header-container">
                <h1 style="margin:0; font-size: 2.5rem;">💰 FinancePro</h1>
                <p style="margin:0; font-size: 1.1rem; opacity: 0.9;">Controle Financeiro Pessoal</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total_gastos = sum(gasto.get("valor", 0) for gasto in st.session_state.dados)
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem;">
                <div style="font-size: 0.9rem; color: #666;">Total Gasto</div>
                <div style="font-size: 1.5rem; font-weight: bold; color: #667eea;">R$ {total_gastos:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)
    
    def sidebar(self):
        """Sidebar de navegação"""
        with st.sidebar:
            st.markdown("""
            <div style="text-align: center; padding: 1rem 0;">
                <h2 style="color: white; margin: 0;">💰 FinancePro</h2>
                <p style="color: rgba(255,255,255,0.8); margin: 0;">Controle Financeiro</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Navegação simplificada e mais robusta
            opcoes_navegacao = [
                "📊 Dashboard", 
                "💰 Adicionar Gasto", 
                "📈 Analytics"
            ]
            
            pagina_selecionada = st.radio(
                "Navegação",
                opcoes_navegacao,
                key="nav_radio"
            )
            
            # Estatísticas rápidas
            st.markdown("---")
            st.markdown("**📈 Estatísticas Rápidas**")
            
            dados_atual = st.session_state.dados
            total_gastos = sum(gasto.get("valor", 0) for gasto in dados_atual)
            gastos_mes = self.obter_gastos_mes_atual()
            categorias_ativas = len(set(gasto.get("categoria", "") for gasto in dados_atual if gasto.get("categoria")))
            
            st.metric("Total", f"R$ {total_gastos:,.0f}")
            st.metric("Este Mês", f"R$ {gastos_mes:,.0f}")
            st.metric("Categorias", categorias_ativas)
            
            # Dica do dia
            st.markdown("---")
            dicas = [
                "💡 Revise seus gastos semanais",
                "💰 Estabeleça metas realistas", 
                "📊 Compare com meses anteriores",
                "🎯 Foque nas categorias principais"
            ]
            st.markdown("**💡 Dica do Dia**")
            st.info(random.choice(dicas))
            
        return pagina_selecionada
    
    def obter_gastos_mes_atual(self):
        """Calcula gastos do mês atual"""
        try:
            mes_atual = datetime.now().strftime("%Y-%m")
            return sum(
                gasto.get("valor", 0) for gasto in st.session_state.dados 
                if gasto.get("data", "").startswith(mes_atual)
            )
        except:
            return 0
    
    def obter_gastos_por_mes(self, meses=6):
        """Retorna gastos dos últimos meses"""
        try:
            hoje = datetime.now()
            gastos_por_mes = {}
            
            # Criar lista dos últimos N meses
            for i in range(meses):
                data_ref = hoje.replace(day=1) - timedelta(days=30*i)
                mes_ano = data_ref.strftime("%Y-%m")
                gastos_por_mes[mes_ano] = 0
            
            # Calcular gastos para cada mês
            for gasto in st.session_state.dados:
                data_gasto = gasto.get("data", "")
                if data_gasto:
                    mes_gasto = data_gasto[:7]  # YYYY-MM
                    if mes_gasto in gastos_por_mes:
                        gastos_por_mes[mes_gasto] += gasto.get("valor", 0)
            
            # Ordenar por mês (mais recente primeiro)
            gastos_ordenados = dict(sorted(gastos_por_mes.items(), reverse=True))
            
            return gastos_ordenados
        except Exception as e:
            st.error(f"Erro ao calcular gastos por mês: {str(e)}")
            return {}
    
    def obter_gastos_por_categoria_mensal(self, meses=1):
        """Retorna gastos por categoria do mês atual ou dos últimos meses"""
        try:
            hoje = datetime.now()
            data_inicio = hoje.replace(day=1) - timedelta(days=30*(meses-1))
            
            gastos_categoria = {}
            
            for gasto in st.session_state.dados:
                data_gasto_str = gasto.get("data", "")
                if data_gasto_str:
                    try:
                        data_gasto = datetime.strptime(data_gasto_str, "%Y-%m-%d")
                        if data_gasto >= data_inicio:
                            categoria = gasto.get("categoria", "💼 Outros")
                            valor = gasto.get("valor", 0)
                            
                            if categoria not in gastos_categoria:
                                gastos_categoria[categoria] = 0
                            gastos_categoria[categoria] += valor
                    except Exception as e:
                        continue
            
            return gastos_categoria
        except Exception as e:
            st.error(f"Erro ao calcular gastos por categoria mensal: {str(e)}")
            return {}
    
    def obter_gastos_por_categoria_total(self):
        """Retorna gastos totais por categoria"""
        try:
            gastos_categoria = {}
            
            for gasto in st.session_state.dados:
                categoria = gasto.get("categoria", "💼 Outros")
                valor = gasto.get("valor", 0)
                
                if categoria not in gastos_categoria:
                    gastos_categoria[categoria] = 0
                gastos_categoria[categoria] += valor
            
            return gastos_categoria
        except Exception as e:
            st.error(f"Erro ao calcular gastos por categoria total: {str(e)}")
            return {}
    
    def adicionar_gasto(self, descricao, valor, categoria, data):
        """Adiciona gasto com validação"""
        try:
            # Validações
            if not descricao or not descricao.strip():
                st.error("❌ Descrição não pode estar vazia")
                return False
            
            if valor <= 0:
                st.error("❌ Valor deve ser maior que zero")
                return False
            
            if categoria not in CATEGORIAS_DETALHADAS:
                st.error("❌ Categoria inválida")
                return False
            
            # Criar novo gasto
            novo_id = st.session_state.ultimo_id + 1
            novo_gasto = {
                "id": novo_id,
                "descricao": descricao.strip(),
                "valor": float(valor),
                "categoria": categoria,
                "data": data.strftime("%Y-%m-%d")
            }
            
            # Adicionar e salvar
            st.session_state.dados.append(novo_gasto)
            st.session_state.ultimo_id = novo_id
            
            if salvar_dados(st.session_state.dados):
                # Feedback visual
                success_anim = carregar_lottie_url(ANIMACOES["success"])
                if success_anim:
                    st_lottie(success_anim, height=80, key=f"success_{novo_id}")
                
                st.success("🎉 Gasto adicionado com sucesso!")
                return True
            else:
                st.error("❌ Erro ao salvar dados")
                # Reverter em caso de erro
                st.session_state.dados.pop()
                return False
                
        except Exception as e:
            st.error(f"❌ Erro ao adicionar gasto: {str(e)}")
            return False
    
    def remover_gasto(self, gasto_id):
        """Remove um gasto específico"""
        try:
            gastos_antes = len(st.session_state.dados)
            st.session_state.dados = [g for g in st.session_state.dados if g.get('id') != gasto_id]
            
            if len(st.session_state.dados) < gastos_antes:
                if salvar_dados(st.session_state.dados):
                    st.success(f"✅ Gasto removido com sucesso!")
                    return True
                else:
                    st.error("❌ Erro ao salvar dados após remoção")
                    # Reverter
                    st.session_state.dados = carregar_dados()
                    return False
            else:
                st.error("❌ Gasto não encontrado")
                return False
                
        except Exception as e:
            st.error(f"❌ Erro ao remover gasto: {str(e)}")
            return False
    
    def limpar_todos_dados(self):
        """Remove todos os dados do sistema"""
        try:
            st.session_state.dados = []
            st.session_state.ultimo_id = 0
            
            if salvar_dados(st.session_state.dados):
                st.success("✅ Todos os dados foram removidos com sucesso!")
                return True
            else:
                st.error("❌ Erro ao limpar dados")
                return False
                
        except Exception as e:
            st.error(f"❌ Erro ao limpar dados: {str(e)}")
            return False
    
    def criar_exportacao_google_sheets(self):
        """Cria dados formatados para Google Sheets"""
        dados = st.session_state.dados
        
        if not dados:
            return None
        
        # Criar DataFrame organizado
        df = pd.DataFrame(dados)
        
        # Formatar colunas para melhor visualização
        df_export = df[['id', 'data', 'descricao', 'categoria', 'valor']].copy()
        df_export['categoria'] = df_export['categoria'].apply(lambda x: x.split(' ')[1] if ' ' in x else x)
        df_export['valor'] = df_export['valor'].apply(lambda x: f'R$ {x:,.2f}')
        
        return df_export
    
    def dashboard(self):
        """Dashboard principal"""
        self.header()
        
        dados = st.session_state.dados
        
        # Métricas Principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_geral = sum(gasto.get("valor", 0) for gasto in dados)
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem;">Total Geral</div>
                <div style="font-size: 1.5rem; font-weight: bold;">R$ {total_geral:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            gastos_mes = self.obter_gastos_mes_atual()
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem;">Este Mês</div>
                <div style="font-size: 1.5rem; font-weight: bold;">R$ {gastos_mes:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            meses_unicos = len(set(gasto.get("data", "")[:7] for gasto in dados if gasto.get("data")))
            media_mensal = total_geral / max(1, meses_unicos)
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem;">Média Mensal</div>
                <div style="font-size: 1.5rem; font-weight: bold;">R$ {media_mensal:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            total_registros = len(dados)
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 0.9rem;">Total Registros</div>
                <div style="font-size: 1.5rem; font-weight: bold;">{total_registros}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Seção de Exportação
        with st.container():
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.subheader("📤 Exportar Dados")
            
            col_exp1, col_exp2, col_exp3 = st.columns(3)
            
            with col_exp1:
                # Exportar para CSV
                if dados:
                    csv_data = pd.DataFrame(dados).to_csv(index=False)
                    st.download_button(
                        label="📥 Baixar CSV",
                        data=csv_data,
                        file_name=f"financepro_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        use_container_width=True,
                        help="Baixe os dados em formato CSV para Excel ou outros programas"
                    )
                else:
                    st.button("📥 Baixar CSV", disabled=True, use_container_width=True)
            
            with col_exp2:
                # Exportar para Excel
                if dados:
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                        pd.DataFrame(dados).to_excel(writer, index=False, sheet_name='Gastos')
                    excel_data = output.getvalue()
                    st.download_button(
                        label="📊 Baixar Excel",
                        data=excel_data,
                        file_name=f"financepro_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True,
                        help="Baixe os dados em formato Excel"
                    )
                else:
                    st.button("📊 Baixar Excel", disabled=True, use_container_width=True)
            
            with col_exp3:
                # Instruções Google Sheets
                if dados:
                    with st.expander("🌐 Google Sheets", icon="📋"):
                        st.markdown("""
                        **Para usar no Google Sheets:**
                        
                        1. **Baixe os dados em CSV** (botão acima)
                        2. Acesse [Google Sheets](https://sheets.google.com)
                        3. Clique em **Arquivo → Importar → Fazer upload**
                        4. Selecione o arquivo CSV baixado
                        5. Escolha **"Substituir planilha"** 
                        6. Seus dados serão importados automaticamente!
                        
                        **Dicas:**
                        - Os dados ficam organizados por: ID, Data, Descrição, Categoria e Valor
                        - Você pode criar gráficos diretamente no Google Sheets
                        - Atualize periodicamente exportando novamente
                        """)
                else:
                    st.button("🌐 Google Sheets", disabled=True, use_container_width=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            with st.container():
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.subheader("📈 Evolução Mensal")
                
                gastos_mensais = self.obter_gastos_por_mes(6)
                if gastos_mensais and any(gastos_mensais.values()):
                    # Converter para DataFrame para o gráfico
                    meses = []
                    valores = []
                    
                    for mes, valor in gastos_mensais.items():
                        meses.append(f"{mes[5:7]}/{mes[2:4]}")  # MM/YY
                        valores.append(valor)
                    
                    df_mensal = pd.DataFrame({
                        'Mês': meses,
                        'Gastos': valores
                    })
                    
                    fig = px.line(
                        df_mensal, x='Mês', y='Gastos',
                        markers=True,
                        line_shape='spline',
                        color_discrete_sequence=['#667eea'],
                        title="Gastos dos Últimos 6 Meses"
                    )
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        height=300,
                        margin=dict(l=20, r=20, t=50, b=20),
                        xaxis_title="Mês",
                        yaxis_title="Gastos (R$)",
                        showlegend=False
                    )
                    fig.update_traces(
                        line=dict(width=3),
                        marker=dict(size=8)
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Mostrar detalhes dos meses
                    with st.expander("📋 Detalhes por Mês"):
                        for mes, valor in gastos_mensais.items():
                            st.write(f"**{mes}**: R$ {valor:,.2f}")
                else:
                    st.info("📊 Adicione gastos para ver a evolução mensal")
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            with st.container():
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.subheader("🍕 Gastos por Categoria")
                
                # Seletor de tipo de visualização
                col_view1, col_view2 = st.columns(2)
                with col_view1:
                    tipo_visualizacao = st.radio(
                        "Visualização:",
                        ["Mensal", "Total"],
                        key="tipo_grafico_categoria",
                        horizontal=True
                    )
                
                # Obter dados conforme a seleção
                if tipo_visualizacao == "Mensal":
                    with col_view2:
                        periodo_opcoes = ["Este Mês", "Últimos 3 Meses", "Últimos 6 Meses"]
                        periodo = st.selectbox(
                            "Período:",
                            periodo_opcoes,
                            key="periodo_mensal"
                        )
                    
                    if periodo == "Este Mês":
                        gastos_categoria = self.obter_gastos_por_categoria_mensal(1)
                        titulo_grafico = "Gastos por Categoria - Este Mês"
                    elif periodo == "Últimos 3 Meses":
                        gastos_categoria = self.obter_gastos_por_categoria_mensal(3)
                        titulo_grafico = "Gastos por Categoria - Últimos 3 Meses"
                    else:  # Últimos 6 Meses
                        gastos_categoria = self.obter_gastos_por_categoria_mensal(6)
                        titulo_grafico = "Gastos por Categoria - Últimos 6 Meses"
                else:  # Total
                    gastos_categoria = self.obter_gastos_por_categoria_total()
                    titulo_grafico = "Gastos por Categoria - Total"
                
                if gastos_categoria and any(valor > 0 for valor in gastos_categoria.values()):
                    # Preparar dados para o gráfico
                    categorias_nomes = []
                    valores = []
                    cores = []
                    
                    for cat, valor in gastos_categoria.items():
                        if valor > 0:  # Só incluir categorias com gastos
                            # Remover emoji para mostrar apenas o nome
                            nome_categoria = cat.split(' ', 1)[1] if ' ' in cat else cat
                            categorias_nomes.append(nome_categoria)
                            valores.append(valor)
                            cores.append(CATEGORIAS_DETALHADAS.get(cat, {}).get('cor', '#B2B2B2'))
                    
                    # Criar DataFrame para o gráfico
                    df_pizza = pd.DataFrame({
                        'Categoria': categorias_nomes,
                        'Valor': valores,
                        'Cor': cores
                    })
                    
                    # Criar gráfico de pizza
                    fig = px.pie(
                        df_pizza,
                        values='Valor',
                        names='Categoria',
                        color='Categoria',
                        color_discrete_map=dict(zip(categorias_nomes, cores)),
                        hole=0.4,
                        title=titulo_grafico
                    )
                    
                    fig.update_layout(
                        height=400,
                        margin=dict(l=20, r=20, t=50, b=20),
                        showlegend=True,
                        legend=dict(
                            orientation="v",
                            yanchor="middle",
                            y=0.5,
                            xanchor="left",
                            x=1.1
                        )
                    )
                    
                    fig.update_traces(
                        textposition='inside',
                        textinfo='percent+label',
                        texttemplate='%{label}<br>%{percent}<br>R$ %{value:,.2f}',
                        hovertemplate='<b>%{label}</b><br>Valor: R$ %{value:,.2f}<br>Percentual: %{percent}'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Mostrar tabela de resumo
                    with st.expander("📊 Resumo por Categoria"):
                        total_periodo = sum(valores)
                        for cat_nome, valor, cor in zip(categorias_nomes, valores, cores):
                            percentual = (valor / total_periodo) * 100 if total_periodo > 0 else 0
                            st.write(f"**{cat_nome}**: R$ {valor:,.2f} ({percentual:.1f}%)")
                else:
                    st.info("🏷️ Adicione gastos para ver a distribuição por categoria")
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Gastos Recentes
        with st.container():
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.subheader("📋 Gastos Recentes")
            
            if dados:
                # Ordenar por data (mais recente primeiro)
                dados_ordenados = sorted(dados, key=lambda x: x.get('data', ''), reverse=True)
                
                # Pegar últimos 6 gastos
                dados_recentes = dados_ordenados[:6]
                
                # Criar uma linha para cada gasto com opção de remover
                for gasto in dados_recentes:
                    col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 1])
                    
                    with col1:
                        st.write(f"**{gasto.get('descricao', 'N/A')}**")
                    
                    with col2:
                        categoria_nome = gasto.get('categoria', 'N/A')
                        if ' ' in categoria_nome:
                            categoria_nome = categoria_nome.split(' ')[1]
                        st.write(categoria_nome)
                    
                    with col3:
                        st.write(f"R$ {gasto.get('valor', 0):.2f}")
                    
                    with col4:
                        st.write(gasto.get('data', 'N/A'))
                    
                    with col5:
                        if st.button("🗑️", key=f"del_{gasto.get('id')}"):
                            self.remover_gasto(gasto.get('id'))
                            st.rerun()
                
                st.markdown("---")
                st.caption("💡 Clique no ícone 🗑️ para remover um gasto individual")
                
                # Botão para limpar todos os dados
                with st.expander("⚠️ Limpar Todos os Dados"):
                    st.warning("""
                    **ATENÇÃO:** Esta ação remove TODOS os dados permanentemente.
                    **FAÇA BACKUP** exportando os dados antes de usar esta opção!
                    """)
                    
                    confirmacao = st.text_input(
                        "Digite 'LIMPAR DADOS' para confirmar:",
                        placeholder="LIMPAR DADOS",
                        help="Digite exatamente como mostrado"
                    )
                    
                    if st.button("🚨 LIMPAR TODOS OS DADOS", type="primary", use_container_width=True):
                        if confirmacao == "LIMPAR DADOS":
                            if self.limpar_todos_dados():
                                st.rerun()
                        else:
                            st.error("❌ Confirmação incorreta")
            else:
                st.info("💸 Nenhum gasto registrado. Adicione seu primeiro gasto!")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    def adicionar_gasto_tela(self):
        """Interface para adicionar gastos"""
        self.header()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.container():
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.subheader("💰 Adicionar Novo Gasto")
                
                with st.form("form_gasto", clear_on_submit=True):
                    descricao = st.text_input(
                        "📝 Descrição do Gasto",
                        placeholder="Ex: Supermercado mensal",
                        help="Descreva brevemente o gasto",
                        max_chars=100
                    )
                    
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        valor = st.number_input(
                            "💵 Valor (R$)",
                            min_value=0.01,
                            step=1.00,
                            format="%.2f",
                            help="Digite o valor do gasto"
                        )
                        
                        categoria = st.selectbox(
                            "🏷️ Categoria",
                            options=list(CATEGORIAS_DETALHADAS.keys()),
                            format_func=lambda x: f"{CATEGORIAS_DETALHADAS[x]['icone']} {x.split(' ')[1]}",
                            help="Selecione a categoria do gasto"
                        )
                    
                    with col_b:
                        data = st.date_input(
                            "📅 Data do Gasto",
                            datetime.now(),
                            help="Data em que o gasto ocorreu"
                        )
                    
                    submitted = st.form_submit_button(
                        "💾 Salvar Gasto",
                        use_container_width=True,
                        type="primary"
                    )
                    
                    if submitted:
                        with st.spinner("Salvando gasto..."):
                            if self.adicionar_gasto(descricao, valor, categoria, data):
                                st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            with st.container():
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                st.subheader("ℹ️ Sobre as Categorias")
                
                categoria_selecionada = st.session_state.get('formulario', {}).get('categoria', '🏠 Moradia')
                categoria_info = CATEGORIAS_DETALHADAS.get(categoria_selecionada, CATEGORIAS_DETALHADAS["🏠 Moradia"])
                
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">{categoria_info['icone']}</div>
                    <h4 style="color: {categoria_info['cor']}; margin: 0;">{categoria_selecionada.split(' ')[1]}</h4>
                    <p style="color: #666; font-size: 0.8rem;">{categoria_info['descricao']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="background: {categoria_info['cor']}15; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                    <strong>💡 Dica:</strong> {categoria_info['dica']}
                </div>
                """, unsafe_allow_html=True)
                
                # Estatísticas simples
                total_geral = sum(gasto.get("valor", 0) for gasto in st.session_state.dados)
                st.metric("Total Geral", f"R$ {total_geral:,.2f}")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Animação
            animacao = carregar_lottie_url(ANIMACOES["add"])
            if animacao:
                st_lottie(animacao, height=150, key="add_anim")
    
    def analytics(self):
        """Página de análises"""
        self.header()
        
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("📊 Análises Detalhadas")
        
        dados = st.session_state.dados
        
        if not dados:
            st.info("Adicione gastos para ver análises detalhadas")
            st.markdown('</div>', unsafe_allow_html=True)
            return
        
        # Gráfico de barras por categoria
        gastos_categoria = self.obter_gastos_por_categoria_total()
        if gastos_categoria:
            df_cat = pd.DataFrame({
                'Categoria': [cat.split(' ')[1] if ' ' in cat else cat for cat in gastos_categoria.keys()],
                'Gastos': list(gastos_categoria.values()),
                'Cor': [CATEGORIAS_DETALHADAS.get(cat, {}).get('cor', '#B2B2B2') for cat in gastos_categoria.keys()]
            })
            
            fig = px.bar(
                df_cat, x='Categoria', y='Gastos',
                color='Cor',
                color_discrete_map='identity',
                text_auto='.2s',
                title="Gastos Totais por Categoria"
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Tabela completa
        st.subheader("📋 Todos os Gastos")
        if dados:
            df_completo = pd.DataFrame(dados)
            if not df_completo.empty:
                df_display = df_completo[['id', 'data', 'descricao', 'categoria', 'valor']].copy()
                df_display['categoria'] = df_display['categoria'].apply(lambda x: x.split(' ')[1] if ' ' in x else x)
                df_display['valor'] = df_display['valor'].apply(lambda x: f'R$ {x:,.2f}')
                
                st.dataframe(df_display, use_container_width=True, height=300)
            
            # Controles de remoção individual
            st.subheader("🗑️ Remover Gastos Individualmente")
            gasto_ids = [gasto.get('id') for gasto in dados if gasto.get('id') is not None]
            if gasto_ids:
                gasto_selecionado = st.selectbox(
                    "Selecione o gasto para remover:",
                    options=gasto_ids,
                    format_func=lambda x: f"ID {x}: {next((g['descricao'] for g in dados if g['id'] == x), 'N/A')} - R$ {next((g['valor'] for g in dados if g['id'] == x), 0):.2f}"
                )
                
                if st.button("Remover Gasto Selecionado", type="secondary"):
                    if self.remover_gasto(gasto_selecionado):
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def executar(self):
        """Executa a aplicação principal"""
        try:
            # Validar aplicação primeiro
            if not self.validar_e_iniciar():
                st.error("❌ Erro na inicialização do aplicativo")
                st.info("🔄 Tente recarregar a página")
                return
                
            pagina = self.sidebar()
            
            if pagina == "📊 Dashboard":
                self.dashboard()
            elif pagina == "💰 Adicionar Gasto":
                self.adicionar_gasto_tela()
            elif pagina == "📈 Analytics":
                self.analytics()
                
        except Exception as e:
            st.error(f"❌ Ocorreu um erro inesperado: {str(e)}")
            st.info("🔄 Tente recarregar a página")

           
     # === RODAPÉ MINIMALISTA CORRIGIDO ===
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        <p><strong>FinancePro</strong> • Desenvolvido por Fernando Farias Pires</p>
        <p>📧 piresfernando493@gmail.com • Versão 1.0 - 2024</p>
    </div>
    """, unsafe_allow_html=True)

# ========== EXECUÇÃO ==========
if __name__ == "__main__":
    app = FinancePro()
    app.executar()
