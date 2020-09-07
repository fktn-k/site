import argparse
import glob
import re
import os
import urllib.request, urllib.error, urllib.parse
import urllib3
import requests
import sys
import time
import random

urllib3.disable_warnings()

def retry_sleep():
    sec = random.uniform(20, 30);
    time.sleep(sec)

def check_url(url: str, retry: int = 5) -> (bool, str):
    try:
        res = requests.get(url, verify=False, timeout=60.0)
        if res.url:
            if res.url == url:
                return res.status_code != 404, "404"
            return check_url(res.url)
        else:
            return res.status_code != 404, "404"
    except requests.exceptions.ConnectionError as e:
        if retry <= 0:
            return False, "requests.exceptions.ConnectionError : {} ".format(e)
        retry_sleep()
        return check_url(url, retry - 1)
    except requests.exceptions.RequestException as e:
        if retry <= 0:
            return False, "requests.exceptions.RequestException : {}".format(e)
        retry_sleep()
        return check_url(url, retry - 1)
    except Exception as e:
        return False, "unknown exception : {}".format(e)

def fix_link(link: str) -> str:
    if "http" in link or ".md" in link:
        if "http" in link and "(" in link:
            link = link + ")"
        return re.sub("#.*", "", link.strip())
    else:
        return ""

def find_all_links(text: str) -> (list, set):
    inner_links = []
    outer_links = set()
    for m in re.finditer(r'\[(.*?)\]\((.*?)\)', text):
        link = fix_link(m.group(2))
        if link:
            if "http" in link:
                if not link.startswith("https://web.archive.org"):
                    outer_links.add(link)
            else:
                inner_links.append(link)
    for m in re.finditer(r'[\*-] (.*?)\[link (.*?)\]', text):
        link = fix_link(m.group(2))
        if link:
            if "http" in link:
                if not link.startswith("https://web.archive.org"):
                    outer_links.add(link)
            else:
                inner_links.append(link)
    return inner_links, outer_links

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description="")
    argparser.add_argument("--check-inner-link",
                           dest='check_inner_link',
                           action='store_true',
                           default=False)
    argparser.add_argument("--check-outer-link",
                           dest='check_outer_link',
                           action='store_true',
                           default=False)
    args = argparser.parse_args()

    if not args.check_inner_link and not args.check_outer_link:
        print("unchecked", file=sys.stderr)
        sys.exit(1)

    found_error = False
    current_dir = os.getcwd()
    outer_link_dict = dict()
    for p in glob.glob("**/*.md", recursive=True):
        dirname = os.path.dirname(p)
        with open(p) as f:
            text = f.read()

        inner_links, outer_links = find_all_links(text)
        for link in outer_links:
            if link in outer_link_dict:
                outer_link_dict[link].append(p)
            else:
                outer_link_dict[link] = [p]

        if args.check_inner_link:
            for link in inner_links:
                rel_link = ""
                if link.startswith("/"):
                    rel_link = os.path.join(current_dir, link.lstrip("/"))
                else:
                    rel_link = os.path.join(dirname, link)

                if link.endswith(".nolink"):
                    if os.path.exists(rel_link.rstrip(".nolink")):
                        print("nolinked {} href {} found.".format(p, link.rstrip(".nolink")), file=sys.stderr)
                        found_error = True
                else:
                    if not os.path.exists(rel_link):
                        print("{} href {} not found.".format(p, link), file=sys.stderr)
                        found_error = True

    if args.check_outer_link:
        for link, from_list in outer_link_dict.items():
            exists, reason = check_url(link)
            if not exists:
                print("URL {} not found. {} from:{}".format(link, reason, from_list), file=sys.stderr)
                found_error = True

    if found_error:
        sys.exit(1)
