'''
The library used to make tree become image file
'''

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from .parse_utility import get_leaf_nodes
import base64

display_fnt = ImageFont.truetype('./fonts/MSJH.TTC', 21)
_, word_height = display_fnt.getsize("DUMMY")

# Some geometry parameters(1)
horizontal_margin_space = 13
vertical_margin_space = 20
vertical_small_space = 6
# Some geometry parameters(2)
between_box_space = 25
relation_line_height = 30
short_line_height = 10

role_pos_height = 2 * word_height
one_node_text_height = role_pos_height + vertical_small_space
one_level_height = one_node_text_height + relation_line_height + short_line_height
pos_node_text_height = word_height + vertical_small_space
pos_level_height = pos_node_text_height + relation_line_height + short_line_height


def assign_draw_info(all_leaf_nodes):
    '''
    Add some attributes for each node.\n
    `height`: length from leaf node.\n
    `width`: box-width of this node, the max of part-of-speech and role\n
    `tree-width`: box width of sub-tree induced by this node.
    '''

    for _leaf_node in all_leaf_nodes:

        _leaf_node['height'] = 0
        if 'role' in _leaf_node:
            _leaf_node['width'] = max(display_fnt.getsize(_leaf_node['pos'])[0], display_fnt.getsize(_leaf_node['role'])[0])
        else:
            _leaf_node['width'] = display_fnt.getsize(_leaf_node['pos'])[0]
        _leaf_node['tree-width'] = max(_leaf_node['width'], display_fnt.getsize(_leaf_node['word'])[0])


        childNode = _leaf_node
        parentNode = childNode['parent']
        while parentNode != None:

            if 'height' in parentNode:
                if parentNode['height'] < childNode['height'] + 1:
                    parentNode['height'] = childNode['height'] + 1
            else:
                parentNode['height'] = childNode['height'] + 1

            if 'role' not in parentNode:
                parentNode['width'] = display_fnt.getsize(parentNode['pos'])[0]
            elif 'pos' not in parentNode:
                parentNode['width'] = display_fnt.getsize(parentNode['role'])[0]
            else:
                parentNode['width'] = max(display_fnt.getsize(parentNode['pos'])[0], display_fnt.getsize(parentNode['role'])[0])
            
            if 'tree-width' not in parentNode:
                parentNode['tree-width'] = list()   # 第一次遇到此 parentNode
            if type(childNode['tree-width']) == int:
                parentNode['tree-width'].append(childNode['tree-width'])

                # Can determine parentNode's tree-width attribute
                if len(parentNode['tree-width']) == len(parentNode['child']):

                    child_treewidth_sum = sum(parentNode['tree-width'])
                    if len(parentNode['tree-width']) > 1:
                        child_treewidth_sum += (len(parentNode['tree-width']) - 1) * between_box_space
                    
                    parentNode['tree-width'] = max(child_treewidth_sum, parentNode['width'])
            
            childNode = parentNode
            parentNode = childNode['parent']

def estimate_TotalWidth(the_root_node):

    return the_root_node['tree-width'] + 2 * horizontal_margin_space

def estimate_TotalHeight(the_root_node, spec='CKIP'):
    if spec == 'CKIP':
        inner_height = the_root_node['height'] * (one_node_text_height + relation_line_height + short_line_height)
        if 'role' not in the_root_node:
            inner_height -= word_height
        inner_height += (one_node_text_height + relation_line_height + word_height)
    else:
        # no role is here
        inner_height = the_root_node['height'] * (pos_node_text_height + relation_line_height + short_line_height)
        inner_height += (pos_node_text_height + relation_line_height + word_height)
    
    return inner_height + 2 * vertical_margin_space

def generateParseTreeImage(the_root_node, saved_filename, spec='CKIP'):
    '''
    Save the CKIP parse tree png file according to the given root node.\n
    '''
    result_image_obj = createParseTreeImageObject(the_root_node, spec)

    result_image_obj.save(saved_filename, format="png")

def createParseTreeImageObject(the_root_node, spec='CKIP'):
    '''
    Draw the CKIP parse tree according to the given root node.\n
    '''

    assign_draw_info(get_leaf_nodes(the_root_node))

    background_w = estimate_TotalWidth(the_root_node)
    background_h = estimate_TotalHeight(the_root_node, spec)
    background = Image.new('RGB', (background_w, background_h), color = 'white')
    
    drawObj = ImageDraw.Draw(background)

    draw_node(drawObj, the_root_node, background_w/2, vertical_margin_space, spec)

    return background

