from collections import defaultdict
from io import StringIO

import math, cairo, svgwrite

# sample data
exp_dict = {
        'leafs': ['沙雕', '藝術', '競賽', '昨天', '上午', '在', '斗六市', '人文', '公園', '舉行', '，'],
        'edges': [(1, 0, 'ATT'), (2, 1, 'ATT'), (9, 2, 'FOB'), (4, 3, 'ATT'), (9, 4, 'ADV'), (9, 5, 'ADV'), (8, 6, 'ATT'), (8, 7, 'ATT'), (5, 8, 'POB'), (9, 10, 'WP'), (-1, 9, 'ROOT')],
        'pos': ['n', 'n', 'v', 'nt', 'nt', 'p', 'ns', 'n', 'n', 'v', 'wp']
}


def textDimension_all(text, fontsize, font_type):
    surface = cairo.SVGSurface('undefined.svg', 1280, 200)
    cr = cairo.Context(surface)
    cr.select_font_face(font_type, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(fontsize)
    xbearing, ybearing, width, height, xadvance, yadvance = cr.text_extents(text)
    return (xbearing, ybearing, width, height, xadvance, yadvance)

def textDimension(text, fontsize=14, font_type='Times New Roman'):
    xbearing, ybearing, width, height, xadvance, yadvance = textDimension_all(text, fontsize, font_type)
    return width, height
    
def textwidth(text, fontsize=14, font_type='Times New Roman'):
    return textDimension_all(text, fontsize, font_type)[4]

WORD_FONT_SIZE = 20     # font size of 實詞
COMMENT_FONT_SIZE = 16  # font size of 詞性
COMMENT_VERTIAL_PADDING = 6  # 實詞 與 詞性 的垂直間距
WORD_FONT = 'Microsoft JhengHei'
LABEL_FONT = 'Times New Roman'
COMMENT_FONT = 'Big Caslon Black'
# 以 'My' 這個字的高度作為其他所有word/pos的高度共同標準(因為不同字的高度，算出結果會不同)
word_height = textDimension('My', WORD_FONT_SIZE, WORD_FONT)[1]
comment_height = textDimension('My', COMMENT_FONT_SIZE, COMMENT_FONT)[1]

WORD_SEP_SIZE = 70 # space between Words
EDGE_VERTICAL_PADDING = 12 # space between edge end point and word
ARC_BASE_HEIGHT = 45
ARC_ANGLE = (8.0/9.0) * math.pi/2.0
ARC_BASE_HORIZON = (ARC_BASE_HEIGHT + 40)
LABEL_VERTICAL_PADDING = 5
LABEL_HORIZONTAL_PADDING = 5

def calculate_arc_height(index_shift):
    '''
    計算 arc的主要高度
    '''
    return ARC_BASE_HEIGHT + (index_shift-1) * 36


def calculate_slant_angle(delta):
    '''
    計算 傾角 (rad)
    '''
    sigmoid_value = 1.0/(1 + math.exp(-0.8*delta))
    return math.pi * (50.0 + 40.0 * sigmoid_value)/180.0

def draw_root_arg(drawingElement, arc_length, node2, relationNode, the_marker):
    x2 = node2['top'][0]
    y2 = node2['top'][1] - EDGE_VERTICAL_PADDING

    x1 = x2
    y1 = y2 - arc_length
    the_root_line = drawingElement.add(drawingElement.line((x1, y1), (x2, y2), stroke=svgwrite.rgb(10, 10, 16, '%')))
    # put arrow head
    the_root_line.set_markers((None, False, the_marker))

    # draw label and its surrounding box
    label_w, label_h = relationNode['width'], relationNode['height']
    rect_w, rect_h = label_w + 2*LABEL_HORIZONTAL_PADDING, label_h + 2*LABEL_VERTICAL_PADDING
    rect_x = x1 - rect_w/2
    rect_y = y1 - rect_h/2
    label_x = x1 - label_w/2
    label_y = y1 + label_h/2
    drawingElement.add(drawingElement.rect(insert=(rect_x, rect_y), size=(rect_w, rect_h), rx=6, ry=6, stroke='black', fill='white'))

    drawingElement.add(drawingElement.text(relationNode['text'], insert=(label_x, label_y), font_size=16, font_family=LABEL_FONT, fill='black'))



def draw_dependency_arg(drawingElement, word_node_list, emit_idx, des_idx, relationNode, the_marker):
    '''
    Point from node1 to node2
    '''
    node1 = word_node_list[emit_idx]
    node2 = word_node_list[des_idx]

    delta_index = int(abs(emit_idx - des_idx))
    primary_arc_height = calculate_arc_height(delta_index)
    secondary_arc_height = primary_arc_height * 0.85

    slant_angle = calculate_slant_angle(delta_index)
    inverse_tangent = 1.0/math.tan(slant_angle)

    x5 = node2['top'][0]
    y5 = node2['top'][1] - EDGE_VERTICAL_PADDING
    if emit_idx < des_idx:
        x0 = node1['top'][0] + node1['width']/2
        y0 = node1['top'][1] - EDGE_VERTICAL_PADDING

        x1 = x0 + secondary_arc_height*inverse_tangent
        y1 = y0 - secondary_arc_height

        a1 = x0 + primary_arc_height*inverse_tangent
        b1 = y0 - primary_arc_height

        x2 = a1 + (primary_arc_height - secondary_arc_height)/math.sin(slant_angle)
        y2 = b1


        x4 = x5 - secondary_arc_height*inverse_tangent
        y4 = y5 - secondary_arc_height

        a2 = x5 - primary_arc_height*inverse_tangent
        b2 = y5 - primary_arc_height

        x3 = a2 - (primary_arc_height - secondary_arc_height)/math.sin(slant_angle)
        y3 = y2
    else:
        x0 = node1['top'][0] - node1['width']/2
        y0 = node1['top'][1] - EDGE_VERTICAL_PADDING

        x1 = x0 - secondary_arc_height*inverse_tangent
        y1 = y0 - secondary_arc_height

        a1 = x0 - primary_arc_height*inverse_tangent
        b1 = y0 - primary_arc_height

        x2 = a1 - (primary_arc_height - secondary_arc_height)/math.sin(slant_angle)
        y2 = b1


        x4 = x5 + secondary_arc_height*inverse_tangent
        y4 = y5 - secondary_arc_height

        a2 = x5 + primary_arc_height*inverse_tangent
        b2 = y5 - primary_arc_height

        x3 = a2 + (primary_arc_height - secondary_arc_height)/math.sin(slant_angle)
        y3 = y2

    path_str = 'M{0} {1} L{2} {3} Q{4} {5}, {6} {7} L{8} {9} Q{10} {11}, {12} {13} L{14} {15}'.format(x0, y0, x1, y1, a1, b1, x2, y2, x3, y3, a2, b2, x4, y4, x5, y5)
    the_path = drawingElement.add(drawingElement.path(d=path_str, stroke_width=1, stroke='black', fill='none'))

    # put arrow head
    the_path.set_markers((None, False, the_marker))

    # draw label
    label_w, label_h = relationNode['width'], relationNode['height']
    rect_w, rect_h = label_w + 2*LABEL_HORIZONTAL_PADDING, label_h + 2*LABEL_VERTICAL_PADDING
    rect_x = (x2 + x3)/2 - rect_w/2
    rect_y = y2 - rect_h/2
    label_x = (x2 + x3)/2 - label_w/2
    label_y = y2 + label_h/2
    drawingElement.add(drawingElement.rect(insert=(rect_x, rect_y), size=(rect_w, rect_h), rx=6, ry=6, stroke='black', fill='white'))

    drawingElement.add(drawingElement.text(relationNode['text'], insert=(label_x, label_y), font_size=16, font_family=LABEL_FONT, fill='black'))


def dependency_graph_generation(word_seq, dep_edges, pos_seq):
    '''
    generate svg data, and return the resultant `Drawing` object
    '''
    dwg = svgwrite.Drawing()

    # create a new marker object
    marker = dwg.marker(refX='10', refY='3.5', size=(10,7), orient='auto')
    marker.add(svgwrite.shapes.Polygon(points=[[0, 0], [10, 3.5], [0, 7]]))
    # add marker to defs section of the drawing
    dwg.defs.add(marker)

    iniX = 15
    totalHeight = 0

    # create dependency edge dictionary and determine the total height
    root_point_index = None
    max_delta_index = 1
    dep_edge_dict = defaultdict(lambda : defaultdict(dict))
    for _dep_edge in dep_edges:

        label_w, label_h = textDimension(_dep_edge[2], 16, LABEL_FONT)
        dep_edge_dict[_dep_edge[0]][_dep_edge[1]] = { 'text': _dep_edge[2], 'width': label_w, 'height': label_h }
        
        if _dep_edge[0] == -1:
            root_point_index = _dep_edge[1]
            continue
        if abs(_dep_edge[0] - _dep_edge[1]) > max_delta_index:
            max_delta_index = abs(_dep_edge[0] - _dep_edge[1])

    # in order to get root line length, find the largest shift index for root node
    max_delta_index_of_root = 1
    for endIdx in dep_edge_dict[root_point_index]:
        if abs(endIdx - root_point_index) > max_delta_index_of_root:
            max_delta_index_of_root = abs(endIdx - root_point_index)
    max_delta_index_of_root += 1
    if max_delta_index_of_root > max_delta_index:
        totalHeight = calculate_arc_height(max_delta_index_of_root) + EDGE_VERTICAL_PADDING + word_height +  word_height + LABEL_VERTICAL_PADDING
    else:
        totalHeight = calculate_arc_height(max_delta_index) + EDGE_VERTICAL_PADDING + word_height +  word_height + LABEL_VERTICAL_PADDING
    if pos_seq is not None:
        totalHeight += comment_height + COMMENT_VERTIAL_PADDING

    # create word node sequence
    word_node_seq = []
    for _word in word_seq:
        word_width = textwidth(_word, WORD_FONT_SIZE, WORD_FONT)
        word_node = {'word': _word, 'width': word_width}
        word_node_seq.append(word_node)
        
    
    # Draw words
    accumulate_x = iniX
    for idx, _wordNode in enumerate(word_node_seq):
        # draw each word
        dynamic_sep = WORD_SEP_SIZE
        if idx in dep_edge_dict:
            if idx + 1 in dep_edge_dict[idx]:
                if dynamic_sep < dep_edge_dict[idx][idx+1]['width'] + 2*LABEL_HORIZONTAL_PADDING:
                    dynamic_sep = dep_edge_dict[idx][idx+1]['width'] + 2*LABEL_HORIZONTAL_PADDING
        if idx + 1 in dep_edge_dict:
            if idx in dep_edge_dict[idx+1]:
                if dynamic_sep < dep_edge_dict[idx+1][idx]['width'] + 2*LABEL_HORIZONTAL_PADDING:
                    dynamic_sep = dep_edge_dict[idx+1][idx]['width'] + 2*LABEL_HORIZONTAL_PADDING

        dwg.add(dwg.text(_wordNode['word'], insert=(accumulate_x, totalHeight - comment_height - COMMENT_VERTIAL_PADDING), font_size=WORD_FONT_SIZE, font_family=WORD_FONT, fill='black'))
        
        # top means the coordinate of top-middle
        _wordNode['top'] = (accumulate_x + 0.5*_wordNode['width'], totalHeight - comment_height - COMMENT_VERTIAL_PADDING - word_height)

        if pos_seq is not None:
            _wordNode['part-of-speech'] = pos_seq[idx]
            pos_width = textwidth(pos_seq[idx], COMMENT_FONT_SIZE, COMMENT_FONT)
            dwg.add(dwg.text(_wordNode['part-of-speech'], insert=(_wordNode['top'][0] - 0.5*pos_width, totalHeight), font_size=COMMENT_FONT_SIZE, font_family=COMMENT_FONT, fill='black'))

        accumulate_x += (_wordNode['width'] + dynamic_sep)

    # <svg> scale的問題用 viewbox屬性搭配width、height屬性來解決
    # do not know why bottom part is cut a little
    dwg.viewbox(0, 0, accumulate_x - dynamic_sep + 20, totalHeight + 3)

    for startIdx in dep_edge_dict:
        for endIdx in dep_edge_dict[startIdx]:
            if startIdx == -1:
                # deal with root
                draw_root_arg(dwg, calculate_arc_height(max_delta_index_of_root), word_node_seq[endIdx], dep_edge_dict[startIdx][endIdx], marker)
            else:
                draw_dependency_arg(dwg, word_node_seq, startIdx, endIdx, dep_edge_dict[startIdx][endIdx], marker)
    
    return dwg


def get_dependency_graph_htmltext(word_seq, dep_edges, pos_seq=None):
    '''
    取得 svg標籤文字
    '''
    drawingObj = dependency_graph_generation(word_seq, dep_edges, pos_seq)

    memory_buffer = StringIO()
    drawingObj.write(memory_buffer, pretty=True)
    # Retrieve contents
    total_html = memory_buffer.getvalue()
    # Close object and discard memory buffer
    memory_buffer.close()

    return total_html

def get_dependency_graph_asFile(word_seq, dep_edges, pos_seq=None, filename='graph.svg'):
    drawingObj = dependency_graph_generation(word_seq, dep_edges, pos_seq)

    with open(str(filename), 'w', encoding='utf8') as f:
        drawingObj.write(f, pretty=True)
        