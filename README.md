# projetFlask

##### Developpeurs
* [Marieme Pouye](https://www.linkedin.com/in/marieme-pouye/)
* [Moustapha Dioum](https://www.linkedin.com/in/moustapha-dioum-02b058200/)
* [Ibrahima Diogoye Diouf](https://www.linkedin.com/in/ibrahima-diogoye-diouf-9a2120224/)
* [Mahamadou KABA](https://www.linkedin.com/in/mahamadou-kaba-457632170/)

### Application flask
#### Création d'un environnement virtuel avec python
```bash
python3 -m venv myproject
```

> ! se placer dans le dossier qui contient  myproject

#### Activation de votre environnement
```bash
source  myproject/bin/activate
```


#### Installation des paquets necessaires
```bash
pip3 install -r requirements.txt
```


#### Installation du SGBD [postgresql](https://www.postgresql.org/download/linux/ubuntu/)

```bash
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get -y install postgresql
```

> Renseigner votre nom d'utilisateur ubuntu pour votre utilisateur postgres
> Choisir le mode super utilisateur aussi pour pouvoir creer la base de donnee grace à votre user

#### Creation de votre utilisateur sur postgres
```bash
sudo -u postgres createuser -P -s -e [votre nom d'utilisateur]
```
> Assurez vous d'avoir le fichier setup.py
#### Creation de votre base de donnee et des tables pour le projet
```bash
python3 setup.py
```
#### editez les fichiers models/users.py et index.py et ajouter la ligne suivante
```python3
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://[votre nom d'utilisateur]:[votre mot de passe]@localhost/[le nom de la base de donnee]"
```
> NB: Mettez le nom de votre utilisateur et votre mot de passe de votre utilisateur postgres cree en haut
#### Executez le fichier index avec la commande suivante pour lancer l'application
```bash
python3 index.py
```

#### Pour desactiver  votre environnement faites:
```bash
deactivate
```
