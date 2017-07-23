"""
Node/Customer
"""
class node():
    def __init__(self, m_id, name, time_window):
        self.matrix_id = m_id
        self.name = name
        self.time_window = time_window
        self.waiting_time = 0

    def set_waiting_time(time):
        self.waiting_time = time

    def set_time_to_prev(time):
        self.time_to_prev = time

    def __repr__(self):
        return str(self.matrix_id) + ": " + self.name + " " + str(self.time_window) + " | " + str(self.waiting_time)

"""
Simple TimeWindow impl.
"""
class time_window():
    def __init__(self, begin_hour, end_hour):
        self.begin = begin_hour * 60 * 60
        self.end = end_hour * 60 * 60

    def __repr__(self):
        return "[" + str((self.begin / 60) / 60) + " : " + str((self.end / 60) / 60) + "]"

"""
Route definition
"""
class route():
    def __init__(self, stops, ident, depot, time_matrix):
        self.r_id = ident
        self.depot = depot
        self.time_matrix = time_matrix
        self.stops = []
        for item in stops:
            self.stops.append(item)

        if len(self.stops) > 0:
            self.start = self.stops[0].matrix_id
            self.end = self.stops[len(self.stops) - 1].matrix_id
        else:
            print("ERROR")

    def __repr__(self):
        return 'id: ' + str(self.r_id) + '\n' + '\n'.join([str(item) for item in self.stops]) + '\n'

    """
    Merge Routestops
    """
    def add_stops(self, route):
        for item in route.stops:
            self.stops.append(item)

        self.end = self.stops[len(self.stops) - 1].matrix_id

"""
dist_matrix in km
time_matrix in sec
"""
class cost_matrix():
    def __init__(self, dis_matrix, time_matrix, size):
        self.matrix = [0 for x in range(size)]
        for i in range(size):
            self.matrix[i] = [0 for x in range(size)]
            for j in range(size):
                dis = dis_matrix[i][j] * 1000
                time = time_matrix[i][j]

                if time == 0:
                    self.matrix[i][j] = 0
                else:
                    self.matrix[i][j] = round(dis * (dis / time), 2)

    def __repr__(self):
        return '\n'.join([''.join(['{:10}'.format(item) for item in row]) for row in self.matrix])

"""
Saving Object
Store of routes with saving-value if linked together
"""
class saving():
    def __init__(self, route_a, route_b, cost_matrix):
        self.r_a = route_a
        self.r_b = route_b

        return self.calc(cost_matrix)

    """
    Calculation of the saving-value if linked as one route
    """
    def calc(self, cost_matrix):
        cost = cost_matrix.matrix

        if self.check_time_windows() is -1:
            return -1

        self.saving = round(cost[self.r_a.end][0] + cost[0][self.r_b.start] - cost[self.r_a.end][self.r_b.start] - self.r_b.stops[0].waiting_time, 2)

    """
    TimeWindow check
    Return -1 if TimeWindow is not reachable in time
    """
    def check_time_windows(self):
        time_matrix = self.r_a.time_matrix
        time = self.r_a.depot.time_window.begin
        prev_stop = self.r_a.depot

        for stop in self.r_a.stops:
            tmp_time = time + time_matrix[prev_stop.matrix_id][stop.matrix_id]
            if tmp_time < stop.time_window.end:
                waiting_time = stop.time_window.begin - tmp_time
                waiting_time = 0 if waiting_time < 0 else waiting_time

                stop.waiting_time = waiting_time

                time = tmp_time + waiting_time + 900
            else:
                return -1

        for stop in self.r_b.stops:
            tmp_time = time + time_matrix[prev_stop.matrix_id][stop.matrix_id]
            if tmp_time < stop.time_window.end:
                waiting_time = stop.time_window.begin - tmp_time
                waiting_time = 0 if waiting_time < 0 else waiting_time

                stop.waiting_time = waiting_time

                time = tmp_time + waiting_time + 900
            else:
                return -1
