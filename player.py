#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Service layer - Lógica de negocio para reproducir canales
"""

from typing import Tuple, Optional
import subprocess
import sys
import os


class StreamPlayer:
    """Maneja la reproducción de streams de video"""

    def __init__(self):
        self._detect_player()

    def _detect_player(self) -> None:
        """Detecta el reproductor de video disponible en el sistema"""
        self.player_command = None
        self.player_executable = None

        # Buscar VLC en el sistema - vlc primero para tener interfaz grafica
        players_to_check = [
            "vlc",
            "/usr/bin/vlc",
            "/usr/local/bin/vlc",
            "/snap/bin/vlc",
        ]

        for player in players_to_check:
            try:
                # Si es un path absoluto, verificar si existe
                if player.startswith("/"):
                    if os.path.isfile(player):
                        # Verificar si funciona
                        result = subprocess.run(
                            [player, "--version"],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            timeout=2,
                        )
                        if result.returncode == 0:
                            self.player_command = player
                            self.player_executable = player
                            print(f"[PLAYER] Usando VLC: {player}")
                            break
                else:
                    # Buscar en PATH
                    result = subprocess.run(
                        ["which", player],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.DEVNULL,
                        timeout=2,
                    )
                    if result.returncode == 0:
                        vlc_path = result.stdout.decode().strip()
                        # Verificar si funciona
                        check_result = subprocess.run(
                            [vlc_path, "--version"],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            timeout=2,
                        )
                        if check_result.returncode == 0:
                            self.player_command = vlc_path
                            self.player_executable = vlc_path
                            print(f"[PLAYER] Usando VLC: {vlc_path}")
                            break
            except (
                subprocess.CalledProcessError,
                FileNotFoundError,
                subprocess.TimeoutExpired,
            ):
                continue

        if self.player_command is None:
            raise RuntimeError(
                "No se encontro VLC instalado. Instala VLC para reproducir canales."
            )

    def play_channel(self, title: str, stream_url: str) -> bool:
        """
        Inicia la reproduccion de un canal

        Args:
            title: Titulo del canal para mostrar en el reproductor
            stream_url: URL del stream de video

        Returns:
            True si se inicio correctamente, False en caso contrario
        """
        print(f"[PLAYER] Reproduciendo: {title}")
        print(f"[PLAYER] Stream URL: {stream_url}")
        print(f"[PLAYER] Reproductor: {self.player_executable}")

        if not self.player_executable:
            print("[PLAYER] ERROR: player_executable es None")
            return False

        try:
            # WSLg: configurar PulseAudio
            import os

            pulse_socket = "/mnt/wslg/PulseServer"
            env = os.environ.copy()
            if os.path.exists(pulse_socket):
                env["PULSE_SERVER"] = f"unix:{pulse_socket}"
                print(f"[PLAYER] Usando PulseAudio WSLg: {pulse_socket}")

            cmd = [
                self.player_executable,
                "--meta-title=" + title,
                stream_url,
            ]
            print(f"[PLAYER] Comando: {' '.join(cmd)}")

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
                env=env,
            )
            print(f"[PLAYER] VLC iniciado con PID: {process.pid}")
            print(f"[PLAYER] Deberia abrirse una ventana de VLC...")

            return True
        except Exception as e:
            print(f"[PLAYER] ERROR al reproducir '{title}': {e}", file=sys.stderr)
            import traceback

            traceback.print_exc(file=sys.stderr)
            return False

    def play_channel_with_player(
        self, title: str, stream_url: str, player: str
    ) -> bool:
        """
        Reproduce un canal usando un reproductor específico

        Args:
            title: Título del canal
            stream_url: URL del stream
            player: Comando del reproductor ('cvlc', 'vlc', 'mpv', etc.)
        """
        try:
            cmd = [player, "--meta-title=" + title, stream_url]
            subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
            return True
        except Exception:
            return False


class ChannelNotFoundException(Exception):
    """Excepción cuando no se encuentra un canal"""

    pass


if __name__ == "__main__":
    try:
        player = StreamPlayer()
        print(f"Reproductor detectado: {player.player_command}")
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)
