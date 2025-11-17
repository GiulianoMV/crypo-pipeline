import polars as pl
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Optional, List, Dict

from src.logger import get_logger


logger = get_logger(__name__)


class FinancialChart:
    def __init__(self, df:pl.DataFrame, config:Dict=None):
        '''
        Inicializa o gerador de gráficos financeiros

        Parameters
        ----------
        df: Dataframe com dados e indicadores
        config: Configurações de visualização
        '''
        self.df = df
        self.config = config or {}
        self.symbol = self._extract_symbol()
        self.theme = self.config.get('theme', 'light')
        self.validate_data()
        self._setup_colors()

    def _extract_symbol(self) -> str:
        '''
        Extração do símbolo do ativo no dataframe.
        '''
        if 'symbol' in self.df.columns:
            return self.df['symbol'][0]
        return 'UNKNOW'
    
    def validate_data(self):
        '''
        Valida colunas necessárias
        '''
        required = ['date', 'open', 'high', 'low', 'close', 'volume']
        missing = [col for col in required if col not in self.df.columns]

        if missing:
            raise ValueError(f'Colunas obrigatórias faltando: {missing}')
    
    def _setup_colors(self):
        '''
        Configura esquema de cores baseadas no tema
        '''
        self.colors = {
            'light':{
                'background':'#FFFFFF',
                'grid':'#D3D3D3'
            },
            'dark':{
                'background':'#1e1e1e',
                'grid':'#2d2d2d'
            }
        }.get(self.theme, self.colors['light'])

    def create_comprehensive_chart(self, hight:int=1200) -> go.Figure:
        '''
        Geração gráfica com todos os indicadores.
        '''
        pass

    def create_performance_dashboard(self) -> go.Figure:
        '''
        Dashboard focado em performance e métricas
        '''
        pass

