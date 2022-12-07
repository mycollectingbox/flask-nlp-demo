import requests, time, json

def build_stanford_parse_tree(parsing_string):
    '''
    Return the root node.\n
    It's attributes are defined by dictionary key.\n
    Node attributes are `pos`, `word`, `depth`, `parent`, `child`, `id`
    '''

    parent_node = None
    current_node = {'id': -1, 'depth': -1, 'parent': None} # initial super root

    node_queue = list()
    txt = ''
    node_id = 0

    # (ROOT (S (NP (PRP$ My) (NN dog)) (ADVP (RB also)) (VP (VBZ likes) (S (VP (VBG eating) (NP (NN sausage))))) (. .)))
    for char in parsing_string:

        if char == '(':
            parent_node = current_node
            if 'child' not in parent_node:
                parent_node['child'] = list()

            current_node = {}
            current_node['parent'] = parent_node
            current_node['depth'] = parent_node['depth'] + 1
            node_queue.append(parent_node)
        
        elif char == ')':

            if len(txt) > 0:
                current_node['word'] = txt
                txt = ''

            parent_node['child'].append(current_node)

            current_node = node_queue.pop()
            parent_node = current_node['parent']

        elif char == ' ':
            if 'pos' not in current_node:
                current_node['pos'] = txt
                txt = ''

        else:
            txt += char

    current_node['child'][0]['parent'] = None

    return current_node['child'][0]

def build_ckip_parse_tree(parsing_string):
    '''
    Return the root node.\n
    It's attributes are defined by dictionary key.\n
    Node attributes are `role`, `pos`, `word`, `depth`, `parent`, `child`, `id`\n
    Leaf node has word positional `index` attribute
    '''
    
    parent_node = None
    current_node = {'id': -1, 'depth': 0, 'parent': None}

    node_queue = list()
    txt = ''
    node_id = 0
    word_position = 0
    
    # VP(time:PP(Head:P43:根據|DUMMY:S(agent:NP(Head:Nba:聯合報)|time:Ndda:日前|Head:VE2:報導))|Head:VE2:指出)
    # S(agent:NP(property:Nab:痞客邦|property:Ncc:旗下|quantifier:Neu:７|property:NP(property:NP•的(head:NP(Nba:Headlines|Head:Nc:網站)|Head:DE:的)|property:Nac:網路|apposition:Nv:票選|Head:Nac:活動)|Head:Nc:中港台)|degree:Dfa:最|agent:NP(property:Nad:時尚|Head:Ncb:機場)|Head:VC:穿搭|goal:NP(property:Nab:女|property:Nab:藝人|Head:Nab:代表))
    # S(agent:NP(Head:Nba:湛錦源)|Head:VE2:表示)#，(COMMACATEGORY)
    for char in parsing_string:
        if char == '(':
            # prevent word is a (
            # Ex: %(apposition:Nba:(|property:VC31:生)
            if len(txt) > 0:
                node_queue.append(parent_node)
                current_node['child'] = list()
                current_node['pos'] = txt
                txt = ''

                parent_node = current_node
                current_node = {}
                current_node['parent'] = parent_node
                current_node['depth'] = parent_node['depth'] + 1
            else:
                txt += char

        elif char == ':':
            if 'role' in current_node:
                current_node['pos'] = txt
            else:
                current_node['role'] = txt
            txt = ''
        
        elif char == '|' or char == ')':
            if len(txt) > 0:
                current_node['word'] = txt
                current_node['index'] = word_position
                word_position += len(txt)
                txt = ''

                # what if ckip omits a pos or role, assume it omits role 
                if 'pos' not in current_node:
                    current_node['pos'] = current_node['role']
                    del current_node['role']
                
            parent_node['child'].append(current_node)
            current_node['id'] = node_id
            node_id += 1

            if char == ')':
                current_node = parent_node
                parent_node = node_queue.pop()
                # no need to care remaining characters
                if parent_node == None:
                    break
            else:
                current_node = {}
                current_node['parent'] = parent_node
                current_node['depth'] = parent_node['depth'] + 1

        else:
            txt += char
    
    if 'child' in current_node:
        if 'role' not in current_node:
            # check whether 'role' is recognized to 'pos'
            # Example: conjunction(Head:Cbca:所以)
            if current_node['pos'][0] in 'abcdefghijklmnopqrstuvwxyz' or current_node['pos'] == 'Head':
                current_node['role'] = current_node['pos']
                del current_node['pos']

    return current_node

