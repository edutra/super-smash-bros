import sys
import pygame as pg

# move up one directory to be able to import the settings and images
sys.path.append("..")
from objects.Button import Button
from objects.CharButton import CharButton
from objects.ReadyButton import ReadyButton
from settings import *
from images import *
from Chat import Chat

class Start:
    def __init__(self, game):
        self.g = game

        back = Button('back', 20, 20, 100, 100)
        ready = ReadyButton('ready', 400, 560, 300, 100)
        mario = CharButton('mario', 25, 210, 150, 350)
        luigi = CharButton('luigi', 210, 210, 150, 350)
        yoshi = CharButton('yoshi', 390, 210, 150, 350)
        popo = CharButton('popo', 575, 210, 150, 350)
        nana = CharButton('nana', 750, 210, 150, 350)
        link = CharButton('link', 920, 210, 150, 350)

        font = pg.font.Font(None, 100)
        screen = 'name'

        old_name = ''
        enteredName = False
        player_ready = False

        while self.g.status == START:

            # repeatedly check if the name is available
            self.g.checkName(self.g.curr_player)

            if screen == 'name':
                self.g.screen.blit(START_NAME_BG, ORIGIN)
            elif screen == 'no_name':
                self.g.screen.blit(START_NO_NAME_BG, ORIGIN)
            elif screen == 'character':
                self.g.screen.blit(START_CHARACTER_BG, ORIGIN)
            elif screen == 'waiting':
                self.g.screen.blit(START_WAITING_BG, ORIGIN)

            if screen == 'name' or screen == 'no_name':
                if not self.g.name_available:
                    if self.g.curr_player != old_name: 
                        self.g.screen.blit(START_NAME_EXISTS_BG, ORIGIN)

                text_surface = font.render(self.g.curr_player, True, WHITE)
                self.g.screen.blit(text_surface, (355,355))
            
            for event in pg.event.get():
                pos = pg.mouse.get_pos()

                if event.type == pg.QUIT:
                    print("You quit in the middle of the game!")
                    self.g.running = False
                    if self.g.playing:
                        self.g.playing = False
                    if enteredName:
                        self.g.disconnectPlayer(self.g.curr_player)
                    quit()
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    if back.isOver(pos) and not player_ready: 
                        if screen == 'name':
                            self.g.status = INTRO
                            if enteredName:
                                self.g.disconnectPlayer(self.g.curr_player)
                            break
                        elif screen == 'no_name':
                            self.g.status = INTRO
                            if enteredName:
                                self.g.disconnectPlayer(self.g.curr_player)
                            break
                        elif screen == 'character':
                            screen = 'name'
                        elif screen == 'waiting':
                            screen = 'character'

                    if screen == 'character':
                        if mario.isOver(pos, 'mario'):
                            self.g.editPlayerCharacter(self.g.curr_player, MARIO)
                            screen = 'waiting'
                        elif luigi.isOver(pos, 'luigi'):
                            self.g.editPlayerCharacter(self.g.curr_player, LUIGI)
                            screen = 'waiting'
                        elif yoshi.isOver(pos, 'yoshi'):
                            self.g.editPlayerCharacter(self.g.curr_player, YOSHI)
                            screen = 'waiting'
                        elif popo.isOver(pos, 'popo'):
                            self.g.editPlayerCharacter(self.g.curr_player, POPO)
                            screen = 'waiting'
                        elif nana.isOver(pos, 'nana'):
                            self.g.editPlayerCharacter(self.g.curr_player, NANA)
                            screen = 'waiting'
                        elif link.isOver(pos, 'link'):
                            self.g.editPlayerCharacter(self.g.curr_player, LINK)
                            screen = 'waiting'

                    if screen == 'waiting':
                        if ready.isOver(pos):
                            if ready.clicked:
                                self.g.editPlayerStatus(self.g.curr_player, 'unready')
                                player_ready = False
                                ready.click()
                            else:
                                self.g.editPlayerStatus(self.g.curr_player, 'ready')
                                player_ready = True
                                ready.click()

                if event.type == pg.MOUSEMOTION:
                    back.isOver(pos)
                    if screen == 'character':
                        mario.isOver(pos, 'mario')
                        luigi.isOver(pos, 'luigi')
                        yoshi.isOver(pos, 'yoshi')
                        popo.isOver(pos, 'popo')
                        nana.isOver(pos, 'nana')
                        link.isOver(pos, 'link')
                    if screen == 'waiting':
                        ready.isOver(pos)

                if event.type == pg.KEYDOWN:
                    if screen == 'name' or screen == 'no_name' or screen == 'waiting':
                        if event.key == pg.K_RETURN:
                            if screen != 'waiting':
                                if len(self.g.curr_player) == 0:
                                    screen = 'no_name'
                                    print("INVALID NAME! Your name cannot be blank!")
                                else:
                                    if self.g.name_available or self.g.curr_player == old_name:
                                        screen = 'character'
                                        if not enteredName:
                                            enteredName = True
                                            old_name = self.g.curr_player
                                            self.g.connectPlayer(self.g.curr_player)
                                        elif enteredName:
                                            self.g.editPlayerName(old_name, self.g.curr_player)
                                            old_name = self.g.curr_player
                                    elif not self.g.name_available:
                                        print("NAME EXISTS! Enter a unique one!")
                            
                            else:
                                if player_ready:
                                    # initialize chat to create lobby
                                    self.g.chat = Chat(self.g)
                                    lobby_id = self.g.chat.createLobby(6).lobby_id
                                    self.g.createChatLobby(lobby_id)

                                    self.g.startGame()

                        else:
                            # limit character length for the screen
                            if len(self.g.curr_player) < 10:
                                char = event.unicode
                                self.g.curr_player += char
            
            if screen == 'name' or screen == 'no_name':
                keys = pg.key.get_pressed()
                if keys[pg.K_BACKSPACE]:
                    self.g.curr_player = self.g.curr_player[:-1]

            if screen == 'character':
                self.g.screen.blit(mario.image, (mario.x, mario.y))
                self.g.screen.blit(luigi.image, (luigi.x, luigi.y))
                self.g.screen.blit(yoshi.image, (yoshi.x, yoshi.y))
                self.g.screen.blit(popo.image, (popo.x, popo.y))
                self.g.screen.blit(nana.image, (nana.x, nana.y))
                self.g.screen.blit(link.image, (link.x, link.y))

            elif screen == 'waiting':
                self.g.getPlayersReadyCount()
                self.g.screen.blit(ready.image, (ready.x, ready.y))
                text_surface = font.render(str(self.g.player_count), True, WHITE)
                self.g.screen.blit(text_surface,(700,440))
                self.g.joinGame()

            if not player_ready:
                self.g.screen.blit(back.image, (back.x, back.y))

            pg.display.flip()