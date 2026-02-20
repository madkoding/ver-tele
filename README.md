# VerTele

Visor de canales de televisión en streaming con GTK3

## Características

- **Cross-platform**: Funciona en Linux, Windows y macOS
- **Arquitectura desacoplada**: Fácil de mantener y testear
- **Base de datos SQLite**: Gestión de canales persistente
- **GTK3**: Interfaz gráfica nativa y ligera

## Requisitos

- Python 3.6+
- GTK3 (python-gi)
- VLC (para reproducir los streams)

### Instalación en Linux (Debian/Ubuntu)

```bash
sudo apt-get install python3-gi vlc
```

### Instalación en Windows

1. Instalar [Python 3](https://www.python.org/downloads/)
2. Instalar [VLC](https://www.videolan.org/vlc/)
3. Instalar python-gi con pip:
   ```bash
   pip install pygobject
   ```

### Instalación en macOS

```bash
brew install python3 vlc
pip3 install pygobject
```

## Estructura del Proyecto

```
ver-tele/
├── VerTele.py       # Punto de entrada principal
├── app.py           # Lógica de la aplicación y coordinación
├── database.py      # Acceso a datos (SQLite)
├── player.py        # Lógica de reproducción de video
├── ui.py            # Interfaz gráfica (Gtk)
├── requirements.txt # Dependencias Python
├── channels.db      # Base de datos de canales (generada)
└── README.md        # Este archivo
```

## Arquitectura

La aplicación sigue el patrón de desacoplamiento por capas:

- **Data Layer** (`database.py`): Maneja la persistencia con SQLite
- **Service Layer** (`player.py`): Lógica de negocio y reproducción
- **UI Layer** (`ui.py`): Interfaz gráfica con GTK3
- **Application Layer** (`app.py`): Coordina los componentes

## Uso

```bash
python VerTele.py
```

O simplemente:

```bash
./VerTele.py
```

## Testing

La arquitectura desacoplada permite testear cada componente individualmente:

```python
# Testear la base de datos
from database import ChannelDatabase
db = ChannelDatabase()
print(db.get_channel_count())

# Testear el reproductor
from player import StreamPlayer
player = StreamPlayer()
player.play_channel("Channel Name", "http://example.com/stream")

# Testear la UI
from ui import ChannelWindow, ChannelButton
```

## Contribuir

1. Clonar el repository
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Hacer commit (`git commit -m 'Add some AmazingFeature'`)
4. Hacer push (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la licencia MIT - ver el archivo LICENSE para más detalles.

<!-- AUTO-UPDATE-DATE -->
**Última actualización:** 2026-02-20 12:16:31 -03
