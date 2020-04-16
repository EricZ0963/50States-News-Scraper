import requests
import json
import time

def parse(line, splitters, discard_ends):
    res = []
    for i, s in enumerate(splitters):
        r = line.split(s, 1)
        res.append(r[0])
        if len(r) == 1:
            break   # the back end doesn't exist so no point checking
        line = r[1]
        if i == len(splitters)-1 and not discard_ends:
            res.append(line)
    if discard_ends: return res[1:]
    else: return res

def get_sources_in_state(url, state):
    print('Finding sources for ' + state + ' in url ' + url)
    res = []
    r = requests.get(url)
    rsplit = r.text.split('\n')
    for line in rsplit:
        if '<li><a rel="nofollow" href="' in line:
            p = parse(line, [
                '<li><a rel="nofollow" href="',
                '">',
                '</a>',
                '[',
                ']'
                ], True)
            #rint(p)
            try:
                res.append(
                    {'url': p[0], 'source': p[1], 'city': p[3], 'state': state}
                )
            except Exception as e:
                # stuff that doesnt have city linked to them, usually just college stuff
                print('\tWarning: Didn\'t process source {} properly due to "{}"'.format(p[1], e))
    return res

def get_sources(url):
    res = []
    r = requests.get(url)
    rsplit = r.text.split('\n')
    for line in rsplit:
        if 'class="displayBlock rounded stateLink orangeHover"' in line:
            p = parse(line, [
                'href="',
                '" title="',
                ' Newspapers"'
                ], True)
            sources = get_sources_in_state(p[0], p[1])
            res += sources
            print('Found {} sources for {}'.format(len(sources), p[1]))
            time.sleep(1) # be nice to the site
    return res




def main():
    all_sources = get_sources('https://www.50states.com/news')
    data = {'sources': all_sources}
    print(all_sources)

    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    main()