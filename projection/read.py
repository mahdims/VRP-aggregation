import numpy as np
import pandas as pd


def convert_the_coordinates(x, y, x_origin, y_origin):
    longitude_conversion_coe = 65.0673235 	#KM
    latitude_conversion_coe = 111.206094  #KM
    C_coord = [int(100*(x-x_origin)*longitude_conversion_coe), int(100*(y-y_origin)*latitude_conversion_coe)]
    return C_coord


def XY_range(customers):
    max_x = customers[1].coord[0]
    min_x = customers[1].coord[0]
    max_y = customers[1].coord[1]
    min_y = customers[1].coord[1]
    for cus in customers.values():
        if cus.coord[0] < min_x:
            min_x = cus.coord[0]
        elif cus.coord[0] > max_x:
            max_x = cus.coord[0]

        if cus.coord[1] < min_y:
            min_y = cus.coord[1]
        elif cus.coord[0] > max_y:
            max_y = cus.coord[1]

    return (min_x, max_x), (min_y, max_y)


class Customer:
    def __init__(self, ID, coord, d, TW=[0,0], ST=0):
        self.ID = ID
        self.coord = coord
        self.demand = d
        self.TW = TW
        self.service_time = ST


def read_the_data(Path_2_file, path_2_dis_mat = None):
    np.random.seed(0)
    f = open(Path_2_file, "r")
    lines = list(f)
    N = int(lines[3].split(":")[1])
    Cap = int(lines[5].split(":")[1])
    f.close()
    clean_data = {}
    customers_coord = lines[7: 7+N]
    customers_demand = lines[8+N:8+2*N]
    depot = lines[9 + 2*N : 11 +2*N]
    customers = {}
    for line_inx, cust in enumerate(customers_coord):

        Id, x, y = [int(a) for a in cust.split("\t")]
        demand = int(customers_demand[line_inx].split("\t")[1])
        customers[Id] = Customer(Id, (x,y), demand)

    x_range, y_range = XY_range(customers)
    # read the distance matrix file
    if path_2_dis_mat:
        file = open(path_2_dis_mat)
        lines = list(file)
        file.close()
        Full_dis = {}
        Full_consump = {}
        for line_inx in range(0, len(lines), 6):
            arc = tuple(lines[line_inx + 1].replace("\n", "").split(" "))
            Full_dis[arc] = int(lines[line_inx + 3].replace("\n", "").split("\t")[3]) / 1000
            Full_consump[arc] = int(lines[line_inx + 5].replace("\n", "").split("\t")[3]) / 1000

        clean_data["Full_dis"] = Full_dis
        clean_data["Full_consump"] = Full_consump

    clean_data["depot"] = depot
    clean_data["Customers"] = customers
    clean_data["N_C"] = N
    clean_data["Clusters"] = {}
    clean_data["C"] = Cap
    clean_data["Axu_depot"] = N + 1
    clean_data["X_range"] = x_range
    clean_data["Y_range"] = y_range

    return clean_data




