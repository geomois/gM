import json

try:
    from collections import OrderedDict
except NameError:
    pass
except ImportError:
	pass

class Document(object):

    def __init__(self, layer):
        self.layer = layer
        self.hotspots = []
        self.error_code = 0
        self.error_string = "OK"
        self.next_page_key = None
        self.more_pages = None
        self.radius = None
        self.refresh_interval = None
        self.refresh_distance = None
        self.full_refresh = None
        self.actions = []
        self.show_message = None
        self.deleted_hotspots = []
        self.animations = Animations()
        self.reference_images = []
        self.full_refresh = True
        self.handlers = {}

    def hotspot(self, id):
        for hotspot in self.hotspots:
            if hotspot.id == id:
                return hotspot

        return None

    def reference_image(self, key):
        for reference_image in self.reference_images:
            if reference_image.key == key:
                return reference_image

        return None

    def to_dict(self):
        data = _ordered_dict()
        data['layer'] = self.layer
        data['errorCode'] = self.error_code
        data['errorString'] = self.error_string

        if self.next_page_key is not None:
            data['nextPageKey'] = self.next_page_key
        if self.more_pages is not None:
            data['morePages'] = self.more_pages
        if self.radius is not None:
            data['radius'] = self.radius
        if self.refresh_interval is not None:
            data['refreshInterval'] = self.refresh_interval
        if self.refresh_distance is not None:
            data['refreshDistance'] = self.refresh_distance
        if self.full_refresh is not None:
            data['fullRefresh'] = self.full_refresh
        if self.actions:
            data['actions'] = [a.to_dict() for a in self.actions]
        if self.show_message is not None:
            data['showMessage'] = self.show_message

        data['hotspots'] = [h.to_dict() for h in self.hotspots]

        if self.animations.has_animations():
            data['animations'] = self.animations.to_dict()

        if self.reference_images:
            data['referenceImages'] = [r.to_dict() for r in self.reference_images]

        if self.deleted_hotspots:
            data['deletedHotspots'] = self.deleted_hotspotsa

        if self.handlers:
            data['handlers'] = {}
            for key in self.handlers:
                data['handlers'][key] = self.handlers[key].to_dict()

        return data

    @staticmethod
    def from_dict(data):
        """ Construct a Document object and fill it with the information from the dictionary"""
        document = Document(data['layer'])
        document.hotspots = [Hotspot.from_dict(h) for h in data['hotspots']]
        document.deleted_hotspots = data['deleted_hotspots'] if 'deleted_hotspots' in data else []
        document.reference_images = [ReferenceImage.from_dict(r) for r in data.get("referenceImages", [])]
        document.animations = Animations.from_dict(data.get("animations", {}))

        if 'handlers' in data:
            for key in data['handlers']:
                document.handlers[key] = EventHandler.from_dict(data['handlers'][key])

        return document

    def to_json(self, pretty=True):
        if pretty:
            return json.dumps(self.to_dict(), sort_keys=False, indent=4, separators=(',', ': '))
        else:
            return json.dumps(self.to_dict(), sort_keys=False)

    def to_file(self, filepath, pretty=True):
        jsonfile = open(filepath, 'w')
        jsonfile.write(self.to_json(pretty))
        jsonfile.close()

    @staticmethod
    def from_json(json_string):
        return Document.from_dict(json.loads(json_string))

    @staticmethod
    def from_file(filepath):
        jsonfile = open(filepath);
        document = Document.from_dict(json.load(jsonfile))
        jsonfile.close()
        return document


