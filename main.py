import os
import datetime
import time

def create_player_directory():
    """Creates the players_list directory if it does not exist."""
    if not os.path.exists("players_list"):
        os.makedirs("players_list")

def create_reserve_directory():
    """Creates the reserve_players_list directory if it does not exist."""
    if not os.path.exists("reserve_players_list"):
        os.makedirs("reserve_players_list")


def create_blacklist_directory():
    """Creates the blacklist_players_list directory if it does not exist."""
    if not os.path.exists("blacklist_players_list"):
        os.makedirs("blacklist_players_list")

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

def write_blacklist_file(player_name, player_data):
    """Writes player data to the blacklist file."""
    file_path = os.path.join("blacklist_players_list", f"{player_name}.txt")
    with open(file_path, 'w') as file:
        file.write(f"--------------- Black List ---------------\n")
        file.write(f"Nom de clone : {player_name}\n")
        file.write(f"Pseudo Discord : {player_data['discord']}\n")
        file.write(f"Nombre de session(s) : {player_data['sessions']}\n")
        file.write(f"Grade : {player_data['grade']}\n")
        file.write(f"Point(s) RP : {player_data['rp_points']}\n")
        file.write(f"Nombre d'avertissement(s) : {player_data['warnings']}\n\n")

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
                print(f"\n\t{name} passe {new_grade}. Félicitations !")
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
    """Deletes a player from the players directory or reserve directory."""
    while True:
        print("\n\n\n\n\tMenu de suppression :\n\n")
        print("\n\t1. Supprimer un joueur de la liste principale\n")
        print("\n\t2. Supprimer un joueur de la réserve\n")
        print("\n\t3. Supprimer tous les joueurs de la réserve\n")
        print("\n\t4. Quitter\n")

        choice = input("\n\tEntrez votre choix : ").strip()

        if choice == '1':
            print("\n")
            delete_main_player()
            print("\n")
            os.system("clear")
        elif choice == '2':
            print("\n")
            delete_reserve_player()
            print("\n")
            os.system("clear")
        elif choice == '3':
            print("\n")
            delete_all_reserve_players()
            print("\n")
            os.system("clear")
        elif choice == '4':
            print("\n\t[+] Sortie du menu de suppression")
            break
        else:
            print("\n\t[!] Choix invalide. Veuillez réessayer.")
            
def delete_main_player():
    """Deletes a player from the main players directory."""
    while True:
        print("\n\t1. Supprimer par nom de clone\n")
        print("\n\t2. Supprimer par pseudo Discord\n")
        choice = input("\n\n\tEntrez votre choix : ").strip()

        if choice == '1':
            name = input("\n\tEntrez le nom du joueur à supprimer : ").strip()
            file_path_main = os.path.join("players_list", f"{name}.txt")

            if os.path.exists(file_path_main):
                verification = input(f"\n\tEs-tu sûr de vouloir supprimer le joueur {name} ? (Y/N) : ")
                if verification.upper() in ["Y", "YES", "OUI"]:
                    os.remove(file_path_main)
                    log_operation(f"Suppression du joueur : {name} de players_list")
                    print(f"\n\t[-] Le joueur {name} a été supprimé de players_list.")
                elif verification.upper() in ["N", "NO", "NON"]:
                    print("\n\t[+] Commande annulée")
                else:
                    print("\n\t[-] Choix invalide")
            else:
                print(f"\n\t[!] Le joueur {name} n'a pas été trouvé dans les dossiers.")
            break

        elif choice == '2':
            discord_name = input("\n\tEntrez le pseudo Discord du joueur à supprimer : ").strip()
            found = False

            for file_name in os.listdir("players_list"):
                file_path = os.path.join("players_list", file_name)
                player_data = read_player_file(file_path)
                if player_data['discord'] == discord_name:
                    name = player_data['name']
                    verification = input(f"\n\tEs-tu sûr de vouloir supprimer le joueur {name} ? (Y/N) : ")
                    if verification.upper() in ["Y", "YES", "OUI"]:
                        os.remove(file_path)
                        log_operation(f"Suppression du joueur : {name} de players_list")
                        print(f"\n\t[-] Le joueur {name} a été supprimé de players_list.")
                    elif verification.upper() in ["N", "NO", "NON"]:
                        print("\n\t[+] Commande annulée")
                    else:
                        print("\n\t[-] Choix invalide")
                    found = True
                    break

            if not found:
                print(f"\n\t[!] Aucun joueur trouvé avec le pseudo Discord {discord_name}.")
            break

        else:
            print("\n\t[!] Choix invalide. Veuillez réessayer.")
    time.sleep(2)

