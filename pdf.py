from bs4 import BeautifulSoup
import re, html, math, json

f = open('outputorigin.html', 'rb').read()

soup = BeautifulSoup(f, 'html.parser')
good_soup = html.unescape(soup)
soup = good_soup.find('body')

#spans = soup.find_all('span')

banished_words = ['st', 'rd', 'th']
multiplier_constant = 1.2364
span_dict = {}
for span in soup.children:
    if span.name == 'div':
        span_dict[span.string] = span
    elif span.name == 'span':
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

            left_px = int(re.search('(?<=left:)[^px]*', span['style']).group(0))
            if current_top_px not in span_dict.keys():
                letter = span.string
                span.string = json.dumps({left_px: letter})
                span_dict[current_top_px] = span
            else:
                if span_dict[current_top_px].string:
                    letter_dict = json.loads(span_dict[current_top_px].string)
                    letter_dict[left_px] = span.string
                    new_string = json.dumps(letter_dict)
                    span_dict[current_top_px].string = new_string
        else:
            pass
    else:
        pass

finished_html = "<html>"
for span in span_dict.values():
    if span.name == 'div':
        try:
            finished_html += str(new_div)
        except NameError:
            pass
        new_div = good_soup.new_tag('div')
        new_div.attrs['class'] = 'page'
    else:
        word_dict = json.loads(span.string)
        word = ''
        spans = []
        sorted_keys = sorted(word_dict.keys(), key=int)

        height = re.search('(?<=height:)[^px]*', span['style'])
        current_span_left = re.search('(?<=left:)[^px]*', span['style']).group(0)
        first_left = sorted_keys[0]
        if int(current_span_left) > int(first_left):
            span['style'] = span['style'].replace(current_span_left, first_left)

        len_keys = len(sorted_keys)
        for i in range(len_keys):
            current_key = sorted_keys[i]
            try:
                next_key = sorted_keys[i + 1]
                current_letter = word_dict[current_key]
                next_letter = word_dict[next_key]

                px_diff = int(next_key) - int(current_key)
                if px_diff > 20:
                    if word:
                        prev_span = good_soup.new_tag('span')
                        prev_span.string = word
                        spans.append(prev_span)
                        word = ''

                    new_span = good_soup.new_tag('span')
                    new_span.attrs['style'] = 'width:{}px;display:inline-block;'.format(px_diff)
                    spans.append(new_span)
                else:
                    current_letter = word_dict[current_key]
                    if current_letter is not None:
                        word += current_letter
            except IndexError:
                current_letter = word_dict[current_key]
                if current_letter is not None:
                    word += current_letter

        new_span = good_soup.new_tag('span')
        new_span.string = word
        if word != '' and word != "":
            spans.append(new_span)
            span.contents = spans
        else:
            span.contents = []

        if height is None:
            extra_attrs = 'white-space: pre; width: 100%;'
            span['style'] += extra_attrs
            span.attrs['class'] = 'line'
        if not(len(word) == 2 and word in banished_words):
            new_div.contents.append(span)

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

span.contents.append(soup.new_tag('<span style="width:{};"/>'.format(px_diff)))
"""