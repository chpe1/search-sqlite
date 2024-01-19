import sqlite3
import os


def recuperer_tables_et_colonnes():
    """
    Récupère les noms des tables et de leurs colonnes associés depuis une base de données SQLite.

    Returns:
    dict: Dictionnaire contenant les tables comme clés et une liste de leurs colonnes comme valeurs.
    """
    tables_et_colonnes = {}
    connexion = sqlite3.connect(nom_base_de_donnees)
    curseur = connexion.cursor()

    # Récupération de la liste des tables
    curseur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = curseur.fetchall()

    # Pour chaque table, récupération des colonnes
    for table in tables:
        table_nom = table[0]

        # Exécution de la requête pour récupérer les colonnes de la table
        curseur.execute(f"PRAGMA table_info({table_nom});")

        # Récupération des noms des colonnes
        colonnes = [colonne[1] for colonne in curseur.fetchall()]

        # Ajout de la table et de ses colonnes au dictionnaire
        tables_et_colonnes[table_nom] = colonnes

    connexion.close()

    # Retourner le dictionnaire
    return tables_et_colonnes


def rechercher_chaine(chaine_recherchee, tables_et_colonnes):
    """
    Recherche une chaîne dans les colonnes des tables d'une base de données SQLite.

    Args:
    chaine_recherchee (str): La chaîne à rechercher.
    tables_et_colonnes (dict): Dictionnaire contenant les tables comme clés et une liste de leurs colonnes comme valeurs.

    Returns:
    tuple: Tuple contenant trois éléments - (1) Dictionnaire des occurrences par table et colonne, (2) Dictionnaire des occurrences totales par table, (3) Liste des résultats exportés.
    """
    occurrences_par_table_colonne = {}
    occurrences_totales_par_table = {}
    # Export des résultats dans une liste
    resultats_export = list()

    # Parcours de chaque table et de ses colonnes
    for table, colonnes in tables_et_colonnes.items():
        nb_occurrences_table = 0

        # Parcours de chaque colonne dans la table
        for colonne in colonnes:
            # Exécution de la requête pour chercher la chaîne dans le colonne
            curseur.execute(
                f"SELECT * FROM {table} WHERE {colonne} LIKE ? COLLATE NOCASE", (f'%{chaine_recherchee}%',))
            # Récupération des résultats
            resultats_table = curseur.fetchall()
            # Nombre d'occurrences dans une colonne
            nb_occurrences = len(resultats_table)
            # Stockage du nombre d'occurrences par table et colonne
            occurrences_par_table_colonne[(table, colonne)] = nb_occurrences
            # Mise à jour du nombre total d'occurrences dans la table
            nb_occurrences_table += nb_occurrences

            for resultat in resultats_table:
                resultats_export.append(
                    f"Trouvé dans la table '{table}', colonne '{colonne}': {resultat}")

        # Stockage du nombre total d'occurrences par table
        occurrences_totales_par_table[table] = nb_occurrences_table
    return occurrences_par_table_colonne, occurrences_totales_par_table, resultats_export


def output_file(donnees_a_enregistrer):
    """
    Enregistre les données dans un fichier texte.

    Args:
    donnees_a_enregistrer (list): Liste des données à enregistrer dans le fichier.
    """
    with open('resultat_fichier.txt', 'w', encoding='utf-8') as fichier:
        for data in donnees_a_enregistrer:
            fichier.write(data + '\n')


if __name__ == '__main__':
    # Récupération des informations utiles à la requête
    while True:
        nom_base_de_donnees = input(
            'Entre le chemin relatif vers la base de données : ')
        if os.path.exists(nom_base_de_donnees):
            try:
                connexion = sqlite3.connect(nom_base_de_donnees)
                curseur = connexion.cursor()
                chaine_recherchee = input(
                    'Entre la chaîne de caractères que tu veux chercher : ')
                break
            except sqlite3.Error as e:
                print(
                    "SQLITE : Connexion impossible. Vérifiez que ce fichier est une base de données SQLITE.")
        else:
            print(
                f"La base de données {nom_base_de_donnees} n'existe pas. Veuillez entrer un chemin valide.")

    # Recherche des tables et des colonnes de la base de données
    tables_et_colonnes = recuperer_tables_et_colonnes()

    # Recherche de la string demandée dans la base de données
    occurrences_par_table_colonne, occurrences_totales_par_table, resultats_export = rechercher_chaine(
        str(chaine_recherchee), tables_et_colonnes)

    # Gestion de l'exportation du résultat
    # Création d'une liste qui contient les données à mettre dans le fichier de sortie (résultats de la requête)
    export = list()
    export.extend(resultats_export)

    # Ajout à la liste "export" du nombre d'occurences par colonne
    for (table, colonne), nb_occurrences in occurrences_par_table_colonne.items():
        if nb_occurrences != 0:
            ligne_occurrences = f"Nombre d'occurrences dans la colonne '{colonne}' de la table '{table}': {nb_occurrences}"
            export.append(ligne_occurrences)
            print(ligne_occurrences)

    # Ajout à la liste "export" du nombre total d'occurrences par table
    for table, nb_occurrences_table in occurrences_totales_par_table.items():
        if nb_occurrences_table != 0:
            ligne_occurrences_totales = f"Nombre total d'occurrences dans la table '{table}': {nb_occurrences_table}"
            export.append(ligne_occurrences_totales)
            print(ligne_occurrences_totales)

    # Ecriture des résultats dans un fichier texte
    if len(export) > 0:
        try:
            output_file(export)
            print(
                'Le résultat de la requête a été écrit dans le fichier : resultat_fichier.txt')
        except:
            print(
                'Une erreur s\'est produite lors de l\'enregistrement du fichier contenant les résultats de cette requête')
    else:
        print(
            'Cette chaine de caractère n\'a pas été trouvée dans la base de données')
    connexion.close()
