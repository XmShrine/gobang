import os
import sys
import datetime

chess_num = 3 # 决定你是几子棋

size_x = 30 # 后续可调整
size_y = 30

play1_sym = "●"
play2_sym = "○"
default_sym = "+"

def create_game_data(date, x, y, fuser, suser, data):
    return {"date":date, "sizex":x, "sizey":y, "first_user":fuser, "second_user":suser, "data":data}

def help_check_win(temp_data):
    if len(temp_data) == 0:
        return False
    x = len(temp_data)
    y = len(temp_data[0])
    for i in range(x):
        for j in range(y):
            if x-i>=chess_num:
                for k in range(chess_num):
                    if temp_data[i+k][j] != 1:
                        break
                else:
                    return True
            if y-j>=chess_num:
                for k in range(chess_num):
                    if temp_data[i][j+k] != 1:
                        break
                else:
                    return True
            if x-i>=chess_num and y>=chess_num-1:
                for k in range(chess_num):
                    if temp_data[i+k][j-k] != 1:
                        break
                else:
                    return True
            if x-i>=chess_num and y-j>=chess_num:
                for k in range(chess_num):
                    if temp_data[i+k][j+k] != 1:
                        break
                else:
                    return True
    return False


def check_win(game_data, x, y):
    temp1 = [[0]*y for _ in range(x)]
    temp2 = [[0]*y for _ in range(x)]
    for i in range(len(game_data)):
        if i%2 == 0:
            temp1[game_data[i][0]][game_data[i][1]] = 1
        else:
            temp2[game_data[i][0]][game_data[i][1]] = 1
        if help_check_win(temp1) == True:
            return -1
        if help_check_win(temp2) == True:
            return 1
    return 0
    pass

def clear():
    if sys.platform.startswith('win'):
        os.system('cls')
    else:
        os.system('clear')

def save_data():
    game_data[0] = len(game_data[1])
    count_file = open(count_file_link, "w")
    count_file.write(f"{game_data[0]}")
    user_file = open(user_file_link, "w")
    user_name = user_data.keys()
    for i in user_name:
        user_file.write(f"{i}\n")
    for i in range(game_data[0]):
        temp = game_data[1][i]
        file = open(f"{i}", "w")
        file.write(f"{temp["date"]}\n{temp["first_user"]}\n{temp["second_user"]}\n{temp["sizex"]}\n{temp["sizey"]}\n")
        for i in temp["data"]:
            file.write(f"{i[0]} {i[1]}\n")
    pass

user_data = {}
game_data = [0, []]

data_link = "GobangData"
count_file_link = "count"
user_file_link = "user"

if not os.path.exists(data_link):
    os.mkdir(data_link)
    print("未创建数据文件夹，已创建")
else:
    try:
        count_file = open(count_file_link, "r")
        try:
            game_data[0] = int(count_file.readline())
        except Exception:
            print("游戏数据文件格式有问题，游戏加载失败")
            exit()
    except FileNotFoundError:
        count_file = open(count_file_link, "w")
        count_file.write("0")
        print("游戏数据次数文件未创建，已创建")
    try:
        user_file = open(user_file_link, "r")
        buff = user_file.readline().strip()
        while buff != "":
            if buff.isalnum():
                if buff in user_data:
                    print(f"出现重复用户名 '{buff}'")
                else:
                    user_data[buff] = 0
            else:
                print(f"用户名 '{buff}' 不符合规范")
            buff = user_file.readline().strip()

    except FileNotFoundError:
        count_file = open(user_file_link, "w")
        print("用户数据文件未创建，已创建")
    
    for i in range(game_data[0]):
        try:
            file = open(f"{i}", "r")
            date = file.readline().strip()
            fuser = file.readline().strip()
            suser = file.readline().strip()
            if fuser not in user_data.keys() or suser not in user_data.keys():
                print(f"第 {i+1} 局游戏中的玩家 {fuser} 或 {suser} 不是已注册玩家")
            else:
                sizex = int(file.readline().strip())
                sizey = int(file.readline().strip())
                temp_data = []
                buff = file.readline().strip()
                while buff != "":
                    temp_buff = buff.split()
                    temp_data.append([int(temp_buff[0]), int(temp_buff[1])])
                    buff = file.readline().strip()
                    win_status = check_win(temp_data, sizex, sizey)
                    if win_status == 1:
                        user_data[suser] += 1
                        break
                    elif win_status == -1:
                        user_data[fuser] += 1
                        break
                game_data[1].append(create_game_data(date, sizex, sizey, fuser, suser, temp_data))
        except FileNotFoundError:
            print(f"第 {i+1} 局游戏数据不存在")
        pass
def main_menu():
    clear()
    print("0 - 保存并退出")
    print("1 - 更改设置")
    print("2 - 开始游戏")
    print("3 - 添加用户")
    print("4 - 比分排名")
    print("5 - 回顾棋局")

def change_setting():
    global size_x
    global size_y
    clear()
    print("输入 -h 查看帮助")
    while True:
        buff = input(">> ").split()
        match buff:
            case ["-h"]:
                print("-x - change the size of x\n-y - change the size of y\n-e - exit the change of setting")
            case ["-x"]:
                print(size_x)
            case ["-y"]:
                print(size_y)
            case ["-x", value]:
                try:
                    size_x = int(value)
                except:
                    print("更改 size_x 失败")
            case ["-y", value]:
                try:
                    size_y = int(value)
                except:
                    print("更改 size_y 失败")
            case ["-e"]:
                return

