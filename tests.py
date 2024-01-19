import unittest
import sqlite3
from main import recuperer_tables_et_colonnes, rechercher_chaine


def create_database():
    # Création d'une connexion à la base de données en mémoire
    connexion = sqlite3.connect(":memory:")
    curseur = connexion.cursor()

    # Création d'une table "utilisateurs" avec deux colonnes : id et nom
    curseur.execute(
        "CREATE TABLE utilisateurs (id INTEGER PRIMARY KEY, nom TEXT);")

    # Création d'une table "articles" avec trois colonnes : id, titre et contenu
    curseur.execute(
        "CREATE TABLE articles (id INTEGER PRIMARY KEY, titre TEXT, contenu TEXT);")

    # Création une table "commandes" avec deux colonnes : id et montant
    curseur.execute(
        "CREATE TABLE commandes (id INTEGER PRIMARY KEY, montant REAL);")

    # Valider les modifications
    connexion.commit()

    return connexion, curseur


class TestRecupererTablesEtColonnes(unittest.TestCase):
    def setUp(self):
        # Création d'une base de données en mémoire pour les tests
        self.connexion, self.curseur = create_database()

    def test_recuperer_tables_et_colonnes(self):
        # Appel de la fonction pour récupérer les tables et colonnes
        resultats = recuperer_tables_et_colonnes(self.curseur)

        # Vérification que la clé "utilisateurs" est bien dans le dictionnaire
        self.assertIn("utilisateurs", resultats)

        # Vérification que la clé "articles" est bien dans le dictionnaire
        self.assertIn("articles", resultats)

        # Vérification que la clé "commandes" est bien dans le dictionnaire
        self.assertIn("commandes", resultats)

        # Vérification que les colonnes de la table "utilisateurs" sont bien "id" et "nom"
        self.assertListEqual(resultats["utilisateurs"], ["id", "nom"])

        # Vérification que les colonnes de la table "articles" sont bien "id", "titre", "contenu"
        self.assertListEqual(resultats["articles"], ["id", "titre", "contenu"])

        # Vérification que les colonnes de la table "commandes" sont bien "id", "montant"
        self.assertListEqual(resultats["commandes"], ["id", "montant"])


class TestRechercherChaine(unittest.TestCase):
    def setUp(self):
        # Création d'une base de données en mémoire pour les tests
        self.connexion, self.curseur = create_database()

    def test_rechercher_chaine(self):
        # Insertion des données de test
        self.curseur.execute(
            "INSERT INTO utilisateurs (nom) VALUES ('Alice');")
        self.curseur.execute(
            "INSERT INTO articles (titre, contenu) VALUES ('Titre 1', 'Contenu 1');")
        self.curseur.execute(
            "INSERT INTO commandes (montant) VALUES (100.0), (150.0), (200.0);")
        self.connexion.commit()

        # Appel de la fonction pour rechercher la chaîne dans les tables
        resultats = rechercher_chaine(
            "Titre", recuperer_tables_et_colonnes(self.curseur), curseur=self.curseur)

        # Vérification des résultats
        # Une occurrence dans la table "articles", colonne "titre"
        self.assertEqual(resultats[0][("articles", "titre")], 1)
        # Une occurrence totale dans la table "articles"
        self.assertEqual(resultats[1]["articles"], 1)
        self.assertIn(
            "Trouvé dans la table 'articles', colonne 'titre'", resultats[2][0])


if __name__ == '__main__':
    unittest.main()
