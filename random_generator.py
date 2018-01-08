import random


def write_datasets(in_memory_data):
    try:
        print("[+] Building datasets for web server")
        filenames = ['plot1', 'plot2', 'plot3', 'plot4', 'plot5',
                     'plot6', 'plot7', 'plot8', 'plot9', 'plot10']

        for i, filename in enumerate(filenames):
            path = "./chainplots/static/data/" + filename
            with open(path, 'w') as f:
                for line in in_memory_data.values():
                    f.write(str(line[i]) + "\n")
            print("[+] Built dataset: " + filename)
    except Exception as e:
        print("[-] Error when trying to save datasets: " + str(e))


def main():
    in_memory_data = {}
    for i in range(0, 500000):
        my_tuple = (
            random.random(),
            random.random(),
            random.random(),
            random.random(),
            random.random(),
            random.random(),
            random.random(),
            random.random(),
            random.random(),
            random.random(),
        )
        in_memory_data[i] = my_tuple
    write_datasets(in_memory_data)


if __name__ == '__main__':
    main()
