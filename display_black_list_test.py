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

            # Vérifier si le joueur est sur la blacklist
            is_blacklisted = False
            for line in lines:
                if line.startswith("Black liste : ") and "Oui" in line:
                    is_blacklisted = True
                    break
            
            # Si le joueur est blackliste, ajouter ses informations à la liste
            if is_blacklisted:
                player_info = ''.join(lines)
                blacklisted_players.append(player_info)
    
    # Afficher les informations des joueurs blacklistés
    if blacklisted_players:
        print("\n\t------------------ BLACK LISTE ------------------")
        for player in blacklisted_players:
            print("\n")
            print(player)
            print("-" * 40)
    else:
        print("Aucun joueur sur la blacklist.")

# Exécution du script
if __name__ == "__main__":
    display_blacklisted_players()