class Hotspot(object):
    """ Class representing a Layar Hotspot"""

    def __init__(self, id):
        self.id = id
        self.anchor = None
        self.object = None
        self.transform = Transform()
        self.actions = []
        self.animations = Animations()
        self.show_small_biw = None
        self.show_biw_onclick = None

    def to_dict(self):
        data = _ordered_dict()
        data['id'] = self.id

        if self.anchor:
            data['anchor'] = self.anchor.to_dict()

        if self.object:
            data['object'] = self.object.to_dict()

        if self.transform and self.transform.has_transformation():
            data['transform'] = self.transform.to_dict()

        if self.actions:
            data['actions'] = [a.to_dict() for a in self.actions]

        if self.animations.has_animations():
            data['animations'] = self.animations.to_dict()

        if self.show_small_biw is not None:
            data['showSmallBiw'] = self.show_small_biw

        if self.show_biw_onclick is not None:
            data['showBiwOnClick'] = self.show_biw_onclick

        return data

    @staticmethod
    def from_dict(data):
        hotspot = Hotspot(data['id'])
        hotspot.anchor = Anchor.from_dict(data['anchor']) if 'anchor' in data else None
        hotspot.object = Object.from_dict(data['object']) if 'object' in data else None
        hotspot.transform = Transform.from_dict(data['transform']) if 'transform' in data else None
        hotspot.actions = [Action.from_dict(a) for a in data.get('actions', [])]
        hotspot.show_small_biw = data.get('showSmallBiw')
        hotspot.show_biw_onclick = data.get('showBiwOnClick')
        hotspot.animations = Animations.from_dict(data.get("animations", {}))
        return hotspot

class Anchor(object):
    @staticmethod
    def from_dict(data):

        if 'referenceImage' in data:
            return AnchorReferenceImage.from_dict(data)

        if 'poi' in data:
            return AnchorPOI(data['poi'])

        if 'geolocation' in data:
            return AnchorUser() if data['geolocation'] == 'user' else AnchorGeolocation.from_dict(data)


class AnchorReferenceImage(object):
    """ Class representing a Hotspot anchor to a reference image """

    def __init__(self, reference_image):
        self.reference_image = reference_image

    def to_dict(self):
        data = _ordered_dict()
        data['referenceImage'] = self.reference_image
        return data

    @staticmethod
    def from_dict(data):
        return AnchorReferenceImage(data['referenceImage'])

class AnchorGeolocation(object):
    """ Class representing a Hotspot anchor to a geographic location """

    def __init__(self, lat, lon, alt=None):
        self.lat = lat
        self.lon = lon
        self.alt = alt

    def to_dict(self):
        data = _ordered_dict()
        data['geolocation'] = _ordered_dict()
        data['geolocation']['lat'] = self.lat
        data['geolocation']['lon'] = self.lon
        if self.alt:
            data['geolocation']['alt'] = self.alt

        return data

    @staticmethod
    def from_dict(data):
        return AnchorGeolocation(data['geolocation']['lat'], data['geolocation']['lon'], data['geolocation'].get('alt'))

class AnchorUser(object):
    """ Class representing a Hotspot anchor to the users location """

    def to_dict(self):
        data = _ordered_dict()
        data['geolocation'] = "user"
        return data

class AnchorPOI(object):
    """ Class representing a Hotspot anchor to another POI """

    def __init__(self, poi):
        self.poi = poi

    def to_dict(self):
        data = _ordered_dict()
        data['poi'] = self.poi
        return data

    @staticmethod
    def from_dict(data):
        return AnchorPOI(data['poi'])


