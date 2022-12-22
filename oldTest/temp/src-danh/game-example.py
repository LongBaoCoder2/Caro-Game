import pygame

#khởi tạo pygame
pygame.init()

#tạo cửa sổ giao diện trong pygame
screen = pygame.display.set_mode((500,600))
pygame.display.set_caption("Game Caro")

#khai báo màu nền cho giao diện
BACKGROUND_COLOR = (100, 100, 100)

#biến vòng lặp game
running = True

#game loop
while running:

    #vẽ màu nền
    screen.fill(BACKGROUND_COLOR)

    #xử lý sự kiện
    for event in pygame.event.get():
        #sự kiện thoát
        if event.type == pygame.QUIT:
            running = False
        #sự kiện chuột
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: #nhấn chuột trái
                print(event.pos) #in tọa độ chuột
    r = 255
    g = 0
    b = 0
    x = 10
    y = 10
    width = 100
    height = 200

    #hàm vẽ hình chữ nhật có điểm trái trên tọa độ (x,y) kích thước (width, height) với màu (r,g,b)
    pygame.draw.rect(screen, (r, g, b), (x, y, width, height))

    x1 = 203
    y1 = 232
    x2 = 432
    y2 = 324
    thickness = 5
    #hàm vẽ đoạn thẳng nối 2 điểm (x1, y1) và (x2, y2) có độ dày thickness
    pygame.draw.line(screen, (r, g, b), (x1, y1), (x2, y2), thickness)
    #vẽ tất cả lên màn hình
    pygame.display.update()


#thoát chương trình
pygame.quit()
