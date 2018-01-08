from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def landing(request):
    context = {
        'plot': 'landing',
        'line_param': 'none',
        'range_max': 1,
    }
    return render(request, 'base.html', context)


def plot1_spent_coinb_vouts(request):
    context = {
        'plot': 'plot1',
        'line_param': 'Spending',
        'range_max': 1,
    }
    return render(request, 'plot1_spent_coinb_vouts.html', context)


def plot2_tts_tts_coinb_txos(request):
    context = {
        'plot': 'plot2',
        'line_param': 'Time-to-spend',
        'range_max': 500000,
    }
    return render(request, 'plot2_tts_coinb_txos.html', context)


def plot3_coinb_addr(request):
    context = {
        'plot': 'plot3',
        'line_param': 'Addresses',
        'range_max': 10,
    }
    return render(request, 'plot3_coinb_addr.html', context)


def plot4_throughput(request):
    context = {
        'plot': 'plot4',
        'line_param': 'Throughput',
        'range_max': 500,
    }
    return render(request, 'plot4_throughput.html', context)


def plot5_tx_count(request):
    context = {
        'plot': 'plot5',
        'line_param': 'Transactions',
        'range_max': 3000,
    }
    return render(request, 'plot5_tx_count.html', context)


def plot6_timelocked_txos(request):
    context = {
        'plot': 'plot6',
        'line_param': 'Timelocked TXs',
        'range_max': 1000,
    }
    return render(request, 'plot6_timelocked_txos.html', context)


def plot7_multisign_txos(request):
    context = {
        'plot': 'plot7',
        'line_param': 'Multisig TXs',
        'range_max': 20,
    }
    return render(request, 'plot7_multisign_txos.html', context)


def plot8_segwit_txs(request):
    context = {
        'plot': 'plot8',
        'line_param': 'Segwit TXs',
        'range_max': 2000,
    }
    return render(request, 'plot8_segwit_txs.html', context)


def plot9_op_return_txos(request):
    context = {
        'plot': 'plot9',
        'line_param': 'OP_RETURN TXs',
        'range_max': 50,
    }
    return render(request, 'plot9_op_return_txos.html', context)


def plot10_app_op_return_txos(request):
    context = {
        'plot': 'plot10',
        'line_param': 'APPs',
        'range_max': 10,
    }
    return render(request, 'plot10_app_op_return_txos.html', context)
