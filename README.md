# API_Points

## Programme de Points pour les vault sur Kiln
Les fournisseurs de produit Defi font face à un problème toujours croissant de fidélisation des consommateurs de vault et autres yield optimizers. Les offres étant nombreuses et toutes plus rentables les unes que les autres, il est important, pour vouloir tirer son épingle du jeu, de réussir à garder ses clients et à en récupérer de nouveaux, c'est ce que vient satisfaire notre produit.
Notre solution est conçue sur un modèle de Point as a service et tente d'améliorer l'expérience des utilisateurs de vaults sur Kiln en récompensant leur fidélité. Notre API attribue des points en fonction de la durée et du montant des dépôts, encourageant les utilisateurs à conserver leurs fonds plus longtemps. Les points peuvent être échangés contre des avantages exclusifs tels que des réductions sur les frais de transaction et/ou des airdrops exclusifs.

## Installation

Pour installer et exécuter ce projet localement, suivez les étapes ci-dessous :

1. Clonez le dépôt :
    ```bash
    git clone https://github.com/username/API_Points.git
    ```

2. Accédez au répertoire du projet :
    ```bash
    cd API_Points
    ```

3. Créez un environnement virtuel :
    ```bash
    python -m venv venv
    ```

4. Activez l'environnement virtuel :
    - Sur Windows :
        ```bash
        venv\Scripts\activate
        ```
    - Sur macOS/Linux :
        ```bash
        source venv/bin/activate
        ```

5. Installez les dépendances :
    ```bash
    pip install -r Flask, request, jsonify
    ```

6. Exécutez l'application Flask :
    ```bash
    python src/data.py
    ```

## Utilisation

Pour utiliser l'API, suivez les étapes ci-dessous :

1. Assurez-vous que l'application Flask est en cours d'exécution.
2. Ouvrez votre navigateur et allez à `http://127.0.0.1:5000/` pour voir la page d'accueil.
3. Pour calculer les points de staking, utilisez le point de terminaison `/points` avec les paramètres [wallet](http://_vscodecontentref_/0) et [vault](http://_vscodecontentref_/1).

Exemple de requête :
```bash
curl "http://127.0.0.1:5000/points?wallet=VOTRE_ADRESSE_WALLET&vault=VOTRE_ADRESSE_VAULT"
```
## Structure du projet

- `src/back/test.py`: Contient les tests pour l'API.
- `src/front/`: Contient les fichiers front-end (HTML, CSS, JS) pour l'interface utilisateur.
- `README.md`: Documentation du projet.
  
## Auteurs

[Hamelin Simon](https://github.com/Simonhamel1)
[Pupier charly](https://github.com/charlyppr/)
[Clabaut Ewan](https://github.com/Clab-ewan)