def build_jimmy_parse_tree(parsed_stree_str):

    # 肯塔基州立大學[Named_University]{肯塔基[GPEcascade]{肯塔基[GPE]}州立[EstablishType]大學[UniversityPhrase]{大學[UniversityWord]}}
    parentNode = None
    currentNode = {}

    depth = 0
    tmp_sb = ''
    for ch in parsed_stree_str:
        if ch == '[':
            if 'word' in currentNode:
                currentNode = {}
            currentNode['word'] = tmp_sb
            currentNode['depth'] = depth
            tmp_sb = ''
        elif ch == ']':
            currentNode['pos'] = tmp_sb
            tmp_sb = ''
            currentNode['parent'] = parentNode

            if parentNode != None:
                if 'child' not in parentNode:
                    parentNode['child'] = []
                parentNode['child'].append(currentNode)
        elif ch == '{':
            parentNode = currentNode
            currentNode = {}
            depth += 1
            parentNode['child'] = []
        elif ch == '}':
            depth -= 1
            currentNode = parentNode
            parentNode = parentNode['parent']
        else:
            tmp_sb += ch
        
    return currentNode

def get_leaf_nodes(the_root_node):
    '''
    給定 `the_root_node`: tree 的 根結點\n
    Return `list` of 葉子節點
    '''

    the_leaf_nodes = list()
    collect_leaf_nodes_helper(the_root_node, the_leaf_nodes)

    return the_leaf_nodes

def collect_leaf_nodes_helper(currentNode, the_leaf_node_list):
    if 'child' in currentNode and len(currentNode['child']) > 0:
        for its_child in currentNode['child']:
            collect_leaf_nodes_helper(its_child, the_leaf_node_list)
    else:
        # this is a leaf node
        the_leaf_node_list.append(currentNode)

def get_sentence(the_root_node, form='ckip'):
    '''
    Get the source sentence from the given parse tree data structure.
    '''

    if form == 'ckip':
        txt = ''
        for _leafnode in get_leaf_nodes(the_root_node):
            txt += _leafnode['word']
        return txt
    elif form == 'stanford':
        txt = ''
        for _leafnode in get_leaf_nodes(the_root_node):
            txt += ' ' + _leafnode['word']
        return txt.lstrip()

def get_sentence_from_parse2(parsing_string):
    sentence = ''
    role = None
    pos = None
    txt = ''
    for char in parsing_string:
        if char == '(':
            if len(txt) > 0:
                pos = txt
                role = None
                txt = ''
            else:
                txt += char
        elif char == ':':
            if role is None:
                role = txt
            else:
                pos = txt
            txt = ''
        elif char == '|' or char == ')':
            if len(txt) > 0:
                sentence += txt
                txt = ''
                
            role = None
            pos = None
        else:
            txt += char
    return sentence

__show_order = ['role', 'pos', 'word', 'id', 'depth', 'height']
def print_node(node, level=0, ch_indent = '   '):
    
    if level:
        print(ch_indent*level+ 'L' + len(ch_indent)*'_')
        prefix = ch_indent*(level+1) + '|'
    else:
        prefix = ''

    for attribute in __show_order:
        v = node.get(attribute, None)
        if v is not None:
            print(prefix + attribute, v)
    for child in node.get('child',[]):
        print_node(child, level+1, ch_indent)


'''
(ROOT 
    (S 
        (NP (PRP$ My) (NN dog))
        (ADVP (RB also)) 
        (VP (VBZ likes) 
            (S 
                (VP (VBG eating) 
                    (NP (NN sausage))))) 
        (. .)))
'''

def print_tree(node):
    return ''.join(print_tree_recursive(node))

