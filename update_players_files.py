import os

def update_player_files(directory):
    """Adds 'Nombre de warns : 0' to each player file if it does not already exist."""
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and filename.endswith(".txt"):
            with open(file_path, 'r+', encoding='iso-8859-1') as file:
                lines = file.readlines()
                warns_present = any("Nombre de warns" in line for line in lines)

                if not warns_present:
                    for i, line in enumerate(lines):
                        if "Nombre d'avertissement(s)" in line:
                            lines.insert(i + 1, "Nombre de warns : 0\n")
                            break

                    file.seek(0)
                    file.writelines(lines)
                    print(f"[+] 'Nombre de warns : 0' ajouté à {filename}")

def update_all_players():
    """Updates all player files in both 'players_list' and 'reserve_players_list'."""
    directories = ["players_list", "reserve_players_list"]

    for directory in directories:
        if os.path.exists(directory):
            update_player_files(directory)
        else:
            print(f"[!] Le dossier {directory} n'existe pas.")

# Appel de la fonction pour mettre à jour tous les fichiers de joueurs
update_all_players()
