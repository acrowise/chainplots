import bitcoin.rpc
import time
import json
import argparse
from datetime import datetime


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
                    f.write(str(line[i]) + "\n")
            print("[+] Built dataset: " + filename)

            # thousand grouped graphics
            filename_1000 = filename + "_1000"
            path_1000 = "./chainplots/static/data/" + filename_1000
            with open(path_1000, 'w') as f:
                sum_value = 0.00
                counter_value = 0
                for line in in_memory_data.values():
                    counter_value += 1
                    sum_value += line[i]
                    if i % 1000 == 0:
                        average_value = sum_value / counter_value
                        f.write(str(average_value) + "\n")
            print("[+] Built dataset: " + filename_1000)

    except Exception as e:
        print("[-] Error when trying to save datasets: " + str(e))


def main(verbose, output_group, first_block_heigh, in_memory_data):
    try:
        proxy = bitcoin.rpc.RawProxy(btc_conf_file=BTC_CONF_FILE)
        print("[+] Startup completed. Using: " + BTC_CONF_FILE)
        print("[i] Get help with -h option. Stop with ctrl + C")
    except Exception as e:
        print("[-] Startup Failed: " + str(e))

    print("[i] Skipping genesis block, (0 heigh)")
    if not verbose:
        print("[i] Quiet mode. If you want verbose, pass -v option")
    else:
        print("[i] Verbose mode. Ready for the stream?")

    time.sleep(3)  # Let user read.
    prev_timestamp = 0
    now = time.time()
    blockchain_depth = proxy.getblockcount()

    """ In memory entrys:
            block_heigh: (
                spent_coinb_vouts,
                tts_coinb_txos,
                coinb_addr,
                throughput,
                tx_count,
                timelocked_txos,
                multisign_txos,
                segwit_txs,
                op_return_txos,
                app_op_return_txos,
            ) """

    """ In memory coinbase TXOs
    (
        block_heigh,
        txos_list,
    ) """
    in_memory_coinbase_txs = []

    # Main loop finding each parameter
    for i in range(first_block_heigh, blockchain_depth + 1):

        # Flags
        spent_a_coinbase_flag = False

        # Get block
        while 1:  # Retry if conection fails!
            try:
                block_hash = proxy.getblockhash(i)
                block = proxy.getblock(block_hash)
            except Exception as e:
                print("[-] Retrying. Proxy error: " + str(e))
                del proxy
                proxy = bitcoin.rpc.RawProxy(btc_conf_file=BTC_CONF_FILE)
                time.sleep(5)
                continue
            break

        # Count TX in block
        tx_set = block['tx']
        tx_count = len(tx_set)

        # Throughput estimation
        timestamp = block['time']
        elapsed_time = timestamp - prev_timestamp
        if elapsed_time <= 0:
            throughput = 0
        else:
            throughput = tx_count / elapsed_time * 60  # tx/min

        # Coinbase transaction: Number of addresses + Spent Ratio
        while 1:  # Retry if conection fails!
            try:
                coinbase_tx = proxy.getrawtransaction(tx_set[0], 1)
            except Exception as e:
                print("[-] Retrying. Proxy error: " + str(e))
                del proxy
                proxy = bitcoin.rpc.RawProxy(btc_conf_file=BTC_CONF_FILE)
                time.sleep(5)
                continue
            break
        # Saving in_memory coinbase list
        in_memory_coinbase_txs.append((i, tx_set[0]))
        coinb_addr = 0
        spent_coinb_vouts = 0
        real_vout_count = len(coinbase_tx['vout'])
        try:
            for index, output in enumerate(coinbase_tx['vout']):
                # counting
                if "scriptPubKey" in output.keys() and\
                        "addresses" in output['scriptPubKey'].keys():
                    coinb_addr += len(output['scriptPubKey']['addresses'])
                # spending ratio
                while 1:  # Retry if conection fails!
                    try:
                        utxo = proxy.gettxout(coinbase_tx['txid'], index, False)
                    except Exception as e:
                        print("[-] Retrying. Proxy error: " + str(e))
                        del proxy
                        proxy = bitcoin.rpc.RawProxy(btc_conf_file=BTC_CONF_FILE)
                        time.sleep(5)
                        continue
                    break
                vout = coinbase_tx['vout'][index]
                if utxo is not None:
                    spent_coinb_vouts += 1
                if "OP_RETURN" in vout['scriptPubKey']['asm']:
                    real_vout_count -= 1
            spent_coinb_vouts = 1 - spent_coinb_vouts / real_vout_count
        except Exception:
            coinb_addr = -1
            spent_coinb_vouts = -1

        # TX analysis in the block
        known_scripts = {
            'pubkey': 0,
            'pubkeyhash': 0,
            'scripthash': 0,
            'multisig': 0,
            'nulldata': 0,  # OP_RETURN excluded
            'witness_v0_scripthash': 0,
            'witness_v0_keyhash': 0,
            'OP_RETURN': 0,
            'timelocked': 0,
        }

        for txid in tx_set:
            while 1:  # Retry if conection fails!
                try:
                    tx = proxy.getrawtransaction(txid, 1)
                except Exception as e:
                    print("[-] Retrying. Proxy error: " + str(e))
                    del proxy
                    proxy = bitcoin.rpc.RawProxy(btc_conf_file=BTC_CONF_FILE)
                    time.sleep(5)
                    continue
                break

            # Look for coinbase spending in the whole block
            for vin in tx['vin']:
                for coindx, coinb_h_txid in enumerate(in_memory_coinbase_txs):
                    coinb_h = coinb_h_txid[0]
                    coinb_txid = coinb_h_txid[1]
                    if 'txid' in vin.keys() and vin['txid'] == coinb_txid:
                        while 1:  # Retry if conection fails!
                            try:
                                found_bh = proxy.getblockhash(coinb_h)
                                found_b = proxy.getblock(found_bh)
                            except Exception as e:
                                print("[-] Retrying. Proxy error: " + str(e))
                                del proxy
                                proxy = bitcoin.rpc.RawProxy(btc_conf_file=BTC_CONF_FILE)
                                time.sleep(5)
                                continue
                            break

                        tts_coinb_txos = block['time'] - found_b['time']
                        # modify a tuple
                        mod_tuple = list(in_memory_data[coinb_h])
                        mod_tuple[1] = tts_coinb_txos
                        in_memory_data[coinb_h] = tuple(mod_tuple)
                        # remove from list
                        del in_memory_coinbase_txs[coindx]
                        spent_a_coinbase_flag = True

            # Looking for timelocked TXOs.
            for vout in tx['vout']:
                vout_type = vout['scriptPubKey']['type']
                vout_asm = vout['scriptPubKey']['asm']
                if vout_type not in known_scripts.keys():
                    print(vout)
                elif vout_type == "nulldata" and\
                        'OP_RETURN' in vout_asm:
                    known_scripts['OP_RETURN'] += 1
                    # print(vout_asm)
                    # print(bytearray.fromhex(vout_asm.split()[1]).decode('ascii'))
                elif 'OP_CHECKLOCKTIMEVERIFY' in vout_asm or\
                        'OP_CHECKSEQUENCEVERIFY' in vout_asm:
                    known_scripts['timelocked'] += 1
                    # print(vout)
                else:
                    # +1 in the counter for the specific script
                    known_scripts[vout_type] += 1
        timelocked_txos = known_scripts['timelocked']
        multisign_txos = known_scripts['multisig']
        segwit_txs = known_scripts['witness_v0_scripthash']
        op_return_txos = known_scripts['OP_RETURN']
        app_op_return_txos = 0

        # Output to terminal
        if i % output_group == 0 and verbose:
            print("[+] Block: {}/{}[{:.1f}%] | TXs: {:>5} | {} "
                  "| {:>7.1f} tx/min | Coinb Addrs: {:>3} "
                  "| Conb Sp: {:>5.1f}% | TX from coinb: {} | "
                  "{} timelocked | {} multisig | {} segwit | "
                  "{} OP_RETURN".format(
                      i,
                      blockchain_depth,
                      i / blockchain_depth * 100,
                      tx_count,
                      str(datetime.utcfromtimestamp(timestamp)),
                      throughput,
                      coinb_addr,
                      spent_coinb_vouts * 100,
                      "yes" if spent_a_coinbase_flag else "no ",
                      timelocked_txos,
                      multisign_txos,
                      segwit_txs,
                      op_return_txos,
                  ))

        prev_timestamp = timestamp

        # Appending in-memory
        in_memory_data[i] = (
            spent_coinb_vouts,
            0,  # tts_coinb_txos initialized. Filled later.
            coinb_addr,
            throughput,
            tx_count,
            timelocked_txos,
            multisign_txos,
            segwit_txs,
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
    ch = "Bitcoind configuration file."
    parser.add_argument("-c", "--conffile", help=ch)
    dh = "Generate the web static data"
    parser.add_argument("-d", "--dataset", help=dh, action="store_true")
    args = parser.parse_args()

    try:
        if args.conffile:
            BTC_CONF_FILE = args.conffile
        else:
            BTC_CONF_FILE = "/media/fede/CLONE/BLOCKCHAIN/bitcoin.conf"

        # Running the main script
        in_memory_data = {}

        main(args.verbose, args.grouping, args.start, in_memory_data)

    except KeyboardInterrupt:
        print("[-] Keyboard Exit!")
    # except Exception as e:
    #     print("[-] Something wrong... " + str(e))
    except bitcoin.rpc.InWarmupError as e:
        print("[-] Please wait. Bitcoind is warming up: " + str(e))
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
