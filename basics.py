# print & comments
print("Hello World!")
    # print()で()の内容を表示
    # #でコメントアウト

# variables (string / numeric)
name: str = "Azure"
price: float = 3_500.0
    # 変数 = "文字列"　←　文字列の変数を定義・代入
    # 変数 = 数値　←　数値の変数を定義・代入
    # 型アノテーション 変数名の後に : 型名 を付けて明示(name: str, price: float)
    # strで文字列、floatは浮動小数点⇒小数を扱う数値型
    # 数値型で_は,と同じ意味(3_500 = 3,500)

# conditionals
if price < 5_000:
    print(f"{name} is affordable!")
    # if 以下に条件を定義　条件はし、":"で終わらせる
    # 改行してインデントして条件に合致した場合の挙動を記載
    # 合致しない場合は if を elif または else: に変えて↑と同様に記載
    # if と elif・ else: は同じ段落レベルで

# loop & collections
squares = [n**2 for n in range (1, 6)]
print("Squares", squares)
    # []を使用してsquaresという配列を定義
    # **は乗数計算　n**2 = n^2
    # for in でループ
    # print( , )で複数の表示が可能

# functions
def factorial(n: int) -> int:
    res = 1
    for i in range(2, n + 1):
       res *= i
    return res
print("S! =", factorial(5))

    # def：関数を定義
    # factorial：関数名
    # (n: int)：引数 n は整数（int）であることの型ヒント
    # -> int：この関数の戻り値が整数であることを明示（Python 3.5+）
    # : 関数の本体がこれから始まることを示す記号
    # return res は計算結果を関数の外へ返す
    # res *= i は res = res * iと同じ
    # return resで計算結果のresを返す

# error handring
try:
   1 / 0
except ZeroDivisionError as e:
    print("ZeroDivisionError:", e)
    # try:「この中でエラーが出るかもしれない」処理を書く場所
    # except ZeroDivisionError as e: try の中で ZeroDivisionError が発生した場合だけ、このブロックが実行
    # as e と書くことで、発生したエラーの情報を e に入れて、あとで使える
    # print("ZeroDivisionError:", e)で実際に起こったエラーの内容を出力