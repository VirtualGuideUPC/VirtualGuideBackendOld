import math

class PlaceService:

    def distance(self, lat1, lon1, lat2, lon2):
        R = 6373.0

        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distancia = R * c #esta distancia te la da en Kms

        return distancia

    def tpnearbylist(self, lat, lon, tplist):
        d = 0
        list = []

        for object in tplist:
            d = self.distance(lat, lon, object.latitude, object.longitude)
            if d < 3:
                list.append(object)

        return list