def display_chess(temp1, temp2):
    for i in range(size_x):
        for j in range(size_y):
            if [i,j] in temp1:
                print(play1_sym, end="")
            elif [i,j] in temp2:
                print(play2_sym, end="")
            else:
                print(default_sym, end="")
            print(" ", end="")
        print()

def play_chess():
    global size_x
    global size_y
    fuser = None
    suser = None
    temp1 = []
    temp2 = []
    while True:
        clear()
        for i in user_data.keys():
            print(i, end=" ")
        print()
        print("输入第一个玩家的名字")
        buff = input(">> ")
        if buff == "-e":
            return
        if buff not in user_data.keys():
            input("未找到玩家，请重新输入")
            continue
        fuser = buff
        break
    while True:
        clear()
        for i in user_data.keys():
            print(i, end=" ")
        print()
        print("输入第二个玩家的名字")
        buff = input(">> ")
        if buff == "-e":
            return
        if buff not in user_data.keys():
            input("未找到玩家，请重新输入")
            continue
        if buff == fuser:
            input("两玩家不可为同一人，请重新输入")
            continue
        suser = buff
        break
    clear()
    input("请以 x y 的形式输入坐标")
    now = datetime.datetime.now()
    iso_format_str = now.strftime("%Y-%m-%dT%H:%M:%S")
    count = 0
    temp = []
    while True:
        clear()
        display_chess(temp1, temp2)
        if len(temp)==size_x*size_y:
            input("和棋")
            game_data[1].append(create_game_data(iso_format_str, size_x, size_y, fuser, suser, temp))
            game_data[0] += 1
            return
        if count%2 == 0:
            buff = input("(Player1) ").split()
        else:
            buff = input("(Player2) ").split()
        if buff == "-e":
            return
        if len(buff) != 2:
            input("请以 x y 的形式输入坐标")
            continue
        try:
            x = int(buff[0])
            y = int(buff[1])
        except:
            input("格式错误，重新输入")
            continue
        if x>size_x or y>size_y or x<=0 or y<=0:
            input("数值过大或过小，重新输入")
            continue
        if [x,y] in temp:
            input("不可重复落子")
            continue
        temp.append([x-1,y-1])
        if count%2 == 0:
            temp1.append([x-1,y-1])
        else:
            temp2.append([x-1,y-1])
        status = check_win(temp, size_x, size_y)
        if status == 1:
            clear()
            display_chess(temp1, temp2)
            input("Player2 Win!")
            game_data[1].append(create_game_data(iso_format_str, size_x, size_y, fuser, suser, temp))
            game_data[0] += 1
            user_data[suser] += 1
            return
        if status == -1:
            clear()
            display_chess(temp1, temp2)
            input("Player1 Win!")
            game_data[1].append(create_game_data(iso_format_str, size_x, size_y, fuser, suser, temp))
            game_data[0] += 1
            user_data[fuser] += 1
            return
        count += 1
    pass

def add_user():
    while True:
        clear()
        print("输入添加用户名")
        buff = input(">> ")
        if buff in user_data.keys():
            input("不可重名")
            continue
        user_data[buff] = 0
        break
    pass

def rank_check():
    clear()
    temp = list(user_data.keys())
    for i in range(len(temp)):
        for j in range(i+1, len(temp)):
            if user_data[temp[i]]<user_data[temp[j]]:
                temp[i], temp[j] = temp[j], temp[i]
    print("Rank\t\tName")
    for i in temp:
        print(f"{user_data[i]}\t\t{i}")
    input("回车以返回...")

def review_game():
    num = 0
    while True:
        clear()
        print("Num\tDate\t\t\tStatus\tPlayer1\t\tPlayer2")
        count = 0
        for i in game_data[1]:
            print(f"{count}\t{i["date"]}\t{check_win(i["data"], i["sizex"], i["sizey"])}\t{i["first_user"]}\t\t{i["second_user"]}")
            count += 1
        print("输入需要查看回放的序号")
        buff = input(">> ")
        try:
            num = int(buff)
        except:
            input("请输入数字，请重试")
            continue
        if num < 0 or num >= len(game_data[1]):
            input("序号出错，请重试")
            continue
        if buff == "-e":
            return
        break
    count = 0
    temp1 = []
    temp2 = []
    temp = []
    while count<len(game_data[1][num]["data"]):
        clear()
        display_chess(temp1, temp2)
        if len(temp)==size_x*size_y:
            input("和棋")
            return
        if count%2 == 0:
            temp1.append(game_data[1][num]["data"][count])
        else:
            temp2.append(game_data[1][num]["data"][count])
        temp.append(game_data[1][num]["data"][count])
        status = check_win(temp, size_x, size_y)
        if status == 1:
            clear()
            display_chess(temp1, temp2)
            input("Player2 Win!")
            return
        if status == -1:
            clear()
            display_chess(temp1, temp2)
            input("Player1 Win!")
            return
        input("回车继续观看...")
        count += 1


while True:
    main_menu()
    buff = input(">> ").strip()
    try:
        buff = int(buff)
    except Exception:
        input("输入不符合规范，回车后重新输入")
        continue
    match buff:
        case 0:
            save_data()
            break
        case 1:
            change_setting()
        case 2:
            play_chess()
        case 3:
            add_user()
        case 4:
            rank_check()
        case 5:
            review_game()
        case _:
            input("无匹配功能，回车后重新输入")

    
