class Utils:
    def __init__(self):
        pass

    def calculate_volume(self, defect):
        # assume all values in m
        l, b, h = map(float, defect['properties']['dim'].split('x'))
        return l * b * h

    def calculate_area(self, defect):
        # assume all values in m
        l, b, h = map(float, defect['properties']['dim'].split('x'))
        return l * b

    def calculate_qty_reqd(self, volume):
        # assume return value in kg
        # assume density = 2400 kg/m3 (usually 2200 - 2400)
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
            setup_time = 300
        elif defect['properties']['defect'] == 'pothole':
            setup_time = 600
        elif defect['properties']['defect'] == 'dent':
            setup_time = 1200
        else:
            # TODO add logger
            # logger.INFO('invalid defect type:', defect['properties']['defect'])
            pass
        
        # TODO validate the constants with realistic information
        # something like a benchmark

        # assume vol*5*60 + area*2*60
        # all time values in s
        service_time = (vol * 300) + (area * 120)
        
        return vol, area, qty_reqd, setup_time, service_time
    
    def divide_jobs():
        pass
