import pygame

#khởi tạo pygame
pygame.init()

# khai báo hằng
MAX_X = 1000
MAX_Y = 750
BACKGROUND_COLORS = [(44, 202, 96), (20, 140, 80)]
LINE_COLOR = (255, 255, 255)
LINE_WIDTH = 4
STEP = 50
COLS = MAX_X // STEP
ROWS = MAX_Y // STEP

#tạo cửa sổ giao diện trong pygame
screen = pygame.display.set_mode((MAX_X+ LINE_WIDTH - 1, MAX_Y + LINE_WIDTH - 1))
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

#biến vòng lặp game
running = True
dot = [(255, 0, 0), (0, 0, 255)]
flag = 0

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
      pygame.draw.circle(screen, dot[flag], tuple(event.pos), 5)
      #đổi sang màu còn lại
      flag = 1 - flag
  #print(click)
  #vẽ tất cả lên màn hình
  pygame.display.update()

#thoát chương trình  
pygame.quit()
  
  
      


