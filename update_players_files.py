import os

def display_blacklisted_players():
    # Liste pour stocker les informations des joueurs blacklistés
    blacklisted_players = []

    # Parcourir tous les fichiers dans le dossier players_list
    for filename in os.listdir("players_list"):
        if filename.endswith(".txt"):
            player_filepath = os.path.join("players_list", filename)
            
            # Lire les informations du joueur avec encodage ISO-8859-1
            try:
                with open(player_filepath, 'r', encoding='ISO-8859-1') as file:
                    lines = file.readlines()
            except UnicodeDecodeError:
                print(f"Erreur de décodage pour le fichier : {filename}")
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
        print("Joueurs sur la blacklist :")
        for player in blacklisted_players:
            print(player)
            print("-" * 40)
    else:
        print("Aucun joueur sur la blacklist.")

# Exécution du script
if __name__ == "__main__":
    display_blacklisted_players()
