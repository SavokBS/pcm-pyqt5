import math
import random
import sys
import time

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QMenu, QDesktopWidget, QTextEdit, \
    QLineEdit, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QPainter, QColor, QKeyEvent, QPaintDevice
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QVariantAnimation


class Dot:
    def __init__(self):
        self.isVisible = True
        self.isPushing = True
        self.x = 200
        self.y = 200
        self.dy = 0
        self.dx = 0

    def __repr__(self):
        return 'Dot'

class Rect:
    def __init__(self):
        self.isVisible = True
        self.isPushing = True
        self.x = 200
        self.y = 200
        self.dy = 0
        self.dx = 0
    def __repr__(self):
        return 'Rect'


class PcmQT(QWidget):
    def __init__(self):
        super().__init__()
        print('[PCM-QT] PyQT5: inited')
        self.initUI()

    def initUI(self):
        # init base and update
        self.setWindowTitle('PCM-QT')
        self.char = Dot()
        self.fps = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateScreen)
        self.timer.start(10)

        # init fps label
        self.fps_visible = True
        self.fps_label = QLabel(self)
        self.fps_label.setStyleSheet("QFrame { background-color: white; border: 2px solid gray; border-radius: 5px; }")
        self.fps_label.setAlignment(Qt.AlignRight | Qt.AlignTop)
        self.fps_label.move(self.width() - self.fps_label.width(), 0)

        # init menu
        self.menu_visible = False
        self.menu_window = QWidget(self)
        self.menu_window.setGeometry(850, 400, 200, 200)
        self.menu_window.hide()

        menu_layout = QVBoxLayout()
        menu_layout.setAlignment(Qt.AlignCenter)
        self.menu_window.setLayout(menu_layout)

        self.menu_floor_btn = QPushButton("Floor: White")
        self.menu_floor_btn.clicked.connect(self.toggleFloor)
        menu_layout.addWidget(self.menu_floor_btn)

        self.menu_exit_button = QPushButton("Exit")
        self.menu_exit_button.clicked.connect(self.close)
        menu_layout.addWidget(self.menu_exit_button)
        self.menu_window.setStyleSheet(
            "QWidget { background-color: white; border: 2px solid gray; border-radius: 5px; }")

        # init debug menu
        self.debug_visible = False
        self.debug_menu = QWidget(self)
        self.debug_menu.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding))
        self.debug_menu.hide()


        debug_layout = QVBoxLayout()
        debug_layout.setAlignment(Qt.AlignTop)
        self.debug_menu.setLayout(debug_layout)

        self.debug_title = QLabel("Debug Menu")
        self.debug_title.setAlignment(Qt.AlignTop)
        self.debug_title.setStyleSheet("background-color: black; color: yellow")
        debug_layout.addWidget(self.debug_title)

        self.debug_crash_btn = QPushButton("Test button (crash)")
        self.debug_crash_btn.clicked.connect(self.close)
        debug_layout.addWidget(self.debug_crash_btn)

        self.debug_fakedot_btn = QPushButton("Add fake dot ")
        self.debug_fakedot_btn.clicked.connect(self.drawFakeDot)
        debug_layout.addWidget(self.debug_fakedot_btn)
        self.fakeDots = []

        self.debug_delfakedots_btn = QPushButton("Del fake dots")
        self.debug_delfakedots_btn.clicked.connect(self.deleteFakeDots)
        debug_layout.addWidget(self.debug_delfakedots_btn)

        self.debug_selfkill_btn = QPushButton("Self-Kill")
        self.debug_selfkill_btn.clicked.connect(self.selfKillDot)
        debug_layout.addWidget(self.debug_selfkill_btn)

        self.debug_togglefps_btn = QPushButton("Toggle FPS")
        self.debug_togglefps_btn.clicked.connect(self.toggleFPS)
        debug_layout.addWidget(self.debug_togglefps_btn)

        self.debug_changechar_btn = QPushButton(f"Char: {self.char.__repr__()}")
        self.debug_changechar_btn.clicked.connect(self.toggleChar)
        debug_layout.addWidget(self.debug_changechar_btn)

        self.build_mode = False
        self.builds = []
        self.debug_buildmode_btn = QPushButton(f"Build mode: {self.build_mode}")
        self.debug_buildmode_btn.clicked.connect(self.buildMode)
        debug_layout.addWidget(self.debug_buildmode_btn)

        self.bullets = []
        self.debug_delbullets_btn = QPushButton("Del bullets")
        self.debug_delbullets_btn.clicked.connect(self.bullets.clear)
        debug_layout.addWidget(self.debug_delbullets_btn)

        self.debug_delbuilds_btn = QPushButton("Del builds")
        self.debug_delbuilds_btn.clicked.connect(self.builds.clear)
        debug_layout.addWidget(self.debug_delbuilds_btn)

        self.debug_togglepushing_btn = QPushButton("Toggle pushing")
        self.debug_togglepushing_btn.clicked.connect(self.togglePushing)
        debug_layout.addWidget(self.debug_togglepushing_btn)

        self.debug_close_btn = QPushButton("Close menu")
        self.debug_close_btn.clicked.connect(self.toggleDebugMenu)
        debug_layout.addWidget(self.debug_close_btn)

        self.debug_menu.setStyleSheet(
            "QWidget { background-color: white; border: 2px solid gray; border-radius: 5px; }")


        # init chat box
        self.chat_widget = QWidget(self)
        self.chat_widget.setGeometry(0, 830, 400, 200)
        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        self.chat_box = QLineEdit()
        self.chat_box.setFocusPolicy(Qt.ClickFocus)
        self.chat_send = QPushButton("✈️")
        self.chat_send.clicked.connect(self.sendMessageChat)

        chat_layout = QVBoxLayout()
        chat_box_layout = QHBoxLayout()
        chat_layout.addWidget(self.chat)
        chat_box_layout.addWidget(self.chat_box)
        chat_box_layout.addWidget(self.chat_send)
        chat_layout.addLayout(chat_box_layout)
        self.chat_widget.setLayout(chat_layout)


        # init fps display counter
        self.fpst = QTimer()
        self.fpst.setInterval(100)
        self.fpst.timeout.connect(self.fps_display)
        self.fpst.start()





        print('[PCM-QT] Battle UI: inited')



    def fps_display(self):
        start_time = time.time()
        counter = 1
        time.sleep(0.015)
        time_now = time.time()
        self.fps = str((counter // (time_now - start_time)))

    def paintEvent(self, e):
        char = self.char.__class__
        qp = QPainter()
        qp.begin(self)
        if self.char.isVisible:
            if char == Dot:
                self.drawDot(qp)
            elif char == Rect:
                self.drawRect(qp)
        for i in self.fakeDots:
            qp.setBrush(QColor(255, 0, 0))
            qp.drawEllipse(i[0], i[1], 50, 50)
        for i in self.builds:
            qp.setBrush(QColor(165, 42, 42))
            qp.drawRect(i[0], i[1], 30, 30)
        for i in self.bullets:
            qp.setBrush(QColor(200, 100, 50))
            qp.drawEllipse(i[0], i[1], 20, 20)
        qp.end()

    def drawRect(self, qp):
        qp.setBrush(QColor(255, 0,0))
        qp.drawRect(self.char.x, self.char.y, 50, 50)

    def drawDot(self, qp):
        qp.setBrush(QColor(255, 0, 0))
        qp.drawEllipse(self.char.x, self.char.y, 50, 50)

    def drawFakeDot(self):
        self.fakeDots.append([random.randint(0, self.width()), random.randint(0, self.height())])

    def drawBuild(self, x,y):
        self.builds.append([x,y])

    def deleteFakeDots(self):
        print(f'[PCM-QT] Debug: deleted fake dots : {len(self.fakeDots)} deleted.')
        self.fakeDots.clear()

    def selfKillDot(self):
        self.char.isVisible = not self.char.isVisible
        print(f'[PCM-QT] Debug: self-killed : {not self.char.isVisible}')
        if self.char.isVisible:
            print('[PCM-QT] Debug: spawn dot at (200;200) : respawn')
            self.char.x, self.char.y = 200, 200

    def buildMode(self):
        self.build_mode = not self.build_mode
        self.debug_buildmode_btn.setText(f"Build mode: {self.build_mode}")
        print(f'[PCM-QT] Debug: build mode: {self.build_mode}')

    def keyPressEvent(self, e: QKeyEvent):
        if not self.char.isVisible:
            return
        if e.key() == Qt.Key_W:
            self.char.dy = -1
        elif e.key() == Qt.Key_A:
            self.char.dx = -1
        elif e.key() == Qt.Key_S:
            self.char.dy = 1
        elif e.key() == Qt.Key_D:
            self.char.dx = 1
        elif e.key() == Qt.Key_Escape:
            self.toggleMenu()
        if e.key() == Qt.Key_F and e.modifiers() == Qt.ShiftModifier:
            #debug
            self.toggleDebugMenu()

    def keyReleaseEvent(self, e: QKeyEvent):
        if e.key() in (Qt.Key_W, Qt.Key_S):
            self.char.dy = 0
        elif e.key() in (Qt.Key_A, Qt.Key_D):
            self.char.dx = 0

    def mousePressEvent(self, e): # a0
        self.click_x = e.x()
        self.click_y = e.y()
        if not self.build_mode:
            angle = math.atan2(self.click_y - self.char.y, self.click_x - self.char.x)
            velocity = (5 * math.cos(angle), 5 * math.sin(angle))
            self.bullets.append([self.char.x, self.char.y, self.click_x, self.click_y, angle, velocity])
        if self.build_mode:
            self.drawBuild(self.click_x, self.click_y)



    def toggleDebugMenu(self):
        self.debug_visible = not self.debug_visible
        self.debug_menu.setVisible(self.debug_visible)
    def toggleMenu(self):
        self.menu_visible = not self.menu_visible
        self.menu_window.setVisible(self.menu_visible)

    def toggleFPS(self):
        self.fps_visible = not self.fps_visible
        self.fps_label.setVisible(self.fps_visible)

    def togglePushing(self):
        self.char.isPushing = not self.char.isPushing

    def toggleChar(self):
        x = self.char.x
        y = self.char.y
        if self.char.__class__ == Dot:
            self.char = Rect()
        elif self.char.__class__ == Rect:
            self.char = Dot()
        self.debug_changechar_btn.setText(f"Char: {self.char.__repr__()}")
        self.char.x = x
        self.char.y = y

    def toggleFloor(self):
        if self.menu_floor_btn.text() == "Floor: White":
            self.menu_window.setStyleSheet(
                "QWidget { background-color: black; border: 2px solid gray; border-radius: 5px; }")
            self.debug_menu.setStyleSheet("QWidget { background-color: black; border: 2px solid gray; border-radius: 5px; }")
            self.fps_label.setStyleSheet(
                "QFrame { background-color: black; border: 2px solid gray; border-radius: 5px; }")
            self.setStyleSheet("background-color: black; color: white;")
            self.menu_floor_btn.setText("Floor: Black")
        else:
            self.menu_window.setStyleSheet(
            "QWidget { background-color: white; border: 2px solid gray; border-radius: 5px; }")
            self.debug_menu.setStyleSheet(
                "QWidget { background-color: white; border: 2px solid gray; border-radius: 5px; }")
            self.fps_label.setStyleSheet(
                "QFrame { background-color: white; border: 2px solid gray; border-radius: 5px; }")
            self.setStyleSheet("background-color: white; color: black;")
            self.menu_floor_btn.setText("Floor: White")

    def sendMessageChat(self):
        # handling chat messages and commands...
        message = self.chat_box.text()
        if message:
            if message == "/debug":
                self.toggleDebugMenu()
                self.chat.append(f"[CONSOLE] debug toggled.")
            elif message == "/menu":
                self.toggleMenu()
                self.chat.append("[CONSOLE] menu opened.")
            elif message == "/floor":
                self.toggleFloor()
                self.chat.append("[CONSOLE] floor toggled.")
            elif message == "/fps":
                self.toggleFPS()
                self.chat.append("[CONSOLE] toggled fps.")
            elif message == "/objects":
                all_objects = len(self.fakeDots) + len(self.bullets) + len(self.builds) + 1 # +1 - char
                fake_dots = len(self.fakeDots)
                bullets = len(self.bullets)
                builds = len(self.builds)
                self.chat.append(f"[CONSOLE] All objects: {all_objects}\nFake dots: {fake_dots}\nBullets: {bullets}\nBuilds: {builds}")
            elif message.split()[0] == "/fakedot":
                try:
                    count = int(message.split()[1])
                    for i in range(count):
                        self.drawFakeDot()
                    self.chat.append(f"[CONSOLE] added {count} fake dots.")
                except Exception as e:
                    self.chat.append(str(e))
            else:
                self.chat.append(f"You: " + message)
            self.chat_box.clear()
            self.chat_box.setFocusPolicy(Qt.ClickFocus)
    def updateScreen(self):
        if self.char.x > self.width():
            self.char.x = self.width()
        elif self.char.x < 0:
            self.char.x = 0
        elif self.char.y > self.height():
            self.char.y = self.height()
        elif self.char.y < 0:
            self.char.y = 0
        else:
            self.char.x += self.char.dx * 3
            self.char.y += self.char.dy * 3

        # battle logic. (builds bypassing.)
        for build_x, build_y in self.builds:
            distance = math.sqrt((self.char.x - build_x)**2 + (self.char.y - build_y)**2)
            min_distance = math.sqrt(2000)
            if distance < min_distance:
                # go away dude
                self.char.x -= 1
                self.char.y -=1

            for i in self.bullets:
                distance = math.sqrt((i[0] - build_x) ** 2 + (i[1] - build_y) ** 2) # i[0] - x, i[1] - y
                min_distance = math.sqrt(500)
                if distance < min_distance:
                    self.bullets.remove(i)

            for i in self.fakeDots:
                distance = math.sqrt((i[0]- build_x) ** 2 + (i[1]- build_y) ** 2) # i[0] - x, i[1] - y
                min_distance = math.sqrt(2000)
                if distance < min_distance:
                    # go away dude
                    i[0] -= 1
                    i[1] -= 1


        for i in self.fakeDots:
            distance = math.sqrt((self.char.x - i[0]) ** 2 + (self.char.y - i[1]) ** 2) # i[0] - x, i[1] - y
            min_distance = math.sqrt(2000)
            if distance < min_distance:
                if self.char.isPushing:
                    self.char.x -= 1
                    self.char.y -= 1
                    i[0] += 1
                    i[1] += 1



        # (bullet logic)
        for i in self.bullets:

            i[0] += int(i[5][0]) # bullet_x += velocity_x
            i[1] += int(i[5][1]) # bullet_y += velocity_y
            if i[0] == i[2] or i[1] == i[3]: # if bullet_x == velocity_X or bullet_y == velocity_y:
                self.bullets.remove(i)

        # update fps label
        self.fps_label.setText(f"{self.fps} fps")
        self.fps_label.adjustSize()
        self.fps_label.move(self.width() - self.fps_label.width(), 0)

        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = PcmQT()
    game.show()
    sys.exit(app.exec_())
