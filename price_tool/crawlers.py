import random
import hashlib
import time
from typing import List, Optional
from datetime import datetime, timedelta
from .models import Product, PriceHistory

class BaseCrawler:
    def __init__(self):
        self.platform_name = "base"
        self.base_url = ""
    
    def search(self, keyword: str, limit: int = 20) -> List[Product]:
        raise NotImplementedError
    
    def get_product_detail(self, product_id: str) -> Optional[Product]:
        raise NotImplementedError
    
    def get_price_history(self, product_id: str, days: int = 30) -> PriceHistory:
        raise NotImplementedError

class MockDataGenerator:
    PLATFORMS = {
        'taobao': {
            'name': '淘宝',
            'base_url': 'https://item.taobao.com/item.htm?id=',
            'shops': ['天猫官方旗舰店', '淘宝优品店', '品牌直销店', '官方授权店', '优质专营店'],
            'price_factor': 1.0
        },
        'jd': {
            'name': '京东',
            'base_url': 'https://item.jd.com/',
            'shops': ['京东自营', '京东官方旗舰店', '京东授权店', '品牌旗舰店'],
            'price_factor': 1.05
        },
        'pdd': {
            'name': '拼多多',
            'base_url': 'https://mobile.yangkeduo.com/goods.html?goods_id=',
            'shops': ['拼多多官方店', '品牌特卖店', '工厂直销店', '百亿补贴店'],
            'price_factor': 0.85
        }
    }
    
    PRODUCT_TEMPLATES = {
        '手机': {
            'prefixes': ['华为', '小米', '苹果', 'OPPO', 'vivo', '三星', '荣耀', 'realme', '一加', '魅族'],
            'models': ['Mate60', 'Mate60 Pro', 'iPhone15', 'iPhone15 Pro', '小米14', '小米14 Pro', 
                      'OPPO Find X7', 'vivo X100', 'Galaxy S24', '荣耀Magic6', '一加12', '魅族21'],
            'base_price': 4000,
            'price_variance': 2000,
            'specs': ['8GB+256GB', '12GB+256GB', '12GB+512GB', '16GB+512GB', '8GB+128GB']
        },
        '笔记本': {
            'prefixes': ['联想', '华为', '戴尔', '惠普', '华硕', '苹果', '小米', '荣耀', 'ThinkPad', '机械革命'],
            'models': ['Pro14', 'Air15', 'XPS15', 'Pavilion15', 'ROG幻14', 'MacBook Air', 'MacBook Pro', 
                      'RedmiBook Pro', 'MagicBook', 'ThinkPad X1', '游戏本Z7'],
            'base_price': 5000,
            'price_variance': 4000,
            'specs': ['i5-13500H 16GB 512GB', 'i7-13700H 16GB 1TB', 'R7-7840HS 16GB 512GB', 
                     'M2 8GB 256GB', 'i9-13900H 32GB 1TB']
        },
        '耳机': {
            'prefixes': ['苹果', '华为', '小米', '索尼', 'Bose', '森海塞尔', '漫步者', 'JBL', 'Beats', 'OPPO'],
            'models': ['AirPods Pro', 'FreeBuds Pro', 'FlipBuds Pro', 'WF-1000XM5', 'QuietComfort', 
                      'Momentum', 'TWS NB2', 'Tune Buds', 'Studio Buds', 'Enco X2'],
            'base_price': 500,
            'price_variance': 1500,
            'specs': ['主动降噪', '通透模式', '无线充电', '长续航', 'Hi-Fi音质']
        },
        '平板': {
            'prefixes': ['苹果', '华为', '小米', '三星', '联想', '荣耀', 'OPPO', 'vivo'],
            'models': ['iPad Pro', 'iPad Air', 'MatePad Pro', 'MatePad', '小米平板6', 'Galaxy Tab S9',
                      '小新Pad Pro', '荣耀平板V8', 'OPPO Pad', 'vivo Pad'],
            'base_price': 2000,
            'price_variance': 3000,
            'specs': ['WiFi 128GB', 'WiFi 256GB', '5G 128GB', '5G 256GB', 'WiFi+蜂窝 512GB']
        },
        '手表': {
            'prefixes': ['苹果', '华为', '小米', '三星', 'OPPO', 'vivo', '荣耀', '佳明'],
            'models': ['Watch Ultra', 'Watch Series9', 'Watch GT4', 'Watch 4', '小米手表S3',
                      'Galaxy Watch6', 'Watch X', 'Watch 3', '荣耀手表4', 'Forerunner 265'],
            'base_price': 1000,
            'price_variance': 2000,
            'specs': ['45mm GPS', '41mm GPS', '45mm 蜂窝', '46mm', '42mm']
        }
    }
    
    def __init__(self):
        self.used_ids = set()
    
    def _generate_product_id(self, platform: str, name: str) -> str:
        base = f"{platform}_{name}_{time.time()}"
        hash_obj = hashlib.md5(base.encode())
        product_id = hash_obj.hexdigest()[:12]
        return product_id
    
    def _generate_price_history(self, base_price: float, days: int = 30) -> List[dict]:
        history = []
        current_price = base_price
        
        for i in range(days):
            date = datetime.now() - timedelta(days=days-i-1)
            variance = random.uniform(-0.1, 0.1)
            current_price = base_price * (1 + variance)
            current_price = max(current_price, base_price * 0.7)
            
            history.append({
                'date': date.strftime('%Y-%m-%d'),
                'price': round(current_price, 2)
            })
        
        return history
    
    def generate_products(self, keyword: str, platforms: List[str] = None, 
                         count_per_platform: int = 5) -> List[Product]:
        products = []
        
        if platforms is None:
            platforms = list(self.PLATFORMS.keys())
        
        category = self._detect_category(keyword)
        template = self.PRODUCT_TEMPLATES.get(category, self.PRODUCT_TEMPLATES['手机'])
        
        for platform in platforms:
            if platform not in self.PLATFORMS:
                continue
            
            platform_info = self.PLATFORMS[platform]
            
            for i in range(count_per_platform):
                product = self._generate_single_product(
                    keyword, platform, platform_info, template, i
                )
                products.append(product)
        
        return products
    
    def _detect_category(self, keyword: str) -> str:
        keyword_lower = keyword.lower()
        
        category_keywords = {
            '手机': ['手机', 'mate', 'iphone', '小米', '华为', '荣耀', 'oppo', 'vivo', '三星', 'phone'],
            '笔记本': ['笔记本', '电脑', 'laptop', 'macbook', 'thinkpad', '游戏本'],
            '耳机': ['耳机', 'earphone', 'airpods', 'freebuds', '降噪', 'tws'],
            '平板': ['平板', 'ipad', 'pad', 'tablet', 'matepad'],
            '手表': ['手表', 'watch', '手环', 'band']
        }
        
        for category, keywords in category_keywords.items():
            for kw in keywords:
                if kw in keyword_lower:
                    return category
        
        return '手机'
    
    def _generate_single_product(self, keyword: str, platform: str, 
                                 platform_info: dict, template: dict, 
                                 index: int) -> Product:
        prefix = random.choice(template['prefixes'])
        model = random.choice(template['models'])
        spec = random.choice(template['specs'])
        
        name_parts = [prefix, model]
        if keyword.lower() not in model.lower():
            name_parts.insert(0, keyword.split()[0] if ' ' in keyword else keyword)
        
        name = ' '.join(name_parts) + f' {spec}'
        
        base_price = template['base_price'] + random.uniform(
            -template['price_variance'] * 0.3, 
            template['price_variance'] * 0.5
        )
        base_price *= platform_info['price_factor']
        
        price_variance = random.uniform(-0.15, 0.2)
        price = base_price * (1 + price_variance)
        price = max(price, base_price * 0.5)
        
        original_price = price * random.uniform(1.1, 1.3) if random.random() > 0.3 else None
        
        sales = random.randint(100, 50000)
        if platform == 'pdd':
            sales = int(sales * random.uniform(1.5, 3.0))
        
        shop_name = random.choice(platform_info['shops'])
        if '官方' in shop_name or '自营' in shop_name:
            shop_rating = round(random.uniform(4.7, 5.0), 1)
        else:
            shop_rating = round(random.uniform(4.2, 4.9), 1)
        
        product_id = self._generate_product_id(platform, name)
        
        locations = ['广东深圳', '浙江杭州', '江苏南京', '北京', '上海', '广东广州', '四川成都']
        
        return Product(
            platform=platform,
            name=name,
            price=round(price, 2),
            original_price=round(original_price, 2) if original_price else None,
            sales=sales,
            shop_name=f"{prefix}{shop_name}",
            shop_rating=shop_rating,
            url=f"{platform_info['base_url']}{product_id}",
            image_url=f"https://via.placeholder.com/200x200?text={prefix}+{model}",
            location=random.choice(locations),
            product_id=product_id,
            category=template.get('category', '数码产品'),
            tags=self._generate_tags(price, base_price, shop_rating, sales)
        )
    
    def _generate_tags(self, price: float, base_price: float, 
                       rating: float, sales: int) -> List[str]:
        tags = []
        
        if price < base_price * 0.8:
            tags.append('限时特惠')
        if sales > 10000:
            tags.append('热销爆款')
        if rating >= 4.8:
            tags.append('好评如潮')
        if sales > 5000 and rating >= 4.5:
            tags.append('品质之选')
        
        return tags

mock_generator = MockDataGenerator()