class Object(object):
    """ Class representing an object for display"""

    def __init__(self, url, content_type=None, size=1):
        self.url = url
        self.content_type = content_type if content_type else _content_type(url)
        self.size = size
        self.preview_image = None
        self.loop_playback = None
        self.auto_playback = None
        self.show_loading_indicator = None
        self.show_playback_controls = None
        self.allow_fullscreen_playback = None
        self.fit_in_popout_mode = None
        self.pickable = None
        self.override_materials = []
        self.viewport = None
        self.event_handlers = {}

    def to_dict(self):
        data = _ordered_dict()
        data['contentType'] = self.content_type
        data['url'] = self.url
        data['size'] = self.size

        if self.preview_image is not None:
            data['previewImage'] = self.preview_image
        if self.loop_playback is not None:
            data['loopPlayback'] = self.loop_playback
        if self.auto_playback is not None:
            data['autoPlayback'] = self.auto_playback
        if self.show_loading_indicator is not None:
            data['showLoadingIndicator'] = self.show_loading_indicator
        if self.show_playback_controls is not None:
            data['showPlaybackControls'] = self.show_playback_controls
        if self.allow_fullscreen_playback is not None:
            data['allowFullscreenPlayback'] = self.allow_fullscreen_playback
        if self.fit_in_popout_mode is not None:
            data['fitInPopoutMode'] = self.fit_in_popout_mode
        if self.pickable is not None:
            data['pickable'] = self.pickable

        if self.override_materials:
            data['override'] = _ordered_dict()
            data['override']['materials'] = [m.to_dict() for m in self.override_materials]

        if self.viewport:
            data['viewport'] = self.viewport.to_dict()

        for event_type in self.event_handlers:
            if event_type in EventHandler.event_types:
                data[event_type] = self.event_handlers[event_type].to_dict()

        return data

    @staticmethod
    def from_dict(data):
        obj = Object(data['url'], data['contentType'], data['size'])
        obj.preview_image = data['previewImage'] if 'previewImage' in data else None
        obj.loop_playback = data['loopPlayback'] if 'loopPlayback' in data else None
        obj.auto_playback = data['autoPlayback'] if 'autoPlayback' in data else None
        obj.show_loading_indicator = data['showLoadingIndicator'] if 'showLoadingIndicator' in data else None
        obj.show_playback_controls = data['showPlaybackControls'] if 'showPlaybackControls' in data else None
        obj.allow_fullscreen_playback = data['allowFullscreenPlayback'] if 'allowFullscreenPlayback' in data else None
        obj.fit_in_popout_mode = data['fitInPopoutMode'] if 'fitInPopoutMode' in data else None
        obj.pickable = data['pickable'] if 'pickable' in data else None

        for event_type in EventHandler.event_types:
            if event_type in data:
                obj.event_handlers[event_type] = EventHandler.from_dict(data[event_type])

        obj.override_materials = [OverrideMaterial.from_dict(m) for m in data.get('override', {}).get('materials', [])]
        return obj

class Viewport(object):
    """ Class representing a HTML widget viewport"""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.interactive = True
        self.scrollable = False

    def to_dict(self):
        data = OrderedDict()
        data['width'] = self.width
        data['height'] = self.height
        data['interactive'] = self.interactive
        data['scrollable'] = self.scrollable

        return data

    @staticmethod
    def from_dict(data):
        viewport = Viewport(data['width'], data['height'])
        if 'interactive' in data:
            viewport.interactive = data['interactive']
        if 'scrollable' in data:
            viewport.scrollable = data['scrollable']

        return viewport;


class OverrideMaterial(object):
    """ Class representing a material override"""

    def __init__(self, material_id,
        texture=None,
        diffuse_color=None,
        ambient_color=None,
        specular_color=None,
        shininess=None,
        opacity=None,
        use_blending=None,
        use_lighting=None
        ):

        self.material_id = material_id
        self.texture = texture
        self.diffuse_color = diffuse_color
        self.ambient_color = ambient_color
        self.specular_color = specular_color
        self.shininess = shininess
        self.opacity = opacity
        self.use_blending = use_blending
        self.use_lighting = use_lighting

    def to_dict(self):
        data = _ordered_dict()
        data['materialId'] = self.material_id
        if self.texture is not None:
            data['texture'] = self.texture.to_dict()
        if self.diffuse_color is not None:
            data['diffuseColor'] = self.diffuse_color
        if self.ambient_color is not None:
            data['ambientColor'] = self.ambient_color
        if self.specular_color is not None:
            data['specularColor'] = self.specular_color
        if self.shininess is not None:
            data['shininess'] = self.shininess
        if self.opacity is not None:
            data['opacity'] = self.opacity
        if self.use_blending is not None:
            data['useBlending'] = self.use_blending
        if self.use_lighting is not None:
            data['useLighting'] = self.use_lighting

        return data

    @staticmethod
    def from_dict(data):
        material = OverrideMaterial(data['materialId'])
        material.texture = Texture.from_dict(data['texture']) if 'texture' in data else None
        material.diffuse_color = data.get('diffuseColor')
        material.ambient_color = data.get('ambientColor')
        material.specular_color = data.get('specularColor')
        material.shininess = data.get('shininess')
        material.opacity = data.get('opacity')
        material.use_blending = data.get('useBlending')
        material.use_lighting = data.get('useLighting')
        return material

