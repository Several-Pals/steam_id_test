```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

collection PZ -
https://steamcommunity.com/sharedfiles/filedetails/?id=3077342790

collection ARMA - https://steamcommunity.com/sharedfiles/filedetails/?id=3293739569

map -
https://steamcommunity.com/sharedfiles/filedetails/?id=2820363371

map -
https://steamcommunity.com/sharedfiles/filedetails/?id=2730975264

mod -
https://steamcommunity.com/sharedfiles/filedetails/?id=2816646537


```bash
pyinstaller --onefile --windowed --icon=pic.icns "Mod Steam Grabber.py"

create-dmg --volname "IDsteam" --background "pic.png" --window-size 600 300 --icon-size 100 --icon "IDsteam.app" 200 190 --app-drop-link 400 185 "YourApp.dmg" "dist/main.app"

dmgbuild -s settings.py "main" "IDsteam.dmg"

python3 setup.py py2app


hdiutil create -volname "Your App Name" -srcfolder "YourAppInstaller" -ov -format UDZO "YourApp.dmg"
```