def print_tree_recursive(node, indent='    '):
    ret = []

    if 'word' in node:
        ret.append('(' + node['pos'] + ' ' + node['word'] + ')')
    else:
        if 'pos' not in node:
            ret.append(indent*node['depth'] + '(' + node['role'])
        else:
            ret.append(indent*node['depth'] + '(' + node['pos'])
        
        needNewLine = False
        for childNode in node['child']:
            if 'word' in childNode:
                if needNewLine:
                    ret.append('\n')
                    ret.append(indent*childNode['depth'])
                    ret.extend(print_tree_recursive(childNode, indent))
                else:
                    ret.append(' ')
                    ret.extend(print_tree_recursive(childNode, indent))
            else:
                needNewLine = True
                ret.append('\n')
                ret.extend(print_tree_recursive(childNode, indent))
        ret.append(')') # 收尾
    return ret

def convert_to_stanford_parsed_string(node):
    '''
    轉換成 stanford parse tree string 格式
    '''
    if 'child' in node:
        sub_parts = []
        for child_node in node['child']:
            sub_parts.append(convert_to_stanford_parsed_string(child_node))
        return '({0} {1})'.format(node['pos'], ' '.join(sub_parts))
    else:
        return '({0} {1})'.format(node['pos'], node['word'])

def get_node_pos(node):
    '''
    Ex: Head:VD2[+NEG]:搶不到 --> VD2
    '''
    if 'pos' not in node:
        return None
    node_PoS = node['pos']
    return node_PoS[:node_PoS.find('[')] if '[' in node_PoS else node_PoS

def get_node_role(node):
    '''
    Ex: topic[+goal]  --> topic
    '''
    node_role = node['role']
    return node_role[:node_role.find('[')] if '[' in node_role else node_role



def get_node_string(node):
    '''
    Return node's ckip parse representation
    '''
    if 'word' in node:
        if 'role' in node:
            return '{}:{}:{}'.format(node['role'], node['pos'], node['word'])
        else:
            return '{}:{}'.format(node['pos'], node['word'])
    else:
        sub_sb = [get_node_string(childNode) for childNode in node['child']]
        if 'role' in node:
            sb = '{}:{}({})'.format(node['role'], node['pos'], '|'.join(sub_sb))
        else:
            sb = '{}({})'.format(node['pos'], '|'.join(sub_sb))
        return sb

def get_node_syntax(node, enclosed=True):
    '''
    Print the syntax of this `node`.\n
    Ex: time:GP(DUMMY:NP(Head:Nab:心)|Head:Ng:裡) ==> `[NP]:Ng`\n
    When `enclosed` = False,\n
    Ex: time:GP(DUMMY:NP(Head:Nab:心)|Head:Ng:裡) ==> NP:Ng\n
    '''
    if 'word' in node:
        return node['pos']
    else:
        if enclosed:
            syntax_list = [childNode['pos'] if 'word' in childNode else '[' + childNode['pos']  + ']' for childNode in node['child']]
        else:
            syntax_list = [childNode['pos'] for childNode in node['child']]
        return ':'.join(syntax_list)

def get_node_syntax_components(node):
    '''
    return the syntax of this node as a `list`\n
    ['[VP]', 'Dbab', 'V_2', '[NP]']
    '''
    syntax_list = []
    if 'word' in node:
        syntax_list.append(node['pos'])
    else:
        syntax_list = [childNode['pos'] if 'word' in childNode else '[' + childNode['pos']  + ']' for childNode in node['child']]
    return syntax_list

def elementary_phrase_finder_recursive(mNode, phType='NP'):
    '''
    Return a list of `node` of phType, that is minimal
    '''
    ret = []

    if 'pos' in mNode:
        if mNode['pos'] == phType:
            # check each child is a leaf
            is_all_leaf = True
            if 'child' in mNode:
                for childNode in mNode['child']:
                    if 'word' not in childNode:
                        is_all_leaf = False
                        break
            else:
                is_all_leaf = False
            
            if is_all_leaf:
                ret.append(mNode)
                return ret

    if 'child' in mNode:
        for childNode in mNode['child']:
            ret += elementary_phrase_finder_recursive(childNode, phType)

    return ret

