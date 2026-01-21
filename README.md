# Drone Destroyer

**Drone Destroyer** je 2D arkádová hra vytvořená v jazyce **Python** pomocí knihovny **Pygame**. Hra funguje na principu klasiky Space Defender, ale je výrazně upravena, 
Hráč se ujímá role pilota stíhačky **F-16**, jehož úkolem je bránit noční město před vlnami nepřátelských bezpilotních dronů. Je nutné se probojovat až k šéfovi, **experimentálnímu letounu**, Jsou informace i o tom, že zvládne **lítat dozadu**. Dokud hráč nezničí toto letadlo, útok na jeho domov přinese katastrofální ztráty, neboť ono nepřátelské letadlo dokáže **vyrábět a vypouštět drony za letu**.

---

## Gameplay

- Ovládáš stíhačku F-16
- Přilétají **vlny nepřátelských dronů**
- Každá další vlna je náročnější
- Pokud nepřítel proletí pod obrazovku → ztrácíš skóre
- Po poslední vlně tě čeká **boss fight**
- Hra končí **vítězstvím** nebo **prohrou**

---

## Hlavní funkce

-  **Systém vln nepřátel** s postupným zvyšováním obtížnosti  
-  **Safe spawn systém** (žádné překrývání nepřátel)
-  **Výbuchy a vizuální efekty**
-  **Boss s unikátním chováním**
-  **Skóre systém** (zabití / únik nepřátel)
-  **Highscore žebříček**
-  **Oddělené nastavení hlasitosti hudby a SFX**
-  **Settings menu**:
  - počet vln
  - rychlost nepřátel
  - hlasitost hudby a zvuků
-  Vlastní **UI design** (menu, settings, end screen)

---

## Ovládání

| Klávesa | Akce |
|------|------|
| ← → ↑ ↓| Pohyb letadla |
| SPACE | Střelba |
| ↑ ↓ | Navigace v menu |
| ENTER | Potvrzení |
| ESC / P | Zpět / pauza |
| H | Zobrazení žebříčku skóre |

---

## Struktura projektu


```
/Projekt-Informatika2/
|--
|-- main.py                # Hlavní soubor
|
|-- src/
|   |-- game.py            # Hlavní třída hry (herní smyčka, stav)
|   |-- enemy.py           # Implementace třídy pro nepřátele
|   |-- bullet.py          # Implementace třídy pro střelbu
|   |-- player.py          # Implementace třídy pro hráče
|   |-- boss_bullet.py     # Implementace třídy pro střelbu bosse
|   |-- explosion.py       # Implementace třídy pro výbuch
|   |-- boss.py            # Implementace třídy pro bosse
|   |-- settings.py        # Nastavení hry
|
|-- assets/
|   |-- fonts/
|   |   |-- Oxanium-Bold.ttf
|   |   |-- Oxanium-Light.ttf
|   |   |-- Oxanium-Regular.ttf
|   |-- img/
|   |   |-- explosion/
|    |    |    |-- exp_{i}
|   |   |-- boss_rocket.png
|   |   |-- boss.png
|   |   |-- bullet.png
|   |   |-- enemy.png
|   |   |-- loss_bg.png
|   |   |-- menu_bg.png
|   |   |-- play_bg.png
|   |   |-- player.png
|   |   |-- win_bg.png
|   |-- sounds/
|   |   |-- boss_hit-player.wav
|   |   |-- collision.wav
|   |   |-- explosion_boss_sound.wav
|   |   |-- menu.wav
|   |   |-- playing1.wav
|   |   |-- shoot.wav
|   |   |-- victory_song.wav
|   |   |-- game_over_song.wav
|   |
|-- .gitignore             # Ignoruje zkompilované soubory
|-- README.md              # Popis projektu
```

---

## Požadavky

- **Python 3.13.7 (funguje i na verzi 3.10.12)**
- **Pygame** 

## Použité nástroje

- **Python 3.13.7**
- **Pygame**
- Vlastní assety (pozadí, efekty) - zvuky: freesound.org || grafika: ChatGPT
- KolourPaint - pro úpravu grafiky
- Audacity - úprava zvuků
- Vlastní fonty (Oxanium)

---

### DISCLAIMER
V tomto programu byla v omezené míře použita **generativní AI**. Jednalo se primárně o assety jako jsou **obrázky**, popřípadě pro některý **bugfixing**.