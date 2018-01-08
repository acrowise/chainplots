import blocksci
from blocksci import Tx
import time
import json
import argparse


def write_to_file(filename, in_memory_data):
    try:
        print("[+] Dumping json file")
        with open(filename, 'w') as f:
            json.dump(in_memory_data, f)
            f.close()
        print("[+] Saved json as: " + filename)
    except Exception as e:
        print("[-] Error when trying to save file: " + str(e))


def write_datasets(in_memory_data):
    try:
        print("[+] Building datasets for web server")
        filenames = ['plot1', 'plot2', 'plot3', 'plot4', 'plot5',
                     'plot6', 'plot7', 'plot8', 'plot9', 'plot10']

        for i, filename in enumerate(filenames):
            # pixel-based files
            path = "./chainplots/static/data/" + filename
            with open(path, 'w') as f:
                for line in in_memory_data.values():
                    if filename == 'plot10':
                        multi_value_line = ""
                        for value in line[i]:
                            multi_value_line += str(value) + " "
                        f.write(multi_value_line.strip(" ") + "\n")
                    else:
                        f.write(str(line[i]) + "\n")
            print("[+] Built dataset: " + filename)

    except Exception as e:
        print("[-] Error when trying to save datasets: " + str(e))


def main(verbose, output_group, first_block_heigh, in_memory_data):
    try:
        chain = blocksci.Blockchain(BTC_CONF_FILE)
        print("[+] Startup completed. Using: " + BTC_CONF_FILE)
        print("[i] Get help with -h option. Stop with ctrl + C")
    except Exception as e:
        print("[-] Startup Failed: " + str(e))

    print("[i] Skipping genesis block, (0 heigh).")
    if not verbose:
        print("[i] Quiet mode. If you want verbose, pass -v option.")
    else:
        print("[i] Verbose mode. Tweak the output with -g.")

    time.sleep(3)  # Let user read.
    prev_timestamp = 0
    now = time.time()
    blockchain_depth = len(chain)

    """ In memory entrys:
            block_heigh: (
                spent_coinb_vouts,
                tts_coinb_txos,
                coinb_addr,
                throughput,
                tx_count,
                timelocked_txos,
                multisign_txos,
                p2sh_txs,
                op_return_txos,
                app_op_return_txos,
            ) """

    """ In memory coinbase TXOs
    (
        block_heigh,
        txos_list,
    ) """

    # Main loop finding each parameter
    for i in range(first_block_heigh, blockchain_depth):

        # Get block
        block = chain[i]

        # Count TX in block
        tx_count = len(block)

        # Throughput estimation
        timestamp = block.timestamp
        elapsed_time = timestamp - prev_timestamp
        if elapsed_time <= 0:
            throughput = 0
        else:
            throughput = tx_count / elapsed_time * 60  # tx/min

        # Coinbase transaction: Number of addresses + Spent Ratio
        coinbase_outs = block.coinbase_tx.outs

        coinb_addr = len(coinbase_outs)
        spent_coinb_vouts = 0
        total_time_to_spend = 0
        for vout in coinbase_outs:
            if vout.is_spent:
                spent_coinb_vouts += 1
                spend_timestamp = Tx.tx_with_index(
                    vout.spending_tx_index).block.timestamp
                total_time_to_spend += spend_timestamp -\
                    timestamp

        # spending ratio
        spent_coinb_vouts = spent_coinb_vouts / coinb_addr
        # time to spend
        tts_coinb_txos = total_time_to_spend / coinb_addr

        # Looping transferences
        timelocked_txos = 0
        multisign_txos = 0
        p2sh_txs = 0
        op_return_txos = 0

        # (Ascribe, Stampery, Factom, Open Assets, Blockstack,
        # Colu, Omni Layer, Unknown, Counterparty)
        app_op_return_txos = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for tx in block:
            if tx.locktime != 0:
                timelocked_txos += 1
            if tx.outs[0].script_type == blocksci.address_type.nulldata:
                op_return_txos += 1
                app_label = blocksci.label_application(tx)
                if app_label == "Ascribe":
                    app_op_return_txos[0] += 1
                if app_label == "Stampery":
                    app_op_return_txos[1] += 1
                if app_label == "Factom":
                    app_op_return_txos[2] += 1
                if app_label == "Open Assets":
                    app_op_return_txos[3] += 1
                if app_label == "Blockstack":
                    app_op_return_txos[4] += 1
                if app_label == "Colu":
                    app_op_return_txos[5] += 1
                if app_label == "Omni Layer":
                    app_op_return_txos[6] += 1
                if app_label == "Unknown":
                    app_op_return_txos[7] += 1
                if app_label == "Counterparty":
                    app_op_return_txos[8] += 1
            for txo in tx.outs:
                if txo.script_type == blocksci.address_type.multisig:
                    multisign_txos += 1
                if txo.script_type == blocksci.address_type.scripthash:
                    p2sh_txs += 1

        # Output to terminal
        if i % output_group == 0 and verbose:
            print("[+] Block: {}/{}[{:.1f}%]".format(
                i,
                blockchain_depth,
                i / blockchain_depth * 100
            ))

        prev_timestamp = timestamp

        # Appending in-memory
        in_memory_data[i] = (
            spent_coinb_vouts,
            tts_coinb_txos,
            coinb_addr,
            throughput,
            tx_count,
            timelocked_txos,
            multisign_txos,
            p2sh_txs,
            op_return_txos,
            app_op_return_txos,
        )

    print("[i] Elapsed time: " + str(time.time() - now))


if __name__ == '__main__':

    # Argument parser setup
    desc = "Blockchain analysis tool. Dataset builder."
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-v", "--verbose", action="store_true")
    sh = "Starting block. Heigh of the first analyzed block. 1 or more."
    parser.add_argument("-s", "--start", type=int, help=sh, default=1)
    gh = "Output grouped by GROUPING elements."
    parser.add_argument("-g", "--grouping", type=int, help=gh, default=1)
    jh = "Output JSON filename. Will be saved in the script directory."
    parser.add_argument("-j", "--jsonfile", help=jh)
    ch = "Blockchain directory."
    parser.add_argument("-c", "--conffile", help=ch)
    dh = "Generate the web static data"
    parser.add_argument("-d", "--dataset", help=dh, action="store_true")
    args = parser.parse_args()

    try:
        if args.conffile:
            BTC_CONF_FILE = args.conffile
        else:
            BTC_CONF_FILE = "/home/ubuntu/bitcoin-data/"

        # Running the main script
        in_memory_data = {}

        main(args.verbose, args.grouping, args.start, in_memory_data)

    except KeyboardInterrupt:
        print("[-] Keyboard Exit!")
    except Exception as e:
        print("[!] We had a problem: " + str(e))
    finally:
        # Web datasets
        if args.dataset:
            write_datasets(in_memory_data)
        else:
            print("[-] Not building datasets. If you want it, pass -d option")

        # Json dump
        if args.jsonfile is None:
            print("[-] Not saving json. If you want it, pass a -j FILENAME")
        else:
            write_to_file(args.jsonfile, in_memory_data)

        print("[i] Script ended")
