import pygame, os, pygame.image, random
# GAME VARIABLES
population = 100
housingCapacity = 0
immigrationRate = 20
taxes = 20
cashflow = 0
treasury = 10000
pollution = 0
congestion = 5
housingAvailable = housingCapacity - population
# BACKGROUND VARIABLES
currentBuildingIndex = 0
buildingCount = [0, 0, 0, 0, 0]
buildingTypeAmount = len(buildingCount)
turnsBeforeLoss = 3
playerLost = False
PopulationLost = False
TreasuryLost = False
PollutionLost = False
PopulationLost=False   
HousingLost = False
maxPopulation = population
inflationOn = False
inflation = 1
taxEvaders = int(random.uniform(population / 20, population/10) * 10) / 10
currentTurn = 1
taxEvasionOn = False

# Building Types
buildingCostDict = {
    0: 200, # House
    1: 100, # Road
    2: 500, # Park
    3: 1000, # Station
    4: 5000, # Airport,
    5: -4000, #Rock 1x1
    6: -14000  #Rock 2x2
}

buildingNameDict = {
    0: "House",
    1: "Road",
    2: "Park",
    3: "Station",
    4: "Airport"
}

backgroundDict = {
    "0" : 26,
    "4" : 27,
    "5" : 28
}


buildingSizeDict = {
    0: (1, 1),
    1: (1, 1),
    2: (2, 2),
    3: (2, 2),
    4: (3, 2),
    5: (1,1),
    6: (2,2)
}

# Game Logic Functions
def NextTurn():
    global turnsBeforeLoss, population, housingCapacity, immigrationRate, taxes, cashflow, treasury, pollution, congestion, playerLost, housingAvailable, HousingLost, TreasuryLost, PollutionLost, PopulationLost, maxPopulation, inflation, taxEvaders, currentTurn
    population += immigrationRate
    if(population > maxPopulation):
        maxPopulation = population
    pollution = int(population * 3)
    treasury += cashflow
    immigrationTurns=0
    treasuryTurns=0
    inflation *= 1.1
    taxEvaders = int(random.uniform(population / 20, population/10) * 10) / 10
    
    if immigrationRate <= 0:
        immigrationTurns += 1
    else:
        immigrationTurns = 0
    
    # Track treasury condition
    if treasury <= 0:
        treasuryTurns += 1
    else:
        treasuryTurns = 0
    
    # Check conditions for player loss
    if immigrationTurns >= 3:
        playerLost = True
        PopulationLost = True
    elif treasuryTurns >= 3:
        playerLost = True
        TreasuryLost = True
    elif pollution > 1000:
        PollutionLost = True
    elif population <= 0:
        playerLost = True
        PopulationLost=True   
    elif -housingAvailable>housingCapacity:
        playerLost = True
        HousingLost = True
    else:
        currentTurn += 1
    

def UpdateValues():
    global turnsBeforeLoss, population, housingCapacity, immigrationRate, taxes, cashflow, treasury, pollution, congestion, playerLost, housingAvailable
    pollution = int(population - buildingCount[2] * 20 + buildingCount[3] * 3 + buildingCount[4] * 10)
    congestion = int(population - buildingCount[1] * 12 + 10 * 3)
    if congestion < 0:
        congestion = 0
    if(taxEvasionOn):
        taxes = int((population-taxEvaders) * 14 - congestion * 4)
    else:
        taxes = int(population * 14 - congestion * 4)
    cashflow = int(taxes + 10 * population - ((1 * buildingCount[1]) + (1 * buildingCount[2]) + (2 * buildingCount[3]) + (3 * buildingCount[4])))
    immigrationRate = int(((10 * housingAvailable) - (pollution) + (buildingCount[3] * 5) + (buildingCount[4] * 6)) / 6 + 50)

    
# Initialize Pygame

pygame.init()
os.chdir(os.path.dirname(__file__))  # Ensure directory is set to current file location

# Define grid properties
grid_size = 32  # Size of each cell (in pixels)
grid_color = (0, 0, 0)  # Color of the grid lines (black)
background_color = (255, 255, 255)  # Background color (white)

# Color Definitions
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

