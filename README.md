<h1 align="center">AtlasFind</h1>

<p align="center">
 <img height="250" src="https://user-images.githubusercontent.com/28122432/222305987-945eed43-d1fe-4b6b-9ea5-1446ce0730ec.png">
</p>

This project is an answer-based search engine that fetches and answers user questions based on content from the [No Man's Sky Wiki fandom](https://nomanssky.fandom.com/wiki/No_Man%27s_Sky_Wiki) page. The search engine is designed to provide quick and accurate answers to questions related to the game, such as information on planets, star systems, resources, creatures, and more.

<p align="center">
<img width="500" alt="Capture d’écran 2023-03-14 à 15 08 25" src="https://user-images.githubusercontent.com/28122432/225151408-bab59e8d-f058-4df7-875f-fa9431222636.png">
</p>

## Getting Started

### Prerequisites

To run this project, you will need:

* Python (version 3.8.0 or higher)
* Django (version 3.0 or highter)
* The text stored in the [No Man's Sky Wiki fandom](https://nomanssky.fandom.com/wiki/No_Man%27s_Sky_Wiki) website

### Installation and Setup

1. Clone this repository to your local machine.

```
git clone https://github.com/Scylidose/AtlasFind.git
```

2. Create and activate a new virtual environment:

```
python3 -m venv venv
source venv/bin/activate # on Linux or macOS
.\venv\Scripts\activate # on Windows
```

3. Install the required Python packages:

```
pip3 install -r requirements.txt
```

This will install all the necessary dependencies.

4. Run project:

```
python manage.py runserver
```

## Contributing

Contributions to this project are welcome. If you find a bug, have a feature request, or want to contribute code, please open an issue or pull request on the project's GitHub page.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
