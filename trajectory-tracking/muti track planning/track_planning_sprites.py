import random
import numpy as np
import pygame


# 屏幕大小的常量
SCREEN_RECT = pygame.Rect(0, 0, 720, 720)
# 刷新的帧率
FRAME_PER_SEC = 60
# 创建小车的定时器常量
CREATE_CAR_EVENT = pygame.USEREVENT
# 定义圆形小车的大小（直径）
CAR_SIZE = 10
# 圆形小车颜色
CAR_COLOUR = [0,0,0]
# 使用连线命令画小车移动轨迹时需要两个初始点（就是你定义的小车初始坐标点）

# POINT_COLOUR = []
# car1相关参数
car1_TARGET_POSITION = (600,150)
car1_POINT_COLOUR_xy = []
car1_positionx = 100
car1_positiony = 620
car1_path_colour = (255,0,0)
car1_path_screen_colour = (255,0,0,255)
car1_track_colour = (0,255,0)
car1_track_screen_colour = (0,255,0,255)

# car1相关参数
car2_TARGET_POSITION = (600,300)
car2_POINT_COLOUR_xy = []
car2_positionx = 300
car2_positiony = 620
car2_path_colour = (0,0,255)
car2_path_screen_colour = (0,0,255,255)
car2_track_colour = (255,255,0)
car2_track_screen_colour = (255,255,0,255)

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
    def __init__(self, car_screen, positionx, positiony, car_speedx=1, car_speedy=1, k=1):     #car_speedx和car_speedy是小车的x和y方向的速度值，k是用来定义小车的速度变化值
        super().__init__()
        self.car_screen = car_screen
        self.car_speedx = car_speedx
        self.car_speedy = car_speedy
        self.positionx = positionx
        self.positiony = positiony
        self.init_positionx = positionx
        self.init_positiony = positiony
        self.k = k
        self.LINES_LIST = [(self.init_positionx,self.init_positiony),(self.init_positionx,self.init_positiony)]
        self.LINES_LIST_NEW = []
        self.path_point = []
    def car_add(self):
        pygame.draw.circle(self.car_screen,CAR_COLOUR,[self.positionx,self.positiony],CAR_SIZE,0)  #最后一个0表示填充，数字代表线宽
    
    def car_update(self):
        self.positionx += self.car_speedx
        self.positiony += self.car_speedy
        self.LINES_LIST.append((self.positionx,self.positiony))
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
    
    def key_test(self, car_right, car_left, car_up, car_down, car_accelerate, car_moderate):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[car_right]:
            self.car_speedx = self.k
        elif keys_pressed[car_left]:
            self.car_speedx = -self.k
        else:
            self.car_speedx = 0

        if keys_pressed[car_up]:
            self.car_speedy = -self.k
        elif keys_pressed[car_down]:
            self.car_speedy = self.k
        else:
            self.car_speedy = 0
        
        if keys_pressed[car_accelerate]:
            self.accelerate()
        elif keys_pressed[car_moderate]:
            self.moderate()
        elif keys_pressed[pygame.K_SPACE]:
            self.bracking()
        
        if keys_pressed[pygame.K_r]:
            self.env_restart()
    
    def detection_error(self, track_colour,error_POINT_COLOUR_xy):
        # c = 0
        d = 100000
        dis = 0
        for i in range(1,720):
            for j in range(1,720):
                a = tuple(pygame.Surface.get_at(self.car_screen,(i,j)))
                if a == track_colour:
                    self.path_point.append((i,j))

        for i in self.path_point:
            if not i in self.LINES_LIST_NEW:
                self.LINES_LIST_NEW.append(i)
        for i in self.LINES_LIST_NEW:
            d = 100000
            for j in error_POINT_COLOUR_xy:
                b = abs(i[0]-j[0])+abs(i[1]-j[1])
                if b<d:
                    d = b
                else:
                    d = d
                # if i[0] == j[0]:
                #     c += abs(i[1]-j[1])
            dis += d
        print(dis)
    
    def env_restart(self):
        self.LINES_LIST = [(self.init_positionx,self.init_positiony),(self.init_positionx,self.init_positiony)]
        self.LINES_LIST_NEW = []
        self.car_screen.fill((255,255,255))
        self.k = 1
        self.positionx = self.init_positionx
        self.positiony = self.init_positiony
