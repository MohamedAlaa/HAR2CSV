#!/usr/bin/env python
"""
HAR2CSV is a quick cl script to parse HTTP Archive (HAR) file and save specific information in csv format
HAR Spec: http://groups.google.com/group/http-archive-specification/web/har-1-2-spec
Copyleft 2013 Mohamed Alaa <malaa83@gmail.com>

Example usage: ./har2csv.py sample.har http://test.com/assets/style.css
"""

import json
import csv
import time
import sys

timestamp = time.time()

if '__main__' == __name__:

    if len(sys.argv) < 3:
        print "Usage: %s <har_file> <asset url>" % sys.argv[0]
        sys.exit(1)

    har_file = sys.argv[1]
    asset_file = sys.argv[2]


    # Read HAR archive (skip over binary header if present - Fiddler2 exports contain this)
    har_data = open(har_file, 'rb').read()
    skip = 3 if '\xef\xbb\xbf' == har_data[:3] else 0

    har = json.loads(har_data[skip:])

    matching_entries = filter(lambda x: asset_file == x['request']['url'], har['log']['entries'])
    matching_urls = set(map(lambda x: x['timings']['wait'], matching_entries))

    save_file = ("har-" + str(timestamp)+".csv")

    with open(save_file, 'w+') as csvfile:
        harwriter = csv.writer(csvfile, delimiter=',', lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
        harwriter.writerow(['file', asset_file])
        harwriter.writerow(['transfer size:'])
        harwriter.writerow(['normal:', matching_entries[0]["response"]["content"]["size"]])
        harwriter.writerow(['gzip:', matching_entries[0]["response"]["content"]["compression"]])
        harwriter.writerow(["\n"])
        harwriter.writerow(['timing:'])
        harwriter.writerow(['blocked:',matching_entries[0]["timings"]["blocked"]])
        harwriter.writerow(['dns:',matching_entries[0]["timings"]["dns"]])
        harwriter.writerow(['connect:',matching_entries[0]["timings"]["connect"]])
        harwriter.writerow(['send:',matching_entries[0]["timings"]["send"]])
        harwriter.writerow(['wait:',matching_entries[0]["timings"]["wait"]])
        harwriter.writerow(['receive:',matching_entries[0]["timings"]["receive"]])
        harwriter.writerow(['ssl:',matching_entries[0]["timings"]["ssl"]])

    print "Finished Saving..."
    sys.exit(1)