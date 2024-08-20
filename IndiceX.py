import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

def app():
    tickers = {"BBAS3.SA": 0.3, "PETR4.SA": 0.5, "EZTC3.SA": 0.2}

    # Funções para cálculos de métricas
    def calcular_retorno_acumulado(df):
        return (df['Close'].iloc[-1] / df['Close'].iloc[0]) - 1

    def calcular_retorno_12_meses(df):
        if len(df) >= 252:
            return (df['Close'].iloc[-1] / df['Close'].iloc[-252]) - 1
        else:
            print("Não há dados suficientes para calcular o retorno dos últimos 12 meses.")
            return np.nan 

    def calcular_volatilidade(df):
        return np.std(df['Close'].pct_change()) * np.sqrt(252)

    def calcular_indice_sharpe(df, risk_free_rate=0.0):
        retorno = df['Close'].pct_change().mean() * 252
        volatilidade = calcular_volatilidade(df)
        return (retorno - risk_free_rate) / volatilidade

    # Placeholder para a API da B3
    def obter_dados_b3(ticker):
        # Substitua este trecho pelo código de integração com a API da B3
        return yf.download(ticker, period="2y")

    # Interface do Streamlit
    st.title("Índice Teste")
    st.write("Este é um índice de teste com 3 ativos: BBAS3, PETR4 e EZTC3.")

    # Obter dados para cada ticker e criar um DataFrame com os dados normalizados
    indice_data = pd.DataFrame()
    for ticker, weight in tickers.items():
        data = obter_dados_b3(ticker)
        if data.empty:
            st.write(f"Não foi possível obter dados para o ticker {ticker}.")
            continue
        indice_data[ticker] = data['Close'] / data['Close'].iloc[0] * 100 * weight

    # Somar os valores ponderados para criar o índice personalizado
    indice_data['Close'] = indice_data.sum(axis=1)

    # Obter dados do benchmark (Ibovespa)
    benchmark_data = obter_dados_b3("^BVSP")
    benchmark_data['Benchmark'] = benchmark_data['Close'] / benchmark_data['Close'].iloc[0] * 100

    # Combinar os dados do índice personalizado e do benchmark
    combined_data = pd.DataFrame({
        'Índice': indice_data['Close'],
        'Benchmark': benchmark_data['Benchmark']
    })

    # Exibir o gráfico de performance com `st.line_chart`
    st.subheader("Gráfico de Performance Normalizado")
    st.line_chart(combined_data)

    # Métricas importantes
    st.subheader("Métricas Importantes")
    retorno_acumulado = calcular_retorno_acumulado(indice_data)
    retorno_12_meses = calcular_retorno_12_meses(indice_data)
    volatilidade = calcular_volatilidade(indice_data)
    indice_sharpe = calcular_indice_sharpe(indice_data)

    # Usar colunas para um layout melhorado
    col1, col2, col3, col4 = st.columns(4)

    # Estilizando as métricas com HTML e CSS
    st.markdown("""
    <style>
    .metric-container {
        text-align: center;
        padding: 20px;
        background-color: #2a2d47;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
    }
    .metric-header {
        font-size: 24px;
        font-weight: bold;
        color: #d8d5ee;
    }
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        color: #20ba80;
    }
    </style>
    """, unsafe_allow_html=True)

    # Exibindo cada métrica em uma coluna com design melhorado
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
            <div class="metric-header">Índice de Sharpe</div>
            <div class="metric-value">{indice_sharpe:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    # Função para criar uma barra visual com emojis
    def criar_barra(porcentagem, total=1, length=20):
        barra = "█" * int(length * porcentagem / total)
        return barra

    # Adicionando a coluna de barras
    tickers_df = pd.DataFrame(list(tickers.items()), columns=["Ticker", "Porcentagem"])
    tickers_df['Gráfico de Porcentagem'] = tickers_df['Porcentagem'].apply(lambda x: criar_barra(x))

    # Exibindo a tabela no Streamlit
    st.subheader("Composição da Carteira")
    st.table(tickers_df)


    # Filtrar os últimos 12 meses
    indice_data = indice_data.last("12M")
    benchmark_data = benchmark_data.last("12M")

    # Calcular os retornos mensais
    indice_data['Retorno'] = indice_data['Close'].pct_change()
    benchmark_data['Retorno'] = benchmark_data['Benchmark'].pct_change()

    # Resample para obter os retornos mensais
    retornos_mensais_indice = indice_data['Retorno'].resample('M').agg(lambda x: (1 + x).prod() - 1).dropna()
    retornos_mensais_benchmark = benchmark_data['Retorno'].resample('M').agg(lambda x: (1 + x).prod() - 1).dropna()

    # Criar uma tabela com 3 linhas (Índice, Benchmark, Diferença) e 12 colunas (meses)
    retornos_mensais = pd.DataFrame({
        'Mês': retornos_mensais_indice.index.strftime('%b-%Y'),
        'Índice': retornos_mensais_indice.values,
        'Benchmark': retornos_mensais_benchmark.values,
    })

    retornos_mensais['Diferença'] = retornos_mensais['Índice'] - retornos_mensais['Benchmark']

    # Transpor a tabela para ter os meses como colunas e as categorias como linhas
    retornos_mensais = retornos_mensais.set_index('Mês').transpose()

    # Formatando os valores como porcentagem
    retornos_mensais_formatted = retornos_mensais.applymap(lambda x: f"{x:.2%}")

    # Exibir a tabela de retornos mensais comparando índice e benchmark
    st.subheader("Tabela de Retornos Mensais x Benchmark")
    st.table(retornos_mensais_formatted)
