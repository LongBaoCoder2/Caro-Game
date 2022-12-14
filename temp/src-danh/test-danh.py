"""
class Car:
  def __init__(self, color : str, milleage : int):
    self.color = color
    self.milleage = milleage
  def __str__(self) -> str:
    return "The %s car has %d miles." % (self.color, self.milleage)
blue = Car("blue", 20000)
red = Car("red", 30000)
print(blue)
print(red)

class Dog:
  species = "Canis familiaris"

  def __init__(self, name, age):
    self.name = name
    self.age = age

  def __str__(self):
    return f"{self.name} is {self.age} years old"

  def speak(self, sound):
    return f"{self.name} says {sound}"
  
class GoldenRetriever(Dog):
  def speak(self, sound = "Bark"):
    return f"{self.name} says {sound}"

lmao = GoldenRetriever("Hello", 10)
print(lmao)
print(lmao.speak())
"""
import pygame
pygame.init()

windows = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Bai tap 1")

x = 50
y = 50 
width = 40
height = 60
vel = 5
run = True

while run:
  pygame.time.delay(10)
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
  
  keys = pygame.key.get_pressed()
  
  if keys[pygame.K_LEFT]: # We can check if a key is pressed like this
    x -= vel
  if keys[pygame.K_RIGHT]:
    x += vel
  if keys[pygame.K_UP]:
    y -= vel
  if keys[pygame.K_DOWN]:
    y += vel
  
  windows.fill((0, 0, 0))
  pygame.draw.rect(windows, (255, 0, 0), (x, y, width, height))
  pygame.display.update()

pygame.quit()
