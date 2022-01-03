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

    def __create_sprites(self):
        bg = Background()
        self.back_group = pygame.sprite.Group(bg)

        self.car1 = CarSimulation(self.screen,car1_positionx,car1_positiony)
        self.car2 = CarSimulation(self.screen,car2_positionx,car2_positiony)
        # self.car_group = pygame.sprite.Group(self.car1,self.car2)
    
    def start_game(self):
        print("游戏开始...")
        pygame.gfxdraw.bezier(self.screen, [(100,620),(300,300),(400,600),(600,150)], 5, car1_path_colour)
        self.get_xy(car1_path_screen_colour,car1_POINT_COLOUR_xy)
        pygame.gfxdraw.bezier(self.screen, [(300,620),(300,300),(400,600),(600,300)], 5, car2_path_colour)
        self.get_xy(car2_path_screen_colour,car2_POINT_COLOUR_xy)
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
    
    def get_xy(self,path_screen_colour,POINT_COLOUR_xy):
        b = 0
        for i in range(1,720):
            for j in range(1,720):
                a = tuple(pygame.Surface.get_at(self.screen,(i,j)))
                if a == path_screen_colour:
                    b += 1
                    POINT_COLOUR_xy.append((i,j))
        print(b)

    def __event_handler(self):
        for event in pygame.event.get():
            # 判断是否退出游戏
            if event.type == pygame.QUIT:
                self.car1.detection_error(car1_track_screen_colour,car1_POINT_COLOUR_xy)
                self.car2.detection_error(car2_track_screen_colour,car2_POINT_COLOUR_xy)
                TrackGame.__game_over()
                # 使用键盘提供的方法获取键盘按键 - 按键元组
        self.car1.key_test(pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN, pygame.K_z, pygame.K_x)
        self.car2.key_test(pygame.K_l, pygame.K_j, pygame.K_i, pygame.K_k, pygame.K_c, pygame.K_v)

    def __check_collide(self):
        print(self.car1.k)
        print(self.car2.k)
    def __update_sprites(self):
        self.back_group.draw(self.screen)
        pygame.draw.circle(self.screen,CAR_COLOUR,car1_TARGET_POSITION,CAR_SIZE,0)  #最后一个0表示填充，数字代表线宽
        # self.car_group.car_add(self.screen)
        pygame.gfxdraw.bezier(self.screen, [(car1_positionx,car1_positiony),(300,300),(400,600),car1_TARGET_POSITION], 5, car1_path_colour)
        pygame.draw.lines(self.screen, car1_track_colour, 0, self.car1.LINES_LIST)
        self.car1.car_add()
        self.car1.car_update()

        pygame.draw.circle(self.screen,CAR_COLOUR,car2_TARGET_POSITION,CAR_SIZE,0)  #最后一个0表示填充，数字代表线宽
        # self.car_group.car_add(self.screen)
        pygame.gfxdraw.bezier(self.screen, [(car2_positionx,car2_positiony),(300,300),(400,600),car2_TARGET_POSITION], 5, car2_path_colour)
        pygame.draw.lines(self.screen, car2_track_colour, 0, self.car2.LINES_LIST)
        self.car2.car_add()
        self.car2.car_update()

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
    game.car1.env_restart()
    game.car2.env_restart()
    # 启动游戏
    game.start_game()
