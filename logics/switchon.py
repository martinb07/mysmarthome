#!/usr/bin/env python

# get triggering item
trigger_source = trigger['source']
logger.debug('SwitchOn triggered by '+trigger_source)
trigger_item = sh.return_item(trigger_source)

if trigger_item():
    # switch on associated item
    item_to_switchon = sh.return_item(trigger_item.conf['switchon'])
    logger.info('Switching on '+str(item_to_switchon))
    item_to_switchon(1)
else:
    logger.debug('SwitchOn trigger item is switched off. Nothing to do.')