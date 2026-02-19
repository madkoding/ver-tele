#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main application - Coordina todos los componentes
"""

import sys
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

from database import ChannelDatabase
from player import StreamPlayer, ChannelNotFoundException
from ui import ChannelWindow


class VerTeleApp:
    """Aplicación principal de VerTele"""

    def __init__(self):
        self.db = ChannelDatabase()
        self.player = None
        self.window = None
        self._init_player()

    def _init_player(self):
        """Inicializa el reproductor con manejo de errores"""
        try:
            self.player = StreamPlayer()
        except RuntimeError as e:
            # Mostrar advertencia pero permitir continuar
            dialog = Gtk.MessageDialog(
                parent=None,
                flags=0,
                type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.OK,
                text="Reproductor no detectado",
                secondary_text=str(e)
                + "\n\nLa aplicación funcionará pero no podrás reproducir canales.",
            )
            dialog.set_title("Advertencia")
            dialog.run()
            dialog.destroy()

    def run(self) -> int:
        """Inicia la aplicación"""
        try:
            self._setup_ui()
            Gtk.main()
            return 0
        except Exception as e:
            self._show_error("Error fatal", str(e))
            return 1

    def _setup_ui(self) -> None:
        """Configura la interfaz de usuario"""
        self.window = ChannelWindow(self._on_channel_selected)
        self.window.connect("delete-event", self._on_delete_event)

        channels = self.db.get_all_channels()
        for channel in channels:
            title, instance, page_url, stream_url = channel
            self.window.add_channel(title, instance, page_url, stream_url)

        self.window.select_default_channel()
        self.window.show_all()

    def _on_channel_selected(
        self, title: str, instance: str, page_url: str, stream_url: str
    ) -> None:
        """Maneja la selección de un canal"""
        print(f"[DEBUG] _on_channel_selected llamado:")
        print(f"[DEBUG]   Title: {title}")
        print(f"[DEBUG]   Instance: {instance}")
        print(f"[DEBUG]   Page URL: {page_url}")
        print(f"[DEBUG]   Stream URL: {stream_url}")

        if self.player is None:
            dialog = Gtk.MessageDialog(
                parent=None,
                flags=0,
                type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="No se puede reproducir",
                secondary_text="VLC no está instalado.\n\nPor favor instala VLC para reproducir canales.",
            )
            dialog.set_title("Error")
            dialog.run()
            dialog.destroy()
            return

        try:
            print("[DEBUG] Buscando canal en base de datos...")
            channel = self.db.get_channel_by_instance(instance)
            print(f"[DEBUG] Canal encontrado: {channel}")

            if channel is None:
                raise ChannelNotFoundException(f"No se encontró el canal: {instance}")

            print(f"[DEBUG] Reproduciendo stream...")
            success = self.player.play_channel(title, stream_url)
            print(f"[DEBUG] Resultado reproducción: {success}")

            if not success:
                raise Exception("No se pudo iniciar la reproducción")
        except ChannelNotFoundException as e:
            print(f"[DEBUG] Canal no encontrado: {e}")
            self._show_error("Error al reproducir", str(e))
        except Exception as e:
            print(f"[DEBUG] Error en reproducción: {e}")
            import traceback

            traceback.print_exc()
            self._show_error("Error al reproducir", str(e))

    def _show_error(self, primary_text: str, secondary_text: str) -> None:
        """Muestra un diálogo de error"""
        dialog = Gtk.MessageDialog(
            parent=None,
            flags=0,
            type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=primary_text,
            secondary_text=secondary_text,
        )
        dialog.set_title("Error")
        dialog.run()
        dialog.destroy()

    def _on_delete_event(self, widget, event):
        """Maneja el cierre de la ventana"""
        Gtk.main_quit()
        return False


def main() -> int:
    """Punto de entrada principal"""
    try:
        app = VerTeleApp()
        return app.run()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
