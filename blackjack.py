# Martin Ivanov
# April 1 2020
# Updated Dec 23 2020
# Blackjack!!
# Need to add a "split" option

import pygame
from card_deck import Deck

_image_library = {}
pygame.init()
pygame.display.set_caption('Blackjack')
programIcon = pygame.image.load('myresources/icon.png')
pygame.display.set_icon(programIcon)

def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image is None:
        image = pygame.image.load(path)
        _image_library[path] = image
    return image


_cached_text = {}


def create_text(text, size, color):
    global _cached_text
    key = '|'.join(map(str, (size, color, text)))
    image = _cached_text.get(key, None)
    if image is None:
        font = pygame.font.SysFont("arialblack", size)
        image = font.render(text, True, color)
        _cached_text[key] = image
    return image


def centre_w(image, surface):
    image_rect = image.get_rect()
    img_w = image_rect.width
    surf_w = surface.get_width()
    return surf_w / 2 - img_w / 2


def centre_h(image, surface):
    image_rect = image.get_rect()
    img_h = image_rect.height
    surf_h = surface.get_height()
    return surf_h / 2 - img_h / 2


def make_button(text, colour):
    button_surface = pygame.Surface((175, 60))
    button_surface.fill((0, 0, 0))
    pygame.draw.rect(button_surface, colour, pygame.Rect(3, 3, 169, 54))
    button_text = create_text(str(text), 25, (0, 0, 0))
    button_surface.blit(button_text, (centre_w(button_text, button_surface), centre_h(button_text, button_surface)))
    return button_surface


def make_button_faded(text, colour):
    button_surface = pygame.Surface((175, 60))
    button_surface.fill((41, 23, 0))
    pygame.draw.rect(button_surface, colour, pygame.Rect(3, 3, 169, 54))
    button_text = create_text(str(text), 25, (0, 0, 0))
    button_surface.blit(button_text, (centre_w(button_text, button_surface), centre_h(button_text, button_surface)))
    return button_surface


def money_format(num):
    return "{:.2f}".format(num)


class SceneBase:
    def __init__(self):
        self.next = self

    def process_input(self, events, pressed_keys):
        pass

    def update(self):
        pass

    def render(self, screen):
        pass

    def switch_to_scene(self, next_scene):
        self.next = next_scene

    def terminate(self):
        self.switch_to_scene(None)


def run_game(starting_scene):
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    active_scene = starting_scene

    while active_scene is not None:
        pressed_keys = pygame.key.get_pressed()

        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or \
                              pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
                elif event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True

            if quit_attempt:
                active_scene.terminate()
            else:
                filtered_events.append(event)

        active_scene.process_input(filtered_events, pressed_keys)
        active_scene.update()
        active_scene.render(screen)

        active_scene = active_scene.next

        pygame.display.flip()
        clock.tick(60)


