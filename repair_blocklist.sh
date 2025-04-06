#!/data/data/com.termux/files/usr/bin/bash

cd ~/blocklist || exit 1
cp adhell3_blocklist_from_nextdns.txt original_backup.txt

awk '
  $1 == "0.0.0.0" && NF >= 2 {
    gsub(/\r/, "", $2);
    domain = tolower($2);
    gsub(/[ \t\r\n]+$/, "", domain);
    seen[domain]++
  }
  END {
    for (d in seen) print "0.0.0.0 " d
  }
' adhell3_blocklist_from_nextdns.txt | sort -u > cleaned_blocklist.txt

mv cleaned_blocklist.txt adhell3_blocklist_from_nextdns.txt

git add adhell3_blocklist_from_nextdns.txt
git commit -m "Repaired blocklist: removed duplicates and normalized entries"
git push

termux-toast -g bottom -s "Blocklist repaired and pushed!"