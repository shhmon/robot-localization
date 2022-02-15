import pygame
from enum import Enum, auto
from Maze import Maze
from Robot import RobotSim
from Dir import Dir
from Localizer import Localizer
from StateModel import StateModel

# -------- Constants -------- 
white = (250,250,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
black = (0,0,0)

name = "Visualizer"
dims = (7, 7)

wallLength = 80

size = width, height = wallLength * dims[0], wallLength * dims[1]

# -------- Pygame -------- 
pygame.init()

screen = pygame.display.set_mode(size)
pygame.display.set_caption(name)
clock = pygame.time.Clock()

maze = Maze(wallLength, 2, black, blue)
robot = RobotSim((3, 6), Dir.N)
stateModel = StateModel(7, 7)
localizer = Localizer(stateModel, stateModel.xyhToRobotState(3, 6, Dir.N.value))
cnt = 0

def draw_probs(surface, trueState):
    tm = localizer.getTransitionModel()
    x, y, h = stateModel.robotStateToXYH(trueState)

    for j in range(tm.dim):
        tx, ty, th = stateModel.robotStateToXYH(j)

        if tm.matrix[trueState, j] > 0:
            start = x * wallLength, y * wallLength
            end = tx * wallLength, ty * wallLength

            if h == Dir.N.value:
                start = start[0] + wallLength/2, start[1] + wallLength/4
            elif h == Dir.W.value:
                start = start[0] + wallLength/4, start[1] + wallLength/2
            elif h == Dir.S.value:
                start = start[0] + wallLength/2, start[1] + wallLength - wallLength/4
            elif h == Dir.E.value:
                start = start[0] + wallLength - wallLength/4, start[1] + wallLength/2
            
            if th == Dir.N.value:
                end = end[0] + wallLength/2, end[1] + wallLength/4
            elif th == Dir.W.value:
                end = end[0] + wallLength/4, end[1] + wallLength/2
            elif th == Dir.S.value:
                end = end[0] + wallLength/2, end[1] + wallLength - wallLength/4
            elif th == Dir.E.value:
                end = end[0] + wallLength - wallLength/4, end[1] + wallLength/2
            
            pygame.draw.line(surface, (200,0,200), start, end, 2)#int(10*tm.matrix[trueState, j]))

#localizer.getTransitionModel().matrix[stateModel.xyhToRobotState(2, 3, Dir.S.value)][stateModel.xyhToRobotState(2, 3, Dir.W.value)] = 1

while True:

    rpos = robot.update(maze)
    rstate = stateModel.xyhToRobotState(rpos[0], rpos[1], rpos[2].value)
    sense = robot.sense(maze)
    #print(f'sensed {sense} at state {rstate}. Prob:', localizer.getObservationModel().vectors[sense][rstate])
    #print(sum(localizer.getTransitionModel().matrix[stateModel.xyhToRobotState(rpos[0], rpos[1], rpos[2].value)]))
    px, py = localizer.update(rstate, sense)

    print(f'update: robot pos {rpos}')
    print(f'update: localizer pos {px, py}')

    screen.fill(white)
    localizer.hmm.draw(screen, stateModel, sense, wallLength)

    rect = pygame.Rect(px * wallLength, py * wallLength, wallLength, wallLength)
    pygame.draw.rect(screen, (200,200,255), rect)

    maze.draw(screen)
    robot.draw(screen, wallLength)
    draw_probs(screen, stateModel.xyhToRobotState(robot.pos[0], robot.pos[1], robot.head.value))

    events = pygame.event.get()

    for e in events:
        if e.type == pygame.MOUSEBUTTONDOWN:
            pass
        elif e.type == pygame.QUIT:
            raise SystemExit()
    
    pygame.display.update()
    clock.tick(3)
    cnt += 1

    # if cnt == 20:
    #     while True:
    #         pass

    