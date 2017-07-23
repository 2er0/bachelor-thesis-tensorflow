class util():

    def sort_savings(savings):
        return sorted(savings, key=lambda item: item.saving, reverse=True)

    def print_savings(savings):
        print("SavingsCount: " + str(len(savings)) + '\n' + '\n'.join([str(item.saving) + ' \n\t r_a: ' + ', '.join([str(stop.matrix_id) for stop in item.r_a.stops]) + ' \n\t r_b: ' + ', '.join([str(stop.matrix_id) for stop in item.r_b.stops]) for item in savings]))
