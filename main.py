import os
import datetime
import time

def create_player_directory():
    """Creates the players_list directory if it does not exist."""
    if not os.path.exists("players_list"):
        os.makedirs("players_list")

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
    if sessions >= 125:
        return 'General'
    elif sessions >= 110:
        return 'Commandant marechal'
    elif sessions >= 95:
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
                print(f"\n\t[!] Entrée mal formee pour {entry}: Il manque le nombre de sessions.")
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
                print(f"\n\t[!] Erreur : Les donnees de session sont manquantes pour {name}.")
                continue

            if entry.startswith("+"):
                player_data['sessions'] += value
                player_data['rp_points'] += 1
                log_operation(f"Ajout de 1 point RP et de {value} session(s) a {name}")
            elif entry.startswith("-"):
                player_data['sessions'] += value
                player_data['rp_points'] -= 1
                log_operation(f"Retrait de 1 point RP et ajout de {value} session(s) a {name}")
            elif entry.startswith("="):
                player_data['sessions'] += value
                log_operation(f"Ajout de {value} session(s) a {name}")

            new_grade = determine_grade(player_data['sessions'])
            old_grade = player_data['grade']
            player_data['grade'] = new_grade

            write_player_file(name, player_data)

            if new_grade != old_grade:
                updated_players.append((name, new_grade))
        else:
            print(f"\n\t[!] Entree mal formee pour {entry}")
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
    """Deletes a player from the players directory."""
    name = input("\n\tEntrez le nom du joueur a supprimer : ").strip()
    file_path = os.path.join("players_list", f"{name}.txt")
    if os.path.exists(file_path):
        verification = input(f"\n\tEs-tu sur de vouloir supprimer le joueur {name} ? (Y/N) : ")
        if verification.upper() in ["Y", "YES", "OUI"]:
            os.remove(file_path)
            log_operation(f"Suppression du joueur : {name}")
            print(f"\n\t[-] Le joueur {name} a ete supprime.")
        elif verification.upper() in ["N", "NO", "NON"]:
            print("\n\t[+] Commande annulee")
        else:
            print("\n\t[-] Choix invalide")
    else:
        print(f"\n\t[!] Le joueur {name} n'a pas ete trouve dans les dossiers.")
    time.sleep(2)

def add_staff_comment():
    """Adds a staff comment to a player's file."""
    name = input("\n\tEntrez le nom du joueur : ").strip()
    staff = input("\n\tEntrez le nom du staff : ").strip()
    comment = input("\n\tEntrez le commentaire : ").strip()
    file_path = os.path.join("players_list", f"{name}.txt")
    if os.path.exists(file_path):
        player_data = read_player_file(file_path)
        player_data['comments'] += f"\n\nCommentaire du staff {staff} : {comment}"
        write_player_file(name, player_data)
        print(f"\n\t[+] Le commentaire a ete ajoute pour {name}.")
    else:
        print(f"\n\t[!] Le joueur {name} n'a pas ete trouve dans les dossiers.")
    time.sleep(2)

def add_warning():
    """Adds a warning to a player's file."""
    name = input("\n\tEntrez le nom du joueur : ").strip()
    reason = input("\n\tEntrez la raison de l'avertissement : ").strip()
    file_path = os.path.join("players_list", f"{name}.txt")
    if os.path.exists(file_path):
        player_data = read_player_file(file_path)
        player_data['warnings'] += 1
        player_data['comments'] += f"\n\nAvertissement {player_data['warnings']} : {reason}"
        write_player_file(name, player_data)
        print(f"\n\t[+] L'avertissement a ete ajoute pour {name}.")
    else:
        print(f"\n\t[!] Le joueur {name} n'a pas ete trouve dans les dossiers.")
    time.sleep(2)

def display_player_info():
    """Displays information about a specific player."""
    name = input("\n\tEntrez le nom du joueur : ").strip()
    file_path = os.path.join("players_list", f"{name}.txt")
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='iso-8859-1') as file:
            print(f"\n\t--- Informations pour {name} ---\n")
            print("\n" + file.read() + "\n")
    else:
        print(f"\n\t[!] Le joueur {name} n'a pas ete trouve dans les dossiers.")
    input("\n\t| Tapez entrer quand c'est bon |")

