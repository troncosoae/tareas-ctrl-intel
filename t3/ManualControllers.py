import pygame
from Simulation import BasicController


# class MouseControler(BasicController):
#     def __init__(self):
#         self.controlling = False
#         self.max_u = 0.05*100

#     def next_u(self, error):
#         next_u = 0
#         for event in pygame.event.get():
#             if self.controlling:
#                 if event.type == pygame.MOUSEBUTTONUP:
#                     self.controlling = False
#                     next_u = 0
#                 if event.type == pygame.MOUSEMOTION:
#                     mouse_x, mouse_y = pygame.mouse.get_pos()
#                     print('position_mouse:', mouse_x, mouse_y)
#                     next_u = self.max_u*(self.window_w/2 - mouse_x)\
#                         / (self.window_w/2)
#         return next_u
