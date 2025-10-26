import os
import psutil
import time

# Lagrar om övervakning är aktiv
monitoring_active = False
# Lagrar larmnivåer
alarms = {
    "cpu": [6],
    "memory": [6],
    "disk": []
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    while True:
        clear_screen()
        print("===== HUVUDMENY =====")
        print("1. Starta övervakning")
        print("2. Lista aktiv övervakning")
        print("3. Skapa larm")
        print("4. Visa larm")
        print("5. Starta övervakningsläge")
        print("6. Avsluta")
        choice = input("Välj ett alternativ: ")
        
        if choice == "1":
            start_monitoring()
        elif choice == "2":
            list_monitoring()
        elif choice == "3":
            create_alarm_menu()
        elif choice == "4":
            show_alarms()
        elif choice == "5":
            monitoring_mode()
        elif choice == "6":
            break
        else:
            print("Ogiltigt val!")
            input("Tryck enter för att fortsätta...")

def start_monitoring():
    global monitoring_active
    monitoring_active = True
    print("Övervakning startad!")
    input("Tryck enter för att gå tillbaka till huvudmenyn...")

def list_monitoring():
    clear_screen()
    if not monitoring_active:
        print("Ingen övervakning är aktiv.")
    else:
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        print(f"CPU Användning: {cpu}%")
        print(f"Minnesanvändning: {memory.percent}% ({round(memory.used / (1024**3), 1)} GB av {round(memory.total / (1024**3), 1)} GB)")
        print(f"Diskanvändning: {disk.percent}% ({round(disk.used / (1024**3), 1)} GB av {round(disk.total / (1024**3), 1)} GB)")
    input("Tryck enter för att gå tillbaka till huvudmenyn...")

def create_alarm_menu():
    while True:
        clear_screen()
        print("=== SKAPA LARM ===")
        print("1. CPU användning")
        print("2. Minnesanvändning")
        print("3. Diskanvändning")
        print("4. Tillbaka till huvudmeny")
        choice = input("Välj ett alternativ: ")

        if choice == "1":
            set_alarm("cpu")
        elif choice == "2":
            set_alarm("memory")
        elif choice == "3":
            set_alarm("disk")
        elif choice == "4":
            break
        else:
            print("Ogiltigt val!")
            input("Tryck enter för att fortsätta...")

def set_alarm(alarm_type):
    while True:
        try:
            level = int(input("Ställ in nivå för alarm mellan 1-100: "))
            if 1 <= level <= 100:
                alarms[alarm_type].append(level)
                print(f"Larm för {alarm_type.upper()} satt till {level}%")
                input("Tryck enter för att fortsätta...")
                return
            print("Värdet måste vara mellan 1 och 100!")
        except ValueError:
            print("Ange ett numeriskt värde!")

def show_alarms():
    clear_screen()
    print("=== KONFIGURERADE LARM ===")
    for key in ["cpu", "disk", "memory"]:
        print(f"\n{key.upper()} larm:")
        for value in sorted(alarms[key]):
            print(f"- {value}%")
    input("Tryck enter för att gå tillbaka till huvudmenyn...")

def monitoring_mode():
    if not monitoring_active:
        print("Övervakning är inte aktiv. Starta den först.")
        input("Tryck enter för att återgå.")
        return

    print("Övervakningsläge startat. Tryck Ctrl+C för att återgå till menyn.")
    try:
        while True:
            clear_screen()
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            
            print(f"=== REALTIDSÖVERVAKNING ===")
            print(f"CPU användning: {cpu}%")
            print(f"Minnesanvändning: {memory}%")
            print(f"Diskanvändning: {disk}%")
            print("\nLarmstatus:")
            
            if any(cpu >= level for level in alarms["cpu"]):
                print(f"⚠️  CPU VARNING: {cpu}% överstiger gräns!")
            if any(memory >= level for level in alarms["memory"]):
                print(f"⚠️  MINNE VARNING: {memory}% överstiger gräns!")
            if any(disk >= level for level in alarms["disk"]):
                print(f"⚠️  DISK VARNING: {disk}% överstiger gräns!")
            
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nÅtergår till huvudmeny...")

if __name__ == "__main__":
    main_menu()