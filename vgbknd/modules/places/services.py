import math

class PlaceService:
    def __init__(self, _lat, _lon):
        self.lat = _lat
        self.lon = _lon

    def distance(self, lat1, lon1, lat2, lon2):
        R = 6373.0
        print('entre')
        print('lat1: ', lat1)
        #lat1 = math.radians(la1)
        #lon1 = math.radians(lo1)
        #lat2 = math.radians(la2)
        #lon2 = math.radians(lo2)

        


        dlon = lon2 - lon1
        dlat = lat2 - lat1

        print('dlon: ', dlon)

        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distancia = R * c #esta distancia te la da en Kms
        print('distancia: ', distancia)
        return distancia

    def tpnearbylist(self, tplist):
        list = []
 
        for tp in tplist:
            print ('tp latitude: ', tp.latitude)
            d = self.distance(self.lat, self.lon, tp.latitude, tp.longitude)
            print('distancia: ', d)
            if d < 3:
                list.append(object)

        return list

