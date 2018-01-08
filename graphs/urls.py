from graphs import views
from django.conf.urls import url
urlpatterns = [
    url(r'^$', views.landing, name='landing'),
    url(r'^plot1$', views.plot1_spent_coinb_vouts, name='plot1'),
    url(r'^plot2$', views.plot2_tts_tts_coinb_txos, name='plot2'),
    url(r'^plot3$', views.plot3_coinb_addr, name='plot3'),
    url(r'^plot4$', views.plot4_throughput, name='plot4'),
    url(r'^plot5$', views.plot5_tx_count, name='plot5'),
    url(r'^plot6$', views.plot6_timelocked_txos, name='plot6'),
    url(r'^plot7$', views.plot7_multisign_txos, name='plot7'),
    url(r'^plot8$', views.plot8_segwit_txs, name='plot8'),
    url(r'^plot9$', views.plot9_op_return_txos, name='plot9'),
    url(r'^plot10$', views.plot10_app_op_return_txos, name='plot10'),
]