class BetScene(SceneBase):
    minus_button = pygame.Rect(275, 240 + 52.5, 35, 35)
    plus_button = pygame.Rect(490, 240 + 52.5, 35, 35)
    continue__button = pygame.Rect(346, 367, 108, 36)
    buttons_surf = pygame.Surface((195, 230))

    def __init__(self, bal):
        SceneBase.__init__(self)
        self.table_colour = (34, 177, 76)
        self.bal = bal
        self.bet = 0
        self.current_bet = 0
        self.avail_minus = False
        self.avail_plus = True
        self.continue_ = False

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if self.minus_button.collidepoint(mouse_pos) and self.avail_minus:
                    self.current_bet -= 25
                if self.plus_button.collidepoint(mouse_pos) and self.avail_plus:
                    self.current_bet += 25
                if self.continue__button.collidepoint(mouse_pos) and self.continue_:
                    self.bet = self.current_bet
                    self.bal -= self.bet
                    self.switch_to_scene(GameScene(self.bal, self.bet))

    def update(self):
        if self.current_bet > 0:
            self.avail_minus = True
        else:
            self.avail_minus = False
        if self.current_bet < self.bal:
            self.avail_plus = True
        else:
            self.avail_plus = False

    def render(self, screen):
        # draw background stuff
        screen.fill(self.table_colour)
        deck_img = get_image('myresources/deckimg.png')
        deck_img = pygame.transform.scale(deck_img, (148, 193))
        screen.blit(deck_img, (35, 85))
        pokerchips1_img = get_image('myresources/pokerchips1.png')
        screen.blit(pokerchips1_img, (5, 345))
        pokerchips2_img = get_image('myresources/pokerchips2.png')
        screen.blit(pokerchips2_img, (600, 0))
        x = 595
        y = 260
        z = 10
        self.buttons_surf.fill((80, 41, 0))
        pygame.draw.rect(self.buttons_surf, (90, 51, 0), pygame.Rect(5, 5, 175 + z, 210 + z))
        screen.blit(self.buttons_surf, (x, y))

        # show balance
        bal_surface = pygame.Surface((200, 50))
        bal_surface.fill((0, 0, 0))
        pygame.draw.rect(bal_surface, (255, 201, 14), pygame.Rect(5, 5, 190, 40))
        bal_text = create_text("$" + str(money_format(self.bal)), 25, (0, 0, 0))
        bal_surface.blit(bal_text, (10, centre_h(bal_text, bal_surface)))
        screen.blit(bal_surface, (10, 10))

        # bet area
        bet_surface = pygame.Surface((290, 120))
        # border
        bet_surface.fill((0, 0, 0))
        pygame.draw.rect(bet_surface, self.table_colour, pygame.Rect(5, 5, 280, 110))
        # bet text
        bet_text = create_text("Bet", 25, (0, 0, 0))
        bet_surface.blit(bet_text, (centre_w(bet_text, bet_surface), 7))
        # minus
        if self.avail_minus:
            bet_surface = self.draw_minus(bet_surface)
        else:
            bet_surface = self.draw_minus_faded(bet_surface)
        # plus
        if self.avail_plus:
            bet_surface = self.draw_plus(bet_surface)
        else:
            bet_surface = self.draw_plus_faded(bet_surface)
        # amount text
        amt_text = create_text("$" + str(self.current_bet), 40, (0, 0, 0))
        bet_surface.blit(amt_text, (centre_w(amt_text, bet_surface), centre_h(amt_text, bet_surface) + 7))
        screen.blit(bet_surface, (255, 240))

        # continue_ text
        continue__faded = create_text("Continue", 25, (17, 90, 39))
        continue__dark = create_text("Continue", 25, (0, 0, 0))
        if self.current_bet == 0 or self.current_bet > self.bal:
            self.continue_ = False
            screen.blit(continue__faded, (centre_w(continue__faded, screen), 367))
        else:
            self.continue_ = True
            screen.blit(continue__dark, (centre_w(continue__dark, screen), 367))

    def draw_minus(self, bet_surface):
        pygame.draw.rect(bet_surface, (0, 0, 0), pygame.Rect(20, 65, 35, 10))
        return bet_surface

    def draw_minus_faded(self, bet_surface):
        pygame.draw.rect(bet_surface, (17, 90, 39), pygame.Rect(20, 65, 35, 10))
        return bet_surface

    def draw_plus(self, bet_surface):
        pygame.draw.rect(bet_surface, (0, 0, 0), pygame.Rect(290 - 20 - 35, 65, 35, 10))
        pygame.draw.rect(bet_surface, (0, 0, 0), pygame.Rect(290 - 20 - 17.5 - 5, 65 - 17.5 + 5, 10, 35))
        return bet_surface

    def draw_plus_faded(self, bet_surface):
        pygame.draw.rect(bet_surface, (17, 90, 39), pygame.Rect(290 - 20 - 35, 65, 35, 10))
        pygame.draw.rect(bet_surface, (17, 90, 39), pygame.Rect(290 - 20 - 17.5 - 5, 65 - 17.5 + 5, 10, 35))
        return bet_surface