def is_elementary_phrase(mNode):
    '''
    True if phrase is elementary. Leaf node will be False.
    '''
    if 'child' in mNode:
        is_all_leaf = True
        for child_node in mNode['child']:
            if 'child' in child_node and get_node_pos(child_node) != 'DM':
                is_all_leaf = False
                return False
                
        if is_all_leaf:
            return True

    return False


def get_ehow_data(sourcefilePath):
    ehow = {}
    with open(sourcefilePath, 'r', encoding='utf8') as sr:
        for line in sr:
            columns = line.strip('\n').split('\t')
            
            word = columns[0]
            part_of_speech = columns[1]
            sense = columns[2]
            if word not in ehow:
                ehow[word] = {}
            if part_of_speech not in ehow[word]:
                ehow[word][part_of_speech] = set()
            ehow[word][part_of_speech].add(sense)
    return ehow

def get_all_specific_phrases(mNode, phTypes):
    '''
    Return a list of `node` of phTypes
    '''
    ret = []
    if 'pos' in mNode:
        if mNode['pos'] in phTypes:
            ret.append(mNode)
    if 'child' in mNode:
        for childNode in mNode['child']:
            ret.extend(get_all_specific_phrases(childNode, phTypes))
            
    return ret


def get_specific_role_childs(mNode, want_rolename, start_index=0):
    main_list = []
    if 'child' in mNode:
        for _child in mNode['child'][start_index:]:
            child_role_name = _child['role']
            if child_role_name.find('[') > 0:
                child_role_name = child_role_name[:child_role_name.find('[')]
            if child_role_name == want_rolename:
                main_list.append(_child)

    return main_list


def get_the_only_Head_index(node_list):
    '''
    return (index of only Head node, amount of Head)\n
    return -1 if not found or multiple Head
    '''
    index_list = []
    for i, node in enumerate(node_list):
        if 'role' in node:
            if node['role'] == 'Head':
                index_list.append(i)

    if len(index_list) == 1:
        return index_list[0], len(index_list)
    else:
        return -1, len(index_list)



def get_VP_DUMMY_Head_recursive(phNode):
    '''
    回傳 (Flag, list of head nodes, list of Caa word)
    '''
    if 'word' in phNode:
        return True, [phNode], []

    if 'child' not in phNode:
        return False, [], []
    else:
        if len(phNode['child']) == 1:
            bOK, dummy_nodes, inner_caa_list = get_VP_DUMMY_Head_recursive(phNode['child'][0])
            if not bOK:
                return False, [], []
            else:
                return True, dummy_nodes, inner_caa_list

    
    head_idx, _ = get_the_only_Head_index(phNode['child'])

    if head_idx == -1:
        return False, [], []
    else:
        head_node = phNode['child'][head_idx]
        if head_node['pos'] != 'Caa':
            return False, [], []
    
    caa_word_list = [head_node['word']]

    dummys = get_NP_DUMMY_childs(phNode)
    if len(dummys) != 2:
        return False, [], []
    ret = []
    for _dummy in dummys:
        bOK, dummy_nodes, inner_caa_list = get_VP_DUMMY_Head_recursive(_dummy)
        caa_word_list.extend(inner_caa_list)
        if not bOK:
            return False, [], []
        else:
            ret.extend(dummy_nodes)
    return True, ret, caa_word_list
    
