import gc

# メモリ使用率を表示する関数
def free(prt=False):
    # ガベージコレクションを実行してメモリを解放する
    gc.collect()
    if prt:
        print("Free memory:", gc.mem_free())