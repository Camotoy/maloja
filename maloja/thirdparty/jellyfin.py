from . import MetadataInterface, InvalidResponse
import urllib.parse
import requests


class Jellyfin(MetadataInterface):
    name = "Jellyfin"
    identifier = "jellyfin"

    settings = {
        "url":"JELLYFIN_URL",
        "apiid":"JELLYFIN_API_KEY"
    }

    metadata = {
        "trackurl": "{url}/Items?IncludeItemTypes=Audio&Recursive=true&artists={artist}&searchTerm={title}",
        "albumurl": "{url}/Items?IncludeItemTypes=MusicAlbum&Recursive=true&artists={artist}&searchTerm={title}",
        "artisturl": "{url}/Items?IncludeItemTypes=MusicArtist&Recursive=true&searchTerm={artist}",
        "required_settings": ["url", "apiid"],
        "enabled_entity_types": ["artist", "album", "track"]
    }

    def get_image_track(self,track):
        artists, title = track
        return self.grab_image("albumurl", album="|".join(artists), title=title)

    def get_image_artist(self,artist):
        return self.grab_image("artisturl", artist=artist)

    def get_image_album(self,album):
        artists, title = album
        return self.grab_image("albumurl", artist="|".join(artists or []), title=title)

    def grab_image(self,type,**kwargs):
        params = {}
        for key, value in kwargs.items():
            params[key] = urllib.parse.quote(value)
        response = requests.get(
            self.metadata[type].format(url=self.settings["url"], **params),
            headers={
                "User-Agent": self.useragent,
                "X-MediaBrowser-Token": self.settings["apiid"]
            }
        )

        json = response.json()
        try:
            items = json.get("Items")
            if items:
                entry = items[0] if len(items) > 0 else None
                if entry and "ImageTags" in entry and "Primary" in entry["ImageTags"]:
                    return "{url}/Items/{id}/Images/Primary".format(url=self.settings["url"], id=entry["Id"])
        except Exception:
            raise InvalidResponse()
        return None