def get_NP_Head_recursive(np_node):
    '''
    找出 NP 最重要的部分\n
    return (a list of nodes, list of Caa nodes).\n
    (Assume the node is a NP)
    '''
    result_node = []

    # base case
    if 'word' in np_node:
        if np_node['pos'][0] == 'N':
            # exclude some part of speech to be a valid Head
            if np_node['pos'].startswith('Ncd'):
                if np_node['pos'] == 'Ncdb':
                    result_node.append(np_node)
                elif np_node['pos'] == 'Ncda':
                    pass
                elif len(np_node['word'])> 1:
                    result_node.append(np_node)
            elif np_node['pos'] == 'Neqa':
                result_node.append(np_node)
            elif np_node['pos'] != 'Ng' and not np_node['pos'].startswith('Nf') and not np_node['pos'].startswith('Ne'):
                result_node.append(np_node)
        return result_node, []
    
    # has childs case
    childs = np_node['child']
    last = childs[-1]
    if 'role' not in last:
        return [], []
    if last['role'] == 'Head' and last['pos'] != 'Cab':
        return get_NP_Head_recursive(last)

    # get first Head node
    first_Head_node = None
    for child_node in childs:
        if get_node_role(child_node) == 'Head':
            first_Head_node = child_node
            break
    if first_Head_node == None:
        return result_node, []

    if first_Head_node['pos'] == 'Caa':
        # DUMMY1 Caa DUMMY2
        Caa_list = []
        dummy_childs = get_NP_DUMMY_childs(np_node)
        for k, part in enumerate(dummy_childs):
            inner_heads, inner_Caas = get_NP_Head_recursive(part)
            result_node.extend(inner_heads)
            Caa_list.extend(inner_Caas)

            if k == 0:
                if 'word' not in first_Head_node:
                    return [], []
                Caa_list.append(first_Head_node)

        return result_node, Caa_list
    elif first_Head_node['pos'] == 'Cab':
        dummy_childs = get_NP_DUMMY_childs(np_node)
        if len(dummy_childs) != 1:
            return result_node, []
        dummyNP = dummy_childs[0]
        result_node.extend(get_NP_Head_recursive(dummyNP)[0])
    elif first_Head_node['pos'].startswith('Nd'):
        # goal:NP(property:Ndabe:上午|Head:Nd:7時|quantifier:Neqb:許)
        result_node.append(first_Head_node)
        return result_node, []

    return result_node, []



def get_NP_DUMMY_childs(np_node):
    dummy_childs = []
    for child_node in np_node['child']:
        if 'role' not in child_node:
            continue

        if child_node['role'].startswith('DUMMY'):
            dummy_childs.append(child_node)

    return dummy_childs

def isAnyThisPartOfSpeech(node_list, testPartOfSpeech):
    '''
    檢查 `node_list` 是否其一有相同的詞類(由`testPartOfSpeech`指定) ? 
    '''
    if len(node_list) == 0:
        return False
    for node in node_list:
        if node['pos'].startswith(testPartOfSpeech):
            return True

    return False

def isAllTheSamePartOfSpeech(node_list, testPartOfSpeech):
    '''
    檢查 `node_list` 是否有相同的詞類(由`testPartOfSpeech`指定) ? 
    '''
    if len(node_list) == 0:
        return False

    for node in node_list:
        if not node['pos'].startswith(testPartOfSpeech):
            return False

    return True

def isAllTheSamePartOfSpeech_string(string_list, testPartOfSpeech):
    '''
    檢查 `string_list` 是否有相同的詞類(由`testPartOfSpeech`指定) ? 
    '''
    if len(string_list) == 0:
        return False

    for pos_string in string_list:
        if not pos_string.startswith(testPartOfSpeech):
            return False

    return True

def get_childs_with_same_partOfSpeech(node, testPartOfSpeech):
    if 'child' not in node:
        return []

    hit_child_list = []
    for _child in node['child']:
        if _child['pos'].startswith(testPartOfSpeech):
            hit_child_list.append(_child)
    return hit_child_list




def get_reduction_word_from_list(rlist):
    '''
    從 nest list 結構，轉成單純 word list\n
    Ex: [["學"], ["畫"]] ==> ["學", "畫"]
    '''
    merge_list = []

    for item in rlist:
        if isinstance(item, list):
            merge_list.extend(get_reduction_word_from_list(item))
        else:
            merge_list.append(item)
            
    return merge_list


def join_by_multi_seperator(word_list, seps):
    '''
    return list of words with seps
    '''
    
    if len(word_list) != len(seps) + 1:
        return []

    final = []
    for i, word in enumerate(word_list):
        final.append(word)
        if i < len(seps):
            final.append(seps[i])
    return final