class GameScene(SceneBase):
    table_colour = (34, 177, 76)
    dealer_surface = pygame.Surface((280, 175))
    d_score_surf = pygame.Surface((80, 35))
    player_surface = pygame.Surface((280, 175))
    p_score_surf = pygame.Surface((80, 35))
    btn_stand = make_button("STAND", (237, 28, 36))
    btn_hit = make_button("HIT", (181, 230, 29))
    btn_double = make_button("DOUBLE", (163, 73, 164))
    btn_stand_faded = make_button_faded("STAND", (237, 28, 36))
    btn_hit_faded = make_button_faded("HIT", (181, 230, 29))
    btn_double_faded = make_button_faded("DOUBLE", (163, 73, 164))
    buttons_surf = pygame.Surface((195, 230))

    # btn_split = make_button("SPLIT", (0, 162, 232))

    def __init__(self, bal, bet):
        SceneBase.__init__(self)
        self.deck = Deck()
        self.bal = bal
        self.bet = bet
        self.score_dealer = 0
        self.score_dealer_alt = 0
        self.cards_dealer = []
        self.score_player = 0
        self.score_player_alt = 0
        self.cards_player = []
        self.game_over = False
        self.game_over_text = ""
        self.avail_stand = True
        self.avail_hit = True
        self.avail_double = False
        self.avail_continue = False
        if self.bal >= self.bet:
            self.avail_double = True
        # deal cards
        for i in range(2):
            self.cards_dealer.append(self.deck.deal_card())
        self.cards_dealer[1].faceup = False
        for i in range(2):
            self.cards_player.append(self.deck.deal_card())
        self.check_scores()

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if pygame.Rect(600, 265, 175, 60).collidepoint(mouse_pos) and self.avail_stand:
                    self.stand()
                if pygame.Rect(600, 340, 175, 60).collidepoint(mouse_pos) and self.avail_hit:
                    self.hit()
                if pygame.Rect(600, 415, 175, 60).collidepoint(mouse_pos) and self.avail_hit:
                    self.double()
                if pygame.Rect(631, 500, 108, 36).collidepoint(mouse_pos) and self.avail_continue:
                    if self.bal < 25:
                         self.switch_to_scene(GameOverScene())
                    else:
                        self.switch_to_scene(BetScene(self.bal))

    def update(self):
        self.calculate_scores()

    def render(self, screen):
        # draw background stuff
        screen.fill(self.table_colour)
        deck_img = get_image('myresources/deckimg.png')
        deck_img = pygame.transform.scale(deck_img, (148, 193))
        screen.blit(deck_img, (35, 85))
        pokerchips1_img = get_image('myresources/pokerchips1.png')
        screen.blit(pokerchips1_img, (5, 345))
        pokerchips2_img = get_image('myresources/pokerchips2.png')
        screen.blit(pokerchips2_img, (600, 0))

        # show balance
        bal_surface = pygame.Surface((200, 50))
        bal_surface.fill((0, 0, 0))
        pygame.draw.rect(bal_surface, (255, 201, 14), pygame.Rect(5, 5, 190, 40))
        bal_text = create_text("$" + str(money_format(self.bal)), 25, (0, 0, 0))
        bal_surface.blit(bal_text, (10, centre_h(bal_text, bal_surface)))
        screen.blit(bal_surface, (10, 10))

        # draw cards
        self.dealer_surface.fill(self.table_colour)
        for i in range(len(self.cards_dealer)):
            self.draw_card(self.dealer_surface, self.cards_dealer[i], i + 1, len(self.cards_dealer))
        screen.blit(self.dealer_surface, (220, 50))
        self.player_surface.fill(self.table_colour)
        for i in range(len(self.cards_player)):
            self.draw_card(self.player_surface, self.cards_player[i], i + 1, len(self.cards_player))
        screen.blit(self.player_surface, (220, 600 - 145 - 175))

        # draw scores
        self.d_score_surf = self.draw_score(self.d_score_surf, self.score_dealer, self.score_dealer_alt)
        screen.blit(self.d_score_surf, (505, 50 + 175 / 3))
        self.p_score_surf = self.draw_score(self.p_score_surf, self.score_player, self.score_player_alt)
        screen.blit(self.p_score_surf, (505, 280 + 175 / 3))

        # draw buttons
        self.draw_buttons(screen)

    def draw_card(self, surface, card, card_index, num_cards):
        if not card.faceup:
            image = get_image('myresources/back.bmp')
        else:
            image = get_image(card.get_path())
        image = pygame.transform.scale(image, (130, 175))
        surface.blit(image, (surface.get_width() - 130 - 30 * (num_cards - card_index), 0))

    def draw_score(self, surf, score, score_alt, ):
        surf.fill((0, 0, 0))
        if score == score_alt:
            score_text = create_text(str(score), 25, (255, 255, 255))
        else:
            score_text = create_text(str(score) + "/" + str(score_alt), 25, (255, 255, 255))
        surf.blit(score_text, (centre_w(score_text, surf), centre_h(score_text, surf)))
        return surf

    def draw_buttons(self, screen):
        x = 595
        y = 260
        z = 10
        if not self.game_over:
            self.buttons_surf.fill((80, 41, 0))
            pygame.draw.rect(self.buttons_surf, (90, 51, 0), pygame.Rect(5, 5, 175 + z, 210 + z))
            if pygame.Rect(x + 5, y + 5, 180, 60).collidepoint(pygame.mouse.get_pos()) and self.avail_stand:
                if self.avail_stand:
                    self.buttons_surf.blit(self.btn_stand, (z, z))
                if self.avail_hit:
                    self.buttons_surf.blit(self.btn_hit_faded, (z, 75 + z))
                if self.avail_double:
                    self.buttons_surf.blit(self.btn_double_faded, (z, 150 + z))
            elif pygame.Rect(x + 5, y + 80, 180, 60).collidepoint(pygame.mouse.get_pos()) and self.avail_hit:
                if self.avail_stand:
                    self.buttons_surf.blit(self.btn_stand_faded, (z, z))
                if self.avail_hit:
                    self.buttons_surf.blit(self.btn_hit, (z, 75 + z))
                if self.avail_double:
                    self.buttons_surf.blit(self.btn_double_faded, (z, 150 + z))
            elif pygame.Rect(x + 5, y + 155, 180, 60).collidepoint(pygame.mouse.get_pos()) and self.avail_hit:
                if self.avail_stand:
                    self.buttons_surf.blit(self.btn_stand_faded, (z, z))
                if self.avail_hit:
                    self.buttons_surf.blit(self.btn_hit_faded, (z, 75 + z))
                if self.avail_double:
                    self.buttons_surf.blit(self.btn_double, (z, 150 + z))
            else:
                if self.avail_stand:
                    self.buttons_surf.blit(self.btn_stand_faded, (z, z))
                if self.avail_hit:
                    self.buttons_surf.blit(self.btn_hit_faded, (z, 75 + z))
                if self.avail_double:
                    self.buttons_surf.blit(self.btn_double_faded, (z, 150 + z))
            screen.blit(self.buttons_surf, (x, y))
        else:
            self.draw_results(screen)

    def draw_results(self, screen):
        x = 595
        y = 260
        z = 10
        self.buttons_surf.fill((80, 41, 0))
        pygame.draw.rect(self.buttons_surf, (90, 51, 0), pygame.Rect(5, 5, 175 + z, 210 + z))
        if self.game_over_text == "BLACKJACK":
            result_text = create_text(self.game_over_text, 25, (255, 255, 255))
        else:
            result_text = create_text(self.game_over_text, 35, (255, 255, 255))
        self.buttons_surf.blit(result_text, (
            centre_w(result_text, self.buttons_surf), centre_h(result_text, self.buttons_surf) - 40))
        amt_text = create_text("Null", 35, (255, 255, 255))
        if self.game_over_text == "PUSH":
            amt_text = create_text("+0.00", 35, (9, 199, 0))
        elif self.game_over_text == "BUST":
            amt_text = create_text("-" + str(money_format(self.bet)), 35, (207, 0, 0))
        elif self.game_over_text == "WIN":
            amt_text = create_text("+" + str(money_format(self.bet)), 35, (9, 199, 0))
        elif self.game_over_text == "BLACKJACK":
            amt_text = create_text("+" + str(money_format(self.bet * 1.5)), 35, (9, 199, 0))
        self.buttons_surf.blit(amt_text,
                               (centre_w(amt_text, self.buttons_surf), centre_h(amt_text, self.buttons_surf) + 25))
        screen.blit(self.buttons_surf, (x, y))
        self.avail_continue = True
        continue__faded = create_text("Continue", 25, (17, 90, 39))
        continue__dark = create_text("Continue", 25, (0, 0, 0))
        if pygame.Rect(631, 500, 108, 36).collidepoint(pygame.mouse.get_pos()):
            screen.blit(continue__dark, (centre_w(continue__dark, self.buttons_surf) + x, 500))
        else:
            screen.blit(continue__faded, (centre_w(continue__faded, self.buttons_surf) + x, 500))

    def stand(self):
        self.avail_stand = False
        self.avail_hit = False
        self.avail_double = False
        self.cards_dealer[1].faceup = True
        self.calculate_scores()
        if self.score_player < self.score_player_alt and self.score_player_alt <= 21:
            self.score_player = self.score_player_alt
        if self.score_dealer > self.score_player:
            self.bust()
        else:
            if self.score_dealer < self.score_dealer_alt and self.score_dealer_alt <= 21:
                self.score_dealer = self.score_dealer_alt
            while self.score_dealer < 17:
                self.hit_dealer()
                self.calculate_scores()
                if self.score_dealer < self.score_dealer_alt and self.score_dealer_alt <= 21:
                    self.score_dealer = self.score_dealer_alt
                self.check_scores()
            self.calculate_scores()
            if self.score_player < self.score_player_alt and self.score_player_alt <= 21:
                self.score_player = self.score_player_alt
            if self.score_dealer < self.score_dealer_alt and self.score_dealer_alt <= 21:
                self.score_dealer = self.score_dealer_alt
            self.check_scores()

    def hit(self):
        self.cards_player.append(self.deck.deal_card())
        self.avail_double = False
        self.calculate_scores()
        self.check_scores()

    def hit_dealer(self):
        self.cards_dealer.append(self.deck.deal_card())

    def double(self):
        self.bal -= self.bet
        self.bet *= 2
        self.avail_double = False
        self.hit()
        self.cards_dealer[1].faceup = True
        self.calculate_scores()
        if self.score_player < self.score_player_alt and self.score_player_alt <= 21:
            self.score_player = self.score_player_alt
        if self.score_dealer > self.score_player or self.score_player > 21:
            self.bust()
        elif self.blackjack(self.cards_player):
            self.win(True)
        else:
            while self.score_dealer < 17:
                self.hit_dealer()
                self.calculate_scores()
                if self.score_dealer < self.score_dealer_alt and self.score_dealer_alt <= 21:
                    self.score_dealer = self.score_dealer_alt
                self.check_scores()
            self.calculate_scores()
            if self.score_player < self.score_player_alt and self.score_player_alt <= 21:
                self.score_player = self.score_player_alt
            if self.score_dealer < self.score_dealer_alt and self.score_dealer_alt <= 21:
                self.score_dealer = self.score_dealer_alt
            self.check_scores()
            
    def blackjack(self, cards):
        score = 0
        score_alt = 0
        for card in cards:
            val = card.get_val()
            if val > 10:
                val = 10
                val_alt = 10
            elif val == 1:
                val = 1
                val_alt = 11
            else:
                val_alt = val
            score += val
            score_alt += val_alt
        if score == 21 or score_alt == 21:
            return True
        else:
            return False

    def calculate_scores(self):
        # calculate scores
        self.score_dealer = 0
        self.score_dealer_alt = 0
        for card in self.cards_dealer:
            if card.faceup:
                val = card.get_val()
                if val > 10:
                    val = 10
                    val_alt = 10
                elif val == 1:
                    val = 1
                    val_alt = 11
                else:
                    val_alt = val
                self.score_dealer += val
                self.score_dealer_alt += val_alt
        if self.score_dealer_alt == 31:
            self.score_dealer = 21
        elif self.score_dealer_alt > 21:
            self.score_dealer_alt = self.score_dealer
        elif self.score_dealer_alt == 21:
            self.score_dealer = self.score_dealer_alt
        self.score_player = 0
        self.score_player_alt = 0
        for card in self.cards_player:
            if card.faceup:
                val = card.get_val()
                if val > 10:
                    val = 10
                    val_alt = 10
                elif val == 1:
                    val = 1
                    val_alt = 11
                else:
                    val_alt = val
                self.score_player += val
                self.score_player_alt += val_alt
        if self.score_player_alt == 31:
            self.score.player = 21
        elif self.score_player_alt > 21:
            self.score_player_alt = self.score_player
        elif self.score_player_alt == 21:
            self.score_player = self.score_player_alt

    def check_scores(self):
        if not self.game_over:
            self.calculate_scores()
            score_dealer = self.score_dealer
            score_player = self.score_player
            if score_dealer < self.score_dealer_alt:
                score_dealer = self.score_dealer_alt
            if score_player < self.score_player_alt:
                score_player = self.score_player_alt
            if self.blackjack(self.cards_dealer) and self.blackjack(self.cards_player):
                self.push()
            elif self.blackjack(self.cards_dealer):
                self.bust()
            elif self.blackjack(self.cards_player):
                self.win(True)
            elif score_dealer > 21 and score_player > 21:
                self.push()
            elif score_player > 21:
                self.bust()
            elif score_dealer > 21:
                self.win(False)
            elif score_player == score_dealer and score_dealer >= 17:
                self.push()
            elif score_player > score_dealer and score_dealer >= 17:
                self.win(False)
            elif score_player < score_dealer and score_dealer >= 17:
                self.bust()

    def push(self):
        self.game_over = True
        self.cards_dealer[1].faceup = True
        self.avail_stand = False
        self.avail_hit = False
        self.avail_double = False
        self.game_over_text = "PUSH"
        self.bal += self.bet

    def bust(self):
        self.game_over = True
        self.cards_dealer[1].faceup = True
        self.avail_stand = False
        self.avail_hit = False
        self.avail_double = False
        self.game_over_text = "BUST"

    def win(self, blackjack):
        self.game_over = True
        self.cards_dealer[1].faceup = True
        self.avail_stand = False
        self.avail_hit = False
        self.avail_double = False
        if blackjack:
            self.game_over_text = "BLACKJACK"
            self.bal += self.bet * 2 + self.bet / 2
        else:
            self.game_over_text = "WIN"
            self.bal += self.bet * 2

class GameOverScene(SceneBase):

    def __init__(self):
        SceneBase.__init__(self)
        self.table_colour = (178, 34, 34)

    def render(self, screen):
        screen.fill(self.table_colour)
        deck_img = get_image('myresources/deckimg.png')
        deck_img = pygame.transform.scale(deck_img, (148, 193))
        screen.blit(deck_img, (35, 85))
        pokerchips1_img = get_image('myresources/pokerchips1.png')
        screen.blit(pokerchips1_img, (5, 345))
        pokerchips2_img = get_image('myresources/pokerchips2.png')
        screen.blit(pokerchips2_img, (600, 0))
        over_text = create_text("GAME OVER", 40, (0, 0, 0))
        exit_text = create_text("Press the Escape key to exit.", 15, (0, 0, 0))
        screen.blit(over_text, (centre_w(over_text, screen), centre_h(over_text, screen) - 30))
        screen.blit(exit_text, (centre_w(exit_text, screen), centre_h(exit_text, screen)))

    def terminate(self):
        self.switch_to_scene(None)

run_game(BetScene(500))

