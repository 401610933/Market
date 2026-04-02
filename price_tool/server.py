#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from price_tool.engine import engine

app = Flask(__name__, static_folder='static')
CORS(app)

SAMPLE_DATA = {
    "keyword": "华为 Mate60",
    "products": [
        {
            "platform": "taobao",
            "name": "华为 Mate60 Pro 12GB+512GB 雅丹黑",
            "price": 6999.00,
            "original_price": 7999.00,
            "sales": 25000,
            "shop_name": "华为天猫官方旗舰店",
            "shop_rating": 4.9,
            "url": "https://item.taobao.com/item.htm?id=sample001",
            "image_url": "https://via.placeholder.com/200x200?text=Mate60+Pro",
            "location": "广东深圳",
            "product_id": "tb001",
            "tags": ["热销爆款", "好评如潮"]
        },
        {
            "platform": "jd",
            "name": "华为 Mate60 12GB+256GB 雅川青",
            "price": 5999.00,
            "original_price": None,
            "sales": 18000,
            "shop_name": "京东自营",
            "shop_rating": 4.8,
            "url": "https://item.jd.com/sample002",
            "image_url": "https://via.placeholder.com/200x200?text=Mate60",
            "location": "北京",
            "product_id": "jd001",
            "tags": ["品质之选"]
        },
        {
            "platform": "pdd",
            "name": "华为 Mate60 Pro 12GB+256GB 南糯紫",
            "price": 6499.00,
            "original_price": 7499.00,
            "sales": 35000,
            "shop_name": "拼多多官方店",
            "shop_rating": 4.7,
            "url": "https://mobile.yangkeduo.com/goods.html?goods_id=sample003",
            "image_url": "https://via.placeholder.com/200x200?text=Mate60+Pro",
            "location": "浙江杭州",
            "product_id": "pdd001",
            "tags": ["限时特惠", "热销爆款"]
        },
        {
            "platform": "taobao",
            "name": "华为 Mate60 8GB+256GB 雅丹黑",
            "price": 5499.00,
            "original_price": 5999.00,
            "sales": 12000,
            "shop_name": "华为品牌直销店",
            "shop_rating": 4.6,
            "url": "https://item.taobao.com/item.htm?id=sample004",
            "image_url": "https://via.placeholder.com/200x200?text=Mate60",
            "location": "广东深圳",
            "product_id": "tb002",
            "tags": ["品质之选"]
        },
        {
            "platform": "jd",
            "name": "华为 Mate60 Pro+ 16GB+512GB 宣白",
            "price": 8999.00,
            "original_price": None,
            "sales": 8000,
            "shop_name": "京东官方旗舰店",
            "shop_rating": 4.9,
            "url": "https://item.jd.com/sample005",
            "image_url": "https://via.placeholder.com/200x200?text=Mate60+Pro+",
            "location": "上海",
            "product_id": "jd002",
            "tags": ["好评如潮"]
        },
        {
            "platform": "pdd",
            "name": "华为 Mate60 12GB+512GB 雅川青",
            "price": 6299.00,
            "original_price": 6999.00,
            "sales": 22000,
            "shop_name": "百亿补贴店",
            "shop_rating": 4.5,
            "url": "https://mobile.yangkeduo.com/goods.html?goods_id=sample006",
            "image_url": "https://via.placeholder.com/200x200?text=Mate60",
            "location": "江苏南京",
            "product_id": "pdd002",
            "tags": ["限时特惠"]
        }
    ],
    "lowest_price": {
        "platform": "taobao",
        "name": "华为 Mate60 8GB+256GB 雅丹黑",
        "price": 5499.00,
        "shop_name": "华为品牌直销店"
    },
    "highest_price": {
        "platform": "jd",
        "name": "华为 Mate60 Pro+ 16GB+512GB 宣白",
        "price": 8999.00,
        "shop_name": "京东官方旗舰店"
    },
    "best_value": {
        "platform": "pdd",
        "name": "华为 Mate60 Pro 12GB+256GB 南糯紫",
        "price": 6499.00,
        "sales": 35000,
        "shop_rating": 4.7,
        "value_score": 0.856
    },
    "avg_price": 6715.67,
    "price_range": 3500.00,
    "total_products": 6,
    "platforms": ["taobao", "jd", "pdd"],
    "recommendations": [
        {
            "rank": 1,
            "name": "华为 Mate60 Pro 12GB+256GB 南糯紫",
            "platform": "pdd",
            "price": 6499.00,
            "recommendation_reason": "综合性价比最高，销量领先，优惠力度大(13%折扣)"
        },
        {
            "rank": 2,
            "name": "华为 Mate60 8GB+256GB 雅丹黑",
            "platform": "taobao",
            "price": 5499.00,
            "recommendation_reason": "价格最低，优惠力度大(8%折扣)"
        },
        {
            "rank": 3,
            "name": "华为 Mate60 12GB+256GB 雅川青",
            "platform": "jd",
            "price": 5999.00,
            "recommendation_reason": "店铺评分优秀，价格合理"
        }
    ],
    "platform_summary": {
        "taobao": {
            "count": 2,
            "min_price": 5499.00,
            "max_price": 6999.00,
            "avg_price": 6249.00,
            "total_sales": 37000
        },
        "jd": {
            "count": 2,
            "min_price": 5999.00,
            "max_price": 8999.00,
            "avg_price": 7499.00,
            "total_sales": 26000
        },
        "pdd": {
            "count": 2,
            "min_price": 6299.00,
            "max_price": 6499.00,
            "avg_price": 6399.00,
            "total_sales": 57000
        }
    }
}

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        keyword = data.get('keyword', '')
        platforms = data.get('platforms', ['taobao', 'jd', 'pdd'])
        count = data.get('count', 8)
        
        if not keyword:
            return jsonify({'error': '请输入搜索关键词'}), 400
        
        result = engine.search(
            keyword=keyword,
            platforms=platforms,
            count_per_platform=count
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sample', methods=['GET'])
def get_sample():
    return jsonify(SAMPLE_DATA)

@app.route('/api/platforms', methods=['GET'])
def get_platforms():
    return jsonify({
        'platforms': [
            {'id': 'taobao', 'name': '淘宝', 'color': '#FF6B00'},
            {'id': 'jd', 'name': '京东', 'color': '#E3393C'},
            {'id': 'pdd', 'name': '拼多多', 'color': '#E02E24'}
        ]
    })

if __name__ == '__main__':
    os.makedirs('static', exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
