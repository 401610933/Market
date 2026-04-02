import re
from typing import List, Dict, Tuple
from collections import defaultdict
from .models import Product, CompareResult

class DataCleaner:
    def __init__(self):
        self.stop_words = ['官方', '旗舰', '专营', '专卖', '直销']
    
    def clean_product_name(self, name: str) -> str:
        name = re.sub(r'\s+', ' ', name)
        name = re.sub(r'[【】\[\]]', '', name)
        name = name.strip()
        return name
    
    def normalize_price(self, price: float) -> float:
        return round(float(price), 2)
    
    def clean_products(self, products: List[Product]) -> List[Product]:
        cleaned = []
        for product in products:
            product.name = self.clean_product_name(product.name)
            product.price = self.normalize_price(product.price)
            if product.original_price:
                product.original_price = self.normalize_price(product.original_price)
            cleaned.append(product)
        return cleaned

class DataDeduplicator:
    def __init__(self, similarity_threshold: float = 0.8):
        self.similarity_threshold = similarity_threshold
    
    def calculate_similarity(self, name1: str, name2: str) -> float:
        words1 = set(name1.lower().split())
        words2 = set(name2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union)
    
    def is_duplicate(self, product: Product, existing: List[Product]) -> bool:
        for existing_product in existing:
            if product.platform == existing_product.platform:
                if product.product_id == existing_product.product_id:
                    return True
                
                similarity = self.calculate_similarity(product.name, existing_product.name)
                if similarity > self.similarity_threshold:
                    if abs(product.price - existing_product.price) < 1:
                        return True
        
        return False
    
    def deduplicate(self, products: List[Product]) -> List[Product]:
        unique = []
        
        for product in products:
            if not self.is_duplicate(product, unique):
                unique.append(product)
        
        return unique

class DataSorter:
    @staticmethod
    def sort_by_price(products: List[Product], ascending: bool = True) -> List[Product]:
        return sorted(products, key=lambda x: x.price, reverse=not ascending)
    
    @staticmethod
    def sort_by_sales(products: List[Product], descending: bool = True) -> List[Product]:
        return sorted(products, key=lambda x: x.sales, reverse=descending)
    
    @staticmethod
    def sort_by_rating(products: List[Product], descending: bool = True) -> List[Product]:
        return sorted(products, key=lambda x: x.shop_rating, reverse=descending)
    
    @staticmethod
    def sort_by_value(products: List[Product]) -> List[Product]:
        if not products:
            return []
        
        min_price = min(p.price for p in products)
        max_price = max(p.price for p in products)
        price_range = max_price - min_price if max_price > min_price else 1
        
        def value_score(product: Product) -> float:
            price_score = 1 - (product.price - min_price) / price_range
            rating_score = product.shop_rating / 5.0
            sales_score = min(product.sales / 10000, 1.0)
            return price_score * 0.4 + rating_score * 0.35 + sales_score * 0.25
        
        return sorted(products, key=value_score, reverse=True)

class DataProcessor:
    def __init__(self):
        self.cleaner = DataCleaner()
        self.deduplicator = DataDeduplicator()
        self.sorter = DataSorter()
    
    def process(self, products: List[Product], keyword: str) -> CompareResult:
        cleaned = self.cleaner.clean_products(products)
        
        unique = self.deduplicator.deduplicate(cleaned)
        
        sorted_products = self.sorter.sort_by_price(unique, ascending=True)
        
        result = CompareResult(keyword=keyword, products=sorted_products)
        result.calculate_stats()
        
        return result
    
    def get_platform_summary(self, products: List[Product]) -> Dict:
        summary = defaultdict(lambda: {
            'count': 0,
            'min_price': float('inf'),
            'max_price': 0,
            'avg_price': 0,
            'total_sales': 0
        })
        
        for product in products:
            platform = product.platform
            summary[platform]['count'] += 1
            summary[platform]['min_price'] = min(summary[platform]['min_price'], product.price)
            summary[platform]['max_price'] = max(summary[platform]['max_price'], product.price)
            summary[platform]['total_sales'] += product.sales
        
        for platform, data in summary.items():
            platform_products = [p for p in products if p.platform == platform]
            if platform_products:
                data['avg_price'] = sum(p.price for p in platform_products) / len(platform_products)
        
        return dict(summary)
    
    def get_price_distribution(self, products: List[Product], bins: int = 10) -> Dict:
        if not products:
            return {'bins': [], 'counts': []}
        
        prices = [p.price for p in products]
        min_price = min(prices)
        max_price = max(prices)
        
        bin_width = (max_price - min_price) / bins if max_price > min_price else 1
        
        bin_ranges = []
        counts = []
        
        for i in range(bins):
            lower = min_price + i * bin_width
            upper = min_price + (i + 1) * bin_width
            bin_ranges.append(f"{lower:.0f}-{upper:.0f}")
            counts.append(0)
        
        for price in prices:
            bin_index = min(int((price - min_price) / bin_width), bins - 1)
            counts[bin_index] += 1
        
        return {'bins': bin_ranges, 'counts': counts}
    
    def filter_products(self, products: List[Product], 
                       min_price: float = None, 
                       max_price: float = None,
                       platforms: List[str] = None,
                       min_rating: float = None) -> List[Product]:
        filtered = products
        
        if min_price is not None:
            filtered = [p for p in filtered if p.price >= min_price]
        
        if max_price is not None:
            filtered = [p for p in filtered if p.price <= max_price]
        
        if platforms:
            filtered = [p for p in filtered if p.platform in platforms]
        
        if min_rating is not None:
            filtered = [p for p in filtered if p.shop_rating >= min_rating]
        
        return filtered
