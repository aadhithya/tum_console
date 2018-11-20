import argparse
from room_info import RoomInfo,Room
from texttable import Texttable
from colr import color
import sys
from __init__ import __package_name__,__description__,__version__



def show_room_info(rooms):

        rows=[]
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_cols_dtype( ['t', 't', 't','t','i'])
        table.set_cols_align( ['r', 'l', 'l','c','c'])
        table.set_cols_width([2,len('01.03.043B'),len('Gruppenarbeitsraum '),len('\x1b[48;5;71m\x1b[38;5;231mOccupied\x1b[0m'),len('free in (min)')])
        rows.append(['#', 'Room Nr.','Room Type','\x1b[48;5;71m\x1b[38;5;231mStatus\x1b[0m','Free in (min)'])
        for idx,r in enumerate(rooms):
          row =  [str(idx+1),r.room_code,r.name, r.get_status(), r.taken_till]
          rows += [row]
        table.add_rows(rows)
        print(table.draw())
        return

def main(args=None):

    parser = argparse.ArgumentParser()
    parser.add_argument('--room-info','-ri',help='Room Info. Tells you which rooms are free. Args: [bibMI, MI, Hbrk]')
    parser.add_argument('--version','-v',help='Version Info.', action='store_true')
    parser.add_argument('--mensa-menu','-mm',help='Returns today\'s Menu at given Mensa.', nargs='+')

    args = parser.parse_args()

    print(args)

    if args.room_info:
        print('room info')
        ri = RoomInfo()
        rooms = ri.get_room_info(where=args.room_info)
        show_room_info(rooms)
    elif args.mensa_menu:
        print('Mensa Menu. Still cooking... ;)')
    elif args.version:
        print(__package_name__+'\n'+__description__+'\n'+'Version: '+__version__)
        sys.exit()
        

if __name__ == "__main__":
    main()