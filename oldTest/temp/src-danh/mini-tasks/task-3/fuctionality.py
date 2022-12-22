from constants import *
import pygame
from pygame import gfxdraw

#global variables
#biến vòng lặp game
running = True
flag = 1
screen = None
# board[x][y]: toa do (X // STEP, Y // STEP)
board = [[0 for j in range(ROWS)] for i in range(COLS)]

def start_caro(name : str):
  global screen
  #khởi tạo pygame
  pygame.init()
  #tạo cửa sổ giao diện trong pygame
  screen = pygame.display.set_mode((MAX_X + LINE_WIDTH - 1, MAX_Y + LINE_WIDTH - 1))
  pygame.display.set_caption(name)

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
  pygame.display.update()
  
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

def in_board(posX : int, posY : int) -> bool:
  return posX >= 0 and posX < COLS and posY >= 0 and posY < ROWS

def check_cell(user: int, posX: int, posY: int) -> int:
  global board
  # nếu ô đó có đúng ký tự của user đó thì return 1
  if in_board(posX, posY) and (board[posX][posY] == USER[user]):
    return 1
  # gặp ký tự của đối thủ thì ăn penalty 
  elif in_board(posX, posY) and (board[posX][posY] == USER[1 - user]):
    return -100
  return 0

def hv_check(user : int, posX : int, posY : int):
  #print()
  for i in range(-4, 1):
    startX = posX + i
    startY = posY + i
    # count lưu giá trị max liên tiếp
    countH, countV, curCountH, curCountV = 0, 0, 0, 0
    for j in range(0, 5):
      curX, curY = startX + j, posY
      point = check_cell(user, curX, curY)
      if point == 0:
        if curCountH:
          countH = max(curCountH, countH)
          curCountH = 0
      else: 
        curCountH += point
      
      curX, curY = posX, startY + j
      point = check_cell(user, curX, curY)
      if point == 0:
        if curCountV:
          countV = max(curCountV, countV)
          curCountV = 0
      else: 
        curCountV += point
    countH = max(curCountH, countH)
    countV = max(curCountV, countV)
    opponent = 1 - user
    leftX = startX - 1
    l = check_cell(opponent, leftX, posY) == 1
    rightX = startX + 5
    r = check_cell(opponent, rightX, posY) == 1
    topY = startY - 1
    t = check_cell(opponent, posX, topY) == 1
    bottomY = startY + 5
    b = check_cell(opponent, posX, bottomY) == 1
    #print("LeftX = %d, LeftY = %d" % (leftX, rightX))
    #print("User %d has %d max horizontal continous steps. This was check at (%d, %d)" % (user, countH, startX, posY))
    #print("User %d has %d max vertical continous steps. This was check at (%d, %d)" % (user, countV, posX, startY))
    if countH == 4 and not(l or r):
      #print("l is %s and r is %s" % (l, r))
      return True
    if countH == 5 and not(l and r):
      return True
    if countV == 4 and not(t or b):
      return True
    if countV == 5 and not(t and b):
      return True
  return False

def main_diag_check(user : int, posX : int, posY : int):
  #print()
  for i in range(-4, 1):
    startX = posX + i
    startY = posY + i
    # count lưu giá trị max liên tiếp
    countM, curCountM = 0, 0
    for j in range(0, 5):
      curX, curY = startX + j, startY + j
      point = check_cell(user, curX, curY)
      if point == 0:
        if curCountM:
          countM = max(curCountM, countM)
          curCountM = 0
      else: 
        curCountM += point
    countM = max(curCountM, countM)
    opponent = 1 - user
    topleftX, topleftY = startX - 1, startY - 1
    tl = check_cell(opponent, topleftX, topleftY) == 1
    bottomrightX, bottomrightY = startX + 5, startY + 5
    br = check_cell(opponent, bottomrightX, bottomrightY) == 1
    if countM == 4 and not(tl or br):
      return True
    if countM == 5 and not(tl and br):
      return True
  return False

def anti_diag_check(user : int, posX : int, posY : int):
  # print()
  for i in range(-4, 1):
    startX = posX + i
    startY = posY - i
    # count lưu giá trị max liên tiếp
    countA, curCountA = 0, 0
    for j in range(0, 5):
      curX, curY = startX + j, startY - j
      point = check_cell(user, curX, curY)
      if point == 0:
        if curCountA:
          countA = max(curCountA, countA)
          curCountA = 0
      else: 
        curCountA += point
    countA = max(curCountA, countA)
    opponent = 1 - user
    toprightX, toprightY = startX + 5, startY - 5
    tr = check_cell(opponent, toprightX, toprightY) == 1
    bottomleftX, bottomleftY = startX - 1, startY + 1
    bl = check_cell(opponent, bottomleftX, bottomleftY) == 1
    #print("LeftX = %d, LeftY = %d" % (leftX, rightX))
    # print("User %d has %d max continous steps. This was check at (%d, %d)" % (user, countA, startX, startY))
    #print("User %d has %d max vertical continous steps. This was check at (%d, %d)" % (user, countV, posX, startY))
    if countA == 4 and not(tr or bl):
      #print(check_cell(opponent, toprightX, toprightY))
      #print(tr, toprightX, toprightY)
      return True
    if countA == 5 and not(tr and bl):
      return True
  return False

def check_win(user: int, posX: int, posY: int):
  if (hv_check(user, posX, posY)):
    print("User %d wins horizontal or vertical" % (user))
  if (main_diag_check(user, posX, posY)):
    print("User %d wins main diag" % (user))
  if (anti_diag_check(user, posX, posY)):
    print("User %d wins anti diag" % (user))
  return hv_check(user, posX, posY)\
          or main_diag_check(user, posX, posY)\
            or anti_diag_check(user, posX, posY)


def play_game():
  global running
  global screen
  global flag
  global board

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
        posX = xClick // STEP
        posY = yClick // STEP
        if board[posX][posY]:
          continue
        board[posX][posY] = 1 if flag else -1
        centerX = posX * STEP + STEP // 2
        centerY = posY * STEP + STEP // 2
        #draw_circle(screen, centerX, centerY, radius = 21, color = dot[flag])
        radius = STEP // 2 - 4
        if flag:
          drawX(screen, RED, centerX, centerY, radius - 4, SYMBOL_WIDTH * 2)
        else:
          drawAACircle(screen, center = (centerX, centerY), radius = radius , color = BLUE, width = SYMBOL_WIDTH)
        #vẽ tất cả lên màn hình
        pygame.display.update()
        if check_win(flag, posX, posY):
          print("Player %d wins\n" % (flag))
          #pygame.time.delay(5000)
        # pygame.draw.circle(screen, dot[flag], (centerX, centerY) , radius = 21, width = 4)
        #đổi sang màu còn lại
        flag = 1 - flag
    
  #thoát chương trình  
  pygame.quit()