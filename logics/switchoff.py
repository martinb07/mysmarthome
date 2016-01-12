#!/usr/bin/env python

# get triggering item
trigger_source = trigger['source']
logger.debug('SwitchOff triggered by '+trigger_source)
trigger_item = sh.return_item(trigger_source)

if not trigger_item():
    # switch off associated item
    item_to_switchoff = sh.return_item(trigger_item.conf['switchoff'])
    logger.info('Switching off '+str(item_to_switchoff))
    item_to_switchoff(0)
else:
    logger.debug('SwitchOff trigger item is switched on. Nothing to do.')