def delete_reserve_player():
    """Deletes a player from the reserve_players_list directory."""
    while True:
        print("\n\t1. Supprimer par nom de clone\n")
        print("\n\t2. Supprimer par pseudo Discord\n")
        choice = input("\n\n\tEntrez votre choix : ").strip()

        if choice == '1':
            name = input("\n\tEntrez le nom du joueur de la réserve à supprimer : ").strip()
            file_path_reserve = os.path.join("reserve_players_list", f"{name}.txt")

            if os.path.exists(file_path_reserve):
                verification = input(f"\n\tEs-tu sûr de vouloir supprimer le joueur {name} de la réserve ? (Y/N) : ")
                if verification.upper() in ["Y", "YES", "OUI"]:
                    os.remove(file_path_reserve)
                    log_operation(f"Suppression du joueur : {name} de reserve_players_list")
                    print(f"\n\t[-] Le joueur {name} a été supprimé de reserve_players_list.")
                elif verification.upper() in ["N", "NO", "NON"]:
                    print("\n\t[+] Commande annulée")
                else:
                    print("\n\t[-] Choix invalide")
            else:
                print(f"\n\t[!] Le joueur {name} n'a pas été trouvé dans la réserve.")
            break

        elif choice == '2':
            discord_name = input("\n\tEntrez le pseudo Discord du joueur de la réserve à supprimer : ").strip()
            found = False

            for file_name in os.listdir("reserve_players_list"):
                file_path = os.path.join("reserve_players_list", file_name)
                player_data = read_player_file(file_path)
                if player_data['discord'] == discord_name:
                    name = player_data['name']
                    verification = input(f"\n\tEs-tu sûr de vouloir supprimer le joueur {name} de la réserve ? (Y/N) : ")
                    if verification.upper() in ["Y", "YES", "OUI"]:
                        os.remove(file_path)
                        log_operation(f"Suppression du joueur : {name} de reserve_players_list")
                        print(f"\n\t[-] Le joueur {name} a été supprimé de reserve_players_list.")
                    elif verification.upper() in ["N", "NO", "NON"]:
                        print("\n\t[+] Commande annulée")
                    else:
                        print("\n\t[-] Choix invalide")
                    found = True
                    break

            if not found:
                print(f"\n\t[!] Aucun joueur trouvé avec le pseudo Discord {discord_name}.")
            break

        else:
            print("\n\t[!] Choix invalide. Veuillez réessayer.")
    time.sleep(2)

def delete_all_reserve_players():
    """Deletes all players from the reserve_players_list directory."""
    verification = input("\n\tEs-tu sûr de vouloir supprimer tous les joueurs de la réserve ? (Y/N) : ")
    if verification.upper() in ["Y", "YES", "OUI"]:
        folder_path = "reserve_players_list"
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("\n\t[-] Tous les joueurs de la réserve ont été supprimés.")
    elif verification.upper() in ["N", "NO", "NON"]:
        print("\n\t[+] Commande annulée")
    else:
        print("\n\t[-] Choix invalide")
    time.sleep(2)

def move_player_to_reserve():
    """Moves a player file to the reserve_players_list directory."""
    name = input("\n\tEntrez le nom du joueur à déplacer en réserve : ").strip()
    file_path = os.path.join("players_list", f"{name}.txt")
    if os.path.exists(file_path):
        verification = input(f"\n\tEs-tu sûr de vouloir déplacer le joueur {name} en réserve ? (Y/N) : ")
        if verification.upper() in ["Y", "YES", "OUI"]:
            reserve_path = os.path.join("reserve_players_list", f"{name}.txt")
            os.rename(file_path, reserve_path)
            log_operation(f"Déplacement du joueur {name} vers la réserve")
            print(f"\n\t[+] Le joueur {name} a été déplacé en réserve.")
        elif verification.upper() in ["N", "NO", "NON"]:
            print("\n\t[+] Commande annulée")
        else:
            print("\n\t[-] Choix invalide")
    else:
        print(f"\n\t[!] Le joueur {name} n'a pas été trouvé dans les dossiers.")
    time.sleep(2)

