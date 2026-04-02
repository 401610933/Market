import json
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import random

class ChartGenerator:
    @staticmethod
    def generate_price_comparison_chart(products: List[dict]) -> dict:
        if not products:
            return {'type': 'bar', 'data': {'labels': [], 'datasets': []}}
        
        platforms = {}
        for product in products:
            platform = product.get('platform', 'unknown')
            if platform not in platforms:
                platforms[platform] = []
            platforms[platform].append(product.get('price', 0))
        
        colors = {
            'taobao': '#FF6B00',
            'jd': '#E3393C',
            'pdd': '#E02E24'
        }
        
        datasets = []
        for platform, prices in platforms.items():
            avg_price = sum(prices) / len(prices)
            datasets.append({
                'label': f"{platform.upper()} 平均价格",
                'data': [round(avg_price, 2)],
                'backgroundColor': colors.get(platform, '#666666'),
                'borderColor': colors.get(platform, '#666666')
            })
        
        return {
            'type': 'bar',
            'data': {
                'labels': ['各平台平均价格对比'],
                'datasets': datasets
            },
            'options': {
                'responsive': True,
                'plugins': {
                    'title': {
                        'display': True,
                        'text': '各平台价格对比'
                    }
                },
                'scales': {
                    'y': {
                        'beginAtZero': False,
                        'title': {
                            'display': True,
                            'text': '价格 (元)'
                        }
                    }
                }
            }
        }
    
    @staticmethod
    def generate_price_distribution_chart(products: List[dict]) -> dict:
        if not products:
            return {'type': 'histogram', 'data': {'labels': [], 'datasets': []}}
        
        prices = [p.get('price', 0) for p in products]
        min_price = min(prices)
        max_price = max(prices)
        
        bins = 10
        bin_width = (max_price - min_price) / bins if max_price > min_price else 1
        
        bin_counts = [0] * bins
        bin_labels = []
        
        for i in range(bins):
            lower = min_price + i * bin_width
            upper = min_price + (i + 1) * bin_width
            bin_labels.append(f"{lower:.0f}-{upper:.0f}")
        
        for price in prices:
            bin_index = min(int((price - min_price) / bin_width), bins - 1)
            bin_counts[bin_index] += 1
        
        return {
            'type': 'bar',
            'data': {
                'labels': bin_labels,
                'datasets': [{
                    'label': '商品数量',
                    'data': bin_counts,
                    'backgroundColor': '#4CAF50',
                    'borderColor': '#4CAF50'
                }]
            },
            'options': {
                'responsive': True,
                'plugins': {
                    'title': {
                        'display': True,
                        'text': '价格分布直方图'
                    }
                },
                'scales': {
                    'x': {
                        'title': {
                            'display': True,
                            'text': '价格区间 (元)'
                        }
                    },
                    'y': {
                        'title': {
                            'display': True,
                            'text': '商品数量'
                        }
                    }
                }
            }
        }
    
    @staticmethod
    def generate_platform_pie_chart(products: List[dict]) -> dict:
        if not products:
            return {'type': 'pie', 'data': {'labels': [], 'datasets': []}}
        
        platform_counts = {}
        for product in products:
            platform = product.get('platform', 'unknown')
            platform_counts[platform] = platform_counts.get(platform, 0) + 1
        
        colors = {
            'taobao': '#FF6B00',
            'jd': '#E3393C',
            'pdd': '#E02E24'
        }
        
        return {
            'type': 'pie',
            'data': {
                'labels': [p.upper() for p in platform_counts.keys()],
                'datasets': [{
                    'data': list(platform_counts.values()),
                    'backgroundColor': [colors.get(p, '#666666') for p in platform_counts.keys()]
                }]
            },
            'options': {
                'responsive': True,
                'plugins': {
                    'title': {
                        'display': True,
                        'text': '各平台商品数量分布'
                    }
                }
            }
        }
    
    @staticmethod
    def generate_price_trend_chart(products: List[dict], days: int = 30) -> dict:
        dates = []
        base_date = datetime.now() - timedelta(days=days-1)
        
        for i in range(days):
            dates.append((base_date + timedelta(days=i)).strftime('%m-%d'))
        
        platform_trends = {}
        colors = {
            'taobao': '#FF6B00',
            'jd': '#E3393C',
            'pdd': '#E02E24'
        }
        
        for product in products:
            platform = product.get('platform', 'unknown')
            base_price = product.get('price', 1000)
            
            if platform not in platform_trends:
                trend = []
                current_price = base_price * random.uniform(0.9, 1.1)
                
                for i in range(days):
                    variance = random.uniform(-0.05, 0.05)
                    current_price = current_price * (1 + variance)
                    current_price = max(current_price, base_price * 0.7)
                    trend.append(round(current_price, 2))
                
                platform_trends[platform] = trend
        
        datasets = []
        for platform, trend in platform_trends.items():
            datasets.append({
                'label': f"{platform.upper()} 价格趋势",
                'data': trend,
                'borderColor': colors.get(platform, '#666666'),
                'fill': False,
                'tension': 0.1
            })
        
        return {
            'type': 'line',
            'data': {
                'labels': dates,
                'datasets': datasets
            },
            'options': {
                'responsive': True,
                'plugins': {
                    'title': {
                        'display': True,
                        'text': '价格趋势图（模拟数据）'
                    }
                },
                'scales': {
                    'y': {
                        'title': {
                            'display': True,
                            'text': '价格 (元)'
                        }
                    },
                    'x': {
                        'title': {
                            'display': True,
                            'text': '日期'
                        }
                    }
                }
            }
        }

