#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import sys
import os
from typing import List, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from price_tool.engine import engine

PLATFORM_NAMES = {
    'taobao': '淘宝',
    'jd': '京东',
    'pdd': '拼多多'
}

def print_header(title: str):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_product_table(products: List[dict], show_rank: bool = True):
    if not products:
        print("  暂无商品数据")
        return
    
    header = f"{'排名':<4} {'平台':<8} {'商品名称':<35} {'价格':<10} {'销量':<10} {'店铺评分':<8}"
    print(f"\n  {header}")
    print("  " + "-" * 85)
    
    for i, product in enumerate(products[:20], 1):
        platform = PLATFORM_NAMES.get(product.get('platform', ''), product.get('platform', ''))
        name = product.get('name', '')[:32] + "..." if len(product.get('name', '')) > 32 else product.get('name', '')
        price = f"¥{product.get('price', 0):.2f}"
        sales = product.get('sales', 0)
        if sales >= 10000:
            sales_str = f"{sales/10000:.1f}万"
        else:
            sales_str = str(sales)
        rating = f"{product.get('shop_rating', 0):.1f}"
        
        tags = product.get('tags', [])
        tag_str = f" [{', '.join(tags)}]" if tags else ""
        
        rank_str = f"{i:<4}" if show_rank else "    "
        print(f"  {rank_str} {platform:<8} {name:<35} {price:<10} {sales_str:<10} {rating:<8}{tag_str}")

def print_summary(result: dict):
    print_header("统计摘要")
    
    print(f"\n  关键词: {result.get('keyword', '')}")
    print(f"  商品总数: {result.get('total_products', 0)}")
    print(f"  涉及平台: {', '.join([PLATFORM_NAMES.get(p, p) for p in result.get('platforms', [])])}")
    print(f"\n  价格统计:")
    print(f"    - 最低价: ¥{result.get('lowest_price', {}).get('price', 0):.2f}")
    print(f"    - 最高价: ¥{result.get('highest_price', {}).get('price', 0):.2f}")
    print(f"    - 平均价: ¥{result.get('avg_price', 0):.2f}")
    print(f"    - 价格区间: ¥{result.get('price_range', 0):.2f}")

def print_best_value(result: dict):
    best = result.get('best_value')
    if not best:
        return
    
    print_header("性价比推荐")
    
    print(f"\n  推荐商品: {best.get('name', '')}")
    print(f"  平台: {PLATFORM_NAMES.get(best.get('platform', ''), best.get('platform', ''))}")
    print(f"  价格: ¥{best.get('price', 0):.2f}")
    print(f"  销量: {best.get('sales', 0)}")
    print(f"  店铺评分: {best.get('shop_rating', 0):.1f}")
    print(f"  店铺: {best.get('shop_name', '')}")
    print(f"  链接: {best.get('url', '')}")

def print_recommendations(recommendations: List[dict]):
    if not recommendations:
        return
    
    print_header("TOP 5 性价比推荐")
    
    for rec in recommendations:
        rank = rec.get('rank', 0)
        name = rec.get('name', '')
        platform = PLATFORM_NAMES.get(rec.get('platform', ''), rec.get('platform', ''))
        price = rec.get('price', 0)
        reason = rec.get('recommendation_reason', '')
        
        print(f"\n  #{rank} [{platform}] {name}")
        print(f"      价格: ¥{price:.2f}")
        print(f"      推荐理由: {reason}")

def print_platform_summary(summary: dict):
    if not summary:
        return
    
    print_header("各平台对比")
    
    for platform, data in summary.items():
        platform_name = PLATFORM_NAMES.get(platform, platform)
        print(f"\n  {platform_name}:")
        print(f"    - 商品数量: {data.get('count', 0)}")
        print(f"    - 最低价: ¥{data.get('min_price', 0):.2f}")
        print(f"    - 最高价: ¥{data.get('max_price', 0):.2f}")
        print(f"    - 平均价: ¥{data.get('avg_price', 0):.2f}")
        print(f"    - 总销量: {data.get('total_sales', 0)}")

def export_to_json(result: dict, output_file: str):
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n  结果已导出到: {output_file}")
    except Exception as e:
        print(f"\n  导出失败: {e}")

def export_to_csv(result: dict, output_file: str):
    try:
        products = result.get('products', [])
        
        with open(output_file, 'w', encoding='utf-8-sig') as f:
            f.write("排名,平台,商品名称,价格,原价,销量,店铺名称,店铺评分,链接\n")
            
            for i, p in enumerate(products, 1):
                platform = PLATFORM_NAMES.get(p.get('platform', ''), p.get('platform', ''))
                name = p.get('name', '').replace(',', '，')
                price = p.get('price', 0)
                original_price = p.get('original_price', '')
                sales = p.get('sales', 0)
                shop_name = p.get('shop_name', '').replace(',', '，')
                rating = p.get('shop_rating', 0)
                url = p.get('url', '')
                
                f.write(f"{i},{platform},{name},{price},{original_price},{sales},{shop_name},{rating},{url}\n")
        
        print(f"\n  结果已导出到: {output_file}")
    except Exception as e:
        print(f"\n  导出失败: {e}")

def main():
    parser = argparse.ArgumentParser(
        description='电商商品价格比较工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  %(prog)s "华为 Mate60"
  %(prog)s "华为 Mate60" -p taobao jd
  %(prog)s "iPhone 15" -p taobao -n 10 -o result.json
  %(prog)s "小米14" --format csv -o xiaomi.csv
        '''
    )
    
    parser.add_argument('keyword', help='搜索关键词')
    parser.add_argument('-p', '--platforms', nargs='+', 
                       choices=['taobao', 'jd', 'pdd'],
                       default=['taobao', 'jd', 'pdd'],
                       help='搜索平台 (默认: 全部)')
    parser.add_argument('-n', '--number', type=int, default=8,
                       help='每个平台获取的商品数量 (默认: 8)')
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('--format', choices=['json', 'csv'], default='json',
                       help='输出格式 (默认: json)')
    parser.add_argument('--no-detail', action='store_true',
                       help='不显示详细信息，只显示商品列表')
    
    args = parser.parse_args()
    
    print_header(f"搜索: {args.keyword}")
    print(f"\n  平台: {', '.join([PLATFORM_NAMES.get(p, p) for p in args.platforms])}")
    print(f"  每平台数量: {args.number}")
    
    print("\n  正在搜索...")
    
    try:
        result = engine.search(
            keyword=args.keyword,
            platforms=args.platforms,
            count_per_platform=args.number
        )
        
        print_summary(result)
        
        print_header("商品列表 (按价格排序)")
        print_product_table(result.get('products', []))
        
        if not args.no_detail:
            print_recommendations(result.get('recommendations', []))
            print_platform_summary(result.get('platform_summary', {}))
            print_best_value(result)
        
        if args.output:
            if args.format == 'json':
                export_to_json(result, args.output)
            else:
                export_to_csv(result, args.output)
        
        print("\n" + "=" * 60)
        print("  搜索完成!")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"\n  错误: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