def draw_node(draw_api, the_node, top_x_coordinate, top_y_coordinate, spec='CKIP'):
    '''
    Draw the sub-tree induced by `the_node`\n
    `top_x_coordinate`: x coordinate of node's center top\n
    `top_y_coordinate`: y coordinate of node's center top
    '''

    if 'word' in the_node:

        # role、詞性 要對齊垂直線置中 !
        # 畫 role
        if 'role' in the_node:
            draw_api.text((top_x_coordinate - the_node['width']/2, top_y_coordinate), the_node['role'], fill=(0,0,0), font=display_fnt)
            top_y_coordinate += word_height
        # 畫 詞性
        draw_api.text((top_x_coordinate - the_node['width']/2, top_y_coordinate), the_node['pos'], fill=(0,0,0), font=display_fnt)
        # 畫 垂直線
        top_y_coordinate += word_height
        top_y_coordinate += vertical_small_space
        draw_api.line([top_x_coordinate, top_y_coordinate, top_x_coordinate, top_y_coordinate + relation_line_height], fill=(0,0,0), width=1)
        # 畫 實詞
        top_y_coordinate += relation_line_height
        draw_api.text((top_x_coordinate - display_fnt.getsize(the_node['word'])[0]/2, top_y_coordinate), the_node['word'], fill=(0,0,0), font=display_fnt)
    else:
        # 畫 role、 詞性 (可能 兩個都有 或 只有其中一個)
        if 'role' in the_node and 'pos' in the_node:
            draw_api.text((top_x_coordinate - the_node['width']/2, top_y_coordinate), the_node['role'], fill=(0,0,0), font=display_fnt)
            draw_api.text((top_x_coordinate - the_node['width']/2, top_y_coordinate + word_height), the_node['pos'], fill=(0,0,0), font=display_fnt)
        elif 'pos' in the_node:
            draw_api.text((top_x_coordinate - the_node['width']/2, top_y_coordinate), the_node['pos'], fill=(0,0,0), font=display_fnt)
        else:
            draw_api.text((top_x_coordinate - the_node['width']/2, top_y_coordinate + word_height), the_node['role'], fill=(0,0,0), font=display_fnt)
        
        # 畫 連接到child的線
        if len(the_node['child']) == 1:
            child_top_x_coordinate = top_x_coordinate
            if spec == 'CKIP':
                child_top_y_coordinate = top_y_coordinate + (the_node['height'] - the_node['child'][0]['height']) * one_level_height
                if 'role' not in the_node:
                    child_top_y_coordinate -= word_height
            else:
                child_top_y_coordinate = top_y_coordinate + (the_node['height'] - the_node['child'][0]['height']) * pos_level_height

            # 畫 垂直線
            draw_api.line([top_x_coordinate, top_y_coordinate + one_node_text_height - (0 if 'role' in the_node else word_height), top_x_coordinate, child_top_y_coordinate], fill=(0,0,0), width=1)
            
            # Recursive draw
            draw_node(draw_api, the_node['child'][0], child_top_x_coordinate, child_top_y_coordinate, spec)
        else:
            left_margin_x_coordinate = top_x_coordinate - the_node['tree-width']/2

            for its_child_node in the_node['child']:
                child_top_x_coordinate = left_margin_x_coordinate + its_child_node['tree-width']/2
                if spec == 'CKIP':
                    child_top_y_coordinate = top_y_coordinate + (the_node['height'] - its_child_node['height']) * one_level_height
                    if 'role' not in the_node:
                        child_top_y_coordinate -= word_height
                else:
                    child_top_y_coordinate = top_y_coordinate + (the_node['height'] - its_child_node['height']) * pos_level_height

                # 需畫 斜線與垂直線
                draw_api.line([top_x_coordinate, top_y_coordinate + one_node_text_height - (0 if 'role' in the_node else word_height) , child_top_x_coordinate, top_y_coordinate + one_node_text_height - (0 if 'role' in the_node else word_height) + relation_line_height, child_top_x_coordinate, child_top_y_coordinate], fill=(0,0,0), width=1)

                # Recursive draw
                draw_node(draw_api, its_child_node, child_top_x_coordinate, child_top_y_coordinate, spec)

                left_margin_x_coordinate += (its_child_node['tree-width'] + between_box_space)

def get_img_base64_string(image_object):
    '''
    將 `Image` 物件儲存成jpeg格式，並將內容使用 base64編碼成字串，回傳
    '''
    byte_buffer = BytesIO()
    image_object.save(byte_buffer, format="JPEG")
    base64_str = str(base64.b64encode(byte_buffer.getvalue()))
    image_base64_str = base64_str[2:-1]

    return image_base64_str