def restore_player_from_reserve():
    """Restores a player from the reserve_players_list directory to the players_list directory."""
    name = input("\n\tEntrez le nom du joueur à restaurer de la réserve : ").strip()
    reserve_path = os.path.join("reserve_players_list", f"{name}.txt")
    
    if os.path.exists(reserve_path):
        file_path = os.path.join("players_list", f"{name}.txt")
        os.rename(reserve_path, file_path)
        log_operation(f"Restauration du joueur {name} de la réserve")
        print(f"\n\t[+] Le joueur {name} a été restauré de la réserve.")
    else:
        print(f"\n\t[!] Le joueur {name} n'a pas été trouvé dans la réserve.")
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
    """Add a warning to a player."""
    player_name = input("\n\tEntrez le nom du joueur : ").strip()
    file_path = os.path.join("players_list", f"{player_name}.txt")

    if not os.path.exists(file_path):
        print("\n\t[!] Le joueur n'existe pas.")
        return

    # Choisir le type d'avertissement
    print("\n\tChoisissez le type d'avertissement :\n")
    print("\n\t1. Non présent à une session")
    print("\n\t2. Insulte (préciser l'insulte et envers qui)")
    print("\n\t3. Autre")
    warning_type_choice = input("\n\tVotre choix : ").strip()

    if warning_type_choice == '1':
        warning_type = "Non présent à une session"
        warning_details = "A coché présent à une session mais n'est pas venu"
    elif warning_type_choice == '2':
        insult = input("\n\tPrécisez l'insulte : ").strip()
        target = input("\n\tEnvers qui : ").strip()
        warning_type = "Insulte"
        warning_details = f"{insult} envers {target}"
    elif warning_type_choice == '3':
        warning_type = input("\n\tPrécisez le type d'avertissement : ").strip()
        warning_details = input("\n\tDétails : ").strip()
    else:
        print("\n\t[!] Choix invalide.")
        return

    current_time = datetime.datetime.now().strftime("%d-%m-%y | %H:%M:%S")
    new_warning = f"({current_time}) Avertissement {warning_type} : {warning_details}"

    player_data = read_player_file(file_path)
    player_data['warnings'] += 1
    player_data['comments'] += f"\n\n{new_warning}"

    write_player_file(player_data['name'], player_data)
    log_operation(f"Ajout d'un avertissement pour le joueur {player_data['name']}: {warning_type} - {warning_details}")
    print(f"\n\t[+] Avertissement ajouté pour {player_data['name']}.")
    input("\n\t| Tapez entrer quand c'est bon |")

def display_player_info():
    """Displays information about a specific player using either clone name or Discord name."""
    search_option = input("\n\tVoulez-vous rechercher par nom de clone (1) ou par pseudo Discord (2) ? ").strip()

    if search_option == '1':
        name = input("\n\tEntrez le nom du joueur : ").strip()
        file_path = os.path.join("players_list", f"{name}.txt")
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                print(f"\n\t--- Informations pour {name} ---\n")
                print(file.read())
        else:
            print(f"\n\t[!] Le joueur {name} n'a pas été trouvé dans les dossiers.")

    elif search_option == '2':
        discord_name = input("\n\tEntrez le pseudo Discord du joueur : ").strip()
        found = False

        for file_name in os.listdir("players_list"):
            file_path = os.path.join("players_list", file_name)
            player_data = read_player_file(file_path)
            if player_data['discord'] == discord_name:
                with open(file_path, 'r') as file:
                    print(f"\n\t--- Informations pour {player_data['name']} ---\n")
                    print(file.read())
                found = True
                break

        if not found:
            print(f"\n\t[!] Aucun joueur trouvé avec le pseudo Discord {discord_name}.")

    else:
        print("\n\t[!] Choix invalide. Veuillez réessayer.")

    input("\n\t| Tapez entrer quand c'est bon |")

def display_all_staff_comments():
    """Displays all staff comments for all players."""
    print("\n\t--- Tous les commentaires du staff ---\n")
    for file_name in os.listdir("players_list"):
        file_path = os.path.join("players_list", file_name)
        player_data = read_player_file(file_path)
        if player_data['comments']:
            print(f"\n\t--- Commentaires pour {player_data['name']} ---")
            print(player_data['comments'])
    input("\n\t| Tapez entrer quand c'est bon |")

