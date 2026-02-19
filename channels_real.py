#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Canales de prueba que FUNCIONAN para VerTele
Incluye videos de demo y canales de prueba verificados
"""

CHANNELS = [
    # ==================== PELICULAS Y VIDEOS DE PRUEBA (FUNCIONAN) ====================
    {
        "title": "Big Buck Bunny",
        "instance": "bigbuckbunny",
        "page_url": "https://peach.blender.org/",
        "stream_url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8",
        "category": "Peliculas",
    },
    {
        "title": "Tears of Steel",
        "instance": "tearsofsteel",
        "page_url": "https://mango.blender.org/",
        "stream_url": "https://demo.unified-streaming.com/k8s/features/stable/video/tears-of-steel/tears-of-steel.ism/.m3u8",
        "category": "Peliculas",
    },
    {
        "title": "Apple Test Stream",
        "instance": "appletest",
        "page_url": "https://developer.apple.com",
        "stream_url": "https://devstreaming-cdn.apple.com/videos/streaming/examples/img_bipbop_adv_example_fmp4/master.m3u8",
        "category": "Peliculas",
    },
    {
        "title": "Sintel",
        "instance": "sintel",
        "page_url": "https://durian.blender.org/",
        "stream_url": "https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8",
        "category": "Peliculas",
    },
    {
        "title": "Elephants Dream",
        "instance": "elephantsdream",
        "page_url": "https://orange.blender.org/",
        "stream_url": "https://bitdash-a.akamaihd.net/content/elephantsdream/hls/playlist.m3u8",
        "category": "Peliculas",
    },
    # ==================== NOTICIAS (PUBLICOS) ====================
    # Nota: Muchos canales de noticias estan geo-bloqueados
    # Si no funcionan, el usuario puede agregar sus propios canales
    # ==================== MUSICA ====================
    {
        "title": "Radio 105 Network",
        "instance": "radio105",
        "page_url": "https://www.radio105.it",
        "stream_url": "https://wowzaprod133-i.akamaihd.net/hls/live/577385/a1e0ad3f/a1e0ad3f_1_1000/chunklist.m3u8",
        "category": "Musica",
    },
    # ==================== DEPORTES ====================
    {
        "title": "Red Bull TV",
        "instance": "redbulltv",
        "page_url": "https://www.redbull.com/int-en/tv",
        "stream_url": "https://rbmn-live.akamaized.net/hls/live/590964/BoRB-AT/master.m3u8",
        "category": "Deportes",
    },
    # ==================== DOCUMENTALES ====================
    {
        "title": "NASA TV",
        "instance": "nasatv",
        "page_url": "https://www.nasa.gov/multimedia/nasatv/",
        "stream_url": "https://ntv1.akamaized.net/hls/live/2014075/NASA-NTV1-HLS/master.m3u8",
        "category": "Documentales",
    },
    # ==================== VARIOS ====================
    {
        "title": "Twit Live",
        "instance": "twitlive",
        "page_url": "https://twit.tv/live",
        "stream_url": "https://twit.live-s.cdn.bitgravity.com/cdn-live-s1/_definst_/twit/live/high/playlist.m3u8",
        "category": "Tecnologia",
    },
]


def get_channels_by_category(category):
    """Retorna canales filtrados por categoria"""
    return [ch for ch in CHANNELS if ch.get("category") == category]


def get_all_channels():
    """Retorna todos los canales"""
    return CHANNELS


if __name__ == "__main__":
    print(f"Total canales: {len(CHANNELS)}")
    for ch in CHANNELS:
        print(f"  - {ch['title']} ({ch['category']})")
