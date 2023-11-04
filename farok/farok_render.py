import pygame

pygame.init()

size = [1000, 500]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Farok_Engine")

close = False
clock = pygame.time.Clock()

while not close:
  
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(30)
     
    # Main Event Loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            close=True # Flag that we are done so we exit this loop

    pygame.display.flip()