def flatten_nested_list(nList):
    merge_list = []
    for item in nList:
        if isinstance(item, list):
            merge_list.extend(get_reduction_word_from_list(item))
        else:
            merge_list.append(item)

    return merge_list

def get_parse_from_web(sentence, wait=True):
    headers = {
        'content-type': 'application/json;charset=UTF-8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    }
    payload = '{{ "text": "{0}" }}'.format(sentence)

    try:
        response = requests.post(
            'https://ckip.iis.sinica.edu.tw/api/corenlp/?conparse=5', 
            headers = headers, 
            data = payload.encode('utf-8'), 
            timeout = 12) # 12 seconds
    except requests.exceptions.Timeout as e: 
        raise Exception(str(e))
        
    root = json.loads(response.text)
    if wait:
        time.sleep(1)

    return root['conparse'][0]


class BaseToken:
    '''
    由 文字、文字位置、文字詞性 組成
    '''
    def __init__(self, position, word, part_of_speech):
        self.position = position
        self.word = word
        self.part_of_speech = part_of_speech

    def end(self):
        return self.position + len(self.word)


    @classmethod
    def from_node_dict(cls, node):
        return BaseToken(node['index'], node['word'], node['pos'])


class ChracterUtility:

    @classmethod
    def IsChineseWord(cls, text):
        '''
        是否為中文字?
        '''

        for character in text:
            encodingNumber = ord(character)
            # Unicode block: CJK Unified Ideographs
            if encodingNumber < 0x4E00 or encodingNumber > 0x9FFF:
                return False
        return True

    @classmethod
    def IsChineseOrDigit(cls, text):
        for character in text:
            encodingNumber = ord(character)
            # Unicode block: CJK Unified Ideographs
            if encodingNumber > 0x9FFF:
                return False
            elif encodingNumber < 0x30:
                return False
            elif encodingNumber > 0x39 and encodingNumber < 0x4E00:
                return False
        return True

    @classmethod
    def IsSuitableForParse(cls, text):
        '''
        允許 中文字、半全形阿拉伯數字(0~9)、中文頓號、小數點(.)
        # Unicode block: CJK Unified Ideographs  4E00~9FFF
        # Unicode block: CJK Compatibility Ideographs  F900~FAFF (中文只到 FA6D)
        # half-width digit & 小數點 & 斜線: 2E~39
        # Full-width digit: FF10~FF19
        # 中文頓號: 3001
        # 
        '''
        for character in text:
            encodingNumber = ord(character)
            if encodingNumber > 0xFF19:
                return False
            elif encodingNumber < 0xFF10 and encodingNumber > 0xFAFF:
                return False
            elif encodingNumber < 0xF900 and encodingNumber > 0x9FFF:
                return False
            elif encodingNumber < 0x4E00 and encodingNumber > 0x3001:
                return False
            elif encodingNumber < 0x3001 and encodingNumber > 0x39:
                return False
            elif encodingNumber < 0x2E:
                return False
        return True


class CKIPUtility:
    def __init__(self):
        self.converter = {}

        with open('./appdata/CKIP_POS.txt', 'r', encoding='utf8') as sr:
            sr.readline()
            for line in sr:
                line = line.strip('\n')
                columns = line.split('\t')

                self.converter[columns[1]] = columns[2]

    def simplified_part_of_speech(self, partofspeech):
        if partofspeech in self.converter:
            return self.converter[partofspeech]
        else:
            return partofspeech

if __name__ == '__main__':
    parse_example = 'S(theme:NP(property:Ndaad:1981年|Head:Nba:黃平洋)|Head:VK2:代表|goal:S(agent:NP(property:Nca:中華|Head:Nab:成棒)|frequency:DM:多次|Head:VC2:|Head:Caa:、|DUMMY2:Nba:世界盃)|Head:Caa:、|DUMMY2:NP(DUMMY:NP(Head:Nba:奧運)|Head:Cab:等))|complement:VP(condition:GP(DUMMY:NP(property:VH11:重大|property:Ncc:國際|property:Nab:棒球|Head:Nab:賽事)|Head:Ng:中)|Head:VH11:大放異彩)))'
    build_ckip_parse_tree(parse_example)