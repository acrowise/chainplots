# Generate files with _1000 suffix. This files are used with line graphs.
# Output values are 1000 input average.


def write_thousands(read_file, write_file):
    value_sum = 0
    for i, line in enumerate(read_file.readlines()):
        value_sum += float(line)
        if i % 1000 == 0:
            average = value_sum / 1000.0
            write_file.write(str(average) + "\n")
            value_sum = 0.00


def write_multi_thousands(read_file, write_file):
    # (Ascribe, Stampery, Factom, Open Assets, Blockstack,
    # Colu, Omni Layer, Unknown, Counterparty)
    app_value_sum = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i, line in enumerate(read_file.readlines()):
        app_string_values = line.split(" ")
        for j, s in enumerate(app_string_values):
            if s != "" and s != "\n":
                app_value_sum[j - 1] += int(s)
        if i % 1000 == 0:
            multi_value_line = ""
            for v in app_value_sum:
                multi_value_line += str(v) + " "
            write_file.write(multi_value_line.strip(" ") + "\n")
            app_value_sum = [0, 0, 0, 0, 0, 0, 0, 0, 0]


def main():
    filenames = ['plot1', 'plot2', 'plot3', 'plot4', 'plot5',
                 'plot6', 'plot7', 'plot8', 'plot9', 'plot10']

    for filename in filenames:
        path_r = "./chainplots/static/data/" + filename
        path_w = path_r + "_1000"
        try:
            with open(path_r, 'r') as r:
                with open(path_w, 'w') as w:
                    if filename == 'plot10':
                        write_multi_thousands(r, w)
                    else:
                        write_thousands(r, w)
        except KeyboardInterrupt as e:
            print("[-] Problem with {}. Exception: {}".format(
                filename,
                str(e),
            ))


if __name__ == '__main__':
    main()
