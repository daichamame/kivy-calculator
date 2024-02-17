#--------------------------------------------------------------------------------------------------
# タイトル：電卓
# 内容：
#    単純な計算ができる
#    丸め処理や上限の制御はしていない
#    小数点第5位までしか表示していない
#    Kivyを勉強するために作成したもの
# 作成者：だいちゃまめ
#--------------------------------------------------------------------------------------------------
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
import sys
import math
# ウィンドウサイズの指定
Window.size=(320,480)
#--------------------------------------------------------------------------------------------------
# シャットダウンコマンド
#--------------------------------------------------------------------------------------------------
class PopupExitDialog(Popup):
    pass
    # プログラム終了
    def exec_exit(self):
       sys.exit()
#--------------------------------------------------------------------------------------------------
# メインウィジット
#--------------------------------------------------------------------------------------------------
class MameWidget(Widget):
    str_numbuf_tmp="0"       # 文字列型の数値の一時保存用変数
    str_numbuf="0"           # 表示用数値の文字列
    f_percent=0              # ％表記か否か
    f_calc = ""              # 演算
    # 初期処理
    def __init__(self, **kwargs):
        super(MameWidget, self).__init__(**kwargs)
    # 電卓描画
    def update_display(self):
        if(self.str_numbuf != ""):
            buf=float(self.str_numbuf)  # 文字列を数字に変換
            if(buf.is_integer()):       # 整数であれば、小数点以下をつけない
                buf=int(buf)
            else:
                buf=round(buf,5)
        else:
            buf=0
        if self.f_percent == 1: # % の表記ならば、%をつける
            self.ids.lbl_display.text = str(buf) + "%"
        else:
            self.ids.lbl_display.text = str(buf)
    # 消去(ACボタン)
    def all_clear(self):
        self.str_numbuf_tmp = "0"
        self.str_numbuf = "0"
        self.f_percent = 0
        self.f_calc = ""
        self.update_display()
    # 変換（＋ー、％、√）
    def convert(self,cmd):
        num = float(self.str_numbuf)  # 数値に変換
        if cmd == 'plusminus':
            self.str_numbuf = str(-num) # 符号変換
        elif cmd == 'percent':
            self.str_numbuf = str((num * 100)*(self.f_percent == 0) + (num / 100)*(self.f_percent == 1))
            self.f_percent = (self.f_percent == 0)
        elif cmd == 'root':
            self.str_numbuf = str(math.sqrt(num))   # 平方根を計算
            self.f_calc = 'equal'
        self.update_display()
    # 数字キー
    def push_num(self,cmd):
        if cmd >= 0 and cmd <= 9 and self.f_calc != 'equal':
            self.str_numbuf = self.str_numbuf + str(cmd)
        self.update_display()
    # 小数点
    def push_period(self):
        if self.str_numbuf.find('.') == -1: # ピリオドは一度しか押せないための判定
            self.str_numbuf = self.str_numbuf + "."
    # 演算（四則演算）
    def push_calc(self,cmd):
        if self.str_numbuf != '0':  # 値が0(数値未入力の場合)は処理しない(2度押し)
            if self.f_calc != "":   # すでに演算ボタンが押されている場合、一度計算する
                self.push_equal()
            self.str_numbuf_tmp = self.str_numbuf
            self.f_calc = cmd   
            self.str_numbuf = "0"
    # 計算（＝もしくは四則演算ボタン）
    def push_equal(self):
        if float(self.str_numbuf) != 0: # 値が0(数値未入力の場合)は処理しない
            if self.f_calc == 'division':
                buf = float(self.str_numbuf_tmp) / float(self.str_numbuf)
            elif self.f_calc == 'multiply':
                buf = float(self.str_numbuf_tmp) * float(self.str_numbuf)
            elif self.f_calc == 'minus':
                buf = float(self.str_numbuf_tmp) - float(self.str_numbuf)
            elif self.f_calc == 'plus':
                buf = float(self.str_numbuf_tmp) + float(self.str_numbuf)
            else:
                return
            self.str_numbuf = str(buf)
            self.f_calc = 'equal'
            self.f_percent = 0
            self.update_display()
    # 終了ダイアログ
    def exit_dialog(self):
        popup = PopupExitDialog()
        popup.open()
# アプリの定義
class MamecalculatorApp(App):  
    def __init__(self, **kwargs):
        super(MamecalculatorApp,self).__init__(**kwargs)
        self.title="Mame App"                          # ウィンドウタイトル名
# メインの定義
if __name__ == '__main__':
    MamecalculatorApp().run()                          # クラスを指定

Builder.load_file('mamecalculator.kv')                 # kvファイル名