def display_all_staff_comments():
    """Displays all staff comments for all players."""
    print("\n\t--- Tous les commentaires du staff ---\n\n")
    for file_name in os.listdir("players_list"):
        file_path = os.path.join("players_list", file_name)
        player_data = read_player_file(file_path)
        if player_data['comments']:
            staff_comments = [comment for comment in player_data['comments'].split('\n') if comment.startswith("Commentaire du staff")]
            if staff_comments:
                print(f"\n\t--- Commentaires pour {player_data['name']} ---")
                print("\n".join(staff_comments) + "\n")
    input("\n\t| Tapez entrer quand c'est bon |")

def display_all_warnings():
    """Displays all warnings for all players."""
    print("\n\t--- Toutes les raisons d'avertissements ---\n")
    for file_name in os.listdir("players_list"):
        file_path = os.path.join("players_list", file_name)
        player_data = read_player_file(file_path)
        if player_data['warnings'] > 0:
            print(f"\n\t--- Avertissements pour {player_data['name']} ---")
            print(f"\n\tNombre d'avertissements : {player_data['warnings']}")
            warnings = [comment for comment in player_data['comments'].split('\n') if comment.startswith("Avertissement")]
            if warnings:
                print("\n".join(warnings) + "\n")
    input("\n\t| Tapez entrer quand c'est bon |")

def log_operation(operation):
    """Logs operations performed on the players."""
    with open("operations_log.txt", "a") as log_file:
        log_file.write(f"{datetime.datetime.now()}: {operation}\n")

def git_push():
    """Adds specified files, commits with a message, and force pushes to the main branch."""
    os.system("git add main.py operations_log.txt players_list")
    os.system('git commit -m "modification apportees"')
    os.system("git push --force origin main")
    print("\n\t[+] Les modifications ont ete poussees au depot distant.")

def git_pull():
    """Pulls the latest code from the main branch of the repository."""
    os.system("git pull origin main")
    print("\n\t[+] Le code a ete mis a jour depuis le depot distant.")

def main():
    git_pull()
    os.system("clear")
    create_player_directory()
    main = True
    
    while main:
        print("\n\n\n\n\tMenu :\n\n")
        print("\t1. Incrémenter les sessions des joueurs et mettre à jour les points RP\n")
        print("\t2. Ajouter un nouveau joueur\n")
        print("\t3. Modifier le nom d'un joueur\n")
        print("\t4. Supprimer un joueur\n")
        print("\t5. Ajouter un commentaire du staff\n")
        print("\t6. Ajouter un avertissement\n")
        print("\t7. Afficher les informations d'un joueur\n")
        print("\t8. Afficher tous les commentaires du staff\n")
        print("\t9. Afficher toutes les raisons d'avertissements\n")
        print("\t10. Quitter en sauvegardant\n")
        print("\t11. Quitter sans sauvegarder\n")

        choice = input("\tEntrez votre choix : ").strip()

        if choice == '1':
            entries = input("\n\tEntrez les noms des joueurs avec + ou - pour les points RP (séparés par des virgules) : ").split(",")
            updated_players = increment_sessions(entries)
            for name, new_grade in updated_players:
                print(f"\n\t{name} a maintenant été promu à {new_grade}.")
            print("\n\t[+] Les sessions ont été mise à jour")
            print("\n")
            os.system("clear")

        elif choice == '2':
            add_player()
            print("\n")
            os.system("clear")

        elif choice == '3':
            modify_player()
            print("\n")
            os.system("clear")

        elif choice == '4':
            delete_player()
            print("\n")
            os.system("clear")

        elif choice == '5':
            add_staff_comment()
            print("\n")
            os.system("clear")

        elif choice == '6':
            add_warning()
            print("\n")
            os.system("clear")

        elif choice == '7':
            display_player_info()
            os.system("clear")

        elif choice == '8':
            display_all_staff_comments()
            os.system("clear")

        elif choice == '9':
            display_all_warnings()
            os.system("clear")

        elif choice == '10':
            git_push()
            break

        elif choice == '11':
            while True:
                sure = input("\n\tEs-tu sur de vouloir quitter sans sauvegarder ? (Y/N) : ")
                if sure.upper() in ['YES', 'OUI', 'Y', 'O']:
                    main = False
                    break
                elif sure.upper() in ['NO', 'NON', 'N']:
                    break
                else:
                    print("\n\t[!] Choix invalide. Veuillez réessayer.")

        else:
            print("\n\t[!] Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()
