dd if=/dev/sdb of=backup.img bs=1024 count=180224
gzip -v9 backup.img