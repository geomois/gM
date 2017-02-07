#!/usr/bin/python

import cgi
import layar
import copy

parameters = cgi.FieldStorage()

layer = parameters.getvalue("layer", "firstroomwp4u")

document = layar.Document(layer)

twit=layar.Hotspot("twit")
twit.anchor=layar.AnchorUser()
twit.object=layar.Object("http://custom.layar.nl/~ioannis/dunhill/arfiles/room3_files/img_twit.png",size=1.0)
twit.actions.append(layar.Action("http//twitter.com","text/html"))
twit.transform.translate.x= -7.079632
twit.transform.translate.y = 0.0
twit.transform.translate.z = 2.009281
twit.transform.rotate_angle = 95.079887
twit.transform.rotate_z = 1.0
twit.show_biw_onclick = False
twit.object.show_loading_indicator = False
document.hotspots.append(twit)

room=layar.Hotspot("room")
room.anchor=layar.AnchorUser()
room.object=layar.Object("http://custom.layar.nl/~ioannis/dunhill/arfiles/room2_files/msh_L3D.l3d", size=16.448834737141926)
room.transform.scale = layar.Vector3f(1012.18,1012.18,1012.18)
room.show_biw_onclick = False
room.object.show_loading_indicator = False
document.hotspots.append(room)

nextRoom=layar.Hotspot("nextRoom")
nextRoom.anchor=layar.AnchorUser()
nextRoom.object=layar.Object("http://custom.layar.nl/~ioannis/dunhill/arfiles/room3_files/door.png",size=1.0)
nextRoom.object.event_handlers["onClick"] = layar.EventHandler(handler="sound")
nextRoom.transform.translate.x= 0.0
nextRoom.transform.translate.y = -51.857521
nextRoom.transform.translate.z = 0.386935
nextRoom.transform.scale = layar.Vector3f(18.342666,18.342666,18.342666)
nextRoom.transform.rotate_angle = 179.999991
nextRoom.transform.rotate_x = 1.0
nextRoom.show_biw_onclick = False
nextRoom.object.show_loading_indicator = False
document.hotspots.append(nextRoom)

second=layar.Hotspot("second")
second.anchor=layar.AnchorUser()
second.object=layar.Object("http://custom.layar.nl/~ioannis/dunhill/arfiles/room2_files/msh_L3D.004.l3d", size=16.448834737141926)
second.object.event_handlers["onLoad"] = layar.EventHandler(handler="delete")
second.transform.scale = layar.Vector3f(1012.18,1012.18,1012.18)
second.show_biw_onclick = False
second.object.show_loading_indicator = True

sound=layar.Hotspot("sound")
sound.anchor=layar.AnchorPOI("room")
sound.object=layar.Object("http://custom.layar.nl/~ioannis/dunhill/arfiles/Unlock.mp3")
sound.show_biw_onclick = False
sound.object.event_handlers["onPlaybackFinish"] = layar.EventHandler(handler="room2")
sound.object.show_playback_controls = False
sound.object.show_loading_indicator = False



url_L=["http://custom.layar.nl/~ioannis/dunhill/arfiles/MonitorComplete_files/matX_screen.mp4","http://custom.layar.nl/~ioannis/dunhill/arfiles/MonitorComplete_files/matB_screen.mp4","http://custom.layar.nl/~ioannis/dunhill/arfiles/MonitorComplete_files/matC_screen.mp4"]

roomTv=layar.Hotspot("roomTv")
roomTv.anchor=layar.AnchorUser()
roomTv.object=layar.Object("http://custom.layar.nl/~ioannis/dunhill/arfiles/MonitorComplete_files/msh_L3D.008.l3d", size=5.1334623495737715)
roomTv.show_biw_onclick = False
roomTv.object.event_handlers['onClick'] = layar.EventHandler(handler="model_Bat")
roomTv.object.show_loading_indicator = False
roomTv.transform.translate.x= 4.65
roomTv.transform.translate.y = 7.65
roomTv.transform.translate.z = 0.45
roomTv.transform.rotate_angle = -40.25
roomTv.transform.rotate_z = 1.0
roomTv.transform.scale = layar.Vector3f(7.424441,7.424441,7.424441)
roomTv.object.override_materials.append(
    layar.OverrideMaterial("screen", diffuse_color="#ffffff", ambient_color="#ffffff",specular_color="#ffffff",
    texture=layar.Texture(url=url_L[0])
    )
)
roomTv.object.override_materials[0].texture.loop_playback=False
roomTv.object.override_materials[0].shininess=50


model_Bat = copy.deepcopy(roomTv)
model_Bat.object.override_materials[0].texture.url=url_L[1]
model_Bat.object.event_handlers['onClick'] = layar.EventHandler(handler="model_Cap")

model_Cap= copy.deepcopy(roomTv)
model_Cap.object.override_materials[0].texture.url=url_L[2]
model_Cap.object.override_materials[0].texture.event_handlers['onPlaybackFinish']=layar.EventHandler(handler="roomTv")
model_Cap.object.event_handlers['onClick'] = layar.EventHandler(handler="roomTv")


rotation=layar.Hotspot("rotation")
rotation.anchor=layar.AnchorUser()
rotation.object=layar.Object("http://custom.layar.nl/~ioannis/dunhill/dunhillRot/dunhillRot.html",content_type="text/html", size=3.0)
rotation.object.viewport=layar.Viewport(height=175,width=125)
rotation.object.viewport.scrollable=True
rotation.transform.scale = layar.Vector3f(1.841071,2.555846,1.0)
rotation.transform.translate.x= 6.35
rotation.transform.translate.y=1.0
rotation.transform.translate.z=1.0281
rotation.show_biw_onclick = False
rotation.object.show_playback_controls = False
rotation.object.show_loading_indicator = True

move_hotspots = []

room.animations.onUpdate.append(layar.Animation("translate",
    from_value = 0,
    to_value = 3800,
    length = 1780,
    persist= False,
    axis_x = 0,
    axis_y = 1,
    axis_z = 0))

move_hotspots.append(room)


document.handlers['delete'] = layar.EventHandler(update=layar.Update(hotspots=[
],deleted_hotspots=["room","twit","nextRoom"]))

document.handlers['sound'] = layar.EventHandler(update=layar.Update(hotspots=[
    sound
]))

document.handlers['model_Bat'] = layar.EventHandler(update=layar.Update(hotspots=[
   model_Bat
]))

document.handlers['model_Cap'] = layar.EventHandler(update=layar.Update(hotspots=[
   model_Cap
]))

document.handlers['roomTv'] = layar.EventHandler(update=layar.Update(hotspots=[
   roomTv
]))

document.handlers['room2'] = layar.EventHandler(update=layar.Update(hotspots=[
    second,
    roomTv
],deleted_hotspots=["sound"]))

print("Content-Type: text/plain\n")
print(document.to_json())
