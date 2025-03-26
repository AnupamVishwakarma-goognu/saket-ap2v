#!/bin/bash
#

if [ -d "/root/anquira" ]
then
	rm -rfv "/root/anquira"
fi
rsync -avz ../anquira /root/
mysqldump -u root anquira > /root/anquira/anquira.sql
