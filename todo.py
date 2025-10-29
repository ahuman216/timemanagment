import os
print('six seven')
TODO_FILE = "todo_list.txt"

def load_tasks():
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, "r") as f:
        return [line.strip() for line in f.readlines()]

def save_tasks(tasks):
    with open(TODO_FILE, "w") as f:
        for task in tasks:
            f.write(task + "\n")

def show_tasks(tasks):
    if not tasks:
        print("\nno tasks yet!")
    else:
        print("\nyour to-do list:")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")

def main():
    tasks = load_tasks()
    while True:
        print("\n=== your to-do list menu! ===")
        print("1. show tasks")
        print("2. add a task")
        print("3. remove a task")
        print("4. clear all tasks")
        print("5. exit")

        choice = input("\nchoose an option (1-5): ").strip()

        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            task = input("enter the task you want to add! ").strip()
            if task:
                tasks.append(task)
                save_tasks(tasks)
                print(f"added: {task}")
        elif choice == "3":
            show_tasks(tasks)
            if tasks:
                try:
                    num = int(input("enter the task number you want to remove! "))
                    removed = tasks.pop(num - 1)
                    save_tasks(tasks)
                    print(f"removed: {removed}")
                except (ValueError, IndexError):
                    print("invalid number, put the right thing in pls")
        elif choice == "4":
            confirm = input("are you sure you want to delete all your tasks? (y/n): ").lower()
            if confirm == "y":
                tasks.clear()
                save_tasks(tasks)
                print("cleared all tasks.")
        elif choice == "5":
            print("bye! i hope you had fun studying!")
            break
        else:
            print("invalid choice, pls try again.")

if __name__ == "__main__":
    main()

