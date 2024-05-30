import os
import datetime
import time

def create_directory_if_not_exists(directory):
    """Creates a directory if it does not exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def create_player_directory():
    """Creates the players_list directory if it does not exist."""
    create_directory_if_not_exists("players_list")

def create_player_file(player_name, discord_name):
    """Creates a file for the new player with the specified details."""
    file_path = os.path.join("players_list", f"{player_name}.txt")
    with open(file_path, 'w') as file:
        file.write(f"Nom de clone : {player_name}\n")
        file.write(f"Pseudo Discord : {discord_name}\n")
        file.write("Nombre de session(s) : 0\n")
        file.write("Grade : Recrue (cadet)\n")
        file.write("Point(s) RP : 0\n")
        file.write("Nombre d'avertissement(s) : 0\n\n")

def read_player_file(file_path):
    """Reads player data from the specified file and returns a dictionary."""
    player_data = {
        'name': '',
        'discord': '',
        'sessions': 0,
        'grade': '',
        'rp_points': 0,
        'warnings': 0,
        'comments': ''
    }
    try:
        with open(file_path, 'r', encoding='iso-8859-1') as file:
            lines = file.readlines()
            if len(lines) > 0:
                player_data['name'] = lines[0].split(": ")[1].strip()
            if len(lines) > 1:
                player_data['discord'] = lines[1].split(": ")[1].strip()
            if len(lines) > 2:
                player_data['sessions'] = int(lines[2].split(": ")[1].strip())
            if len(lines) > 3:
                player_data['grade'] = lines[3].split(": ")[1].strip()
            if len(lines) > 4:
                player_data['rp_points'] = int(lines[4].split(": ")[1].strip())
            if len(lines) > 5:
                player_data['warnings'] = int(lines[5].split(": ")[1].strip())
            if len(lines) > 7:
                player_data['comments'] = "".join(lines[7:]).strip()
    except FileNotFoundError:
        pass
    return player_data

def write_player_file(player_name, player_data):
    """Writes player data to the specified file."""
    file_path = os.path.join("players_list", f"{player_name}.txt")
    with open(file_path, 'w') as file:
        file.write(f"Nom de clone : {player_data['name']}\n")
        file.write(f"Pseudo Discord : {player_data['discord']}\n")
        file.write(f"Nombre de session(s) : {player_data['sessions']}\n")
        file.write(f"Grade : {player_data['grade']}\n")
        file.write(f"Point(s) RP : {player_data['rp_points']}\n")
        file.write(f"Nombre d'avertissement(s) : {player_data['warnings']}\n\n")
        file.write(player_data['comments'])

def determine_grade(sessions):
    """Determines the grade based on the number of sessions."""
    if sessions >= 150:
        return 'General'
    elif sessions >= 120:
        return 'Colonel'
    elif sessions >= 110:
        return 'Lieutenant Colonel'
    elif sessions >= 100:
        return 'Commandant'
    elif sessions >= 80:
        return 'Capitaine'
    elif sessions >= 70:
        return 'Capitaine en second'
    elif sessions >= 65:
        return 'Lieutenant'
    elif sessions >= 57:
        return 'Lieutenant en second'
    elif sessions >= 50:
        return 'Major'
    elif sessions >= 45:
        return 'Major Aspirant'
    elif sessions >= 38:
        return 'Adjudant-chef'
    elif sessions >= 31:
        return 'Adjudant'
    elif sessions >= 25:
        return 'Sergent Major'
    elif sessions >= 18:
        return 'Sergent'
    elif sessions >= 11:
        return 'Caporal chef'
    elif sessions >= 6:
        return 'Caporal'
    elif sessions >= 1:
        return 'Soldat (trooper)'
    else:
        return 'Recrue (cadet)'

def increment_sessions(entries):
    """Updates the session count for the specified players based on the provided entries."""
    updated_players = []
    for entry in entries:
        entry = entry.strip()
        if entry.startswith("+") or entry.startswith("-") or entry.startswith("="):
            parts = entry[1:].strip().split(" ")
            if len(parts) < 2:
                print(f"\n\t[!] Entrée mal formée pour {entry}: Il manque le nombre de sessions.")
                continue

            name = " ".join(parts[:-1]).strip()
            try:
                value = int(parts[-1])
            except ValueError:
                print(f"\n\t[!] Valeur non valide pour les sessions : {parts[-1]}")
                continue

            file_path = os.path.join("players_list", f"{name}.txt")
            player_data = read_player_file(file_path)
            if 'sessions' not in player_data:
                print(f"\n\t[!] Erreur : Les données de session sont manquantes pour {name}.")
                continue

            if entry.startswith("+"):
                player_data['sessions'] += value
                player_data['rp_points'] += 1
                log_operation(f"Ajout de 1 point RP et de {value} session(s) à {name}")
            elif entry.startswith("-"):
                player_data['sessions'] += value
                player_data['rp_points'] -= 1
                log_operation(f"Retrait de 1 point RP et ajout de {value} session(s) à {name}")
            elif entry.startswith("="):
                player_data['sessions'] += value
                log_operation(f"Ajout de {value} session(s) à {name}")

            new_grade = determine_grade(player_data['sessions'])
            old_grade = player_data['grade']
            player_data['grade'] = new_grade

            write_player_file(name, player_data)

            if new_grade != old_grade:
                updated_players.append((name, new_grade))
                print(f"\n\t{name} passe {new_grade}. Félicitations !")
        else:
            print(f"\n\t[!] Entrée mal formée pour {entry}")
    input("\n\t| Tapez entrer quand c'est bon |")
    return updated_players

def add_player():
    """Adds a new player to the players directory."""
    name = input("\n\tEntrez le nom de clone du nouveau joueur : ").strip()
    discord_name = input("\n\tEntrez le pseudo Discord du nouveau joueur : ").strip()
    file_path = os.path.join("players_list", f"{name}.txt")
    if os.path.exists(file_path):
        print(f"\n\t[!] Le joueur {name} existe déjà.")
    else:
        create_player_file(name, discord_name)
        log_operation(f"Creation d'un nouveau joueur nomme : {name}")
        print(f"\n\t[+] Le joueur {name} a ete ajoute.")
    time.sleep(2)

def modify_player():
    """Modifies the name of an existing player."""
    old_name = input("\n\tEntrez le nom actuel du joueur : ").strip()
    old_file_path = os.path.join("players_list", f"{old_name}.txt")
    if os.path.exists(old_file_path):
        new_name = input("\n\tEntrez le nouveau nom du joueur : ").strip()
        player_data = read_player_file(old_file_path)
        player_data['name'] = new_name
        os.rename(old_file_path, os.path.join("players_list", f"{new_name}.txt"))
        write_player_file(new_name, player_data)
        print(f"\n\tLe joueur {old_name} a ete renomme en {new_name}.")
    else:
        print(f"\n\tLe joueur {old_name} n'a pas ete trouve dans les dossiers.")
    time.sleep(2)

def delete_player():
    """Deletes a player from the players directory by moving their file to deleted_players."""
    name = input("\n\tEntrez le nom du joueur à supprimer : ").strip()
    file_path = os.path.join("players_list", f"{name}.txt")
    if os.path.exists(file_path):
        verification = input(f"\n\tEs-tu sûr de vouloir supprimer le joueur {name} ? (Y/N) : ")
        if verification.upper() in ["Y", "YES", "OUI"]:
            create_directory_if_not_exists("deleted_players")
            new_file_path = os.path.join("deleted_players", f"{name}.txt")
            os.rename(file_path, new_file_path)
            log_operation(f"Suppression (déplacement) du joueur : {name}")
            print(f"\n\t[-] Le joueur {name} a été supprimé et déplacé dans deleted_players.")
        elif verification.upper() in ["N", "NO", "NON"]:
            print("\n\t[+] Commande annulée")
        else:
            print("\n\t[-] Choix invalide")
    else:
        print(f"\n\t[!] Le joueur {name} n'a pas été trouvé dans les dossiers.")
    time.sleep(2)

def log_operation(operation):
    """Logs an operation with the current timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("log.txt", 'a') as file:
        file.write(f"[{timestamp}] {operation}\n")

