# ゲームの準備
import os
import pygame as pg
import sys
import random

from pygame.transform import scale

pg.init()
pg.mixer.init(frequency=44100)
screen = pg.display.set_mode((800, 600))

# データ
# プレイヤーデータ
myrect = pg.Rect(50, 200, 40, 50)
# 障害物データ
boxrect = pg.Rect(300, 200, 100, 100)
# 壁データ
walls = [pg.Rect(0, 0, 800, 20),
         pg.Rect(0, 0, 20, 600),
         pg.Rect(780, 0, 20, 600),
         pg.Rect(0, 580, 800, 20), ]
# お化けデータ
enemyrect = pg.Rect(650, 200, 50, 50)
# ゴールデータ
goalrect = pg.Rect(750, 250, 30, 100)
# メインで使う変数
rightFlag = True
pushFlag = False
page = 1

# 画像の読み込み
# プレイヤーRイメージ
main_path = os.path.dirname(os.path.abspath(__file__))
file_path_1 = os.path.join(main_path, "playerR.png")
myimgR = pg.image.load(file_path_1)
# スケールの変更
myimgR = pg.transform.scale(myimgR, (40, 50))
# プレイヤーRを反転
myimgL = pg.transform.flip(myimgR, True, False)
# 罠イメージ
main_path = os.path.dirname(os.path.abspath(__file__))
file_path_2 = os.path.join(main_path, "images/uni.png")
trapimg = pg.image.load(file_path_2)
# スケールの変更
trapimg = pg.transform.scale(trapimg, (30, 30))
# 空のリスト
traps = []
# 罠の複製
for i in range(20):
    wx = 150+i*30
    wy = random.randint(20, 550)
    traps.append(pg.Rect(wx, wy, 30, 30))
# ボタンイメージ
main_path = os.path.dirname(os.path.abspath(__file__))
file_path_3 = os.path.join(main_path, "replaybtn.png")
replay_img = pg.image.load(file_path_3)
# お化けイメージ
main_path = main_path = os.path.dirname(os.path.abspath(__file__))
file_path_4 = os.path.join(main_path, "obake.png")
enemyimgR = pg.image.load(file_path_4)
# スケールの変更
enemyimgR = pg.transform.scale(enemyimgR, (50, 50))
# 画像の反転
enemyimgL = pg.transform.flip(enemyimgR, True, False)


# ボタンを押したらnewpageにジャンプする


def button_to_jamp(btn, newpage):
    global page, pushFlag
    # ユーザーからの入力を調べる
    # どのボタンが押されているのか
    mdown = pg.mouse.get_pressed()
    # どの場所が指されているのか
    (mx, my) = pg.mouse.get_pos()
    # 左クリック時の処理
    if mdown[0]:
        # 左クリックした点がbtnの範囲に入っている、且ボタンが押されていない場合
        if btn.collidepoint(mx, my) and pushFlag == False:
            pg.mixer.music.load("/Users/pgy-t/Documents/python/pi.mp3")
            pg.mixer.music.play(1)
            page = newpage
            pushFlag = True
    # 押されてない時の処理
    else:
        pushFlag = False


# ゲームステージ


def gamestage():
    global rightFlag
    global page
    # 画面の初期化
    screen.fill(pg.Color("DEEPSKYBLUE"))
    vx = 0
    vy = 0
    # ユーザーからの入力を調べる
    key = pg.key.get_pressed()
    # 絵を描いたり判定したりする
    if key[pg.K_RIGHT]:
        vx = 4
        rightFlag = True
    if key[pg.K_LEFT]:
        vx = -4
        rightFlag = False
    if key[pg.K_UP]:
        vy = -4
    if key[pg.K_DOWN]:
        vy = 4
    # プレイヤーの処理
    myrect.x += vx
    myrect.y += vy
    # 壁との衝突判定
    if myrect.collidelist(walls) != -1:
        myrect.x -= vx
        myrect.y -= vy
    if rightFlag:
        screen.blit(myimgR, myrect)
    else:
        screen.blit(myimgL, myrect)
    # 壁の処理
    for wall in walls:
        pg.draw.rect(screen, pg.Color("DARKGREEN"), wall)
    # 罠の処理
    for trap in traps:
        screen.blit(trapimg, trap)
    # 罠との衝突判定
    if myrect.collidelist(traps) != -1:
        myrect.x -= vx
        myrect.y -= vy
        pg.mixer.music.load("/Users/pgy-t/Documents/python/down.mp3")
        pg.mixer.music.play(1)
        page = 2
    # ゴールの処理
    pg.draw.rect(screen, pg.Color("GOLD"), goalrect)
    if myrect.colliderect(goalrect):
        # 音楽ファイルの読み込み
        pg.mixer.music.load("/Users/pgy-t/Documents/python/up.mp3")
        # 音楽の再生回数
        pg.mixer.music.play()
        page = 3
    # お化けの処理
    ovx = 0
    ovy = 0
    if enemyrect.x < myrect.x:
        ovx = 1
    else:
        ovx = -1
    if enemyrect.y < myrect.y:
        ovy = 1
    else:
        ovy = -1
    enemyrect.x += ovx
    enemyrect.y += ovy
    if ovx > 0:
        # 表示
        screen.blit(enemyimgR, enemyrect)
    else:
        # 表示
        screen.blit(enemyimgL, enemyrect)
    if myrect.colliderect(enemyrect):
        # 音楽ファイルの読み込み
        pg.mixer.music.load("/Users/pgy-t/Documents/python/down.mp3")
        # 音楽の再生回数
        pg.mixer.music.play()
        page = 2
# データのリセット


def gamereset():
    myrect.x = 50
    myrect.y = 100
    for d in range(20):
        traps[d].x = 150+d*30
        traps[d].y = random.randint(20, 550)

# ゲームオーバー


def gameover():
    gamereset()
    screen.fill(pg.Color("NAVY"))
    font = pg.font.Font(None, 150)
    text = font.render("GAMEOVER", True, pg.Color("RED"))
    screen.blit(text, (100, 200))
    btn1 = screen.blit(replay_img, (320, 480))
    # 絵を描いたり判定したりする
    button_to_jamp(btn1, 1)

# ゲームクリア


def gameclear():
    gamereset()
    screen.fill(pg.Color("GOLD"))
    font = pg.font.Font(None, 150)
    text = font.render("GAMECLEAR", True, pg.Color("RED"))
    screen.blit(text, (60, 200))
    btn1 = screen.blit(replay_img, (320, 480))
    # 絵を描いたり判定したりする
    button_to_jamp(btn1, 1)


# この下をループさせる
while True:
    if page == 1:
        gamestage()
    elif page == 2:
        gameover()
    elif page == 3:
        gameclear()
# 画面を表示する
    pg.display.update()
    pg.time.Clock().tick(60)
# 閉じるボタンが押されたら終了する（Whleから抜ける）
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            pg.display.quite()
            pg.quite()
            sys.exit()
