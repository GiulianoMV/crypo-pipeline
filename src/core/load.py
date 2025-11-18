import plotly.graph_objects as go
import polars as pl
import shutil
import sys
import os

from src.logger import get_logger


logger = get_logger(__name__)


def save_table(df:pl.DataFrame, path:str):
    '''
    Salva tabelas no formato .parquet

    Parameters
    ----------
    df: Dataframe a ser salvo
    path: Caminho completo para salvar df
    '''
    try:
        logger.info('[>>] Começando processo de salvamento de tabela.')
        os.makedirs(path, exist_ok=True)
        df.write_parquet(path)
        logger.info(f'[+] Tabela salva em "{path}"')
        logger.info('[<<] Finalizado processo de salvamento de tabela.')
        sys.exit(0)
    except Exception:
        logger.error('[!] Erro apresentado durante salvamento de tabela.', exc_info=True)
        sys.exit(1)


def save_chart(figure:go.Figure, path:str, chart_name:str=None, format:str='png', dpi:int=300):
    '''
    Salva gráficos gerados pelo plotly.

    Parameters
    ----------
    figure: Elemento fig do go
    path: Caminho completo para salvar chart
    chart_name: Nome do chart (opcional)
    format: Formato da imagem (png, jpg, svg, pdf)
    dpi: Resolução para formatos raster
    '''
    try:
        logger.info('[>>] Começando processo de salvamento do chart.')
        os.makedirs(path, exist_ok=True)

        if format.lower() in ['html', 'htm']:
            figure.write_html(path)
        else:
            figure.write_image(path, format=format, scale=dpi/100)
        logger.info(f'[+] Chart salvo em "{path}')
        sys.exit(0)
    except Exception:
        logger.error('[!] Erro apresentado durante salvamento do chart.', exc_info=True)
        sys.exit(1)