#Popup
popup_open = True  # Flag to check if popup is open
def draw_popup():
    popup_rect = pygame.Rect(150, 100, 660, 400)  # Popup rectangle position and size
    pygame.draw.rect(screen, (255,255,254), popup_rect)    # Draw popup background
    pygame.draw.rect(screen, BLUE, popup_rect, 3)  # Border for the popup
    
    # Popup instructions
    display_text("Welcome to the Game!", 160, 130 + (0*40))
    display_text("Goal: Manage population, resources, and infrastructure", 160, 130 + (1*40))
    display_text("Instructions:", 160, 130 + (2*40))
    display_text(" - Use 'a' and 'd' keys to switch building types.", 160, 130 + (3*40))
    display_text(" - Click the 'Next Turn' button to progress.", 160, 130 + (4*40))
    display_text("Left click to place tiles, right click to delete", 160, 130 + (5*40))
    display_text(" - Buildings will be placed from the top left", 160, 130 + (6*40))
    display_text(" - When deleting buildings you MUST click in the top left", 160, 130 + (7*40))
    display_text("Click anywhere to close this popup and start playing.", 160, 130 + (8*40))

# Load and scale building images
buildingImageDict = {
    0 : pygame.image.load("sprite_00.png"),
    1 : pygame.image.load("sprite_31.png"), #Hor
    2 : pygame.image.load("sprite_32.png"), #Ver
    3 : pygame.image.load("sprite_33.png"), #DR
    4 : pygame.image.load("sprite_34.png"), #DL
    5 : pygame.image.load("sprite_35.png"), #UR
    6 : pygame.image.load("sprite_36.png"), #UL
    7 : pygame.image.load("sprite_37.png"), #URD
    8 : pygame.image.load("sprite_38.png"), #LUR
    9 : pygame.image.load("sprite_39.png"), #LDR
    10: pygame.image.load("sprite_40.png"), #ULD
    11: pygame.image.load("sprite_41.png"), #UDLR
    12: pygame.image.load("sprite_20.png"),
    13: pygame.image.load("sprite_21.png"),
    14: pygame.image.load("sprite_22.png"),
    15: pygame.image.load("sprite_23.png"),
    16: pygame.image.load("sprite_64.png"),
    17: pygame.image.load("sprite_65.png"),
    18: pygame.image.load("sprite_66.png"),
    19: pygame.image.load("sprite_67.png"),
    20: pygame.image.load("sprite_14.png"),
    21: pygame.image.load("sprite_15.png"),
    22: pygame.image.load("sprite_16.png"),
    23: pygame.image.load("sprite_17.png"),
    24: pygame.image.load("sprite_18.png"),
    25: pygame.image.load("sprite_19.png"),
    26: pygame.image.load("sprite_99.png"), #Grass
    27: pygame.image.load("sprite_100.png"),#Sand
    28: pygame.image.load("sprite_101.png"), #Water
    29: pygame.image.load("sprite_83.png"), #Rock 1x1
    30: pygame.image.load("sprite_84.png"),
    31: pygame.image.load("sprite_85.png"),
    32: pygame.image.load("sprite_86.png"),
    33: pygame.image.load("sprite_87.png"),
}

for key in buildingImageDict:
    buildingImageDict[key] = pygame.transform.scale(buildingImageDict[key], (grid_size, grid_size))

# Button settings
button_color = BLUE
button_hover_color = RED
button_rect_1 = pygame.Rect(10, 10 + (12 * 40), 80, 30)  # Position and size of the button
button_rect_2 = pygame.Rect(10, 10 + (13*40), 80, 30)
button_rect_3 = pygame.Rect(100, 10 + (13*40), 80, 30)
font = pygame.font.SysFont('Montserrat', 20)
nextTurnButtonPressTime = pygame.time.get_ticks()
button_pressed_1 = False
button_pressed_2 = False
button_pressed_3 = False


# Display Text
def display_text(text, x, y):
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

# Placing tiles
placed_tiles = []

def place_tile(mouse_pos, type, drawingType):
    col = mouse_pos[0]
    row = mouse_pos[1]
    placed_tiles.append((col, row, type, drawingType))

