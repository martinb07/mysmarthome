#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
# Waterkotte EcoTouch Plugin
#########################################################################
# Copyright 2014 Thomas Kastner
#########################################################################
#  Free for non-commercial use
#########################################################################

import logging
import time
import re
import http.client

logger = logging.getLogger('')


class Waterkotte():
    _key2tag= {
        'temp_aussen': 'A1',
        'temp_aussen_1h': 'A2',
        'temp_aussen_24h': 'A3',
        'temp_quelle_ein': 'A4',
        'temp_quelle_aus': 'A5',
        'temp_verdampfung': 'A6',
        'temp_sauggas': 'A7',
        'druck_verdampfung': 'A8',
        'temp_soll': 'A10',
        'temp_ruecklauf': 'A11',
        'temp_vorlauf': 'A12',
        'temp_kodensation': 'A14',
        'druck_kondensation': 'A15',
        'temp_speicher': 'A16',
        'temp_raum': 'A17',
        'temp_raum_1h': 'A18',
        'temp_ww': 'A19',
        'pow_comp': 'A25',
        'pow_therm': 'A26',
        'pow_cool': 'A27',
        'cop_comp': 'A28',
        'cop_cool': 'A29',
        'temp_hk': 'A30',
        'temp_gefordert_hk': 'A31',
        'temp_gefordert_ww': 'A37',
        'temp_soll_ww': 'A38',
        'rpm_hk': 'A51',
        'rpm_sole': 'A52',
        'valve_exp': 'A23',
        'jaz_wp': 'A460',
		'stat_heizbetrieb': 'I30',
		'stat_heizen': 'I137',
		'stat_ww': 'I139',
		'bsz_verdichter': 'A516',
		'bsz_heizpumpe': 'A522',
		'bsz_ext_waerme': 'A528',

    }

    def __init__(self, smarthome, ip, cycle=300):
        self._sh = smarthome
        self.ip = ip
        self.cycle = int(cycle)
        self._items = []
        self._values = {}

    def run(self):
        self.alive = True
        self._sh.scheduler.add('Waterkotte', self._refresh, cycle=self.cycle)

    def stop(self):
        self.alive = False

    def parse_item(self, item):
        if 'waterkotte' in item.conf:
            waterkotte_key = item.conf['waterkotte']
            if waterkotte_key in self._key2tag:
                self._items.append([item, waterkotte_key])
                return self.update_item
            else:
                logger.warn('invalid key {0} configured', waterkotte_key)
        return None

    def parse_logic(self, logic):
        pass

    def update_item(self, item, caller=None, source=None, dest=None):
        if caller != 'Waterkotte':
            pass

    def _refresh(self):
        start = time.time()
        try:
                # log in to web interface, retrieve Cookie
                token = self._sh.tools.fetch_url('http://' + self.ip + '/cgi/login?username=admin&password=wtkadmin', timeout=10).decode()
                token = re.search('IDALToken=\w*', token)
                token = token.group(0)

                # update all items
                for waterkotte_key in self._key2tag:

                    # send request using previously aquired Cookie
                    data2 = self.fetch_url_cookie('http://' + self.ip +'/cgi/readTags?&n=1&t1=' + self._key2tag[waterkotte_key], token).decode()
                    data2 = re.sub('#\w*\tS_OK\n\w*\t', '', data2)
                    data2 = re.sub('\n', '', data2)

                    # analog values A### are 16 bit integers; divide by 10 to get real value
                    value = float(data2)/10

                    self._values[waterkotte_key] = value
                for item_cfg in self._items:
                    if item_cfg[1] in self._values:
                        item_cfg[0](self._values[item_cfg[1]], 'Waterkotte')
        except Exception as e:
                    logger.error(
                        'could not retrieve data from {0}: {1}'.format(self.ip, e))
        return

        cycletime = time.time() - start
        logger.debug("cycle takes {0} seconds".format(cycletime))
        
    # this is fetch_url from lib/tools.py, extended to use the Cookie 'token' in the http request        
    def fetch_url_cookie(self, url, token, username=None, password=None, timeout=10):
        headers = {'Accept': 'text/plain'}
        headers['Cookie'] = token
        plain = True
        if url.startswith('https'):
            plain = False
        lurl = url.split('/')
        host = lurl[2]
        purl = '/' + '/'.join(lurl[3:])
        if plain:
            conn = http.client.HTTPConnection(host, timeout=timeout)
        else:
            conn = http.client.HTTPSConnection(host, timeout=timeout)
        if username and password:
            headers['Authorization'] = ('Basic '.encode() + base64.b64encode((username + ':' + password).encode()))
        try:
            conn.request("GET", purl, headers=headers)
        except Exception as e:
            logger.warning("Problem fetching {0}: {1}".format(url, e))
            conn.close()
            return False
        resp = conn.getresponse()
        if resp.status == 200:
            content = resp.read()
        else:
            logger.warning("Problem fetching {0}: {1} {2}".format(url, resp.status, resp.reason))
            content = False
        conn.close()
        return content
