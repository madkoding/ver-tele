#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
UI layer - Interfaz gráfica usando Gtk con categorías
"""

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from typing import List, Tuple, Dict, Optional


class ChannelWindow(Gtk.Window):
    """Ventana principal de la aplicación con categorías"""

    CATEGORIES = {
        "Peliculas": [
            "Big Buck Bunny",
            "Tears of Steel",
            "Apple Test Stream",
            "Sintel",
            "Elephants Dream",
        ],
        "Deportes": [
            "Red Bull TV",
        ],
        "Documentales": [
            "NASA TV",
        ],
        "Musica": [
            "Radio 105 Network",
        ],
        "Tecnologia": [
            "Twit Live",
        ],
    }

    def __init__(self, on_channel_selected):
        super().__init__(title="VerTele - Visor de Canales")
        self.on_channel_selected = on_channel_selected
        self.selected_channel = None
        self.channels_by_category = {}

        self.set_border_width(10)
        self.set_default_size(600, 600)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.selected_treeview = None
        self.treeviews = {}
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configura la interfaz de usuario con categorías"""
        # Notebook para las categorías
        notebook = Gtk.Notebook()
        notebook.set_tab_pos(Gtk.PositionType.TOP)

        # Crear pestañas para cada categoría
        for category, channels in self.CATEGORIES.items():
            scrolled_window = Gtk.ScrolledWindow()
            scrolled_window.set_policy(
                Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC
            )
            scrolled_window.set_min_content_height(300)

            # ListStore para esta categoría
            channel_list = Gtk.ListStore(str, str, str, str)
            self.channels_by_category[category] = channel_list

            # TreeView con filtrado
            treeview = Gtk.TreeView(model=channel_list)
            self.treeviews[category] = treeview

            # Renderer para el nombre del canal
            renderer_text = Gtk.CellRendererText()
            column_title = Gtk.TreeViewColumn("Canal", renderer_text, text=0)
            treeview.append_column(column_title)

            # Buscador rápido
            search_entry = Gtk.Entry()
            search_entry.set_placeholder_text("Buscar canal...")
            search_entry.connect(
                "changed", self._on_search_changed, treeview, channel_list
            )

            # Layout vertical para la categoría
            category_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            category_box.pack_start(search_entry, False, False, 0)
            category_box.pack_start(treeview, True, True, 0)

            scrolled_window.add(category_box)
            notebook.append_page(scrolled_window, Gtk.Label(label=category))

        # Botón de reproducción
        self.play_button = Gtk.Button(label="▶ Reproducir")
        self.play_button.set_sensitive(False)
        self.play_button.connect("clicked", self._on_play_button_clicked)
        print(
            f"[UI] Botón 'Reproducir' creado, estado inicial: {self.play_button.get_sensitive()}"
        )

        # Layout principal
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.pack_start(notebook, True, True, 0)
        main_box.pack_start(self.play_button, False, False, 0)

        self.add(main_box)

        # Conectar selección en TreeView
        for category, channel_list in self.channels_by_category.items():
            treeview = self._get_treeview_for_category(category)
            if treeview:
                treeview.connect("cursor-changed", self._on_treeview_cursor_changed)

        # Actualizar estado inicial del botón
        self._update_play_button_state()
        print(
            f"[UI] UI configurada. Treeviews disponibles: {list(self.treeviews.keys())}"
        )

    def _get_treeview_for_category(self, category: str):
        """Obtiene el TreeView de una categoría"""
        return self.treeviews.get(category)

    def _on_search_changed(
        self, entry: Gtk.Entry, treeview: Gtk.TreeView, store: Gtk.ListStore
    ) -> None:
        """Filtro de búsqueda"""
        text = entry.get_text().lower()
        if text:
            store.set_visible_func(
                lambda model, iter, data: text in model[iter][0].lower()
            )
        else:
            store.set_visible_func(None)
        treeview.expand_all()

    def _on_treeview_cursor_changed(self, treeview: Gtk.TreeView) -> None:
        """Maneja la selección en TreeView"""
        self.selected_treeview = treeview
        selection = treeview.get_selection()
        if selection:
            model, tree_iter = selection.get_selected()
            if tree_iter:
                title, instance, page_url, stream_url = model[tree_iter][:]
                self.selected_channel = (title, instance, page_url, stream_url)
                self._update_play_button_state()
            else:
                self.selected_channel = None
                self._update_play_button_state()

    def _update_play_button_state(self) -> None:
        """Actualiza el estado del botón reproducir"""
        self.play_button.set_sensitive(self.selected_channel is not None)

    def _on_play_button_clicked(self, button: Gtk.Button) -> None:
        """Maneja el clic en el botón reproducir"""
        print(
            f"[UI] _on_play_button_clicked - Canal seleccionado: {self.selected_channel}"
        )
        if self.selected_channel:
            title, instance, page_url, stream_url = self.selected_channel
            print(f"[UI] Llamando callback con: title={title}, instance={instance}")
            if self.on_channel_selected:
                self.on_channel_selected(title, instance, page_url, stream_url)
        else:
            print("[UI] WARNING: No hay canal seleccionado")
            dialog = Gtk.MessageDialog(
                parent=self,
                flags=0,
                type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.OK,
                text="No se ha seleccionado un canal",
                secondary_text="Por favor selecciona un canal de la lista.",
            )
            dialog.set_title("Advertencia")
            dialog.run()
            dialog.destroy()

    def add_channel(
        self, title: str, instance: str, page_url: str, stream_url: str
    ) -> None:
        """Agrega un canal a su categoría"""
        # Determinar categoría basada en el título
        category = self._get_category_for_channel(title)
        if category and category in self.channels_by_category:
            self.channels_by_category[category].append(
                [title, instance, page_url, stream_url]
            )

    def _get_category_for_channel(self, title: str) -> Optional[str]:
        """Determina la categoría para un canal"""
        for category, channels in self.CATEGORIES.items():
            if title in channels:
                return category
        return "Otros"

    def select_default_channel(self):
        """Selecciona el primer canal disponible"""
        for category, channel_list in self.channels_by_category.items():
            if len(channel_list) > 0:
                treeview = self.treeviews.get(category)
                if treeview:
                    self.selected_treeview = treeview
                    selection = treeview.get_selection()
                    if selection:
                        iterator = channel_list.get_iter_first()
                        if iterator:
                            selection.select_iter(iterator)
                            # Obtener datos seleccionados
                            model, tree_iter = selection.get_selected()
                            if tree_iter:
                                title, instance, page_url, stream_url = model[
                                    tree_iter
                                ][:]
                                self.selected_channel = (
                                    title,
                                    instance,
                                    page_url,
                                    stream_url,
                                )
                break

        # Actualizar estado del botón después de seleccionar
        self._update_play_button_state()


if __name__ == "__main__":

    def dummy_callback(title, instance, page_url, stream_url):
        print(f"Canal: {title}, Instance: {instance}")

    win = ChannelWindow(dummy_callback)

    # Agregar canales de prueba
    test_channels = [
        ("Canal 13", "canal13", "https://www.canal13.cl/", "stream1"),
        ("TVN", "tvn", "https://www.tvn.cl/", "stream2"),
        ("Películas+", "peliculasmas", "https://peliculasmas.lat/", "stream3"),
        ("SeriesLatino", "serieslatino", "https://serieslatino.net/", "stream4"),
    ]

    for channel in test_channels:
        win.add_channel(*channel)

    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
