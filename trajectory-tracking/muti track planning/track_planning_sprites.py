import random
import pygame

# 屏幕大小的常量
SCREEN_RECT = pygame.Rect(0, 0, 720, 720)
# 刷新的帧率
FRAME_PER_SEC = 60
# 创建小车的定时器常量
CREATE_CAR_EVENT = pygame.USEREVENT
# 定义目标点的位置
TARGET_POSITION = [600,150]
# 定义圆形小车的大小（直径）
CAR_SIZE = 10
# 圆形小车颜色
CAR_COLOUR = [0,0,0]
LINES_LIST = [(100,620),(100,620)]


class TrackSprite(pygame.sprite.Sprite):
    """轨迹规划游戏精灵"""

    def __init__(self, image_name, speed=1):

        # 调用父类的初始化方法
        super().__init__()

        # 定义对象的属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):

        # 在屏幕的垂直方向上移动
        self.rect.y += self.speed

class Background(TrackSprite):
    """游戏背景精灵"""

    def __init__(self):

        # 1. 调用父类方法实现精灵的创建(image/rect/speed)
        super().__init__("./picture\TrackGamebackground.png")


class CarSimulation(pygame.sprite.Sprite):
    """小车仿真精灵"""
    def __init__(self, positionx, positiony, car_speedx=1, car_speedy=1, k=1):     #car_speedx和car_speedy是小车的x和y方向的速度值，k是用来定义小车的速度变化值
        super().__init__()
        self.car_speedx = car_speedx
        self.car_speedy = car_speedy
        self.positionx = positionx
        self.positiony = positiony
        self.k = k
    
    def car_add(self,car_screen):
        pygame.draw.circle(car_screen,CAR_COLOUR,[self.positionx,self.positiony],CAR_SIZE,0)  #最后一个0表示填充，数字代表线宽
    
    def car_update(self):
        self.positionx += self.car_speedx
        self.positiony += self.car_speedy
        LINES_LIST.append((self.positionx,self.positiony))
        # 控制小车不能离开屏幕
        if (self.positionx - CAR_SIZE/2)< 0:
            self.positionx = CAR_SIZE/2
        elif (self.positionx + CAR_SIZE/2)> SCREEN_RECT.right:
            self.positionx = SCREEN_RECT.right - CAR_SIZE/2

        if (self.positiony - CAR_SIZE/2)< 0:
            self.positiony = CAR_SIZE/2
        elif (self.positiony + CAR_SIZE/2)> SCREEN_RECT.bottom:
            self.positiony = SCREEN_RECT.bottom - CAR_SIZE/2
    
    def accelerate(self):
        self.k += 1

    def moderate(self):
        self.k -= 1
        if self.k <=0:
            self.k=0

    def bracking(self):
        pygame.time.delay(500)
        self.car_speedx = 0
        self.car_speedy = 0
