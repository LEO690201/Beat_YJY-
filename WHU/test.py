
import pygame
import sys
from pygame.locals import *

class CoordinatePicker:
    def __init__(self):
        # 初始化pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        
        # 窗口设置（与游戏窗口尺寸一致）
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("坐标拾取工具 - 点击获取8个洞口位置")
        
        # 存储点击的坐标
        self.coordinates = []
        self.max_points = 8  # 需要获取8个坐标
        
        # 加载背景图片（与游戏相同的加载方式）
        self.background = self.load_background()
        
    def load_background(self):
        """以与游戏相同的方式加载背景图片"""
        try:
            # 加载并缩放背景图片（不做透明处理）
            background = pygame.image.load('image1.png').convert()
            return pygame.transform.scale(background, (self.width, self.height))
        except Exception as e:
            print(f"图片加载错误: {e}")
            print("请确保image1.png与程序在同一目录下")
            pygame.quit()
            sys.exit()
    
    def draw(self):
        """绘制界面"""
        # 绘制背景
        self.screen.blit(self.background, (0, 0))
        
        # 显示提示文字
        font = pygame.font.SysFont("SimHei", 24)
        info_text = f"已选择 {len(self.coordinates)}/{self.max_points} 个位置"
        text_surface = font.render(info_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (20, 20))
        
        # 绘制已选择的点
        for i, (x, y) in enumerate(self.coordinates):
            # 绘制点
            pygame.draw.circle(self.screen, (0, 255, 0), (x, y), 5)
            # 显示坐标文字
            coord_text = f"({x}, {y})"
            coord_surface = font.render(coord_text, True, (255, 255, 0))
            self.screen.blit(coord_surface, (x + 10, y - 10))
        
        # 显示完成提示
        if len(self.coordinates) == self.max_points:
            done_text = "已获取8个位置！坐标已输出到控制台"
            done_surface = font.render(done_text, True, (0, 255, 255))
            self.screen.blit(done_surface, (20, 60))
        
        pygame.display.flip()
    
    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:  # 左键点击
                if len(self.coordinates) < self.max_points:
                    # 记录点击坐标
                    self.coordinates.append(event.pos)
                    # 打印到控制台
                    print(f"已添加位置 {len(self.coordinates)}: {event.pos}")
                # 如果已收集8个点，打印完整列表
                if len(self.coordinates) == self.max_points:
                    print("\n坐标列表（可直接复制到游戏代码中）：")
                    print("self.hole_positions = [")
                    for coord in self.coordinates:
                        print(f"    ({coord[0]}, {coord[1]}),")
                    print("]")
    
    def run(self):
        """主循环"""
        while True:
            self.handle_events()
            self.draw()
            self.clock.tick(60)

if __name__ == "__main__":
    picker = CoordinatePicker()
    picker.run()