import pygame
import sys
import neat

from Car import Car
from Button import Button
from config import width, height

generation = 0
cars_left = 30
start = False


def run_generation(genomes, config):
    nets = []
    cars = []

    # init genomes
    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0  # every genome is not successful at the start

        # init cars
        cars.append(Car())

    # init the game
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    road = pygame.image.load('sprites/road.png')

    font = pygame.font.SysFont("Roboto", 40)
    heading_font = pygame.font.SysFont("Roboto", 80)

    global generation
    global start
    global cars_left
    generation += 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = True
            # elif event.type == pygame.MOUSEBUTTONUP:
            #     pos = pygame.mouse.get_pos()
            #     print(pos)

        screen.blit(road, (0, 0))

        exit_btn = Button((70, 60), (124, 116), None, None, 'sprites/exit.png')
        exit_btn.draw(screen)
        if exit_btn.is_clicked():
            exit()

        start_btn = Button((780, 800), (250, 70), 'Start', (235, 202, 138))
        start_btn.draw(screen)
        if start_btn.is_clicked():
            start = True

        start_btn = Button((300, 800), (250, 70), 'Stop', (235, 202, 138))
        start_btn.draw(screen)
        if start_btn.is_clicked():
            start = False

        if start:
            for i, car in enumerate(cars):
                output = nets[i].activate(car.get_data())
                i = output.index(max(output))

                if i == 0:
                    car.angle += 5
                elif i == 1:
                    car.angle = car.angle
                elif i == 2:
                    car.angle -= 5

            cars_left = 0
            for i, car in enumerate(cars):
                if car.is_alive:
                    cars_left += 1
                    car.update(road)
                    genomes[i][1].fitness += car.get_reward()

            if not cars_left:
                break

        for car in cars:
            if car.is_alive:
                car.draw(screen)
            # car.draw_center(screen)
            # car.draw_collision_points(road, screen)

        label = heading_font.render("Поколение: " + str(generation), True, (73, 168, 70))
        label_rect = label.get_rect()
        label_rect.center = (width / 1.5, 300)
        screen.blit(label, label_rect)

        label = font.render("Машин осталось: " + str(cars_left), True, (51, 59, 70))
        label_rect = label.get_rect()
        label_rect.center = (width / 1.5, 375)
        screen.blit(label, label_rect)

        pygame.display.flip()
        clock.tick(120)


if __name__ == "__main__":
    # setup config
    config_path = "config_neat.txt"
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)

    # init NEAT
    p = neat.Population(config)

    # run NEAT
    p.run(run_generation, 1000)
