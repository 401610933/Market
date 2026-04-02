import json
import random
from typing import List, Dict, Optional
from .crawlers import mock_generator
from .processor import DataProcessor
from .visualization import ChartGenerator, RecommendationEngine
from .models import Product, CompareResult

class PriceCompareEngine:
    def __init__(self):
        self.processor = DataProcessor()
        self.chart_generator = ChartGenerator()
        self.recommendation_engine = RecommendationEngine()
    
    def search(self, keyword: str, platforms: List[str] = None, 
               count_per_platform: int = 8) -> Dict:
        products = mock_generator.generate_products(
            keyword=keyword,
            platforms=platforms,
            count_per_platform=count_per_platform
        )
        
        result = self.processor.process(products, keyword)
        
        result_dict = result.to_dict()
        
        result_dict['charts'] = {
            'price_comparison': self.chart_generator.generate_price_comparison_chart(result_dict['products']),
            'price_distribution': self.chart_generator.generate_price_distribution_chart(result_dict['products']),
            'platform_pie': self.chart_generator.generate_platform_pie_chart(result_dict['products']),
            'price_trend': self.chart_generator.generate_price_trend_chart(result_dict['products'])
        }
        
        result_dict['recommendations'] = self.recommendation_engine.get_recommendations(
            result_dict['products'], top_n=5
        )
        
        result_dict['platform_summary'] = self.processor.get_platform_summary(products)
        
        result_dict['price_distribution'] = self.processor.get_price_distribution(products)
        
        return result_dict
    
    def search_raw(self, keyword: str, platforms: List[str] = None,
                   count_per_platform: int = 8) -> List[Product]:
        return mock_generator.generate_products(
            keyword=keyword,
            platforms=platforms,
            count_per_platform=count_per_platform
        )
    
    def compare_specific(self, product_ids: List[str]) -> Dict:
        pass
    
    def get_price_history(self, product_id: str, platform: str, days: int = 30) -> Dict:
        history = mock_generator._generate_price_history(
            base_price=random.uniform(1000, 5000),
            days=days
        )
        
        return {
            'product_id': product_id,
            'platform': platform,
            'history': history
        }

engine = PriceCompareEngine()
