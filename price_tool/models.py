from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import json

@dataclass
class Product:
    platform: str
    name: str
    price: float
    original_price: Optional[float]
    sales: int
    shop_name: str
    shop_rating: float
    url: str
    image_url: str
    location: str = ""
    product_id: str = ""
    category: str = ""
    tags: List[str] = field(default_factory=list)
    crawl_time: datetime = field(default_factory=datetime.now)
    
    def to_dict(self):
        return {
            'platform': self.platform,
            'name': self.name,
            'price': self.price,
            'original_price': self.original_price,
            'sales': self.sales,
            'shop_name': self.shop_name,
            'shop_rating': self.shop_rating,
            'url': self.url,
            'image_url': self.image_url,
            'location': self.location,
            'product_id': self.product_id,
            'category': self.category,
            'tags': self.tags,
            'crawl_time': self.crawl_time.isoformat() if isinstance(self.crawl_time, datetime) else self.crawl_time
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            platform=data.get('platform', ''),
            name=data.get('name', ''),
            price=float(data.get('price', 0)),
            original_price=data.get('original_price'),
            sales=int(data.get('sales', 0)),
            shop_name=data.get('shop_name', ''),
            shop_rating=float(data.get('shop_rating', 0)),
            url=data.get('url', ''),
            image_url=data.get('image_url', ''),
            location=data.get('location', ''),
            product_id=data.get('product_id', ''),
            category=data.get('category', ''),
            tags=data.get('tags', []),
            crawl_time=datetime.fromisoformat(data['crawl_time']) if 'crawl_time' in data else datetime.now()
        )

@dataclass
class PriceHistory:
    product_id: str
    platform: str
    prices: List[dict] = field(default_factory=list)
    
    def add_price(self, price: float, timestamp: datetime = None):
        self.prices.append({
            'price': price,
            'timestamp': (timestamp or datetime.now()).isoformat()
        })
    
    def to_dict(self):
        return {
            'product_id': self.product_id,
            'platform': self.platform,
            'prices': self.prices
        }

@dataclass
class CompareResult:
    keyword: str
    products: List[Product]
    lowest_price: Optional[Product] = None
    highest_price: Optional[Product] = None
    best_value: Optional[Product] = None
    avg_price: float = 0.0
    price_range: float = 0.0
    total_products: int = 0
    platforms: List[str] = field(default_factory=list)
    
    def calculate_stats(self):
        if not self.products:
            return
        
        self.total_products = len(self.products)
        self.platforms = list(set(p.platform for p in self.products))
        
        sorted_by_price = sorted(self.products, key=lambda x: x.price)
        self.lowest_price = sorted_by_price[0]
        self.highest_price = sorted_by_price[-1]
        
        prices = [p.price for p in self.products]
        self.avg_price = sum(prices) / len(prices)
        self.price_range = max(prices) - min(prices)
        
        self.best_value = self._calculate_best_value()
    
    def _calculate_best_value(self) -> Optional[Product]:
        if not self.products:
            return None
        
        best_score = -1
        best_product = None
        
        for product in self.products:
            if product.price <= 0:
                continue
            
            price_score = 1 - (product.price - self.lowest_price.price) / (self.highest_price.price - self.lowest_price.price + 0.01)
            rating_score = product.shop_rating / 5.0
            sales_score = min(product.sales / 10000, 1.0)
            
            score = price_score * 0.4 + rating_score * 0.35 + sales_score * 0.25
            
            if score > best_score:
                best_score = score
                best_product = product
        
        return best_product
    
    def to_dict(self):
        return {
            'keyword': self.keyword,
            'products': [p.to_dict() for p in self.products],
            'lowest_price': self.lowest_price.to_dict() if self.lowest_price else None,
            'highest_price': self.highest_price.to_dict() if self.highest_price else None,
            'best_value': self.best_value.to_dict() if self.best_value else None,
            'avg_price': round(self.avg_price, 2),
            'price_range': round(self.price_range, 2),
            'total_products': self.total_products,
            'platforms': self.platforms
        }