def display_all_warnings():
    """Displays all warnings for all players."""
    print("\n\t--- Toutes les raisons d'avertissements ---\n")
    for file_name in os.listdir("players_list"):
        file_path = os.path.join("players_list", file_name)
        player_data = read_player_file(file_path)
        if player_data['warnings'] > 0:
            print(f"\n\t--- Avertissements pour {player_data['name']} ---")
            print(f"\tNombre d'avertissements : {player_data['warnings']}")
            comments = player_data['comments'].split('\n')
            for comment in comments:
                if "Avertissement" in comment:
                    print(comment)
    input("\n\t| Tapez entrer quand c'est bon |")

def remove_old_warnings():
    """Removes warnings that are older than one month."""
    current_date = datetime.datetime.now()
    updated_players = []

    for file_name in os.listdir("players_list"):
        file_path = os.path.join("players_list", file_name)
        player_data = read_player_file(file_path)
        comments = player_data['comments'].split('\n\n')
        new_comments = []
        warnings_to_remove = 0

        # Filtrer les avertissements trop anciens
        for comment in comments:
            if "Avertissement" in comment:
                try:
                    date_str = comment.split(') ')[0].strip('(')
                    warning_date = datetime.datetime.strptime(date_str, "%d-%m-%y | %H:%M:%S")
                    if (current_date - warning_date).days <= 30:
                        new_comments.append(comment)
                    else:
                        warnings_to_remove += 1
                except ValueError:
                    new_comments.append(comment)
            else:
                new_comments.append(comment)

        # Réindexer les avertissements restants
        reindexed_comments = []
        warning_count = 1
        for comment in new_comments:
            if "Avertissement" in comment:
                parts = comment.split(' ', 2)
                reindexed_comment = f"{parts[0]} Avertissement {warning_count} : {parts[2]}"
                reindexed_comments.append(reindexed_comment)
                warning_count += 1
            else:
                reindexed_comments.append(comment)

        if warnings_to_remove > 0:
            player_data['warnings'] -= warnings_to_remove
            player_data['comments'] = '\n\n'.join(reindexed_comments)
            write_player_file(player_data['name'], player_data)
            updated_players.append(player_data['name'])
            log_operation(f"Retrait de {warnings_to_remove} avertissement(s) pour le joueur {player_data['name']}")

    if updated_players:
        print(f"\n\t[+] Les avertissements de plus d'un mois ont été retirés pour les joueurs suivants : {', '.join(updated_players)}")
    else:
        print("\n\t[+] Aucun avertissement à retirer.")
    input("\n\t| Tapez entrer quand c'est bon |")

def move_player_to_blacklist():
    """Adds a player to the blacklist."""
    name = input("\n\tEntrez le nom de clone du joueur à mettre dans la black list : ").strip()
    file_path = os.path.join("players_list", f"{name}.txt")
    if os.path.exists(file_path):
        verification = input(f"\n\tEs-tu sûr de vouloir mettre le joueur {name} dans la black list ? (Y/N) : ")
        if verification.upper() in ["Y", "YES", "OUI"]:
            player_data = read_player_file(file_path)
            write_blacklist_file(name, player_data)
            os.remove(file_path)
            log_operation(f"Mise du joueur {name} dans la black list")
            print(f"\n\t[+] Le joueur {name} a été ajouté à la black list.")
        elif verification.upper() in ["N", "NO", "NON"]:
            print("\n\t[+] Commande annulée")
        else:
            print("\n\t[-] Choix invalide")
    else:
        print(f"\n\t[!] Le joueur {name} n'a pas été trouvé dans les dossiers.")
    input("\n\t| Tapez entrer quand c'est bon |")

def restore_player_from_blacklist():
    """Removes a player from the blacklist."""
    name = input("\n\tEntrez le nom de clone du joueur à retirer de la black list : ").strip()
    file_path = os.path.join("blacklist_players_list", f"{name}.txt")
    if os.path.exists(file_path):
        verification = input(f"\n\tEs-tu sûr de vouloir retirer le joueur {name} de la black list ? (Y/N) : ")
        if verification.upper() in ["Y", "YES", "OUI"]:
            os.remove(file_path)
            log_operation(f"Retrait du joueur {name} de la black list")
            print(f"\n\t[+] Le joueur {name} a été retiré de la black list.")
        elif verification.upper() in ["N", "NO", "NON"]:
            print("\n\t[+] Commande annulée")
        else:
            print("\n\t[-] Choix invalide")
    else:
        print(f"\n\t[!] Le joueur {name} n'a pas été trouvé dans la black list.")
    input("\n\t| Tapez entrer quand c'est bon |")