class Texture(object):
    """ Class representing a texture"""

    def __init__(self, url, content_type=None, repeat_s=False, repeat_t=False,loop_playback=True):
        self.url = url
        self.content_type = content_type if content_type else _content_type(url)
        self.repeat_s = repeat_s
        self.repeat_t = repeat_t
        self.loop_playback = loop_playback
        self.event_handlers = {}

    def to_dict(self):
        data = _ordered_dict()
        data['contentType'] = self.content_type
        data['url'] = self.url
        if self.repeat_s:
            data['repeatS'] = self.repeat_s
        if self.repeat_t:
            data['repeatT'] = self.repeat_t
        if self.loop_playback is not None:
            data['loopPlayback'] = self.loop_playback
        for event_type in self.event_handlers:
            if event_type in EventHandler.event_types:
                data[event_type] = self.event_handlers[event_type].to_dict()
        return data

    @staticmethod
    def from_dict(data):
        texture = Texture(data['url'], data['contentType'])
        texture.repeat_s = data.get('repeatS', False)
        texture.repeat_t = data.get('repeatT', False)
        texture.loop_playback = data.get('loopPlayback')
        for event_type in EventHandler.event_types:
            if event_type in data:
                texture.event_handlers[event_type] = EventHandler.from_dict(data[event_type])

        return texture

class Transform(object):
    """ Class representing a tranformation"""

    def __init__(self):
        self.translate = Vector3f(0.0, 0.0, 0.0)
        self.rotate_angle = 0.0
        self.rotate_axis = Vector3f(0.0, 0.0, 1.0)
        self.scale = Vector3f(1.0, 1.0, 1.0)

    def has_transformation(self):
        return self.has_translation() or self.has_rotation() or self.has_scaling()

    def has_translation(self):
        return self.translate.x != 0.0 or self.translate.y != 0.0 or self.translate.z != 0.0

    def has_rotation(self):
        return self.rotate_angle != 0.0

    def has_scaling(self):
        return self.scale.x != 1.0 or self.scale.y != 1.0 or self.scale.z != 1.0

    def has_uniform_scale(self):
        return self.scale.x == self.scale.y and self.scale.y == self.scale.z

    def to_dict(self, force_non_uniform=False):
        data = _ordered_dict()

        if self.has_translation():
            data['translate'] = self.translate.to_dict()

        if self.has_rotation():
            data['rotate'] = _ordered_dict()
            data['rotate']['angle'] = self.rotate_angle
            data['rotate']['axis'] = self.rotate_axis.to_dict()

        if self.has_scaling():
            if not force_non_uniform and self.has_uniform_scale():
                data['scale'] = self.scale.x
            else:
                data['scale'] = self.scale.to_dict()

        return data

    @staticmethod
    def from_dict(data):
        transform = Transform()

        if 'translate' in data:
            transform.translate = Vector3f.from_dict(data['translate'])

        if 'rotate' in data:
            transform.rotate_angle = data['rotate']['angle']
            transform.rotate_axis.x = data['rotate']['axis']['x']
            transform.rotate_axis.y = data['rotate']['axis']['y']
            transform.rotate_axis.z = data['rotate']['axis']['z']

        if 'scale' in data:
            if isinstance(data['scale'], dict):
                transform.scale = Vector3f.from_dict(data['scale'])
            else:
                transform.scale.x = data['scale']
                transform.scale.y = data['scale']
                transform.scale.z = data['scale']

        return transform