def draw_placed_tiles():
    for tile in placed_tiles:
        col, row, type, drawingType = tile
        if(type == 1):
            #Road Logic
            up = False
            left = False
            down = False
            right = False
            
            for tile2 in placed_tiles:
                if(tile2[2] == 1):
                    if((col, row - 1) == (tile2[0], tile2[1])):
                        up = True
                    elif((col-1, row) == (tile2[0], tile2[1])):
                        left = True
                    elif((col, row + 1) == (tile2[0], tile2[1])):
                        down = True
                    elif((col+1, row) == (tile2[0], tile2[1])):
                        right = True
            
            if(up and left and down and right):
                drawingType = 11
            elif(up and left and down and (not right)):
                drawingType = 10
            elif((not up) and left and down and right):
                drawingType = 9
            elif(left and up and right and (not down)):
                drawingType = 8
            elif(up and right and down and (not left)):
                drawingType = 7
            elif(up and left and (not down) and (not right)):
                drawingType = 6
            elif(up and right and (not down) and (not left)):
                drawingType = 5
            elif(down and left and (not up) and (not right)):
                drawingType = 4
            elif(down and right and (not up) and (not left)):
                drawingType = 3
            elif(up and down and (not left) and (not right)) or (up and (not down) and (not left) and (not right)) or (down and (not up) and (not left) and (not right)):
                drawingType = 2
            elif(left and right and (not up) and (not down)) or (left and (not down) and (not right) and (not up)) or (right and (not down) and (not up) and (not left)):
                drawingType = 1
        screen.blit(buildingImageDict[drawingType], (col * grid_size, row * grid_size))
                    

#Delete Tiles
def delete_tiles(mouse_pos):
    global treasury
    col = mouse_pos[0] // grid_size
    row = mouse_pos[1] // grid_size
    
    validTile = False
    targetedTile = None
    for tile in placed_tiles:
        if(tile[0] == col) and (tile[1] == row):
            validTile = True
            targetedTile = tile
            break

    if(validTile):
        size = buildingSizeDict[targetedTile[2]]
        tilesToRemove = []
        for i in range(size[0]):
            for j in range(size[1]):
                for tile in placed_tiles:
                    if((tile[0], tile[1]) == (col + i, row + j)):
                        tilesToRemove.append(tile)
        
        if(treasury + (buildingCostDict[tilesToRemove[0][2]] / 2) > 0):
            for tileToRemove in tilesToRemove:
                    placed_tiles.remove(tileToRemove)
                    treasury += buildingCostDict[tileToRemove[2]] / (2 * size[0] * size[1])
                    treasury = int(treasury)

# Set up the display
screen_width = grid_size * 30
screen_height = grid_size * 20
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hackathon Game")

# Calculate number of rows and columns
num_cols = screen_width // grid_size
num_rows = screen_height // grid_size

fileHandle = open("Background.txt", "r")
linesRaw = fileHandle.readlines()
lines = []
for lineRaw in linesRaw:
    lines.append([*lineRaw.strip()])
fileHandle.close()

#Place rocks

#2x2
for i in range(4):
    attemptsLeft = 100
    succeeded = False
    targetedPosition = (0,0)
    while(not succeeded and attemptsLeft > 0):
        attemptValid = True
        targetedPosition = (random.randint(8,26), random.randint(0,17))
        for tile in placed_tiles:
            if(attemptValid):
                break
            for i in range(2):
                for j in range(2):
                    if not((tile[0] + i == targetedPosition[0]) and (tile[1] + j == targetedPosition[1])):
                        attemptValid = True

        if(attemptValid):
            succeeded = True
            for i in range(2):
                for j in range(2):
                    place_tile((targetedPosition[0] + j, targetedPosition[1] + i), 6, 30 + i*2 + j)
            
        else:
            attemptsLeft -= 1

#1x1
for i in range(10):
    attemptsLeft = 100
    succeeded = False
    targetedPosition = (0,0)
    while(not succeeded and attemptsLeft > 0):
        attemptValid = True
        targetedPosition = (random.randint(8,27), random.randint(0,18))
        for tile in placed_tiles:
            if not(attemptValid):
                break
            if (tile[0] == targetedPosition[0]) and (tile[1] == targetedPosition[1]):
                attemptValid = False

        if(attemptValid):
            succeeded = True
            place_tile((targetedPosition[0], targetedPosition[1]), 6, 29)
            
        else:
            attemptsLeft -= 1
        
# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and popup_open:
            popup_open = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                currentBuildingIndex = (currentBuildingIndex - 1) % buildingTypeAmount
            elif event.key == pygame.K_d:
                currentBuildingIndex = (currentBuildingIndex + 1) % buildingTypeAmount
            elif event.key == pygame.K_1:
                currentBuildingIndex = 0
            elif event.key == pygame.K_2:
                currentBuildingIndex = 1
            elif event.key == pygame.K_3:
                currentBuildingIndex = 2
            elif event.key == pygame.K_4:
                currentBuildingIndex = 3
            elif event.key == pygame.K_5:
                currentBuildingIndex = 4

    #HERRERER
    if playerLost == True and PopulationLost==True:
        screen.fill((255, 255, 255))  # Fill the screen with black
        display_text("Game Over", 200, 130)
        display_text("You lost the game due to having 0 population.", 200, 150)
        display_text(f"Your max population was {maxPopulation} people", 200, 170)
        display_text(f"You lasted {currentTurn} turns", 200, 190)
        display_text("Press 'Q' to quit or restart the program to play again.",200, 210)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                running = False
        continue
    elif playerLost == True and TreasuryLost==True:
        screen.fill((255, 255, 255))  # Fill the screen with black
        display_text("Game Over", 200, 130)
        display_text("You lost the game due to having 0 Treasury for 3 turns.", 200, 150)
        display_text(f"Your max population was {maxPopulation} people", 200, 170)
        display_text(f"You lasted {currentTurn} turns", 200, 190)
        display_text("Press 'Q' to quit or restart the program to play again.",200, 210)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                running = False
        continue
    elif playerLost == True and PollutionLost==True:
        screen.fill((255, 255, 255))  # Fill the screen with black
        display_text("Game Over", 200, 130)
        display_text("You lost the game due to having over 100% pollution.", 200, 150)
        display_text(f"Your max population was {maxPopulation} people", 200, 170)
        display_text(f"You lasted {currentTurn} turns", 200, 190)
        display_text("Press 'Q' to quit or restart the program to play again.",200, 210)
        pygame.display.flip()
        # Allow the player to quit after game over
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                running = False
        continue
    elif playerLost == True and HousingLost==True:
        screen.fill((255, 255, 255))  # Fill the screen with black
        display_text("Game Over", 200, 130)
        display_text("You lost the game due to having too many homeless", 200, 150)
        display_text(f"Your max population was {maxPopulation} people", 200, 170)
        display_text(f"You lasted {currentTurn} turns", 200, 190)
        display_text("Press 'Q' to quit or restart the program to play again.",200, 210)
        pygame.display.flip()
        # Allow the player to quit after game over
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                running = False
        continue
    elif playerLost == True:
        screen.fill((255, 255, 255))  # Fill the screen with black
        display_text("Game Over", 200, 130)
        display_text("You lost the game ", 200, 150)
        display_text(f"Your max population was {maxPopulation} people", 200, 170)
        display_text(f"You lasted {currentTurn} turns", 200, 190)
        display_text("Press 'Q' to quit or restart the program to play again.",200, 210)
        pygame.display.flip()
        # Allow the player to quit after game over
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                running = False
        continue


    # Fill the screen with the background color
    screen.fill(background_color)
    #screen.blit(pygame.image.load("Final Background (1).png"), (8 * grid_size, 0))
    
    for i in range(20):
        for j in range(20):
            screen.blit(buildingImageDict[backgroundDict[lines[j][i]]],((i+8)*grid_size,j*grid_size))    

    # Draw the grid lines
    """for col in range(8, 29):
        x = col * grid_size
        pygame.draw.line(screen, grid_color, (x, 0), (x, screen_height))
    for row in range(num_rows + 1):
        y = row * grid_size
        pygame.draw.line(screen, grid_color, (8 * grid_size, y), (screen_width - (2 * grid_size), y))"""

    # Draw button
    pygame.draw.rect(screen, button_color, button_rect_1, border_radius=4)
    pygame.draw.rect(screen,button_color, button_rect_2, border_radius=4)
    pygame.draw.rect(screen, button_color, button_rect_3, border_radius=4)
    
    # Check for single click on button with delay
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if button_rect_1.collidepoint(mouse_x, mouse_y):
        if pygame.mouse.get_pressed()[0] and not button_pressed_1:
            button_pressed_1 = True
            nextTurnButtonPressTime = pygame.time.get_ticks()
            NextTurn()
    elif pygame.time.get_ticks() - nextTurnButtonPressTime >= 100:
        button_pressed_1 = False
        
    if button_rect_2.collidepoint(mouse_x, mouse_y):
        if pygame.mouse.get_pressed()[0] and not button_pressed_2:
            button_pressed_2 = True
            nextTurnButtonPressTime = pygame.time.get_ticks()
            inflationOn = not inflationOn
    elif pygame.time.get_ticks() - nextTurnButtonPressTime >= 100:
        button_pressed_2 = False
        
    if button_rect_3.collidepoint(mouse_x, mouse_y):
        if pygame.mouse.get_pressed()[0] and not button_pressed_3:
            button_pressed_3 = True
            nextTurnButtonPressTime = pygame.time.get_ticks()
            taxEvasionOn = not taxEvasionOn
    elif pygame.time.get_ticks() - nextTurnButtonPressTime >= 100:
        button_pressed_3 = False

    # Render text on the button
    text_surface_1 = font.render("Next Turn", True, WHITE)
    text_rect_1 = text_surface_1.get_rect(center=button_rect_1.center)
    screen.blit(text_surface_1, text_rect_1)
    
    
    if(inflationOn):
        text_surface_2 = font.render("Inflation Off", True, WHITE)
    
    else:
        text_surface_2 = font.render("Inflation On", True, WHITE)
    
    text_rect_2 = text_surface_2.get_rect(center=button_rect_2.center)
    screen.blit(text_surface_2, text_rect_2)

    if(taxEvasionOn):
        text_surface_3 = font.render("Evasion Off", True, WHITE)
    
    else:
        text_surface_3 = font.render("Evasion On", True, WHITE)
    
    text_rect_3 = text_surface_3.get_rect(center=button_rect_3.center)
    screen.blit(text_surface_3, text_rect_3)

    # Place tiles if possible
    if pygame.mouse.get_pressed()[0] and treasury >= buildingCostDict[currentBuildingIndex] and 271 < mouse_x < 912:
        tileAvailable = True
        for tile in placed_tiles:
            if tile[0] == (mouse_x // grid_size) and tile[1] == mouse_y // grid_size:
                tileAvailable = False
        
        if tileAvailable:
            for i in range(buildingSizeDict[currentBuildingIndex][1]):
                for j in range(buildingSizeDict[currentBuildingIndex][0]):
                    for tile in placed_tiles:
                        if (mouse_x // grid_size) + j == tile[0] and (mouse_y // grid_size) + i == tile[1]:
                            tileAvailable = False

        if tileAvailable and (((mouse_x // grid_size) + buildingSizeDict[currentBuildingIndex][0]) > 57 or ((mouse_y // grid_size) + buildingSizeDict[currentBuildingIndex][0]) > 40):
            tileAvailable = False
        
        if tileAvailable and currentBuildingIndex != 1:
            for i in range(buildingSizeDict[currentBuildingIndex][1]):
                for j in range(buildingSizeDict[currentBuildingIndex][0]):
                    if(lines[mouse_y//grid_size + i][(mouse_x//grid_size) - 8 + j] == "5"):
                        tileAvailable = False
                        break
                if not(tileAvailable):
                    break
            
            #lines[mouse_y//grid_size][(mouse_x//grid_size) - 8] == "5"
            #tileAvailable = False
        
        if(tileAvailable) and (currentBuildingIndex == 1) and (buildingCount[1] > 0):
            success = False
            
            for tile in placed_tiles:
                if(tile[2] == 1):
                    
                    if (tile[0] == (mouse_x // grid_size)) and (tile[1] == (mouse_y // grid_size) + 1) or ((tile[0] == (mouse_x // grid_size)) and (tile[1] == (mouse_y // grid_size) - 1)) or ((tile[0] == (mouse_x // grid_size) - 1) and (tile[1] == (mouse_y // grid_size))) or ((tile[0] == (mouse_x // grid_size) + 1) and (tile[1] == (mouse_y // grid_size))):
                        success = True
                        break
            
            tileAvailable = success
        
        
        if(tileAvailable) and (currentBuildingIndex != 1):
            success = False
            
            for tile in placed_tiles:
                if(success):
                    break
                if(tile[2] == 1):
                    for i in range(buildingSizeDict[currentBuildingIndex][1]):
                        for j in range(buildingSizeDict[currentBuildingIndex][0]):
                            if((tile[0] == (mouse_x // grid_size) + i - 1) and (tile[1] == (mouse_y // grid_size) + j)) or ((tile[0] == (mouse_x // grid_size) + i + 1) and (tile[1] == (mouse_y // grid_size) + j)) or ((tile[0] == (mouse_x // grid_size) + i) and (tile[1] == (mouse_y // grid_size) + j - 1)) or ((tile[0] == (mouse_x // grid_size) + i) and (tile[1] == (mouse_y // grid_size) + j + 1)): 
                                success = True
            
            tileAvailable = success
                            
        if tileAvailable:
            buildingType = 19
            for i in range(buildingSizeDict[currentBuildingIndex][1]):
                for j in range(buildingSizeDict[currentBuildingIndex][0]):
                    if currentBuildingIndex == 0:
                        buildingType = 0
                    elif currentBuildingIndex == 1:
                        buildingType = 1
                    elif currentBuildingIndex == 2:
                        buildingType = 12 + j + (i * 2)
                    elif currentBuildingIndex == 3:
                        buildingType = 16 + j + (i * 2)
                    elif currentBuildingIndex == 4:
                        buildingType += 1
                    
                    for tile in placed_tiles:
                        if(tile[0] == i) and (tile[1] == j):
                            placed_tiles.remove(tile)
                    
                    place_tile(((mouse_x // grid_size) + j, (mouse_y // grid_size) + i), currentBuildingIndex, buildingType)
                    #print(((mouse_x // grid_size) + j, (mouse_y // grid_size) + i))
            if(inflationOn):
                treasury -= (buildingCostDict[currentBuildingIndex] * inflation)
            else:
                treasury -= buildingCostDict[currentBuildingIndex]
            
            treasury = int(treasury)
            buildingCount[currentBuildingIndex] += 1

    elif(pygame.mouse.get_pressed()[2]):
        delete_tiles((mouse_x, mouse_y))
    
    # Draw placed tiles
    draw_placed_tiles()

    # Display game variables
    if popup_open:
        draw_popup()
    else:
        display_text(f"Population: {population}", 10, 10)
        display_text(f"Immigration Rate: {immigrationRate}", 10, 10 + (1 * 40))
        display_text(f"Capacity / Availability: {housingCapacity} / {housingAvailable}", 10, 10 + (2 * 40))
        display_text(f"Taxes: {taxes}", 10, 10 + (3 * 40))
        display_text(f"Income: {cashflow}", 10, 10 + (4 * 40))
        display_text(f"Pollution %: {pollution / 1000}", 10, 10 + (5 * 40))
        display_text(f"Congestion: {congestion}", 10, 10 + (6 * 40))
        display_text(f"Treasury: {treasury}", 10, 10 + (7 * 40))
        display_text(f"Selected Building: {buildingNameDict[currentBuildingIndex]}", 10, 10 + (8 * 40))
        display_text(f"Turns before Loss: {turnsBeforeLoss}", 10, 10 + (9 * 40))
        display_text("Switch Building Type with a and d.",10, 10 + (10*40))
        display_text(f"Current Turn : {currentTurn}",10, 10 + (11*40)) 
        display_text(f"Inflation On : {inflationOn}", 10, 10+(14*40))
        display_text(f"Tax Evasion On : {taxEvasionOn}", 10, 10+(15*40))
    
    
    housingCapacity = 5 * buildingCount[0]
    housingAvailable = housingCapacity - population
    
    # Update the display
    UpdateValues()
    pygame.display.flip()

# Quit Pygame
pygame.quit()