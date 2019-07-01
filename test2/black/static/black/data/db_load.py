# # 独立使用django的model
# import sys
# import os

# pwd = os.path.dirname(os.path.realpath(__file__))
# sys.path.append(pwd+"../")
# # 找到根目录（与工程名一样的文件夹）下的settings
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VueShop.settings')

# import django
# django.setup()

# # 引入的位置必须在这里，不可提前
# from black.models import Player_info
# from black.static.black.data import json_test
# def load():
#     raw_data = json_test.load_json()
#     for name in raw_data:
#         for time in raw_data[name]:
#             game = Game_info()
#             game.name = name
#             game.game_time = time
#             game.score = raw_data[name][time]['得分']
#             game.save()
#             print(game.name,"saved")
