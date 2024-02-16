import sys
import select

def input_with_timeout(timeout=1, prompt=""):
    sys.stdout.write(prompt)
    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    if ready:
        text = sys.stdin.readline().rstrip('\n')
        print(text)
        return text
    else:
        return 'None'

def main():
    # 5秒の入力待ち時間を設定
    user_input = input_with_timeout(timeout=2,prompt="Enter something: ")
    if user_input is not 'None':
        print("You entered:", user_input)
    else:
        print("\nTimeout reached, no input received.")

if __name__ == '__main__':
    main()