def show_player_list():
    """Displays the list of players and their details."""
    create_directory_if_not_exists("players_list")
    print("\n\tListe des joueurs :")
    player_files = sorted(os.listdir("players_list"))
    for player_file in player_files:
        player_data = read_player_file(os.path.join("players_list", player_file))
        print(f"\t- Nom : {player_data['name']}, Grade : {player_data['grade']}, Sessions : {player_data['sessions']}, Points RP : {player_data['rp_points']}, Avertissements : {player_data['warnings']}")

def main_menu():
    """Displays the main menu and handles user input."""
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("\n\t---- Gestion des Joueurs ----\n")
        print("\t1. Ajouter un nouveau joueur")
        print("\t2. Modifier le nom d'un joueur")
        print("\t3. Supprimer un joueur")
        print("\t4. Afficher la liste des joueurs")
        print("\t5. Mettre à jour les sessions des joueurs")
        print("\t0. Quitter")
        choice = input("\n\tVotre choix : ")

        if choice == "1":
            add_player()
        elif choice == "2":
            modify_player()
        elif choice == "3":
            delete_player()
        elif choice == "4":
            show_player_list()
            input("\n\t| Tapez entrer pour revenir au menu |")
        elif choice == "5":
            entries = input("\n\tEntrez les mises à jour des sessions (une par ligne, format +Nom Nb, -Nom Nb, =Nom Nb) :\n\t").strip().split("\n")
            updated_players = increment_sessions(entries)
            if updated_players:
                print("\n\tMises à jour des grades :")
                for name, grade in updated_players:
                    print(f"\t- {name} est maintenant {grade}.")
            input("\n\t| Tapez entrer pour revenir au menu |")
        elif choice == "0":
            break
        else:
            print("\n\tChoix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    create_player_directory()
    main_menu()
