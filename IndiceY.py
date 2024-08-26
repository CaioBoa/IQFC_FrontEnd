import streamlit as st
import pandas as pd
import yfinance as yf
from utils import *

def obter_dados_b3(ticker):
    return yf.download(ticker, period="2y")

def app():
    tickers = {"ITUB4.SA": 0.4, "PETR4.SA": 0.2, "BBDC3.SA": 0.4}

    st.title("Índice Teste")
    st.write("Este é um índice de teste com 3 ativos: ITUB4, PETR4 e BBDC3.")

    indice_data = pd.DataFrame()
    for ticker, weight in tickers.items():
        data = obter_dados_b3(ticker)
        if data.empty:
            st.write(f"Não foi possível obter dados para o ticker {ticker}.")
            continue
        indice_data[ticker] = data['Close'] / data['Close'].iloc[0] * 100 * weight

    indice_data['Close'] = indice_data.sum(axis=1)

    benchmark_data = obter_dados_b3("^BVSP")
    benchmark_data['Benchmark'] = benchmark_data['Close'] / benchmark_data['Close'].iloc[0] * 100

    combined_data = pd.DataFrame({
        'Índice': indice_data['Close'],
        'Benchmark': benchmark_data['Benchmark']
    })

    st.subheader("Gráfico de Performance Normalizado")
    st.line_chart(combined_data)

    st.subheader("Métricas Importantes")
    retorno_acumulado = calcular_retorno_acumulado(indice_data)
    retorno_12_meses = calcular_retorno_12_meses(indice_data)
    volatilidade = calcular_volatilidade(indice_data)
    indice_sharpe = calcular_indice_sharpe(indice_data)
    
    # Cálculos adicionais para o benchmark
    retorno_acumulado_benchmark = calcular_retorno_acumulado(benchmark_data)
    retorno_12_meses_benchmark = calcular_retorno_12_meses(benchmark_data)
    volatilidade_benchmark = calcular_volatilidade(benchmark_data)
    sharpe_ratio_benchmark = calcular_indice_sharpe(benchmark_data)

    # Cálculos dos índices utilizando as funções implementadas
    sortino_ratio = calcular_sortino_ratio(indice_data)
    sortino_ratio_benchmark = calcular_sortino_ratio(benchmark_data)

    information_ratio = calcular_information_ratio(indice_data, benchmark_data)

    omega_ratio = calcular_omega_ratio(indice_data)
    omega_ratio_benchmark = calcular_omega_ratio(benchmark_data)

    beta = calcular_beta(indice_data, benchmark_data)

    pior_drawdown = calcular_pior_drawdown(indice_data)
    pior_drawdown_benchmark = calcular_pior_drawdown(benchmark_data)

    tempo_medio_recuperacao = calcular_tempo_medio_recuperacao(indice_data)

    col1, col2, col3, col4 = st.columns(4)

    st.markdown("""
    <style>
    .metric-container {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        text-align: center;
        padding: 15px;
        background-color: #2a2d47;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
    }
    .metric-header {
        font-size: 18px;
        font-weight: bold;
        color: #d8d5ee;
        align-self: center;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #20ba80;
        align-self: center;
    }

    @media (max-width: 768px) {
        .metric-container {
            min-height: 9rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-header">Retorno Acumulado</div>
            <div class="metric-value">{retorno_acumulado:.2%}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-header">Retorno 12 Meses</div>
            <div class="metric-value">{retorno_12_meses:.2%}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-header">Volatilidade</div>
            <div class="metric-value">{volatilidade:.2%}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-header">Índice Sharpe</div>
            <div class="metric-value">{indice_sharpe:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    # Dados da composição da carteira
    tickers_df = pd.DataFrame(list(tickers.items()), columns=["Ticker", "Porcentagem"])
    tickers_df['Barra de Porcentagem'] = tickers_df['Porcentagem'].apply(lambda x: criar_barra(x))

    st.subheader("Composição da Carteira")

    st.markdown(
        """
        <style>
        .stDataFrame {margin-left: auto; margin-right: auto;}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.data_editor(
        tickers_df,
        hide_index=True,
        column_config={
            "Ticker": "Ticker",
            "Porcentagem": "Porcentagem",
            "Barra de Porcentagem": "Barra de Porcentagem"
        },
        width=800
    )

    # Adicionando a Tabela de Métricas
    st.subheader("Tabela de Métricas Comparativa")

    metricas_df = pd.DataFrame({
        'Métrica': ['Retorno Acumulado', 'Retorno 12 meses', 'Volatilidade', 'Beta', 'Pior Drawdown', 'Tempo médio de recuperação (dias)', 'Sharpe Ratio', 'Sortino Ratio', 'Information Ratio', 'Omega Ratio'],
        'Índice': [f"{retorno_acumulado:.2%}", f"{retorno_12_meses:.2%}", f"{volatilidade:.2%}", beta, f"{pior_drawdown:.2%}", tempo_medio_recuperacao, f"{indice_sharpe:.2f}", f"{sortino_ratio:.2f}", f"{information_ratio:.2f}", f"{omega_ratio:.2f}"],
        'Benchmark': [f"{retorno_acumulado_benchmark:.2%}", f"{retorno_12_meses_benchmark:.2%}", f"{volatilidade_benchmark:.2%}", 'N/A', f"{pior_drawdown_benchmark:.2%}", 'N/A', f"{sharpe_ratio_benchmark:.2f}", f"{sortino_ratio_benchmark:.2f}", 'N/A', f"{omega_ratio_benchmark:.2f}"]
    })

    st.markdown(
        """
        <style>
        .stDataFrame {margin-left: auto; margin-right: auto;}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.data_editor(
        metricas_df,
        hide_index=True,
        column_config={
            "Métrica": "Métrica",
            "Índice": "Índice",
            "Benchmark": "Benchmark"
        },
        width=800
    )

    # Calcular retornos mensais para o índice e o benchmark
    indice_data['Retorno Mensal'] = indice_data['Close'].pct_change().resample('M').apply(lambda x: (1 + x).prod() - 1)
    benchmark_data['Retorno Mensal'] = benchmark_data['Benchmark'].pct_change().resample('M').apply(lambda x: (1 + x).prod() - 1)

    # Criar DataFrame para tabela de retornos mensais
    retornos_mensais_df = pd.DataFrame({
        'Mês': indice_data['Retorno Mensal'].index.strftime('%b-%Y'),
        'Índice': indice_data['Retorno Mensal'].values,
        'Benchmark': benchmark_data['Retorno Mensal'].values
    })

    # Remover linhas com NaN (caso existam meses sem dados completos)
    retornos_mensais_df.dropna(inplace=True)

    # Calcular a diferença entre os retornos mensais do índice e do benchmark
    retornos_mensais_df['Diferença'] = retornos_mensais_df['Índice'] - retornos_mensais_df['Benchmark']

    # Exibir a tabela de retornos mensais no Streamlit
    st.subheader("Tabela de Retornos Mensais x Benchmark")
    st.data_editor(
        retornos_mensais_df,
        hide_index=True,
        column_config={
            "Mês": "Mês",
            "Índice": "Índice",
            "Benchmark": "Benchmark",
            "Diferença": "Diferença"
        },
        width=800
    )
