import pygame
from pygame import gfxdraw
from track_planning_sprites import *



class TrackGame(object):
    def __init__(self):
        print("游戏初始化")
        # 1. 创建游戏的窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 2. 创建游戏的时钟
        self.clock = pygame.time.Clock()
        # 3. 调用私有方法，精灵和精灵组的创建
        self.__create_sprites()
        self.LINES_LIST_NEW = []
        self.path_point = []

    def __create_sprites(self):
        bg = Background()
        self.back_group = pygame.sprite.Group(bg)

        self.car1 = CarSimulation(100,620)
        self.car2 = CarSimulation(300,620)
        self.car_group = pygame.sprite.Group(self.car1,self.car2)
    
    def start_game(self):
        print("游戏开始...")
        pygame.gfxdraw.bezier(self.screen, [(100,620),(300,300),(400,600),(600,150)], 5, (255,0,0))
        self.get_xy()
        while True:
            # 1. 设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            # 2. 事件监听
            self.__event_handler()
            # 3. 碰撞检测
            self.__check_collide()
            # 4. 更新/绘制精灵组
            self.__update_sprites()
            # 5. 更新显示
            pygame.display.update()
    
    def env_restart(self):
        self.car1.LINES_LIST = [(100,620),(100,620)]
        self.LINES_LIST_NEW = []
        self.screen.fill((255,255,255))
        self.car1.k = 1
        self.car1.positionx = 100
        self.car1.positiony = 620

    def detection_error(self):
        c = 0
        d = 0
        for i in range(1,720):
            for j in range(1,720):
                a = tuple(pygame.Surface.get_at(self.screen,(i,j)))
                if a == (0,255,0,255):
                    self.path_point.append((i,j))

        for i in self.path_point:
            if not i in self.LINES_LIST_NEW:
                self.LINES_LIST_NEW.append(i)
        for i in self.LINES_LIST_NEW:
            for j in POINT_COLOUR_xy:
                if i[0] == j[0]:
                    c += abs(i[1]-j[1])
                    d += 1

        print(c)
        
    
    def get_xy(self):
        b = 0
        for i in range(1,720):
            for j in range(1,720):
                a = tuple(pygame.Surface.get_at(self.screen,(i,j)))
                if a == (255,0,0,255):
                    b += 1
                    POINT_COLOUR_xy.append((i,j))
        print(b)

    def __event_handler(self):
        for event in pygame.event.get():
            # 判断是否退出游戏
            if event.type == pygame.QUIT:
                self.detection_error()
                TrackGame.__game_over()
                # 使用键盘提供的方法获取键盘按键 - 按键元组
        keys_pressed = pygame.key.get_pressed()
        # 判断元组中对应的按键索引值 1
        if keys_pressed[pygame.K_RIGHT]:
            self.car1.car_speedx = self.car1.k
        elif keys_pressed[pygame.K_LEFT]:
            self.car1.car_speedx = -self.car1.k
        else:
            self.car1.car_speedx = 0

        if keys_pressed[pygame.K_UP]:
            self.car1.car_speedy = -self.car1.k
        elif keys_pressed[pygame.K_DOWN]:
            self.car1.car_speedy = self.car1.k
        else:
            self.car1.car_speedy = 0
        
        if keys_pressed[pygame.K_z]:
            self.car1.accelerate()
        elif keys_pressed[pygame.K_x]:
            self.car1.moderate()
        elif keys_pressed[pygame.K_SPACE]:
            self.car1.bracking()
        
        if keys_pressed[pygame.K_r]:
            self.env_restart()

    def __check_collide(self):
        print(self.car1.k)

    def __update_sprites(self):
        self.back_group.draw(self.screen)
        pygame.draw.circle(self.screen,CAR_COLOUR,TARGET_POSITION,CAR_SIZE,0)  #最后一个0表示填充，数字代表线宽
        # self.car_group.car_add(self.screen)
        # print(type(self.car_group))
        self.car_group.car_speedx = 2
        pygame.gfxdraw.bezier(self.screen, [(100,620),(300,300),(400,600),(600,150)], 5, (255,0,0))
        pygame.draw.lines(self.screen, (0,255,0), 0, self.car1.LINES_LIST)
        self.car1.car_add(self.screen)
        self.car1.car_update()

        # self.car2.car_add(self.screen)
        # self.car2.car_update()

    @staticmethod
    def __game_over():
        print("游戏结束")

        pygame.quit()
        exit()

if __name__ == '__main__':
    pygame.init()
    # 创建游戏对象
    game = TrackGame()
    game.env_restart()
    # 启动游戏
    game.start_game()
