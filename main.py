#!/usr/bin/python
import gi

gi.require_version("Playerctl", "2.0")
gi.require_version("GLib", "2.0")
from gi.repository import Playerctl
from gi.repository import GLib

from pypresence import Presence, InvalidID
import time
import os
import math

rpc = Presence("834396257312964608")
manager = Playerctl.PlayerManager()


def connect_to_rpc():
	os.system(r"notify-send Discord\ RPC Connecting\ to\ Discord\ RPC")
	while True:
		try:
			rpc.connect()
			os.system(r"notify-send Discord\ RPC Connected")
			break
		except ConnectionRefusedError as e:
			os.system(r"notify-send Discord\ RPC Failed\ to\ connect\ to\ Discord\ RPC!\ Try\ again\ in\ 10s")
			time.sleep(10)
		except InvalidID as e:
			os.system(r"notify-send Discord\ RPC Client\ ID\ is not valid, Exiting")
			exit(-1)


def init_player(name):
	ncm = Playerctl.Player.new_from_name(name)
	ncm.connect("playback-status", on_change)
	ncm.connect("metadata", on_change)
	manager.manage_player(ncm)
	update_info(ncm)


def on_change(plr, *args):
	update_info(plr)


def on_name_appear(plr, name):
	if name.name == "netease-cloud-music":
		init_player(name)


def on_name_vanish(*args):
	rpc.clear()


def get_track_info(plr):
	song_title = plr.get_title()
	song_artist = plr.get_artist()
	status = plr.props.playback_status
	return song_title, song_artist, status


def get_track_time(plr):
	plr = Playerctl.Player.new("netease-cloud-music")
	track_time = int(int(plr.print_metadata_prop("mpris:length")) // 1e6)
	track_time_secs = math.ceil(track_time)
	cac_current_pos = plr.get_position()
	current_pos = math.floor(cac_current_pos / 1e6)
	left_sec = track_time_secs - current_pos
	return left_sec


def sec_to_epoch_time(pos:int):
	if not isinstance(pos, int):
		print("Value Error")
	else:
		epoch_time = math.floor(time.time())
		epoch_pos = epoch_time + pos
		return epoch_pos


def update_info(plr):
	t_title, artist, status = get_track_info(plr)
	track_t = get_track_time(plr)
	real_t = sec_to_epoch_time(track_t)
	if len(t_title) <= 2:
		title = t_title + " "
	else: title = t_title
	if status == 0:
		status_mark = "playing"
	elif status == 1 or status == 2:
		status_mark = "pausing"
	try:
		rpc.update(details=title, state=artist, large_image="netease", small_image=status_mark, \
	            large_text="Netease Cloud Music", small_text=status_mark, end=real_t)
	except BrokenPipeError as e:
		os.system("notify-send Discord\ RPC Lost\ connection\ to\ Discord,\ reconnecting")
	except InvalidID as e:
		os.system("notify-send Discord\ RPC Lost\ connection\ Discord,\ reconnecting")
		connect_to_rpc()


def main():
	connect_to_rpc()
	manager.connect("name-appeared", on_name_appear)
	manager.connect("player-vanished", on_name_vanish)
	for player in manager.props.player_names:
		if player.name == "netease-cloud-music":
			init_player(player)


if __name__ == "__main__":
	main()
	GLib.MainLoop().run()
