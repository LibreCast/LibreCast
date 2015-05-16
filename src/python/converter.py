import math


class Converter():
    def ConvertSize(self, size):
        size_name = ('Octets', 'Kio', 'Mio', 'Gio', 'Tio', 'Pio', 'Eio', 'Zio', 'Yio')
        try:
            i = int(math.floor(math.log(size, 1024)))
            p = math.pow(1024, i)
            s = round(size/p, 2)
            if (s > 0):
                return '%.1f %s' % (s, size_name[i])
            else:
                return '0 octets'
        except:
            return '0 octets'

    def ConvertTime(self, seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)

        if h > 1:
            if m > 1:
                return '%d heures et %02d minutes restantes' % (h, m)
            else:
                return '%d heures restantes' % (h)
        elif h > 0:
            if m > 1:
                return '%d heure et %02d minutes restante' % (h, m)
            else:
                return '%d heure restante' % (h)
        elif m > 1:
                return '%d minutes restantes' % (m)
        elif m > 0:
            return '%d minute restante' % (m)
        elif s > 1:
            return '%d secondes restantes' % s
        elif m > 1:
            return '%d secondes restante' % s
        else:
            return '0 seconde restante'
