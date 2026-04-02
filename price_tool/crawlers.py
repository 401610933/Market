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
        },
        '智能音箱': {
            'prefixes': ['小米', '天猫精灵', '小度', '苹果', '华为', '百度', '小爱同学', 'HomePod'],
            'models': ['小爱音箱Pro', '天猫精灵X5', '小度X8', 'HomePod mini', 'Sound 4', '音响Pro', '智能音响'],
            'base_price': 200,
            'price_variance': 800,
            'specs': ['标准版', 'Pro版', '带屏幕', '立体声', '便携版']
        },
        '智能门锁': {
            'prefixes': ['小米', '凯迪仕', '德施曼', '鹿客', '飞利浦', '三星', 'TCL', '华为智选'],
            'models': ['全自动', '指纹锁', '密码锁', '人脸识别', '猫眼版', '可视对讲', 'Pro'],
            'base_price': 1500,
            'price_variance': 2000,
            'specs': ['指纹+密码', '人脸识别', '猫眼可视', 'WiFi直连', 'NFC解锁']
        },
        '电动牙刷': {
            'prefixes': ['飞利浦', '欧乐B', '小米', '素士', '松下', '博朗', '华为智选', 'usmile'],
            'models': ['声波电动牙刷', '钻石系列', 'Sonicare', 'Pro系列', 'Ultra', '青春版', '护龈款'],
            'base_price': 200,
            'price_variance': 800,
            'specs': ['基础款', '升级款', '专业款', '礼盒装', '含替换刷头']
        },
        '空气净化器': {
            'prefixes': ['小米', '飞利浦', '布鲁雅尔', '霍尼韦尔', '松下', '戴森', '美的', '格力'],
            'models': ['Pro H', 'AC4076', 'Blueair 280i', 'KJ500', '空气净化器', '除醛款', '智能款'],
            'base_price': 1500,
            'price_variance': 3000,
            'specs': ['除甲醛', '除PM2.5', '除菌', '智能控制', '静音模式']
        },
        '加湿器': {
            'prefixes': ['小米', '飞利浦', '戴森', '美的', '格力', '亚都', '小熊', '智米'],
            'models': ['无雾加湿器', '蒸发式', '超声波', 'Pro', '智能加湿器', '除菌款', '静音款'],
            'base_price': 300,
            'price_variance': 1000,
            'specs': ['4L大容量', '智能恒湿', '除菌净化', '静音模式', 'App控制']
        },
        '扫地机器人': {
            'prefixes': ['科沃斯', '石头', '小米', '追觅', '云鲸', 'iRobot', '美的', '海尔'],
            'models': ['T20 Pro', 'G20', '扫地机器人2', 'X30', 'J3', 'i7+', '全能基站款'],
            'base_price': 3000,
            'price_variance': 5000,
            'specs': ['扫拖一体', '自动集尘', '自动洗拖布', '热风烘干', '全能基站']
        },
        '投影仪': {
            'prefixes': ['极米', '坚果', '小米', '当贝', '爱普生', '明基', '索尼', '海信'],
            'models': ['H6 Pro', 'J10S', '投影仪2', 'X3', '4K投影仪', '智能投影', '激光电视'],
            'base_price': 3000,
            'price_variance': 5000,
            'specs': ['1080P', '4K', '激光光源', '自动对焦', '梯形校正']
        },
        '电视': {
            'prefixes': ['小米', '海信', 'TCL', '创维', '索尼', '三星', 'LG', '华为智慧屏'],
            'models': ['Redmi MAX', '85英寸', '量子点', 'OLED', 'Mini LED', '游戏电视', '智能电视'],
            'base_price': 3000,
            'price_variance': 10000,
            'specs': ['55英寸', '65英寸', '75英寸', '85英寸', '4K/8K']
        },
        '冰箱': {
            'prefixes': ['海尔', '美的', '西门子', '容声', '卡萨帝', '松下', '三星', 'LG'],
            'models': ['对开门', '十字对开门', '多门', '法式多门', '超薄款', '大容量', '变频节能'],
            'base_price': 3000,
            'price_variance': 8000,
            'specs': ['风冷无霜', '变频', '智能控制', '大容量', '超薄嵌入']
        },
        '洗衣机': {
            'prefixes': ['海尔', '美的', '西门子', '小天鹅', '松下', 'LG', '三星', '卡萨帝'],
            'models': ['滚筒', '波轮', '洗烘一体', '热泵烘干', '超薄款', '大容量', '智能投放'],
            'base_price': 2500,
            'price_variance': 6000,
            'specs': ['10kg', '洗烘一体', '热泵烘干', '除菌洗', '智能控制']
        },
        '空调': {
            'prefixes': ['格力', '美的', '海尔', '奥克斯', '小米', 'TCL', '海信', '科龙'],
            'models': ['冷静王', '风尊', '新一级能效', '立柜式', '挂机', '中央空调', '新风空调'],
            'base_price': 3000,
            'price_variance': 8000,
            'specs': ['1.5匹', '2匹', '3匹', '新一级能效', '变频节能']
        },
        '微波炉': {
            'prefixes': ['美的', '格兰仕', '松下', '东芝', '海尔', '小米', '方太', '老板'],
            'models': ['智能微波炉', '光波炉', '蒸烤一体机', '变频', '微蒸烤', '家用款'],
            'base_price': 600,
            'price_variance': 2000,
            'specs': ['23L', '平板式', '变频', '智能菜单', '微蒸烤一体']
        },
        '电烤箱': {
            'prefixes': ['海氏', '长帝', '美的', '柏翠', '松下', '凯度', '老板', '方太'],
            'models': ['C40', '搪瓷内胆', '风炉', '蒸烤箱', '嵌入式', '台式', '专业烘焙'],
            'base_price': 800,
            'price_variance': 3000,
            'specs': ['40L', '搪瓷内胆', '热风循环', '智能控温', '双层玻璃']
        },
        '吸尘器': {
            'prefixes': ['戴森', '小狗', '美的', '追觅', '小米', '莱克', '飞利浦', '松下'],
            'models': ['V15', 'T12', '无线吸尘器', '手持吸尘器', '除螨仪', '激光探测', '智能款'],
            'base_price': 1500,
            'price_variance': 3500,
            'specs': ['无线手持', '激光探测', '60分钟续航', '智能感应', '除螨刷头']
        },
        '吹风机': {
            'prefixes': ['戴森', '松下', '飞利浦', '小米', '素士', '徕芬', '飞科', '追觅'],
            'models': ['HD08', 'NA9C', '高速吹风机', '负离子', '水光离子', '护发', '便携款'],
            'base_price': 300,
            'price_variance': 2500,
            'specs': ['高速马达', '负离子', '恒温护发', '多档调节', '低噪音']
        },
        '咖啡机': {
            'prefixes': ['雀巢', '德龙', '飞利浦', '西门子', '松下', '柏翠', '小米', '小熊'],
            'models': ['胶囊咖啡机', '全自动', '半自动', '意式', '美式', '滴滤式', '便携款'],
            'base_price': 500,
            'price_variance': 4000,
            'specs': ['胶囊式', '全自动', '意式浓缩', '奶泡系统', '一键制作']
        },
        '电饭煲': {
            'prefixes': ['美的', '苏泊尔', '九阳', '松下', '虎牌', '象印', '小米', '飞利浦'],
            'models': ['IH电饭煲', '智能预约', '球釜', '柴火饭', '低糖', '快速煮', '多功能'],
            'base_price': 300,
            'price_variance': 1500,
            'specs': ['4L容量', 'IH加热', '球釜内胆', '智能预约', '低糖功能']
        },
        '运动鞋': {
            'prefixes': ['耐克', '阿迪达斯', '李宁', '安踏', '特步', '361度', '乔丹', '鸿星尔克'],
            'models': ['Air Max', 'Ultraboost', '韦德之道', 'KT系列', '竞速跑鞋', '篮球鞋', '休闲鞋'],
            'base_price': 400,
            'price_variance': 1000,
            'specs': ['42码', '43码', '44码', '41码', '40码']
        },
        '羽绒服': {
            'prefixes': ['波司登', '优衣库', '北面', '加拿大鹅', '安踏', '李宁', '阿迪达斯', '耐克'],
            'models': ['极寒系列', '轻薄款', '中长款', '短款', '户外款', '鹅绒', '鸭绒'],
            'base_price': 800,
            'price_variance': 2000,
            'specs': ['90%白鹅绒', '800蓬松度', '防风防水', '连帽款', '短款/长款']
        },
        '牛仔裤': {
            'prefixes': ['李维斯', 'Lee', 'Wrangler', '优衣库', 'GAP', '杰克琼斯', 'ZARA', 'H&M'],
            'models': ['501', '经典直筒', '修身小脚', '宽松版型', '复古款', '破洞款', '原色'],
            'base_price': 300,
            'price_variance': 800,
            'specs': ['29码', '30码', '31码', '32码', '蓝色/黑色']
        },
        'T恤': {
            'prefixes': ['优衣库', 'GAP', 'ZARA', 'H&M', '耐克', '阿迪达斯', '李宁', '安踏'],
            'models': ['纯棉', '圆领', 'V领', '印花', '纯色', '重磅', '速干'],
            'base_price': 100,
            'price_variance': 300,
            'specs': ['M码', 'L码', 'XL码', 'XXL码', '多色可选']
        },
        '连衣裙': {
            'prefixes': ['ZARA', 'H&M', '优衣库', 'ONLY', 'VERO MODA', '伊芙丽', '太平鸟', '欧时力'],
            'models': ['碎花', '纯色', '雪纺', '针织', '法式', '通勤', '度假风'],
            'base_price': 300,
            'price_variance': 800,
            'specs': ['S码', 'M码', 'L码', 'XL码', '长款/短款']
        },
        '化妆品': {
            'prefixes': ['兰蔻', '雅诗兰黛', '资生堂', 'SK-II', '香奈儿', '迪奥', '海蓝之谜', '赫莲娜'],
            'models': ['小黑瓶', '小棕瓶', '神仙水', '精华液', '面霜', '眼霜', '粉底液'],
            'base_price': 500,
            'price_variance': 2000,
            'specs': ['30ml', '50ml', '75ml', '100ml', '正装/小样']
        },
        '口红': {
            'prefixes': ['迪奥', '香奈儿', 'MAC', 'YSL', '兰蔻', '阿玛尼', '纪梵希', 'NARS'],
            'models': ['999', '丝绒', '哑光', '缎光', '唇釉', '唇膏', '限定款'],
            'base_price': 300,
            'price_variance': 400,
            'specs': ['正红色', '豆沙色', '复古红', '珊瑚色', '多色号']
        },
        '香水': {
            'prefixes': ['香奈儿', '迪奥', '祖马龙', '汤姆福特', '古驰', '宝格丽', '爱马仕', '普拉达'],
            'models': ['5号', '真我', '蓝风铃', '乌木沉香', '花悦', '大吉岭茶', '大地'],
            'base_price': 600,
            'price_variance': 1500,
            'specs': ['30ml', '50ml', '100ml', 'EDT/EDP', '礼盒装']
        },
        '零食': {
            'prefixes': ['三只松鼠', '良品铺子', '百草味', '来伊份', '洽洽', '旺旺', '奥利奥', '乐事'],
            'models': ['坚果礼盒', '薯片', '饼干', '巧克力', '牛肉干', '芒果干', '零食大礼包'],
            'base_price': 50,
            'price_variance': 200,
            'specs': ['500g', '1kg', '礼盒装', '混合装', '单口味']
        },
        '茶叶': {
            'prefixes': ['天福茗茶', '八马茶业', '中茶', '武夷星', '竹叶青', '吴裕泰', '张一元', '艺福堂'],
            'models': ['铁观音', '大红袍', '西湖龙井', '普洱茶', '茉莉花茶', '红茶', '绿茶'],
            'base_price': 200,
            'price_variance': 800,
            'specs': ['250g', '500g', '特级', '一级', '礼盒装']
        },
        '红酒': {
            'prefixes': ['张裕', '长城', '奔富', '拉菲', '黄尾袋鼠', '奥普斯', '蒙特斯', '干露'],
            'models': ['解百纳', '赤霞珠', '梅洛', '西拉', '干红', '干白', '甜白'],
            'base_price': 200,
            'price_variance': 1000,
            'specs': ['750ml', '单支', '双支礼盒', '整箱', '年份酒']
        },
        '牛奶': {
            'prefixes': ['伊利', '蒙牛', '特仑苏', '金典', '光明', '三元', '德亚', '安佳'],
            'models': ['纯牛奶', '低脂牛奶', '脱脂牛奶', '高钙奶', '有机奶', '酸奶', '早餐奶'],
            'base_price': 60,
            'price_variance': 100,
            'specs': ['250ml*12盒', '250ml*24盒', '1L*6盒', '整箱装', '礼盒装']
        },
        '大米': {
            'prefixes': ['五常', '稻花香', '金龙鱼', '福临门', '十月稻田', '柴火大院', '北大荒', '中粮'],
            'models': ['稻花香2号', '长粒香', '珍珠米', '泰国香米', '五常大米', '有机大米'],
            'base_price': 80,
            'price_variance': 200,
            'specs': ['5kg', '10kg', '25kg', '真空包装', '当季新米']
        },
        '食用油': {
            'prefixes': ['金龙鱼', '福临门', '鲁花', '多力', '胡姬花', '西王', '长寿花', '中粮'],
            'models': ['大豆油', '花生油', '菜籽油', '玉米油', '葵花籽油', '调和油', '橄榄油'],
            'base_price': 80,
            'price_variance': 150,
            'specs': ['5L', '4L', '10L', '物理压榨', '非转基因']
        },
        '书籍': {
            'prefixes': ['中信出版社', '人民文学', '商务印书馆', '机械工业', '电子工业', '湛庐文化', '磨铁', '读客'],
            'models': ['小说', '历史', '哲学', '科技', '经济', '管理', '心理', '励志'],
            'base_price': 50,
            'price_variance': 150,
            'specs': ['平装', '精装', '电子书', '套装', '珍藏版']
        },
        '玩具': {
            'prefixes': ['乐高', '美泰', '孩之宝', '万代', '奥迪双钻', '泡泡玛特', '迪士尼', '费雪'],
            'models': ['积木', '盲盒', '手办', '遥控车', '芭比', '变形金刚', '拼图', '益智玩具'],
            'base_price': 100,
            'price_variance': 500,
            'specs': ['适合3-6岁', '适合6-12岁', '成人收藏', '礼盒装', '限量版']
        },
        '文具': {
            'prefixes': ['晨光', '得力', '斑马', '百乐', '三菱', '国誉', '无印良品', '施耐德'],
            'models': ['中性笔', '钢笔', '笔记本', '文件夹', '订书机', '计算器', '剪刀', '笔筒'],
            'base_price': 30,
            'price_variance': 100,
            'specs': ['黑色', '蓝色', '红色', '0.5mm', '按动/盖帽']
        },
        '厨具': {
            'prefixes': ['双立人', '菲仕乐', '柳宗理', '苏泊尔', '九阳', '美的', '炊大皇', '爱仕达'],
            'models': ['炒锅', '汤锅', '蒸锅', '压力锅', '刀具', '菜板', '厨具套装', '不粘锅'],
            'base_price': 300,
            'price_variance': 1000,
            'specs': ['32cm', '34cm', '不锈钢', '铸铁', '陶瓷涂层']
        },
        '床上用品': {
            'prefixes': ['富安娜', '罗莱', '水星', '梦洁', '博洋', '多喜爱', '紫罗兰', '堂皇'],
            'models': ['四件套', '羽绒被', '蚕丝被', '羊毛被', '枕头', '床垫', '床单', '被套'],
            'base_price': 400,
            'price_variance': 1500,
            'specs': ['1.8m床', '2.0m床', '纯棉', '真丝', '磨毛']
        },
        '绿植': {
            'prefixes': ['绿萝', '发财树', '多肉', '吊兰', '虎皮兰', '芦荟', '龟背竹', '仙人掌'],
            'models': ['盆栽', '种子', '水培', '土培', '室内观叶', '开花植物', '观果植物'],
            'base_price': 30,
            'price_variance': 200,
            'specs': ['含花盆', '不含花盆', '小盆栽', '大盆栽', '多肉组合']
        },
        '宠物用品': {
            'prefixes': ['皇家', '渴望', '巅峰', '麦富迪', '顽皮', '伯纳天纯', '卫仕', '小佩'],
            'models': ['猫粮', '狗粮', '猫砂', '狗窝', '猫爬架', '宠物玩具', '牵引绳', '食盆'],
            'base_price': 100,
            'price_variance': 400,
            'specs': ['1.5kg', '5kg', '10kg', '成猫/幼猫', '成犬/幼犬']
        },
        '通用': {
            'prefixes': ['精选', '品质', '热销', '畅销', '新品', '特卖', '爆款', '推荐'],
            'models': ['商品', '产品', '好物', '精品', '优品', '精选', '特惠', '爆款'],
            'base_price': 200,
            'price_variance': 800,
            'specs': ['标准款', '升级款', '豪华款', '套装', '单品']
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
            '手机': ['手机', 'mate', 'iphone', '小米', '华为', '荣耀', 'oppo', 'vivo', '三星', 'phone', 'realme', '一加', '魅族'],
            '笔记本': ['笔记本', '电脑', 'laptop', 'macbook', 'thinkpad', '游戏本', '联想', '戴尔', '惠普', '华硕'],
            '耳机': ['耳机', 'earphone', 'airpods', 'freebuds', '降噪', 'tws', '索尼', 'bose', '森海塞尔', '漫步者'],
            '平板': ['平板', 'ipad', 'pad', 'tablet', 'matepad', '小米平板', '三星平板'],
            '手表': ['手表', 'watch', '手环', 'band', 'apple watch', '华为手表', '佳明', '智能手表'],
            '智能音箱': ['音箱', '音响', '天猫精灵', '小度', '小爱', 'homepod', '智能音箱', '蓝牙音箱'],
            '智能门锁': ['门锁', '智能门锁', '指纹锁', '密码锁', '凯迪仕', '德施曼', '鹿客'],
            '电动牙刷': ['电动牙刷', '牙刷', '飞利浦', '欧乐b', '素士', 'usmile', '声波牙刷'],
            '空气净化器': ['空气净化器', '净化器', '除甲醛', '飞利浦', '布鲁雅尔', '霍尼韦尔'],
            '加湿器': ['加湿器', '加湿', '无雾', '超声波', '蒸发式'],
            '扫地机器人': ['扫地机器人', '扫地机', '科沃斯', '石头', '追觅', '云鲸', 'irobot'],
            '投影仪': ['投影仪', '投影', '极米', '坚果', '当贝', '爱普生', '明基', '激光电视'],
            '电视': ['电视', '电视机', '海信', 'tcl', '创维', '索尼电视', '小米电视', '华为智慧屏'],
            '冰箱': ['冰箱', '电冰箱', '海尔', '美的', '西门子', '容声', '卡萨帝', '对开门'],
            '洗衣机': ['洗衣机', '洗烘', '滚筒', '波轮', '小天鹅', '松下', 'lg'],
            '空调': ['空调', '挂机', '立柜', '格力', '美的', '海尔', '奥克斯'],
            '微波炉': ['微波炉', '光波炉', '蒸烤箱', '格兰仕', '美的', '松下'],
            '电烤箱': ['烤箱', '电烤箱', '蒸烤箱', '海氏', '长帝', '柏翠', '烘焙'],
            '吸尘器': ['吸尘器', '无线吸尘器', '戴森', '小狗', '追觅', '除螨仪'],
            '吹风机': ['吹风机', '电吹风', '戴森', '松下', '素士', '徕芬', '高速'],
            '咖啡机': ['咖啡机', '咖啡', '胶囊', '德龙', '飞利浦', '雀巢', '意式'],
            '电饭煲': ['电饭煲', '电饭锅', '九阳', '苏泊尔', '美的', '虎牌', '象印', 'ih'],
            '运动鞋': ['运动鞋', '跑鞋', '篮球鞋', '耐克', '阿迪达斯', '李宁', '安踏', '乔丹', '特步'],
            '羽绒服': ['羽绒服', '羽绒', '鹅绒', '鸭绒', '波司登', '优衣库', '北面', '加拿大鹅'],
            '牛仔裤': ['牛仔裤', '牛仔', '李维斯', 'lee', 'wrangler', '修身', '直筒'],
            'T恤': ['t恤', '短袖', 't恤衫', '优衣库', 'gap', 'zara', '纯棉', '印花'],
            '连衣裙': ['连衣裙', '裙子', '长裙', '短裙', '碎花', '雪纺', 'zara', 'hm', 'only'],
            '化妆品': ['化妆品', '护肤', '精华', '面霜', '眼霜', '兰蔻', '雅诗兰黛', '资生堂', 'sk-ii'],
            '口红': ['口红', '唇膏', '唇釉', '迪奥', '香奈儿', 'mac', 'ysl', '阿玛尼', '纪梵希'],
            '香水': ['香水', '淡香水', '浓香水', '香奈儿', '迪奥', '祖马龙', '汤姆福特', '古驰'],
            '零食': ['零食', '小吃', '坚果', '薯片', '饼干', '巧克力', '三只松鼠', '良品铺子', '百草味'],
            '茶叶': ['茶叶', '茶', '铁观音', '大红袍', '龙井', '普洱', '花茶', '红茶', '绿茶'],
            '红酒': ['红酒', '葡萄酒', '干红', '干白', '张裕', '长城', '奔富', '拉菲', '黄尾袋鼠'],
            '牛奶': ['牛奶', '纯牛奶', '酸奶', '特仑苏', '金典', '伊利', '蒙牛', '光明'],
            '大米': ['大米', '米', '稻花香', '五常', '金龙鱼', '福临门', '东北大米'],
            '食用油': ['食用油', '油', '花生油', '大豆油', '菜籽油', '橄榄油', '金龙鱼', '鲁花', '福临门'],
            '书籍': ['书籍', '书', '图书', '小说', '历史', '哲学', '中信', '人民文学', '商务印书馆'],
            '玩具': ['玩具', '积木', '乐高', '芭比', '变形金刚', '盲盒', '手办', '迪士尼', '费雪'],
            '文具': ['文具', '笔', '笔记本', '文件夹', '晨光', '得力', '斑马', '百乐', '无印良品'],
            '厨具': ['厨具', '锅', '炒锅', '汤锅', '刀具', '双立人', '菲仕乐', '苏泊尔', '九阳'],
            '床上用品': ['床上用品', '四件套', '被套', '床单', '被子', '枕头', '富安娜', '罗莱', '水星'],
            '绿植': ['绿植', '盆栽', '花', '多肉', '绿萝', '发财树', '吊兰', '仙人掌', '龟背竹'],
            '宠物用品': ['宠物', '猫粮', '狗粮', '猫砂', '狗窝', '皇家', '渴望', '麦富迪', '小佩']
        }
        
        for category, keywords in category_keywords.items():
            for kw in keywords:
                if kw in keyword_lower:
                    return category
        
        return '通用'
    
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
        base_price = max(base_price, template['base_price'] * 0.5)
        base_price *= platform_info['price_factor']
        
        price_variance = random.uniform(-0.15, 0.2)
        price = base_price * (1 + price_variance)
        price = max(price, base_price * 0.6)
        
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
