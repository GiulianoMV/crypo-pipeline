import polars as pl
import yfinance as yf
import sys

from src.logger import get_logger


logger = get_logger(__name__)


def out_error():
    logger.critical('[<<] Encerrando script forçadamente, erro apresentado.')
    sys.exit(1)


def flatten_col(col):
    '''
        Achata o nome das colunas, removendo listas ou tuplas.
        
        Parameters
        ----------
        col: str | list | tuple
            colunas que serão achatadas, podendo ser uma tupla, lista ou string.
    '''
    try:
        logger.info('[>>] Começando achatamneto de colunas.')
        
        if isinstance(col, tuple):
            parts = [str(x).strip() for x in col if x is not None and str(x).strip() != ""]
        else:
            parts = [str(col).strip()]
        
        logger.info('[<<] Achatamento de colunas concluido.')
        return "_".join(parts).lower()
    except Exception:
        logger.error('[!] Erro apresentado durante o processo de achatamneto de colunas.', exc_info=True)
        out_error()


def download_asset_data(symbol:str, period:str="3mo") -> pl.DataFrame:
    '''
        Baixa dados do yfinance e converte para Polars.
    
        Parameters
        ----------
        symbol: str
            Simbolo do ativo escolhido para download de dados; Necessário utilização da lista disponibilizada em config/settings.yaml para alteração.

        period: str
            Régua de tempo usado para limitar período de dados baixados, padrão de 3 meses; Necessário utilização da lista disponibilizada em config/settings.yaml para alteração.
    '''
    try:
        logger.info(f'[>>] Começando donwload de dados do ativo {symbol}.')
        
        data = yf.download(symbol, period=period, interval="1d")
        data = data.reset_index()
        data.columns = [flatten_col(c) for c in data.columns]
        
        logger.info('[<<] Download de dados comcluído.')
        return pl.from_pandas(data)
    except Exception:
        logger.error('[!] Algo deu errado no download dos dados.', exc_info=True)
        out_error()

def preformat_data(data:pl.DataFrame, symbol:str) -> pl.DataFrame:
    '''
        Pré-processamento de dados antes do export.
    '''
    try:
        logger.info('[>>] Começando pré-processamento de dados.')
        
        mapping_rename = {}
        for col in data.columns:
            new_colname = col.split('_')[0]
            mapping_rename[col] = new_colname
        data = data.rename(mapping_rename)
        logger.info('[+] Mapping e rename de colunas concluído.')

        data = data.filter(pl.col('close').is_not_null())
        data = data.with_columns(pl.col('date').dt.replace_time_zone('UTC').dt.convert_time_zone('America/Sao_Paulo'))
        logger.info('[+] Removido qualquer linha com valor de fechamento (close) nulo. Convertido data para timezone de SP.')

        data = data.with_columns(pl.lit(symbol).alias('symbol'))
        data = data.select(
            pl.col('date'),
            pl.col('symbol'),
            pl.col('open'),
            pl.col('high'),
            pl.col('low'),
            pl.col('close'),
            pl.col('symbol')
        ).sort('date', descending=True)
        logger.info('[+] Adicionado coluna "symbol" e ordenado tabela de dados por data.')

        logger.info('[<<] Encerrando pré-processamento de dados.')
        return data
    except Exception:
        logger.error('[!] Algo deu errado durante o pré-processamento dos dados do ativo.', exc_info=True)
        out_error()
