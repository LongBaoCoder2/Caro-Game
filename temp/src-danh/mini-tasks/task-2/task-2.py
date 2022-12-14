import pygame
from pygame import gfxdraw

#khởi tạo pygame
pygame.init()

# khai báo hằng
STEP = 50
MAX_X = STEP * 32
MAX_Y = MAX_X * 9 // 16
BACKGROUND_COLORS = [(44, 202, 96), (20, 140, 80)]
LINE_COLOR = (255, 255, 255)
LINE_WIDTH = 4
COLS = MAX_X // STEP
ROWS = MAX_Y // STEP
RED = (255, 0, 0)
BLUE = (0, 0, 255)
SYMBOL_WIDTH = 6

#tạo cửa sổ giao diện trong pygame
screen = pygame.display.set_mode((MAX_X + LINE_WIDTH - 1, MAX_Y + LINE_WIDTH - 1))
pygame.display.set_caption("Bai tap 1")

# https://youtu.be/vnd3RfeG3NM?t=1287
def draw_board():
  global screen
  #screen.fill(BACKGROUND_COLOR)
  for i in range(0, ROWS):
    for j in range(0, COLS):
      pygame.draw.rect(screen, BACKGROUND_COLORS[(i + j) % 2], (j * STEP, i * STEP, STEP, STEP))
  #hàm vẽ đoạn thẳng nối 2 điểm (x1, y1) và (x2, y2) có độ dày thickness
  for x in range(0, MAX_X + STEP, STEP):
    pygame.draw.line(screen, LINE_COLOR, (x, 0), (x, MAX_Y + LINE_WIDTH), LINE_WIDTH)
  for y in range(0, MAX_Y + STEP, STEP):
    pygame.draw.line(screen, LINE_COLOR, (0, y), (MAX_X + LINE_WIDTH, y), LINE_WIDTH)
  
draw_board()


# https://stackoverflow.com/questions/23852917/antialiasing-shapes-in-pygame
def draw_circle(surface, x, y, radius, color):
  gfxdraw.aacircle(surface, x, y, radius, color)
  #gfxdraw.filled_circle(surface, x, y, radius, color)
  
# https://stackoverflow.com/questions/64816341/how-do-you-draw-an-antialiased-circular-line-of-a-certain-thickness-how-to-set
def drawAACircle(surf, color, center : tuple, radius, width):
  gfxdraw.aacircle(surf, center[0], center[1], radius, color)  
  gfxdraw.aacircle(surf, center[0], center[1], radius-width, color)  
  pygame.draw.circle(surf, color, center, radius, width) 

def drawX(surface, color, x, y, radius, width):
  pygame.draw.line(surface, color, (x - radius, y - radius), (x + radius, y + radius), width)
  pygame.draw.line(surface, color, (x + radius, y - radius), (x - radius, y + radius), width)

#biến vòng lặp game
running = True
flag = 1

while running:
  # tạm dừng 0.25s
  pygame.time.delay(250)
  #xử lý sự kiện
  for event in pygame.event.get():
    #sự kiện thoát
    if event.type == pygame.QUIT:
      running = False
    #sự kiện chuột
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
      #nhấn chuột trái
      #vẽ hình tròn tại tọa độ
      (xClick, yClick) = tuple(event.pos)
      # xClick // STEP -> ra chỉ số cột của ô vuông đang bấm (một dạng nén tọa độ)
      # sau đó lấy chỉ số này nhân cho STEP ta ra được tọa độ góc trái trên
      # cộng x và y cho STEP // 2 ta ra tâm hình vuông
      centerX = xClick // STEP * STEP + STEP // 2
      centerY = yClick // STEP * STEP + STEP // 2
      #draw_circle(screen, centerX, centerY, radius = 21, color = dot[flag])
      radius = STEP // 2 - 4
      if flag:
        drawX(screen, RED, centerX, centerY, radius - 4, SYMBOL_WIDTH * 2)
      else:
        drawAACircle(screen, center = (centerX, centerY), radius = radius , color = BLUE, width = SYMBOL_WIDTH)
      # pygame.draw.circle(screen, dot[flag], (centerX, centerY) , radius = 21, width = 4)
      #đổi sang màu còn lại
      flag = 1 - flag
  #print(click)
  #vẽ tất cả lên màn hình
  pygame.display.update()

#thoát chương trình  
pygame.quit()