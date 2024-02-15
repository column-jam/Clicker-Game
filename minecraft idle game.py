import pygame

pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.NOFRAME)
clock = pygame.time.Clock()
running = True
dt = 0


wood_count = 0
stone_count = 0
iron_count = 0


def texture_loader(file_name, file_dimensions, file_center):
    file_scaled = pygame.transform.scale(pygame.image.load(file_name), file_dimensions)
    file_rect = file_scaled.get_rect(center=file_center)
    return file_scaled, file_rect

def text_loader(font, size, text, antialiasing, color, text_center):
    temp_text = pygame.font.SysFont(font, size).render(text, antialiasing, color)
    temp_text_center = temp_text.get_rect(center=text_center)
    return temp_text, temp_text_center


close_texture, close_texture_rect = texture_loader("close.png", (50,50), (1895,25))


wood_scoreboard, wood_rect = text_loader("Times New Roman", 50, "Wood: 0", False, "black", (1920/2, 200))
wood_texture, wood_texture_rect = texture_loader("minecraft_log.png", (300,300), (1920/2, 1080/2))
wood_texture_pre = wood_texture

fist_texture, fist_texture_rect = texture_loader("fist.webp", (100,100), (1920/2, 1000))

wooden_axe_texture, wooden_axe_texture_rect = texture_loader("wooden_axe.webp", (100,100), (1920/2, 1000))

crafting_texture, crafting_texture_rect = texture_loader("crafting_table.webp", (100,100), (400,1000))

planks_texture, planks_texture_rect = texture_loader("planks.webp", (100,100), (300,200))
planks_text1, planks_text_rect1 = text_loader('Arial', 30, "Planks: 0", False, "Black", (450,170))
planks_text2, planks_text_rect2 = text_loader('Arial', 30, "Cost: 1 Wood", False, "Black", (450,200))
planks_text3, planks_text_rect3 = text_loader('Arial', 30, "Output: 4 Planks", False, "Black", (450, 230))

sticks_texture, sticks_texture_rect = texture_loader("stick.webp", (100,100), (300,300))
sticks_text1, sticks_text_rect1 = text_loader('Arial', 30, "Sticks: 0", False, "Black", (400, 300))
sticks_text2, sticks_text_rect2 = text_loader('Arial', 30, "Cost: 2 Planks", False, "Black", (400, 330))
sticks_text3, sticks_text_rect3 = text_loader('Arial', 30, "Output: 4 Sticks", False, "Black", (400, 360))

tab_selector, tab_selector_rect = texture_loader("item_frame.png", (200,200), (1920/2, 1000))



blitionary_wood = [
    (wood_texture, wood_texture_rect),
    (crafting_texture, crafting_texture_rect),
    (fist_texture, fist_texture_rect),
    (close_texture, close_texture_rect)
]

blitionary_shop = [
    (close_texture, close_texture_rect),
    (crafting_texture, crafting_texture_rect),
    (fist_texture, fist_texture_rect),
    (planks_texture, planks_texture_rect),
    (planks_text2, planks_text_rect2),
    (planks_text3, planks_text_rect3),
]


class Shop:
    def __init__(self, name, text, resource, cost, output, owned):
        self.name = name
        self.text = text
        self.resource = resource
        self.cost = cost
        self.output = output
        self.owned = owned

    def buy(self, new_resource):
        self.resource = new_resource
        if self.resource - self.cost >= 0:      
            self.resource -= self.cost 
            self.owned += self.output 
            self.text = pygame.font.SysFont('Arial', 30).render(self.name + ": " + str(self.owned), False, "Black")
            

Item1 = Shop("Planks", planks_text1,  wood_count, 1, 4, 0)
Item2 = Shop("Sticks", sticks_text1, Item1.owned, 2, 4, 0)

def animate_wood(): 
    global wood_animation, wood_count
    wood_animation = True
    for x in range(31):
        if x <= 15:
             wood_texture_dimensions = (300-x, 300-x)
        else:
             wood_texture_dimensions = (270+x, 270+x)
        wood_texture = pygame.transform.scale(wood_texture_pre, wood_texture_dimensions)
        wood_texture_rect = wood_texture.get_rect(center=(1920/2, 1080/2))
        
        screen.blit(wood_texture, wood_texture_rect)
        screen.blit(wood_scoreboard, wood_rect)
        pygame.display.update()
    wood_count += 1
    wood_animation = False

def stick_render():
        blitionary_shop.append((sticks_texture, sticks_texture_rect))
        blitionary_shop.append((sticks_text2, sticks_text_rect2))
        blitionary_shop.append((sticks_text3, sticks_text_rect3))
        return True

wood_animation = False
wood_check = True
crafting_check = False
stick_render_check = False
game_loop = True


while game_loop == True:
    while wood_check == True:
        tab_selector_rect = tab_selector.get_rect(center=(1920/2, 1000))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_loop = False
                wood_check = False
            if event.type == pygame.MOUSEBUTTONDOWN and not wood_animation:
                if close_texture_rect.collidepoint(event.pos):
                    wood_check = False
                    game_loop = False
                if wood_texture_rect.collidepoint(event.pos):
                    animate_wood()
                if crafting_texture_rect.collidepoint(event.pos):
                    crafting_check = True
                    wood_check = False

        if wood_count % 10 == 0:
            wood_rect = wood_scoreboard.get_rect(center=(1920/2, 200))
        wood_scoreboard = pygame.font.SysFont("Times New Roman", 50).render("Wood: " + str(wood_count), False, "black")

        screen.fill("light blue")
        screen.blit(tab_selector, tab_selector_rect)
        screen.blit(wood_scoreboard, wood_rect)
        for surface, rect in blitionary_wood:
            screen.blit(surface, rect)

 
        pygame.display.update()
        

    while crafting_check == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_loop = False
                crafting_check = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if close_texture_rect.collidepoint(event.pos):
                    crafting_check = False
                    game_loop = False
                if fist_texture_rect.collidepoint(event.pos):
                    crafting_check = False
                    wood_check = True
                if planks_texture_rect.collidepoint(event.pos):
                    Item1.buy(wood_count)
                    wood_count = Item1.resource
                    planks_text1 = Item1.text = pygame.font.SysFont('Arial', 30).render("Planks: " + str(Item1.owned), False, "Black")
                if sticks_texture_rect.collidepoint(event.pos):
                    Item2.buy(Item1.owned)
                    Item1.owned = Item2.resource 
                    sticks_text1 = Item2.text
                    planks_text1 = Item1.text = pygame.font.SysFont('Arial', 30).render("Planks: " + str(Item1.owned), False, "Black")


        tab_selector_rect = tab_selector.get_rect(center=(400, 1000))
        screen.fill("light blue")
        screen.blit(wood_scoreboard, wood_rect)
        screen.blit(tab_selector, tab_selector_rect)
        screen.blit(planks_text1, planks_text_rect1)
        for surface, rect in blitionary_shop:
            screen.blit(surface, rect)
        if Item1.owned > 0 and stick_render_check == 0:
            stick_render_check = stick_render()
        if stick_render_check:
            screen.blit(sticks_text1, sticks_text_rect1)
        pygame.display.update()