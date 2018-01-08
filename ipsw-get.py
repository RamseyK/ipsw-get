import argparse
import sys
import os
import requests
import json
from pkg_resources import parse_version

USE_PYCRYPTODOME = False
try:
    # Faster
    import Crypto
    USE_PYCRYPTODOME = True
except:
    import hashlib


def download(url, expected_md5, output_dir):

    if not url.endswith('.ipsw'):
        print("URL does not point to an ipsw")
        return

    # Check to see if the ipsw has already been downloaded to the output dir
    fn = os.path.basename(url)
    filepath = os.path.join(os.path.join(output_dir, fn))
    if os.path.exists(filepath):
        print("{} already exists, skipping..".format(fn))
        return

    # Download ipsw in chunks
    print("Downloading {} ...".format(fn))

    if USE_PYCRYPTODOME:
        hash_md5 = Crypto.Hash.MD5()
    else:
        hash_md5 = hashlib.md5()

    r = requests.get(url, stream=True)
    with open(filepath, 'wb') as fh:
        for chunk in r.iter_content(chunk_size=1024):
            fh.write(chunk)
            hash_md5.update(chunk)

    hash_matched = (hash_md5.hexdigest().lower() == expected_md5.lower())
    print("MD5: {} - {}\n".format(hash_md5.hexdigest(), 'MATCH' if hash_matched else '! MISMATCH !'))


def main():

    parser = argparse.ArgumentParser(description='A tool to automate the bulk download of IPSWs using ipsw.me')
    parser.add_argument('-min', '--min-version', required=False, type=str, help='Minimum iOS version')
    parser.add_argument('-max', '--max-version', required=False, type=str, help='Maximum iOS version')
    parser.add_argument('-device', '--device-identifier', required=False, type=str, help='Full or partial device identifier to filter on (eg. iPhone7,2 / iPhone / iPod)')
    parser.add_argument('-o', '--output', required=True, type=str, help='Output directory to download files to')

    args = parser.parse_args()

    if not args.output or not os.path.isdir(args.output):
        print("Output must point to an output directory that exists")
        parser.print_help()
        return -1

    print("ipsw-get powered by ipsw.me\n")

    # Filters
    filter_device_name = ''
    filter_min_version = parse_version(args.min_version) if args.min_version else parse_version('0.1')
    filter_max_version = parse_version(args.max_version) if args.max_version else parse_version('999.0')

    if args.device_identifier:
        filter_device_name = args.device_identifier.lower()

    # Download firmwares.json from ipsw.me to parse. This file has all of the metadata we need
    try:
        firmwares_resp = requests.get('https://api.ipsw.me/v2.1/firmwares.json')
    except Exception as e:
        print("Could not retrieve firmware metadata from ipsw.me API: {}".format(e))
        return -1

    firmwares = json.loads(firmwares_resp.content)
    if len(firmwares['devices']) == 0:
        print("Error: No devices could be found in the firmwares.json")
        return -1

    target_firmwares = []

    # Go through all device firmware and only promote the firmwares that match our criteria into the target_devices dict
    for name, info in firmwares['devices'].items():

        # If we are filtering one device name, ensure this matches first
        if filter_device_name:

            if filter_device_name in name.lower():

                if args.min_version or args.max_version:
                    # If we are also filtering on min/max version, check that here for each firmware
                    for fw in info['firmwares']:

                        if (parse_version(fw['version']) >= filter_min_version) and \
                                (parse_version(fw['version']) <= filter_max_version):
                            target_firmwares.append(fw)

                else:
                    # If we are just matching on the device name, then add all its firmwares here
                    target_firmwares.extend(info['firmwares'])

        elif args.min_version or args.max_version:
            # If we are just filtering on min/max version, check that here

            for fw in info['firmwares']:

                if (parse_version(fw['version']) >= filter_min_version) and (
                        parse_version(fw['version']) <= filter_max_version):

                    target_firmwares.append(fw)
        else:
            # Nothing matched
            continue

    if len(target_firmwares) == 0:
        print("No IPSWs matched provided criteria. Nothing to do.")
        return 0

    print("Downloading {} matched IPSWs..\n".format(len(target_firmwares)))
    # print(target_firmwares)

    for fw in target_firmwares:
        download(fw['url'], fw['md5sum'], args.output)

    return 0


if __name__ == '__main__':
    sys.exit(main())