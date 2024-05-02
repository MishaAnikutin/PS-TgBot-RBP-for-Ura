import enum
from types import MappingProxyType
from typing import Union
from ..secrets.config import BW_PAGE_PRICE, COLORED_PAGE_PRICE, BW2_PAGE_PRICE, COLORED2_PAGE_PRICE
from dataclasses import dataclass, field


class PageColors:
    bw = 'Черно-белая'
    colored = 'Цветная'
    bw_2 = 'Черно-белая (с двух сторон)'
    colored_2 = 'Цветная (с двух сторон)'


PagePrices = MappingProxyType({
    PageColors.bw: int(BW_PAGE_PRICE),
    PageColors.colored: int(COLORED_PAGE_PRICE),
    PageColors.bw_2: int(BW_PAGE_PRICE),
    PageColors.colored_2: int(COLORED_PAGE_PRICE)
})   


@dataclass 
class Page:
    page_color: PageColors
    page_doubleprint: bool = False 
    page_price: int = field(init=False)
    page_format: str = 'А4'
    
    def __post_init__(self):        
        self.page_price = PagePrices[self.page_color]

        
    def total_value(self, total_pages):
        
        return self.page_price * total_pages
