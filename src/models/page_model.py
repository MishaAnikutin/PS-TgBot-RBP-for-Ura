class Page:
    page_price: int = 8
    page_color: str = 'Белый'
    page_format: str = 'А4'
    
    @classmethod
    def total_value(self, total_pages):
        return self.page_price * total_pages
         