class Action(object):
    """ Class representing an action """

    def __init__(self, uri, content_type="application/vnd.layar.internal", label=None):
        self.uri = uri
        self.content_type = content_type
        self.label = label

    def to_dict(self):
        data = _ordered_dict()
        data['contentType'] = self.content_type
        data['uri'] = self.uri
        if self.label:
            data['label'] = self.label

        return data

    @staticmethod
    def from_dict(data):
        return Action(data['uri'], data['contentType'], data.get('label', None))

    @staticmethod
    def layar_intent(layer, parameters):
        uri_params = []
        for key in parameters:
            uri_params.append(key + "=" + parameters[key])

        uri = "layar://{0}/?{1}".format(layer, "&".join(uri_params))
        return Action(uri)

class Update(object):
    """ Class representing an update for the current hotspots that can be used in an event handler """

    def __init__(self, hotspots = [], deleted_hotspots = []):
        self.hotspots = hotspots
        self.deleted_hotspots = deleted_hotspots

    def to_dict(self):
        data = _ordered_dict()
        if self.hotspots:
            data['hotspots'] = [h.to_dict() for h in self.hotspots]
        if self.deleted_hotspots:
            data['deletedHotspots'] = self.deleted_hotspots

        return data

    @staticmethod
    def from_dict(data):
        update = Update()
        update.hotspots = [Hotspot.from_dict(h) for h in data['hotspots']]
        update.deleted_hotspots = data['deleted_hotspots'] if 'deleted_hotspots' in data else []
        return update

class EventHandler(object):
    """ Class representing a event handler for a POI object """

    event_types = [ "onLoad", "onRender", "onClick", "onPlaybackStart", "onPlaybackFinish","onFocus","onDelete","onUpdate","onCreate" ]

    def __init__(self, handler = None, action = None, update = None):
        self.handler = handler
        self.action = action
        self.update = update

    def to_dict(self):
        data = _ordered_dict()
        if self.handler:
            data['handler'] = self.handler
        if self.action:
            data['action'] = self.action.to_dict()
        if self.update:
            data['update'] = self.update.to_dict()

        return data

    @staticmethod
    def from_dict(data):
        handler = EventHandler()
        handler.handler = data['handler'] if 'handler' in data else None
        handler.action = data['action'] if 'action' in data else None
        handler.update = data['update'] if 'update' in data else None
        return handler




class ReferenceImage(object):
    """ Class representing a reference image and its links to other images """

    def __init__(self, key, features_url = None, image_url = None):
        self.key = key
        self.features_url = features_url
        self.image_url = image_url
        self.links = []

    def to_dict(self):
        data = _ordered_dict()
        data['key'] = self.key

        if self.features_url is not None:
            data['featuresUrl'] = self.features_url
        if self.image_url is not None:
            data['imageUrl'] = self.image_url

        if self.links:
            data['links'] = [l.to_dict() for l in self.links]

        return data

    @staticmethod
    def from_dict(data):
        reference_image = ReferenceImage(data['key'], data.get('featuresUrl'), data.get('imageUrl'))
        reference_image.links = [ReferenceImageLink.from_dict(l) for l in data.get('links', [])]
        return reference_image


class ReferenceImageLink(object):
    """ Class representing a reference image link """

    def __init__(self, to, transform):
        self.to = to
        self.transform = transform

    def to_dict(self):
        data = _ordered_dict()
        data['to'] = self.to
        data['transform'] = self.transform.to_dict(force_non_uniform=False)
        return data

    @staticmethod
    def from_dict(data):
        return ReferenceImageLink(data['to'], Transform.from_dict(data['transform']))