class RecommendationEngine:
    @staticmethod
    def calculate_value_score(product: dict, all_products: List[dict]) -> float:
        if not all_products or not product:
            return 0.0
        
        prices = [p.get('price', 0) for p in all_products]
        min_price = min(prices)
        max_price = max(prices)
        price_range = max_price - min_price if max_price > min_price else 1
        
        price_score = 1 - (product.get('price', 0) - min_price) / price_range
        
        rating = product.get('shop_rating', 0)
        rating_score = rating / 5.0
        
        sales = product.get('sales', 0)
        max_sales = max(p.get('sales', 0) for p in all_products)
        sales_score = sales / max_sales if max_sales > 0 else 0
        
        value_score = price_score * 0.4 + rating_score * 0.35 + sales_score * 0.25
        
        return round(value_score, 3)
    
    @staticmethod
    def get_recommendations(products: List[dict], top_n: int = 5) -> List[dict]:
        if not products:
            return []
        
        for product in products:
            product['value_score'] = RecommendationEngine.calculate_value_score(product, products)
        
        sorted_products = sorted(products, key=lambda x: x.get('value_score', 0), reverse=True)
        
        recommendations = []
        for i, product in enumerate(sorted_products[:top_n]):
            rec = product.copy()
            rec['rank'] = i + 1
            rec['recommendation_reason'] = RecommendationEngine._get_reason(product, i)
            recommendations.append(rec)
        
        return recommendations
    
    @staticmethod
    def _get_reason(product: dict, rank: int) -> str:
        reasons = []
        
        price = product.get('price', 0)
        sales = product.get('sales', 0)
        rating = product.get('shop_rating', 0)
        
        if rank == 0:
            reasons.append("综合性价比最高")
        
        if rating >= 4.8:
            reasons.append("店铺评分优秀")
        
        if sales >= 10000:
            reasons.append("销量领先")
        elif sales >= 5000:
            reasons.append("销量较高")
        
        if product.get('original_price'):
            discount = (product['original_price'] - price) / product['original_price'] * 100
            if discount >= 20:
                reasons.append(f"优惠力度大({discount:.0f}%折扣)")
        
        if not reasons:
            reasons.append("价格合理")
        
        return "，".join(reasons)
    
    @staticmethod
    def get_price_alerts(products: List[dict], target_price: float = None) -> List[dict]:
        alerts = []
        
        if not products:
            return alerts
        
        avg_price = sum(p.get('price', 0) for p in products) / len(products)
        
        for product in products:
            price = product.get('price', 0)
            
            if price < avg_price * 0.8:
                alerts.append({
                    'type': 'low_price',
                    'product': product,
                    'message': f"发现低价商品：{product.get('name', '')}，价格 {price}元，低于均价 {((avg_price - price) / avg_price * 100):.1f}%"
                })
            
            if target_price and price <= target_price:
                alerts.append({
                    'type': 'target_reached',
                    'product': product,
                    'message': f"达到目标价格：{product.get('name', '')}，价格 {price}元"
                })
            
            if product.get('original_price'):
                discount = (product['original_price'] - price) / product['original_price'] * 100
                if discount >= 30:
                    alerts.append({
                        'type': 'big_discount',
                        'product': product,
                        'message': f"大额折扣：{product.get('name', '')}，折扣 {discount:.0f}%"
                    })
        
        return alerts
