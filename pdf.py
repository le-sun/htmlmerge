from bs4 import BeautifulSoup
import re, html, math

f = open('output2.html', 'rb').read()

soup = BeautifulSoup(f, 'html.parser')
soup = html.unescape(soup)
spans = soup.find_all('span')

debug_index = 0
all_spans = {}
letters = ''
pre_span, pre_top_px, index = None, -99, -1
for span in spans:
    height = re.search('(?<=height:)[^px]*', span['style'])
    if height is None:
        height = 4
    else:
        height = int(height.group(0))

    if height < 5:
        debug_index += 1
        current_top_px = int(re.search('(?<=top:)[^px]*', span['style']).group(0))

        if math.fabs(current_top_px - pre_top_px) > 1:
            try:
                # Idea: make all spans into dictionary with top pixel as key, so insert all span strings to that span with the specific top pixel
                all_spans[pre_top_px].string += letters
                #all_spans[index].string += letters
            except:
                pass
            letters = ''
            if not current_top_px in all_spans.keys():
                all_spans[current_top_px] = span
            else:
                all_spans[pre_top_px] = span
            index += 1
            pre_span = span
            pre_top_px = int(current_top_px)
        elif current_top_px == pre_top_px:
            if span.string:
                letters += span.string
            pre_span = span
            pre_top_px = int(current_top_px)
    else:
        pass

finished_html = "<html>"
for span in all_spans.values():
    finished_html += str(span)
finished_html += "</html>"
print(finished_html)