class Animations(object):
    def __init__(self):
        self.onCreate = []
        self.onUpdate = []
        self.onDelete = []
        self.onFocus = []
        self.onClick = []

    def has_animations(self):
        return self.onCreate or self.onUpdate or self.onDelete or self.onFocus or self.onClick

    def to_dict(self):
        data = _ordered_dict()

        if self.onCreate:
            data['onCreate'] = [a.to_dict() for a in self.onCreate]
        if self.onUpdate:
            data['onUpdate'] = [a.to_dict() for a in self.onUpdate]
        if self.onDelete:
            data['onDelete'] = [a.to_dict() for a in self.onDelete]
        if self.onFocus:
            data['onFocus'] = [a.to_dict() for a in self.onFocus]
        if self.onClick:
            data['onClick'] = [a.to_dict() for a in self.onClick]

        return data

    @staticmethod
    def from_dict(data):
        animations = Animations()
        animations.onCreate = [Animation.from_dict(a) for a in data.get('onCreate', [])]
        animations.onUpdate = [Animation.from_dict(a) for a in data.get('onUpdate', [])]
        animations.onDelete = [Animation.from_dict(a) for a in data.get('onDelete', [])]
        animations.onFocus = [Animation.from_dict(a) for a in data.get('onFocus', [])]
        animations.onClick = [Animation.from_dict(a) for a in data.get('onClick', [])]
        return animations

class Animation(object):
    def __init__(self,
        type,
        length=None,
        delay=None,
        repeat=None,
        persist=None,
        from_value=None,
        to_value=None,
        axis_x=None,
        axis_y=None,
        axis_z=None,
        interpolation=None,
        interpolation_param=None):

        self.type = type
        self.length = length
        self.delay = delay
        self.repeat = repeat
        self.persist = persist
        self.from_value = from_value
        self.to_value = to_value
        self.axis = Vector3f(axis_x, axis_y, axis_z)
        self.interpolation = interpolation
        self.interpolation_param = interpolation_param

    def to_dict(self):
        data = _ordered_dict()
        data['type'] = self.type
        data['length'] = self.length

        if self.delay is not None:
            data['delay'] = self.delay
        if self.repeat is not None:
            data['repeat'] = self.repeat
        if self.persist is not None:
            data['persist'] = self.persist
        if self.from_value is not None:
            data['from'] = self.from_value
        if self.to_value is not None:
            data['to'] = self.to_value
        if self.axis and self.axis.x != None and self.axis.y != None and self.axis.z != None:
            data['axis'] = self.axis.to_dict()
        if self.interpolation is not None:
            data['interpolation'] = self.interpolation
        if self.interpolation_param is not None:
            data['interpolationParam'] = self.interpolation_param

        return data

    @staticmethod
    def from_dict(data):
        animation = Animation(data['type'])
        animation.length = data['length']
        animation.delay = data.get('delay')
        animation.repeat = data.get('repeat')
        animation.persist = data.get('persist')
        animation.from_value = data.get('from')
        animation.to_value = data.get('to')
        animation.axis = Vector3f.from_dict(data['axis']) if 'axis' in data else Vector3f()
        animation.interpolation = data.get('interpolation')
        animation.interpolation_param = data.get('interpolationParam')
        return animation

class Vector3f(object):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def to_dict(self):
        data = _ordered_dict()
        data['x'] = self.x
        data['y'] = self.y
        data['z'] = self.z

        return data

    @staticmethod
    def from_dict(data):
        return Vector3f(data.get('x', 0.0), data.get('y', 0.0), data.get('z', 0.0))

def _content_type(url):
    ul = url.lower()

    if ul.endswith(".l3d"):
        return "model/vnd.layar.l3d"

    if ul.endswith(".mp4"):
        return "video/mp4"

    if ul.endswith(".mp3"):
        return "audio/mp3"

    if ul.endswith(".jpg"):
        return "image/jpeg"

    if ul.endswith(".gif"):
        return "image/gif"

    return "image/png"

def _ordered_dict():
    try:
        return OrderedDict()
    except NameError:
        return {}