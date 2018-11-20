import simplejson as json
import requests
from pprint import pprint
from colr import color
#from colorama import Fore, Back, Style

class Room():

    def __init__(self,json):
        self.room_code = str(json['raum_code'])
        self.status = str(json['status'])

        if self.status.lower() in 'belegt':
            self.status = 'Occupied'
            self.taken_till = int(json['belegung_fuer']/60)
        if self.status.lower() in 'frei':
            self.status = 'Free'
            self.taken_till = 0

        self.name = str(json['raum_name'])

    def get_color(self):
        if self.status is 'Free':
            return '#44AC42'
        else:
            return 'red'
    def get_status(self):
        status = color(self.status,back=self.get_color(),fore='#ffffff',style='bright')
        #print(status)
        return status

class RoomInfo():

    def __init__(self):
            self.__api_endpoint = 'https://www.devapp.it.tum.de/iris/ris_api.php?format=json'


    def get_room_info(self, where=None):
        res = json.loads(requests.get(self.__api_endpoint).text)
        bmi_ids = res['gruppen'][0]['raeume']
        mi_ids = res['gruppen'][1]['raeume']
        hbrk_ids = res['gruppen'][2]['raeume']
        if 'BIBMI' in where.upper():
            rooms = self.__get_rooms(res['raeume'], bmi_ids)
        elif 'MI' in where.upper():
            rooms = self.__get_rooms(res['raeume'], mi_ids)
        elif 'HBRK' in where.upper():
            rooms = self.__get_rooms(res['raeume'], hbrk_ids)
        else:
            room_ids = bmi_ids + mi_ids + hbrk_ids
            rooms = self.__get_rooms(res['raeume'], room_ids)
        #print(rooms)
        #self.__show_info(rooms)
        return rooms

    def __get_rooms(self, room_json,room_ids):
        rooms = []
        for r in room_json:
            if r['raum_nr'] in room_ids:
                rooms += [Room(r)]
        return rooms

    def __show_info(self, rooms):
        from texttable import Texttable
        #from colr import color

        rows=[]
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_cols_dtype( ['t', 't', 't','t','i'])
        table.set_cols_align( ['r', 'l', 'l','c','c'])
        table.set_cols_width([2,len('01.03.043B'),len('Gruppenarbeitsraum '),len('\x1b[48;5;71m\x1b[38;5;231mOccupied\x1b[0m'),len('free in (min)')])
        #table.set_cols_width([2,len('01.03.043B'),len('Gruppenarbeitsraum '),len('Occupied'),len('free in (min)')])
        rows.append(['#', 'Room Nr.','Room Type','\x1b[48;5;71m\x1b[38;5;231mStatus\x1b[0m','Free in (min)'])
        for idx,r in enumerate(rooms):
          #status = r.status#color(r.status,fore='#fff',back=r.get_color(),style='bright')
          row =  [str(idx+1),r.room_code,r.name, r.get_status(), r.taken_till]
          #print(row)
          rows += [row]
        table.add_rows(rows)
        print(table.draw())
        return



room_info = RoomInfo()
room_info.get_room_info(where='bibmi')
    