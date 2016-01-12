#!/usr/bin/env python
# send notification if washing machine or tumbler is finished

### Trockner ###    
#Letzte Statusaenderung auf FALSE vor mehr als 4 Minuten
if sh.eg.hwr.trockner.strom.last_change() <= sh.now() - datetime.timedelta(seconds=240) and sh.eg.hwr.trockner.strom() == False:
        pass
#Letzte Statusaenderung auf FALSE vor weniger als 5 Minuten
else:
    if sh.eg.hwr.trockner.strom() == False:
        # ruf diese Logik in 5 Minuten noch einmal auf
        logic.trigger(dt=sh.now() + datetime.timedelta(seconds=300))
        logger.info('Trockner laeuft < 5 min')

#Letzte Statusaenderung auf TRUE    
if sh.eg.hwr.trockner.strom() == True:
    sh.notify('HWR', 'Trockner ist fertig', 2)

### Waschmaschine ###
#Letzte Statusaenderung auf FALSE vor mehr als 4 Minuten
if sh.eg.hwr.waschmaschine.strom.last_change() <= sh.now() - datetime.timedelta(seconds=240) and sh.eg.hwr.waschmaschine.strom() == False:
        pass  
#Letzte Statusaenderung auf FALSE vor weniger als 5 Minuten
else:
    if sh.eg.hwr.waschmaschine.strom() == False:
        # ruf diese Logik in 5 Minuten noch einmal auf
        logic.trigger(dt=sh.now() + datetime.timedelta(seconds=300))
        logger.info('Waschmaschine laeuft < 5 min')

#Letzte Statusaenderung auf TRUE    
if sh.eg.hwr.waschmaschine.strom() == True:
    sh.notify('HWR', 'Waschmaschine ist fertig', 2)