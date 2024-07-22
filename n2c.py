import argparse
import requests
import csv
import time
import os
import shelve
import keyboard
from collections import defaultdict
from datetime import datetime, timedelta

# Constants for API URLs
RXNORM_API_URL = "https://rxnav.nlm.nih.gov/REST/rxcui"
RXCLASS_API_URL = "https://rxnav.nlm.nih.gov/REST/rxclass/class/byRxcui"

def get_rxcui_from_ndc(ndc, cache):
    """Get RxNorm CUI from NDC, using cache."""
    if ndc in cache:
        return cache[ndc]
    try:
        response = requests.get(f"{RXNORM_API_URL}?idtype=NDC&id={ndc}", headers={"Accept": "application/json"})
        response.raise_for_status()
        data = response.json()
        rxcui = data.get('idGroup', {}).get('rxnormId', [None])[0]
        cache[ndc] = rxcui
        return rxcui
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except ValueError as json_err:
        print(f"JSON decode error: {json_err}")
    cache[ndc] = None
    return None

def get_atc_classes_from_rxcui(rxcui, cache):
    """Get ATC classes from RxNorm CUI, using cache."""
    if rxcui in cache:
        return cache[rxcui]
    try:
        response = requests.get(f"{RXCLASS_API_URL}?rxcui={rxcui}&classTypes=ATC", headers={"Accept": "application/json"})
        response.raise_for_status()
        data = response.json()
        classes = data.get('rxclassDrugInfoList', {}).get('rxclassDrugInfo', [])
        atc_classes = [cls['rxclassMinConceptItem']['classId'] for cls in classes if cls['rxclassMinConceptItem']['classType'] == 'ATC1-4']
        cache[rxcui] = atc_classes
        return atc_classes
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except ValueError as json_err:
        print(f"JSON decode error: {json_err}")
    cache[rxcui] = []
    return []

def validate_ndc(ndc):
    """Validate the format of the NDC code."""
    if len(ndc) in [10, 11, 12] and ndc.replace("-", "").isdigit():
        return True
    print(f"Invalid NDC format: {ndc}")
    return False

def format_time(seconds):
    """Format time in seconds to a human-readable format."""
    periods = [
        ('hour', 3600),
        ('minute', 60),
        ('second', 1)
    ]
    time_str = []
    for period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            if period_value > 1:
                period_name += 's'
            time_str.append(f"{period_value} {period_name}")
    return ', '.join(time_str)

def process_ndc_list(input_file, output_file, cache):
    ndc_to_rxcui = {}
    rxcui_to_atc = defaultdict(list)
    results = []
    ndcs_with_atc = 0

    # Read NDCs from input file
    with open(input_file, 'r') as file:
        ndcs = [line.strip() for line in file if validate_ndc(line.strip())]

    total_ndcs = len(ndcs)
    api_calls = 0
    start_time = datetime.now()

    try:
        for idx, ndc in enumerate(ndcs, start=1):
            if keyboard.is_pressed('p'):
                raise KeyboardInterrupt

            if ndc in cache:
                rxcui = cache[ndc]
            else:
                current_time = datetime.now()
                elapsed_time = current_time - start_time
                api_calls += 1
                estimated_total_time = (elapsed_time / api_calls) * total_ndcs
                remaining_time = estimated_total_time - elapsed_time
                remaining_seconds = int(remaining_time.total_seconds())
                print(f"Processing {idx}/{total_ndcs}: {ndc} - Estimated completion in {format_time(remaining_seconds)}")

                rxcui = get_rxcui_from_ndc(ndc, cache)
                # Save the cache every 10 iterations to minimize data loss
                if idx % 10 == 0:
                    cache.sync()

            if rxcui:
                if rxcui in cache:
                    atc_classes = cache[rxcui]
                else:
                    atc_classes = get_atc_classes_from_rxcui(rxcui, cache)
                    # Save the cache every 10 iterations to minimize data loss
                    if idx % 10 == 0:
                        cache.sync()
                
                if atc_classes:
                    ndcs_with_atc += 1

                for atc_class in atc_classes:
                    results.append({'NDC': ndc, 'ATC_class': atc_class})
            # else:
                # print(f"No RxCUI found for NDC {ndc}")

        completion_percentage = (ndcs_with_atc / total_ndcs) * 100
        print(f"Completed: {completion_percentage:.2f}% of NDCs have at least one ATC class associated.")

    except KeyboardInterrupt:
        completion_percentage = (ndcs_with_atc / idx) * 100
        print(f"Interrupted. {completion_percentage:.2f}% of NDCs queried have at least one ATC class associated.")
        cache.sync()

    # De-duplicate the results
    unique_results = {tuple(result.items()) for result in results}
    unique_results = [dict(result) for result in unique_results]

    # Write results to CSV
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['NDC', 'ATC_class']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(unique_results)

    print(f"Results written to {output_file}")

def generate_output_filename(input_file):
    """Generate the output filename based on the input filename."""
    base, ext = os.path.splitext(input_file)
    return f"{base}_ATC_classes.csv"

def generate_cache_filename(input_file):
    """Generate the cache filename based on the input filename."""
    base = os.path.splitext(input_file)[0]
    return f"{base}_cache.shelve"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a list of NDCs and map them to ATC classes.')
    parser.add_argument('input_file', type=str, help='Input file containing NDCs (one per line).')

    args = parser.parse_args()

    output_file = generate_output_filename(args.input_file)
    cache_file = generate_cache_filename(args.input_file)

    print("Will start querying the NDCs. If you need to interrupt, press P.")

    # Use shelve to create a persistent cache in the same directory as the input file
    with shelve.open(cache_file) as cache:
        process_ndc_list(args.input_file, output_file, cache)
