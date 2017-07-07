from bs4 import BeautifulSoup
import re, html, math, json

f = open('output2.html', 'rb').read()

soup = BeautifulSoup(f, 'html.parser')
soup = html.unescape(soup)
spans = soup.find_all('span')

multiplier_constant = 1.2364
span_dict = {}
for span in spans:
    height = re.search('(?<=height:)[^px]*', span['style'])
    width = re.search('(?<=width:)[^px]*', span['style'])
    current_top_px = int(re.search('(?<=top:)[^px]*', span['style']).group(0))

    if height is None:
        height_threshold = 4
    else:
        height_threshold = int(height.group(0))

    if height_threshold < 5:
        if not height_threshold:
            new_width = math.floor(int(width.group(0)) * multiplier_constant)
            span['style'] = span['style'].replace(str(width.group(0)), str(new_width))

        left_px = height = int(re.search('(?<=left:)[^px]*', span['style']).group(0))
        if current_top_px not in span_dict.keys():
            letter = span.string
            span.string = json.dumps({left_px: letter})
            span_dict[current_top_px] = span
        else:
            try:
                letter_dict = json.loads(span_dict[current_top_px].string)
                letter_dict[left_px] = span.string
                new_string = json.dumps(letter_dict)
                span_dict[current_top_px].string = new_string
            except:
                # This could probably just be an if statement
                pass
    else:
        pass

finished_html = "<html>"
for span in span_dict.values():
    word_dict = json.loads(span.string)
    word = ''
    for key in sorted(word_dict.keys()):
        current_letter = word_dict[key]
        if current_letter is not None:
            word += current_letter
    span.string = word
    finished_html += str(span)
finished_html += "</html>"
print(finished_html)


"""
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
"""