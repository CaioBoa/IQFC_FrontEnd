import numpy as np

def calcular_retorno_acumulado(df):
    return round((df['Close'].iloc[-1] / df['Close'].iloc[0]) - 1, 4)

def calcular_retorno_12_meses(df):
    if len(df) >= 252:
        return round((df['Close'].iloc[-1] / df['Close'].iloc[-252]) - 1, 4)
    else:
        print("Não há dados suficientes para calcular o retorno dos últimos 12 meses.")
        return np.nan 

def calcular_volatilidade(df):
    return round(np.std(df['Close'].pct_change()) * np.sqrt(252), 4)

def calcular_indice_sharpe(df, risk_free_rate=0.0):
    retorno = df['Close'].pct_change().mean() * 252
    volatilidade = calcular_volatilidade(df)
    return round((retorno - risk_free_rate) / volatilidade, 4)

def criar_barra(porcentagem, total=1, length=20):
    barra = "█" * int(length * porcentagem / total)
    return barra

def calcular_sortino_ratio(df, risk_free_rate=0.0):
    """
    Calcula o Sortino Ratio de um DataFrame de preços.
    """
    retornos = df['Close'].pct_change().dropna()
    downside_risk = np.std(retornos[retornos < 0]) * np.sqrt(252)
    retorno_esperado = retornos.mean() * 252
    return round((retorno_esperado - risk_free_rate) / downside_risk, 4) if downside_risk != 0 else np.nan

def calcular_information_ratio(df, benchmark_df):
    """
    Calcula o Information Ratio entre o ativo e o benchmark.
    """
    retornos_ativo = df['Close'].pct_change().dropna()
    retornos_benchmark = benchmark_df['Close'].pct_change().dropna()
    retorno_excedente = retornos_ativo - retornos_benchmark
    return round(retorno_excedente.mean() * 252 / (retorno_excedente.std() * np.sqrt(252)), 4)

def calcular_omega_ratio(df, target_return=0.0):
    """
    Calcula o Omega Ratio para um DataFrame de preços.
    """
    retornos = df['Close'].pct_change().dropna()
    ganhos = retornos[retornos > target_return].sum()
    perdas = -retornos[retornos < target_return].sum()
    return round(ganhos / perdas, 4) if perdas != 0 else np.nan

def calcular_beta(df, benchmark_df):
    """
    Calcula o Beta de um ativo em relação a um benchmark.
    """
    retornos_ativo = df['Close'].pct_change().dropna()
    retornos_benchmark = benchmark_df['Close'].pct_change().dropna()
    cov_matrix = np.cov(retornos_ativo, retornos_benchmark)
    beta = cov_matrix[0, 1] / cov_matrix[1, 1]
    return round(beta, 4)

def calcular_pior_drawdown(df):
    """
    Calcula o pior drawdown de um DataFrame de preços.
    """
    roll_max = df['Close'].cummax()
    daily_drawdown = df['Close'] / roll_max - 1.0
    max_drawdown = daily_drawdown.cummin()
    return round(max_drawdown.min(), 4)

def calcular_tempo_medio_recuperacao(df):
    """
    Calcula o tempo médio de recuperação (em dias) após um drawdown.
    """
    roll_max = df['Close'].cummax()
    daily_drawdown = df['Close'] / roll_max - 1.0
    fim_drawdown = daily_drawdown == 0
    duracao_drawdown = (fim_drawdown.cumsum() - fim_drawdown.cumsum().where(~fim_drawdown).ffill().fillna(0))
    return round(duracao_drawdown[duracao_drawdown != 0].mean(), 4)
