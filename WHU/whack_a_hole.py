import pygame
import random
import time
import sys
from pygame.locals import *

class WhackAMole:
    def __init__(self):
        # 初始化pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        
        # 游戏窗口设置
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("打地鼠游戏")
        
        # 定义8个洞口位置（根据100x100图片尺寸优化坐标）
        # self.hole_positions = [
        #     (200, 220), (400, 220), (600, 220),  # 第一行洞口（略微下移适配大图片）
        #     (200, 370), (400, 370), (600, 370),  # 第二行洞口
        #     (200, 520), (400, 520)               # 第三行洞口
        # ]
        self.hole_positions = [
            (225, 456),
            (541, 446),
            (332, 399),
            (569, 399),
            (566, 362),
            (302, 364),
            (460, 363),
            (755, 363),
        ]
        
        # 游戏状态变量
        self.filled_holes = set()  # 已被填满的洞口索引
        self.current_moles = []    # 当前显示的地鼠
        self.game_over = False     # 游戏是否结束
        self.game_win = False      # 游戏是否胜利
        self.game_over_time = 0    # 游戏结束时间
        self.red_border = False    # 是否显示红色边框
        self.red_border_end = 0    # 红色边框结束时间
        
        # 进度图片排列参数
        self.progress_cols = 5  # 每行显示5个进度图片
        self.progress_spacing = 10  # 图片间距
        self.progress_row_offset = 60  # 两行之间的垂直距离
        
        # 加载游戏图片（包含白底透明化处理和尺寸调整）
        self.images = self.load_images()
        
    def make_white_transparent(self, image):
        """将图片中的白色背景转换为透明"""
        image = image.convert_alpha()
        
        # 遍历所有像素，将白色(接近白色)的像素设为透明
        for x in range(image.get_width()):
            for y in range(image.get_height()):
                r, g, b, a = image.get_at((x, y))
                # 如果颜色接近白色，设置为透明
                if r > 240 and g > 240 and b > 240:
                    image.set_at((x, y), (r, g, b, 0))  # 设置alpha为0（完全透明）
        
        return image
    
    def load_images(self):
        """加载游戏所需的所有图片，并处理白底透明化和尺寸调整"""
        images = {}
        try:
            # 加载背景图片（缩放到窗口大小）
            images['background'] = pygame.image.load('image1.png').convert()
            images['background'] = pygame.transform.scale(images['background'], (self.width, self.height))
            
            # 加载地鼠图片（白底转透明，缩放至100x100）
            target_size = (100, 100)  # 统一设置目标尺寸为100x100
            images['moles'] = [
                pygame.transform.scale(self.make_white_transparent(pygame.image.load('image2.png')), target_size),
                pygame.transform.scale(self.make_white_transparent(pygame.image.load('image3.png')), target_size),
                pygame.transform.scale(self.make_white_transparent(pygame.image.load('image4.png')), target_size),
                pygame.transform.scale(self.make_white_transparent(pygame.image.load('image5.png')), target_size)
            ]
            
            # 加载锤子图片（白底转透明，缩放至100x100）
            images['hammer'] = pygame.transform.scale(
                self.make_white_transparent(pygame.image.load('image6.png')), 
                (100, 100)  # 锤子尺寸调整为100x100
            )
            
            # 加载打击特效图片（白底转透明，缩放至100x100）
            images['hit_effect'] = pygame.transform.scale(
                self.make_white_transparent(pygame.image.load('image7.png')), 
                target_size
            )
            
            # 加载已填充洞口的图片（白底转透明，缩放至100x100）
            images['filled_hole'] = pygame.transform.scale(
                self.make_white_transparent(pygame.image.load('image8.png')), 
                target_size
            )
            
            # 加载进度图片（保持原始大小，约150x50）
            images['progress'] = [
                pygame.image.load('image9.png').convert_alpha(),   # 索引0
                pygame.image.load('image10.png').convert_alpha(),  # 索引1
                pygame.image.load('image11.png').convert_alpha(),  # 索引2
                pygame.image.load('image12.png').convert_alpha(),  # 索引3
                pygame.image.load('image13.png').convert_alpha(),  # 索引4
                pygame.image.load('image14.png').convert_alpha(),  # 索引5
                pygame.image.load('image15.png').convert_alpha(),  # 索引6
                pygame.image.load('image16.png').convert_alpha()   # 索引7
            ]
            
            # 加载游戏结束图片（失败，保持200x200）
            images['game_over'] = pygame.transform.scale(
                pygame.image.load('image17.png').convert_alpha(), 
                (200, 200)
            )
            
            # 加载游戏胜利图片（全屏显示）
            images['game_win'] = pygame.image.load('image18.png').convert()
            images['game_win'] = pygame.transform.scale(images['game_win'], (self.width, self.height))
            
        except Exception as e:
            print(f"图片加载错误: {e}")
            print("请确保image1.png到image18.png文件与游戏程序在同一目录下")
            pygame.quit()
            sys.exit()
            
        return images
    
    def create_mole(self):
        """随机在未被填充的洞口创建一个地鼠"""
        # 找出所有未被填充的洞口
        available_holes = [i for i in range(8) if i not in self.filled_holes]
        
        if not available_holes:
            return  # 所有洞口都被填充，游戏胜利
        
        # 随机选择一个洞口和地鼠类型
        hole_idx = random.choice(available_holes)
        mole_type = random.randint(0, 3)  # 4种地鼠图片
        
        # 记录地鼠出现的时间和位置
        return {
            'hole_idx': hole_idx,
            'type': mole_type,
            'appear_time': time.time(),
            'hit': False,
            'hit_time': 0
        }
    
    def check_mole_hit(self, mole, mouse_pos):
        """检查鼠标点击是否击中地鼠（适配100x100图片尺寸）"""
        x, y = self.hole_positions[mole['hole_idx']]
        # 获取地鼠图片的实际大小
        mole_img = self.images['moles'][mole['type']]
        mole_width, mole_height = mole_img.get_size()
        # 根据100x100图片尺寸创建碰撞检测区域
        mole_rect = pygame.Rect(
            x - mole_width // 2, 
            y - mole_height // 2, 
            mole_width, 
            mole_height
        )
        return mole_rect.collidepoint(mouse_pos)
    
    def update(self):
        """更新游戏状态"""
        if self.game_over:
            # 检查游戏结束后是否已超过3秒，超过则退出
            if time.time() - self.game_over_time > 3:
                pygame.quit()
                sys.exit()
            return
        
        # 检查是否需要生成新地鼠（调整概率适配更大图片）
        if not self.current_moles and random.random() < 0.12:  # 略微提高生成概率
            new_mole = self.create_mole()
            if new_mole:  # 确保成功创建了地鼠
                self.current_moles.append(new_mole)
        
        # 检查地鼠是否超时未被击中（适配更大图片延长显示时间）
        current_time = time.time()
        for mole in self.current_moles[:]:
            if not mole['hit'] and current_time - mole['appear_time'] > 2.5:  # 延长至2.5秒
                # 地鼠超时未被击中，游戏结束（失败）
                self.game_over = True
                self.game_win = False
                self.game_over_time = current_time
                self.red_border = True
                self.red_border_end = current_time + 2
                return
        
        # 移除显示时间已足够的击中特效
        self.current_moles = [
            mole for mole in self.current_moles 
            if not (mole['hit'] and current_time - mole['hit_time'] > 0.6)  # 略微延长特效时间
        ]
    
    def draw(self):
        """绘制游戏画面（适配100x100图片尺寸）"""
        # 绘制背景
        self.screen.blit(self.images['background'], (0, 0))
        
        # 绘制已填充的洞口
        for hole_idx in self.filled_holes:
            x, y = self.hole_positions[hole_idx]
            hole_img = self.images['filled_hole']
            hole_width, hole_height = hole_img.get_size()
            # 居中绘制100x100的填充洞口图片
            self.screen.blit(hole_img, (x - hole_width // 2, y - hole_height // 2))
        
        # 绘制地鼠和击中特效
        for mole in self.current_moles:
            x, y = self.hole_positions[mole['hole_idx']]
            if mole['hit']:
                # 绘制击中特效
                effect_img = self.images['hit_effect']
                effect_width, effect_height = effect_img.get_size()
                self.screen.blit(effect_img, (x - effect_width // 2, y - effect_height // 2))
            else:
                # 绘制地鼠
                mole_img = self.images['moles'][mole['type']]
                mole_width, mole_height = mole_img.get_size()
                self.screen.blit(mole_img, (x - mole_width // 2, y - mole_height // 2))
        
        # 绘制进度图片（保持两行排列）
        progress_count = len(self.filled_holes)
        for i in range(progress_count):
            progress_img = self.images['progress'][i]
            img_width = progress_img.get_width()
            
            # 计算行和列位置
            row = i // self.progress_cols  # 0表示第一行，1表示第二行
            col = i % self.progress_cols   # 列索引
            
            # 计算x坐标：左侧边距 + 列索引*(图片宽度+间距)
            x = 20 + col * (img_width + self.progress_spacing)
            # 计算y坐标：顶部边距 + 行索引*行偏移量
            y = 20 + row * self.progress_row_offset
            
            self.screen.blit(progress_img, (x, y))
        
        # 绘制锤子（跟随鼠标，适配100x100尺寸）
        mouse_pos = pygame.mouse.get_pos()
        hammer_img = self.images['hammer']
        hammer_width, hammer_height = hammer_img.get_size()
        # 调整锤子图片位置，使其看起来是用锤子尖点击
        self.screen.blit(hammer_img, (mouse_pos[0] - hammer_width // 2, mouse_pos[1] - hammer_height // 2))
        
        # 绘制游戏结束画面
        if self.game_over:
            if self.game_win:
                # 显示胜利图片（全屏）
                self.screen.blit(self.images['game_win'], (0, 0))
            else:
                # 显示失败图片（窗口靠上位置）
                go_img = self.images['game_over']
                go_width, go_height = go_img.get_size()
                # 计算位置使其靠上居中显示
                x = self.width // 2 - go_width // 2
                y = 50  # 距离顶部50像素
                self.screen.blit(go_img, (x, y))
        
        # 绘制红色边框（仅失败时）
        if self.red_border and time.time() < self.red_border_end:
            pygame.draw.rect(self.screen, (255, 0, 0), 
                             (0, 0, self.width, self.height), 5)
        elif self.red_border:
            self.red_border = False
        
        # 更新显示
        pygame.display.flip()
    
    def handle_events(self):
        """处理用户输入事件"""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:  # 左键点击
                if not self.game_over:
                    self.handle_click(event.pos)
    
    def handle_click(self, mouse_pos):
        """处理鼠标点击事件（适配100x100图片的碰撞检测）"""
        for mole in self.current_moles:
            if not mole['hit'] and self.check_mole_hit(mole, mouse_pos):
                # 击中地鼠
                mole['hit'] = True
                mole['hit_time'] = time.time()
                self.filled_holes.add(mole['hole_idx'])
                
                # 检查是否所有洞口都被填充
                if len(self.filled_holes) == 8:
                    self.game_over = True
                    self.game_win = True  # 标记为胜利
                    self.game_over_time = time.time()
                return
    
    def run(self):
        """游戏主循环"""
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

if __name__ == "__main__":
    game = WhackAMole()
    game.run()