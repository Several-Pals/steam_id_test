import sys
import requests
from bs4 import BeautifulSoup
import re
import asyncio
import aiohttp
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QMessageBox, QHBoxLayout, QLabel
from PySide6.QtGui import QFont
from PySide6.QtCore import QThread, Signal

def is_mod_collection(item_id):
    url = f"https://steamcommunity.com/sharedfiles/filedetails/?id={item_id}"
    response = requests.get(url)
    if response.status_code != 200:
        return False
    soup = BeautifulSoup(response.text, 'html.parser')
    subscribe_text = soup.find('span', class_='general_btn subscribe')
    return subscribe_text is not None

def is_valid_steam_collection_url(url):
    pattern = r'https://steamcommunity\.com/sharedfiles/filedetails/\?id=\d+'
    if re.match(pattern, url):
        item_id = url.split('id=')[1]
        return is_mod_collection(item_id)
    return False

def get_mod_ids_from_steam_collection(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        mods = soup.find_all('div', class_='collectionItem')
        mod_ids = []
        for mod in mods:
            mod_link = mod.find('a', href=True)
            if mod_link:
                mod_url = mod_link['href']
                mod_id = mod_url.split('id=')[1]
                mod_ids.append(mod_id)
        return mod_ids
    except requests.exceptions.RequestException as e:
        QMessageBox.critical(None, "Error", f"Error loading the page: {e}")
        return []

def get_game_name_from_steam_collection(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        game_name_tag = soup.find('div', class_='apphub_AppName')
        if game_name_tag:
            return game_name_tag.text.strip()
        else:
            return "Unknown Game"
    except requests.exceptions.RequestException as e:
        QMessageBox.critical(None, "Error", f"Error loading the page: {e}")
        return "Unknown Game"

async def find_map_folder_name_async(session, item_id):
    url = f"https://steamcommunity.com/sharedfiles/filedetails/?id={item_id}"
    async with session.get(url) as response:
        if response.status != 200:
            return None
        text = await response.text()
        soup = BeautifulSoup(text, 'html.parser')
        for element in soup.find_all(string=True):
            if "Map Folder:" in element:
                name = element.split("Map Folder: ")[1].strip()
                return name
        return None

async def fetch_map_names(mod_ids):
    async with aiohttp.ClientSession() as session:
        tasks = [find_map_folder_name_async(session, mod_id) for mod_id in mod_ids]
        results = await asyncio.gather(*tasks)
        return [result for result in results if result is not None]

class AsyncWorker(QThread):
    result_ready = Signal(list)

    def __init__(self, mod_ids):
        super().__init__()
        self.mod_ids = mod_ids

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        map_names = loop.run_until_complete(fetch_map_names(self.mod_ids))
        self.result_ready.emit(map_names)

class SteamModCollectionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Steam Mod Collection Extractor')
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        url_label = QLabel("Enter Steam Collection URL:", self)
        url_label.setFont(QFont("Arial", 18))
        self.layout.addWidget(url_label)

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("https://steamcommunity.com/sharedfiles/filedetails/?id=123456789")
        self.layout.addWidget(self.url_input)

        separator_label = QLabel("Separator for IDs (optional):", self)
        separator_label.setFont(QFont("Arial", 12))
        self.layout.addWidget(separator_label)

        self.separator_input = QLineEdit(self)
        self.separator_input.setText("\n")
        self.layout.addWidget(self.separator_input)

        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.on_start_button_click)
        self.layout.addWidget(self.start_button)

        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        self.layout.addWidget(self.output_text)

        self.info_label = QLabel("", self)
        self.layout.addWidget(self.info_label)

        self.map_button = QPushButton('Get Map Folder', self)
        self.map_button.clicked.connect(self.on_map_button_click)
        self.map_button.hide()
        self.layout.addWidget(self.map_button)

        self.map_output_text = QTextEdit(self)
        self.map_output_text.setReadOnly(True)
        self.map_output_text.hide()
        self.layout.addWidget(self.map_output_text)

        self.setLayout(self.layout)

    def on_start_button_click(self):
        url = self.url_input.text()
        separator = self.separator_input.text()
        if is_valid_steam_collection_url(url):
            self.mod_ids = get_mod_ids_from_steam_collection(url)
            game_name = get_game_name_from_steam_collection(url)
            self.output_text.setText(separator.join(self.mod_ids))
            self.info_label.setText(f"INFO | Amount: {len(self.mod_ids)} | Game: {game_name}")

            if "Project Zomboid" in game_name:
                self.map_button.show()
                self.map_output_text.show()
            else:
                self.map_button.hide()
                self.map_output_text.hide()
        else:
            QMessageBox.warning(self, "Invalid URL", "Please enter a valid Steam collection URL.")

    def on_map_button_click(self):
        if not hasattr(self, 'mod_ids'):
            QMessageBox.warning(self, "No IDs", "Please extract IDs first.")
            return

        self.worker = AsyncWorker(self.mod_ids)
        self.worker.result_ready.connect(self.on_map_names_ready)
        self.worker.start()

    def on_map_names_ready(self, map_names):
        self.map_output_text.setText("\n".join(map_names))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SteamModCollectionApp()
    window.show()
    sys.exit(app.exec())