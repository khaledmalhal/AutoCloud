#!/bin/bash
#
# Installation of AutoCloud service in Debian
# based systems. This script copies the daemon
# service in /etc/init.d/ and creates the runlevel
# services.
#
# Written by Khaled Malhal Abbas <khaled.malhal at estudiantat.upc.edu>

test -f ./autocloud || exit 0

cp ./autocloud /etc/init.d/

ln -sf ../init.d/autocloud /etc/rc0.d/K99autocloud
ln -sf ../init.d/autocloud /etc/rc1.d/K99autocloud
ln -sf ../init.d/autocloud /etc/rc2.d/S99autocloud
ln -sf ../init.d/autocloud /etc/rc3.d/S99autocloud
ln -sf ../init.d/autocloud /etc/rc4.d/S99autocloud
ln -sf ../init.d/autocloud /etc/rc5.d/S99autocloud
ln -sf ../init.d/autocloud /etc/rc6.d/K99autocloud