def display_player_in_blacklist():
    """Displays information about a player in the blacklist."""
    name = input("\n\tEntrez le nom de clone du joueur à afficher dans la black list : ").strip()
    file_path = os.path.join("blacklist_players_list", f"{name}.txt")
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            print(f"\n\t--- Informations pour {name} ---\n")
            print(file.read())
    else:
        print(f"\n\t[!] Le joueur {name} n'a pas été trouvé dans la black list.")
    input("\n\t| Tapez entrer quand c'est bon |")

def display_all_players_in_blacklist():
    """Displays all players in the blacklist."""
    blacklist_directory = "blacklist_players_list"
    if os.path.exists(blacklist_directory):
        print("\n\t--- Joueurs dans la black list ---\n")
        blacklist_players = os.listdir(blacklist_directory)
        if blacklist_players:
            for player in blacklist_players:
                print(f"\t- {player[:-4]}")  # Remove '.txt' extension
        else:
            print("\tAucun joueur dans la black list.")
    else:
        print("\n\tLe dossier de la black list est vide.")

def log_operation(operation):
    """Logs operations performed on the players."""
    with open("operations_log.txt", "a") as log_file:
        log_file.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {operation}\n")

def git_push():
    """Adds specified files, commits with a message, and force pushes to the main branch."""
    os.system("git add main.py operations_log.txt players_list reserve_players_list")
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
    create_reserve_directory()
    create_blacklist_directory()  # Add this line to create the blacklist directory
    main = True
    
    while main:
        print("\n\n\n\n\tMenu :\n\n")
        print("\t1. Incrémenter les sessions des joueurs et mettre à jour les points RP\n")
        print("\t2. Ajouter un nouveau joueur\n")
        print("\t3. Modifier le nom d'un joueur\n")
        print("\t4. Supprimer un joueur\n")
        print("\t5. Déplacer un joueur vers la réserve\n")
        print("\t6. Restaurer un joueur de la réserve\n")  
        print("\t7. Ajouter un commentaire du staff\n")
        print("\t8. Ajouter un avertissement\n")
        print("\t9. Afficher les informations d'un joueur\n")
        print("\t10. Afficher tous les commentaires du staff\n")
        print("\t11. Afficher toutes les raisons d'avertissements\n")
        print("\t12. Retirer les avertissements de plus d'un mois\n")
        print("\t13. Mettre un joueur dans la Black List\n")
        print("\t14. Sortir un joueur de la Black List\n")
        print("\t15. Afficher un joueur dans la Black List\n")
        print("\t16. Afficher tous les joueurs dans la black list\n")
        print("\t17. Quitter en sauvegardant\n")
        print("\t18. Quitter sans sauvegarder\n")

        choice = input("\tEntrez votre choix : ").strip()

        if choice == '1':
            entries = input(
                "\n\tEntrez les noms des joueurs avec + ou - pour les points RP (séparés par des virgules) : ").split(
                ",")
            updated_players = increment_sessions(entries)
            for name, new_grade in updated_players:
                print(f"\n\t{name} a maintenant été promu à {new_grade}.")
            print("\n\t[+] Les sessions ont été mises à jour")
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
            move_player_to_reserve()
            print("\n")
            os.system("clear")

        elif choice == '6':
            restore_player_from_reserve()
            print("\n")
            os.system("clear")

        elif choice == '7':
            add_staff_comment()
            print("\n")
            os.system("clear")

        elif choice == '8':
            add_warning()
            print("\n")
            os.system("clear")

        elif choice == '9':
            display_player_info()
            print("\n")
            os.system("clear")

        elif choice == '10':
            display_all_staff_comments()
            print("\n")
            os.system("clear")

        elif choice == '11':
            display_all_warnings()
            print("\n")
            os.system("clear")

        elif choice == '12':
            remove_old_warnings()
            print("\n")
            os.system("clear")

        elif choice == '13':
            move_player_to_blacklist()
            print("\n")
            os.system("clear")

        elif choice == '14':
            restore_player_from_blacklist()
            print("\n")
            os.system("clear")

        elif choice == '15':
            display_player_in_blacklist()
            print("\n")
            os.system("clear")

        elif choice == '16':
            display_all_players_in_blacklist()
            print("\n")
            os.system("clear")
        
        elif choice == '17':
            git_push()
            break

        elif choice == '18':
            while True:
                sure = input("\n\tEs-tu sûr de vouloir quitter sans sauvegarder ? (Y/N) : ")
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
