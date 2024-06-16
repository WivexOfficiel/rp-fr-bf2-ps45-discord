import os

players_list_directory = "players_list"

def read_file_with_fallback(filepath):
    encodings = ['utf-8', 'ISO-8859-1', 'latin-1']
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as file:
                return file.readlines()
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(f"Erreur de décodage pour le fichier : {filepath}")

def display_blacklisted_players():
    # Liste pour stocker les informations des joueurs blacklistés
    blacklisted_players = []

    # Parcourir tous les fichiers dans le dossier players_list
    for filename in os.listdir(players_list_directory):
        if filename.endswith(".txt"):
            player_filepath = os.path.join(players_list_directory, filename)
            
            # Lire les informations du joueur avec gestion de plusieurs encodages
            try:
                lines = read_file_with_fallback(player_filepath)
            except UnicodeDecodeError as e:
                print(e)
                continue

            # Initialiser les variables
            clone_name = ""
            discord_pseudo = ""
            is_blacklisted = False

            # Parcourir les lignes pour extraire les informations nécessaires
            for line in lines:
                if line.startswith("Nom de clone : "):
                    clone_name = line.split("Nom de clone : ")[1].strip()
                elif line.startswith("Pseudo Discord : "):
                    discord_pseudo = line.split("Pseudo Discord : ")[1].strip()
                elif line.startswith("Black liste : ") and "Oui" in line:
                    is_blacklisted = True

            # Si le joueur est blackliste, ajouter ses informations à la liste
            if is_blacklisted:
                blacklisted_players.append((clone_name, discord_pseudo))
    
    # Afficher les informations des joueurs blacklistés
    if blacklisted_players:
        print("\n\t-------------- BLACK LISTE -------------\n")
        for clone_name, discord_pseudo in blacklisted_players:
            print(f"\n\tNom de clone : {clone_name}")
            print(f"\tPseudo Discord : {discord_pseudo}\n")
            print("\t--------------------------------------")
    else:
        print("Aucun joueur sur la blacklist.")
