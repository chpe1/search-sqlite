import sqlite3


def recuperer_tables_et_champs():
    # Dictionnaire pour stocker les tables et leurs champs
    tables_et_champs = {}

    # Récupération de la liste des tables
    curseur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = curseur.fetchall()

    # Pour chaque table, récupération des champs
    for table in tables:
        table_nom = table[0]

        # Exécution de la requête pour récupérer les champs de la table
        curseur.execute(f"PRAGMA table_info({table_nom});")

        # Récupération des noms des champs
        champs = [champ[1] for champ in curseur.fetchall()]

        # Ajout de la table et de ses champs au dictionnaire
        tables_et_champs[table_nom] = champs

    # Retourner le dictionnaire
    return tables_et_champs


def rechercher_chaine(chaine_recherchee, tables_et_champs):
    # Dictionnaire pour stocker le nombre d'occurrences par table et par champ
    occurrences_par_table_champ = {}
    # Dictionnaire pour stocker le nombre total d'occurrences par table
    occurrences_totales_par_table = {}

    # Pour chaque table et ses champs, recherche de la chaîne
    for table, champs in tables_et_champs.items():
        # Initialiser le nombre total d'occurrences pour la table actuelle
        nb_occurrences_table = 0

        for champ in champs:
            # Exécution de la requête pour rechercher la chaîne
            curseur.execute(
                f"SELECT * FROM {table} WHERE {champ} LIKE ?", (f'%{chaine_recherchee}%',))

            # Récupération des résultats
            resultats_table = curseur.fetchall()

            # Nombre d'occurrences pour le champ et la table actuels
            nb_occurrences = len(resultats_table)

            # Ajouter au dictionnaire occurrences_par_table_champ
            occurrences_par_table_champ[(table, champ)] = nb_occurrences

            # Ajouter au nombre total d'occurrences pour la table
            nb_occurrences_table += nb_occurrences

            # Afficher les résultats pour chaque champ et chaque table
            for resultat in resultats_table:
                print(
                    f"Trouvé dans la table '{table}', champ '{champ}': {resultat}")

        # Ajouter le nombre total d'occurrences pour la table au dictionnaire
        occurrences_totales_par_table[table] = nb_occurrences_table

    # Afficher le nombre d'occurrences pour chaque champ et chaque table
    for (table, champ), nb_occurrences in occurrences_par_table_champ.items():
        if nb_occurrences != 0:
            print(
                f"Nombre d'occurrences dans la table '{table}', champ '{champ}': {nb_occurrences}")

    # Afficher le nombre total d'occurrences par table
    for table, nb_occurrences_table in occurrences_totales_par_table.items():
        if nb_occurrences_table != 0:
            print(
                f"Nombre total d'occurrences dans la table '{table}': {nb_occurrences_table}")


nom_base_de_donnees = 'user.db'
chaine_recherchee = 'Marcq'

# Connexion à la base de données
connexion = sqlite3.connect(nom_base_de_donnees)
curseur = connexion.cursor()

tables_et_champs = recuperer_tables_et_champs()
resultats = rechercher_chaine(chaine_recherchee, tables_et_champs)

# Fermeture de la connexion
connexion.close()

print(resultats)
