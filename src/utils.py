class Utils:
    def __init__(self):
        pass

    def calculate_volume(self, defect):
        # assume all values in m
        l, w, d = map(float, defect['properties']['dim'].split('x'))
        return l * w * d

    def calculate_area(self, defect):
        # assume all values in m
        l, w, d = map(float, defect['properties']['dim'].split('x'))
        return l * w

    def calculate_qty_reqd(self, volume):
        # assume return value in kg
        # assume density = 2288 kg/m3 (usually 2200 - 2400)
        density = 2400
        return volume * density
    
    def calculate_eta(self, defect):
        # repairing a pothole involves 
        vol = self.calculate_volume(defect)
        area = self.calculate_area(defect)

        # qty_reqd
        qty_reqd = self.calculate_qty_reqd(vol)

        setup_time = 0
        if defect['properties']['defect'] == 'crack':
            setup_time = 120 # 2 min
        elif defect['properties']['defect'] == 'pothole':
            setup_time = 300 # 5 min
        elif defect['properties']['defect'] == 'dent':
            setup_time = 600 # 10 min
        else:
            print('invalid defect type:')
            pass

        # assume vol*5*60 + area*2*300
        # all time values in s
        service_time = (vol * 300) + (area * 600)
        
        return vol, area, qty_reqd, setup_time, service_time
