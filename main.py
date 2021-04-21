import gi
gi.require_version("Playerctl", "2.0")
gi.require_version("GLib", "2.0")
from gi.repository import Playerctl
from gi.repository import GLib

from pypresence import Presence, InvalidID
import time

rpc = Presence("834396257312964608")
manager = Playerctl.PlayerManager()

def connect_to_rpc():
	while True:
		try:
			rpc.connect()
			break
		except ConnectionRefusedError as e:
			print("Failed to connect to discord rich presence! Try again in 10s")
			time.sleep(10)
		except InvalidID as e:
			print("Client ID is not valid, please check your client ID")


def init_player(name):
	ncm = Playerctl.Player.new_from_name(name)
	ncm.connect("playback-status::playing", on_playing)
	ncm.connect("playback-status::paused", on_paused)
	ncm.connect("metadata", on_metadata)
	manager.manage_player(ncm)
	update_info(ncm)


def on_playing(plr, sts):
	update_info(plr)


def on_paused(plr, sts):
	update_info(plr)


def on_metadata(plr, metadata):
	update_info(plr)


def get_song_info(plr):
	song_title = plr.get_title()
	song_artist = plr.get_artist()
	status = plr.props.playback_status
	return song_title, song_artist, status


def update_info(plr):
	title, artist, status = get_song_info(plr)
	if status == 0:
		status_mark = "playing"
	elif status == 1 or status == 2:
		status_mark = "pausing"
	rpc.update(details=title, state=artist, large_image="neteaseicon", small_image=status_mark,\
	           large_text="Netease Cloud Music", small_text=status_mark)


connect_to_rpc()

for player in manager.props.player_names:
	init_player(player)

GLib.MainLoop().run()




