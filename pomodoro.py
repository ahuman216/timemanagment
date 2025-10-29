import time

def pomodoro_timer(work_minutes=25, short_break=5, long_break=15, cycles=4):
    for i in range(1, cycles + 1):
        print(f"\npomodoro {i} - work for {work_minutes} minutes!")
        countdown(work_minutes * 60)
        print("\nbreak time!")

        if i < cycles:
            countdown(short_break * 60)
        else:
            print("\n cycles complete! time for a long break!")
            countdown(long_break * 60)
    
    print("\n Study session finished!")

def countdown(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = f"{mins:02d}:{secs:02d}"
        print(f"\r{timer}", end="")
        time.sleep(1)
        seconds -= 1

if __name__ == "__main__":
    print("=== pomodoro timer! ===")
    try:

        work = int(input("enter work duration (minutes, default 25): "))
    except:
        work = 25
        print("invalid input, defaulting to 25 min")
    try: 
        short = int(input("enter short break (minutes, default 5): "))
    except: 
        short = 5
        print("invalid input, defaulting to 5 min")
    try:
        long = int(input("enter long break (minutes, default 15): "))
    except:
        long = 15
        print("invalid input, defaulting to 25 min")
    try:
        cycles = int(input("enter number of pomodoros (default 4): "))
    except:
        cycles = 4
        print("invalid input, defaulting to 4 rounds")
        

    pomodoro_timer(work, short, long, cycles)
