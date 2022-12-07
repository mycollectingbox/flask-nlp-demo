from .parse_utility import *
from collections import defaultdict


class FB_extrator:

    def __init__(self):
        # log format: key: message category, Value: list of messageTuple(reason, node)
        self.VALUE_PREPROCESS = '前處理'
        self.VALUE_HEAD = 'Head V'
        self.VALUE_PATTERN = '句型'
        self.VALUE_TIMEWORD = '時間詞'
        self.logs = defaultdict(list)

        self.general_v_arg_role = {
            'agent', 'experiencer', 'theme', 'goal', 'target', 'beneficiary', 
            'companion', 'source', 'comparison', 'causer', 'topic', 'range' }
        
        self.verb_pattern_dict = {
            'VA11': [
                [('*', 'theme', True), ('VA11', 'Head', True)],
                [('VA11', 'Head', True), ('NP', 'theme', True)]],
            'VA12': [
                [('*', 'theme', True), ('VA12', 'Head', True)], 
                [('VA12', 'Head', True), ('NP', 'theme', True)]],
            'VA13': [[('*', 'theme', True), ('VA13', 'Head', True)]],
            'VA2': [
                [('*', 'theme', True), ('VA2', 'Head', True)],
                [('*','causer', False), ('VA2', 'Head', True), ('*', 'theme', True)]],	
            'VA3': [[('*','theme', True), ('VA3', 'Head', True)]],
            'VA4': [
                [('*','agent', True), ('VA4', 'Head', True)]],
            'VB11': [
                [('{NP,PP[由]}', 'agent', True), ('PP{把,將,朝,向,給,幫,為,替,以}', 'goal', True), ('VB11', 'Head', True)],
                [('{NP,PP[由]}', 'agent', True), ('VB11', 'Head', True), ('PP[給]', 'goal', True, '#')],
                [('NP', 'goal', True, 'X'), ('{PP,P{被,給}}', 'agent', True), ('VB11', 'Head', True)],
                [('{NP,PP{關於,至於}}', 'goal', True, 'X'), ('{NP,PP[由]}', 'agent', True), ('VB11', 'Head', True)]],
            'VB12': [
                [('NP', 'goal', True), ('VB12', 'Head', True)],
                [('{NP,PP[由]}', 'agent', True), ('PP{把,將,朝,向,給,幫,為,替}', 'goal', True), ('VB12', 'Head', True)],
                [('NP', 'goal', True), ('{PP,P{被,給}}', 'agent', True), ('VB12', 'Head', True)]],
            'VB2': [
                [('{NP,PP[由]}', 'agent', True), ('PP{把,將}', 'theme', True), ('VB2', 'Head', True)],
                [('{NP,PP[由]}', 'agent', True), ('VB2', 'Head', True), ('PP[給]', 'theme', True)],
                [('NP', 'theme', True, 'X'), ('{PP,P{被,給}}', 'agent', True), ('VB2', 'Head', True)]],
            'VC1': [
                [('{NP,PP[由]}', 'theme', True), ('VC1', 'Head', True), ('{NP,PP,GP}', 'goal', True)]],	
            'VC2': [
                [('{NP,PP[由]}', 'agent', True), ('VC2', 'Head', True), ('{NP,DM}', 'goal', True)],           # 大量遊客破壞公園景觀; 用了5元
                [('{NP,PP[由]}', 'agent', True), ('PP', 'goal', True), ('VC2', 'Head', True)],	
                [('{NP,PP[由]}', 'agent', True), ('PP', 'goal', True), ('VC2', 'Head', True), ('{NP,DM}', 'theme', False)]],
            'VC31': [
                [('{NP,PP[由]}', 'agent', True), ('VC31', 'Head', True), ('{NP,DM}', 'theme', True)],
                [('{NP,PP[由]}', 'agent', True), ('PP', 'theme', True), ('VC31', 'Head', True)], 
                [('{NP,PP[由]}', 'agent', True), ('VC31', 'Head', True), ('NP', 'source', False), ('{NP,DM}', 'theme', True)], 
                [('{NP,PP[由]}', 'agent', True), ('PP{向,跟}', 'source', False),('VC31', 'Head', True), ('{NP,DM}', 'theme', True)],
                [('{NP,PP[由]}', 'agent', True), ('PP{對,向}', 'goal', False), ('VC31', 'Head', True), ('NP', 'theme', True)],	
                [('{NP,PP[由]}', 'agent', True), ('PP', 'theme', True), ('VC31', 'Head', True), ('PP[在]', 'goal', False, '#')]],	
            'VC32': [
                [('{NP,PP[由]}', 'agent', True), ('VC32', 'Head', True), ('{NP,DM}', 'theme', True)]],
            'VC33': [
                [('{NP,PP[由]}', 'agent', True), ('VC33', 'Head', True), ('{NP,DM}', 'theme', True)],
                [('VC33', 'Head', True), ('{NP,DM}', 'theme', True)]],
            'VD1': [
                [('{NP,PP[由]}', 'agent', True), ('VD1', 'Head', True), ('NP', 'goal', True), ('{NP,DM}', 'theme', True)],
                [('{NP,PP[由]}', 'agent', True), ('VD1', 'Head', True), ('PP[給]', 'goal', True, '#'), ('{NP,DM}', 'theme', True)], 
                [('{NP,PP[由]}', 'agent', True), ('VD1', 'Head', True), ('{NP,DM}', 'theme', True), ('PP[給]', 'goal', True, '#')]],
            'VD2': [
                [('{NP,PP[由]}', 'agent', True), ('VD2', 'Head', True), ('NP', 'source', True), ('{NP,DM}', 'theme', True)], 
                [('{NP,PP[由]}', 'agent', True), ('PP{向,跟}', 'source', True), ('VD2', 'Head', True), ('{NP,DM}', 'theme', True)]],	
            'VE11': [[('{NP,PP[由]}', 'agent', True), ('VE11', 'Head', True), ('NP', 'goal', True), ('{NP,VP,S}', 'theme', True)]],
            'VE12': [[('{NP,PP[由]}', 'agent', True), ('VE12', 'Head', True), ('NP', 'goal', True), ('{NP,VP,S}', 'theme', True)]],
            'VE2': [[('{NP,PP[由]}', 'agent', True), ('VE2', 'Head', True), ('{S,VP,NP}', 'goal', True)]],
            'VF1': [[('NP', 'agent', True), ('VF1', 'Head', True), ('VP', 'goal', True)]],
            'VF2': [[('{NP,PP[由]}', 'agent', True), ('VF2', 'Head', True), ('NP', 'goal', True), ('{VP,NP}', 'theme', True)]],	
            'VG1': [
                [('NP', 'agent', True), ('VG1', 'Head', True), ('NP', 'theme', True), ('NP', 'range', True, '#')], 
                [('NP', 'agent', True), ('VG1', 'Head', True), ('NP', 'theme', True), ('PP{為,作}', 'range', True, '#')]],
            'VG2': [
                [('*', 'theme', True), ('VG2', 'Head', True), ('{NP,VP,S}', 'range', True)],
                [('*', 'theme', True), ('VG2', 'Head', True), ('PP{為,作}', 'range', True, '#')]],	
            'VH11':[[('*', 'theme', True), ('VH11', 'Head', True)]],
            'VH12':[[('*', 'theme', True), ('VH12', 'Head', True), ('*', 'range', True)]],	
            'VH13':[
                [('*', 'theme', True), ('VH13', 'Head', True), ('{NP,Na*,Nb*,Nc*,Nd*,Ne*,Nh*}', 'comparison', True), ('*', 'range', True)],          # 他高我10公分
                [('*', 'theme', True), ('PP', 'comparison', False), ('VH13', 'Head', True), ('*', 'range', True)]],         # 爸爸比叔叔高10公分	
            'VH14':[
                [('*', 'theme', True), ('VH14', 'Head', True)],
                [('VH14', 'Head', True), ('NP', 'theme', True)]],
            'VH15':[
                [('{VP,S}', 'theme', True), ('VH15', 'Head', True)],
                [('VH15', 'Head', True), ('{VP,S}', 'theme', True)],	
                [('NP', 'topic', False), ('VH15', 'Head', True), ('{VP,S}', 'theme', True)]],	
            'VH16':[
                [('NP', 'theme', True), ('VH16', 'Head', True)],
                [('{NP,VP,S}', 'causer', False), ('VH16', 'Head', True), ('NP', 'theme', True)]],
            'VH17':[[('*', 'recipient', False), ('VH17', 'Head', True), ('NP', 'theme', True)]],
            'VH21':[[('VH21', 'experiencer', True), ('VH21', 'Head', True)]],
            'VH22':[
                [('{NP,GP}', 'experiencer', True), ('VH22', 'Head', True)],
                [('{NP,VP,S}', 'causer', False), ('VH22', 'Head', True),  ('NP', 'experiencer', True)]],
            'VI1': [
                [('*', 'experiencer', True), ('PP[對]', 'goal', True), ('VI1', 'Head', True)],		
                [('*', 'experiencer', True), ('VI1', 'Head', True), ('PP[於]', 'goal', True)]],
            'VI2': [
                [('*', 'theme', True), ('PP{對,以}', 'goal', True), ('VI2', 'Head', True)],
                [('*', 'theme', True), ('VI2', 'Head', True), ('PP[於]', 'goal', True)]],
            'VI3': [
                [('*', 'theme', True), ('VI3', 'Head', True), ('PP{自,於}', 'source', True, '#')],	
                [('*', 'theme', True, 'X'), ('PP{歸,為}', 'source', True), ('VI3', 'Head', True)]],
            'VJ1': [
                [('*', 'theme', True), ('VJ1', 'Head', True), ('NP', 'goal', True)],
                [('*', 'theme', True), ('PP', 'goal', True), ('VJ1', 'Head', True)],
                [('*', 'theme', True), ('VJ1', 'Head', True), ('NP', 'goal', True), ('*','range', True)],
                [('*', 'theme', True), ('VJ1', 'Head', True), ('*','range', True)]],	
            'VJ2': [
                [('*', 'experiencer', True), ('VJ2', 'Head', True), ('NP', 'goal', True)],
                [('*', 'experiencer', True), ('PP', 'goal', True), ('VJ2', 'Head', True)]],	
            'VJ3': [[('*', 'theme', True), ('VJ3', 'Head', True), ('*', 'range', True)]],
            'VK1': [[('*', 'experiencer', True), ('VK1', 'Head', True), ('{NP,S,VP}', 'goal', True)]],
            'VK2': [[('{NP,VP,S}', 'theme', True), ('VK2', 'Head', True), ('{NP,S,VP}', 'goal', True)]],	
            'VL1': [[('NP', 'experiencer', True), ('VL1', 'Head', True), ('{VP,NP}', 'goal', True)]],	
            'VL2': [[('NP', 'theme', True), ('VL2', 'Head', True), ('{VP,NP}', 'goal', True)]],
            'VL3': [
                [('VL3', 'Head', True), ('NP', 'goal', True), ('VP', 'theme', True)],	
                [('NP', 'topic', False), ('VL3', 'Head', True), ('*', 'goal', True), ('VP', 'theme', True)]],	
            'VL4': [[('{NP,VP,S}', 'causer', True), ('VL4', 'Head', True), ('NP', 'goal', True), ('VP', 'theme', True)]]
        }

        self.passiveVerb_pattern_dict = {
            'VC2': {
                'S': [
                    ([('{NP,PP[由]}', 'agent', True, 'V_left'), ('PP', 'goal', True, 'V_right'), ('VC2', 'Head', True)], 'PP:goal:{把,將}'),
                    ([('{NP,PP[由]}', 'agent', True, 'V_left'), ('PP', 'goal', False), ('VC2', 'Head', True), ('NP', 'theme', True, 'V_right')], 'PP:goal:{把,將}'),
                    ([('NP', 'goal', True, 'V_right'), ('{PP,P{被,給,挨,遭}}', 'agent', True, 'V_left'), ('VC2', 'Head', True)], '{PP,P}:agent:{被,給,挨,遭}'),
                    ([('NP', 'goal', False), ('{PP,P{被,給,遭}}', 'agent', True, 'V_left'), ('VC2', 'Head', True), ('NP', 'theme', True, 'V_right')], '{PP,P}:agent:{被,給,遭}')
                ],
                'VP': [
                    ([('PP', 'goal', True, 'V_right'), ('VC2', 'Head', True)], 'PP:goal:{把,將}'),
                    ([('PP', 'goal', False), ('VC2', 'Head', True), ('NP', 'theme', True, 'V_right')], 'PP:goal:{把,將}'),
                    ([('{PP,P{被,給,挨,遭}}', 'agent', True, 'V_left'), ('VC2', 'Head', True)], '{PP,P}:agent:{被,給,挨,遭}'),
                    ([('{PP,P{被,給,遭}}', 'agent', True, 'V_left'), ('VC2', 'Head', True), ('NP', 'theme', True, 'V_right')], '{PP,P}:agent:{被,給,遭}')
                ]
            },
            'VC31': {
                'S': [
                    ([('{NP,PP[由]}', 'agent', True, 'V_left'), ('PP', 'theme', True, 'V_right'), ('VC31', 'Head', True)], 'PP:theme:{把,將}'),
                    ([('{NP,PP[由]}', 'agent', True, 'V_left'), ('PP', 'theme', True, 'V_right'), ('VC31', 'Head', True), ('PP[在]', 'goal', False, '#')], 'PP:theme:{把,將}'),
                    ([('NP', 'theme', True, 'V_right'), ('{PP,P{被,給,遭}', 'agent', True, 'V_left'), ('VC31', 'Head', True)], '{PP,P}:agent:{被,給,遭}')
                ],
                'VP': [
                    ([('PP', 'theme', True,'V_right'), ('VC31', 'Head', True)], 'PP:theme:{把,將}'),
                    ([('PP', 'theme', True, 'V_right'), ('VC31', 'Head', True), ('PP[在]', 'goal', False, '#')], 'PP:theme:{把,將}'),
                    ([('{PP,P{被,給,遭}', 'agent', True, 'V_left'), ('VC31', 'Head', True)], '{PP,P}:agent:{被,給,遭}')
                ]
            },
            'VD2': {
                'S': [
                    ([('NP', 'source', True, 'V_right'), ('{PP,P[被]}', 'agent', True, 'V_left'), ('VD2', 'Head', True), ('NP', 'theme', True, 'V_right')], '{PP, P}:agent:[被]')
                ],
                'VP': [
                    ([('{PP,P[被]}', 'agent', True, 'V_left'), ('VD2', 'Head', True), ('NP', 'theme', True, 'V_right')], '{PP,P}:agent:[被]')
                ]
            },
            'VJ2': {
                'S': [
                    ([('NP', 'goal', True, 'V_right'), ('PP[受]', 'experiencer', True, 'V_left'), ('VJ2', 'Head', True)], 'PP:experiencer:[受]')
                ],
                'VP': [
                    ([('PP[受]', 'experiencer', True, 'V_left'), ('VJ2', 'Head', True)], 'PP:experiencer:[受]')
                ]
            }
        }

        self.DE_mix = {
            ('N•的', 'N•的'), ('N•的', 'NP•的'), ('NP•的', 'N•的'), ('NP•的', 'NP•的'), ('V•的', 'V•的'), 
            ('V•的', 'VP•的'), ('VP•的', 'V•的'), ('VP•的', 'VP•的')
        }

        self.Head_pos_filter = {
            'Cab', 'DM', 'Nbc', 'Ncd', 'Ncda', 'Ncdb', 'Ndaac', 'Nddc', 'Nep', 'Neqa', 'Neqb', 'Nes', 'Neu', 'Nhb', 'Nhc' 
        }
        self.Modifier_pos_filter = {
            'D', 'Da', 'Daa', 'Dab', 'Dbaa', 'Dbab', 'Dbb', 'Dbc', 'Dc', 'Dd', 'DE', 'Dfa', 'Dg', 'Dh', 'Dj',
            'Ndaad', 'Neu', 'Nf', 'Nfa', 'Nfb', 'Nfc', 'Nfd', 'Nfe', 'Nfg', 'Nfi', 
            'VA', 'VA11', 'VA12', 'VA13', 'VA3', 'VA4', 'VB', 'VB11', 'VB12', 'VB2', 'VC', 'VC2', 'VC31', 'VC32', 'VC33',
            'VE', 'VE11', 'VE2', 'VF', 'VG', 'VG1', 'VG2', 'VI', 'VI1', 'VI2', 'VI3', 'VK1', 'VK2', 'VL', 'VL1', 'VL2', 'VL3', 'VL4'
        }

        self.load_knowledge()

    def load_knowledge(self):
        self.ckip_tk = CKIPUtility()

        # key: verb pos,  Value: possible arguments
        self.verb_arg_dict = defaultdict(set)
        self.__prepare_verb_argument()

        # normal SVO order scenario
        # key: verb pos, value: list of pattern.  pattern consists of (arg's role, pos-word constraint, need to make a pair?, sticky to front?)
        self.v_pattern_dict = self.__prepare_v_pattern_dict()

        # not SVO order scenario
        # key: verb pos, 
        self.v_passive_pattern_dict = self.__parse_passive_verb_pattern()

    def check_tree_rationality(self, root):
        '''
        1. NP 的 最後一個 child 若是 Head, 詞性必須要 N(排除 Nf*、Ng*、Ne*) or DM
        2. 若 Head 的詞性為 Caa, 只允許 對稱的「詞性」。(其中 Nd要對 Nd)

        DUMMY數目≠2
        Head 詞性不合理
        左右邊詞性不對稱
        '''
        # tree node traversal
        node_queue = [root]
        while len(node_queue) > 0:
            current_node = node_queue.pop(0)

            if 'child' in current_node:
                node_queue.extend(current_node['child'])
            else:
                continue

            # extract the Head node
            head_index, _ = get_the_only_Head_index(current_node['child'])
            if head_index != -1:
                head_node = current_node['child'][head_index]

            # examine condition beasd on phrase type
            if current_node['pos'] == 'NP':
                if head_index != -1:
                    if head_node['pos'][0] == 'N':
                        if len(head_node['pos']) >= 2:
                            if head_node['pos'][1] in {'f', 'g'} or head_node['pos'][-1] == '的':
                                self.logs[self.VALUE_PREPROCESS].append(('Head 詞性不合理 (NP)', root))
                                return False
                    elif head_node['pos'] == 'Caa':
                        # get DUMMY child
                        dummy_childs = get_NP_DUMMY_childs(current_node)

                        if len(dummy_childs) == 2:
                            dummy1_pos = dummy_childs[0]['pos']
                            dummy2_pos = dummy_childs[1]['pos']
                            if dummy1_pos[0] == 'N' and dummy1_pos[-1] != '的' and dummy2_pos[0] == 'N' and dummy2_pos[-1] != '的':
                                if dummy1_pos.startswith('Nf') or dummy1_pos.startswith('Ng'):
                                    self.logs[self.VALUE_PREPROCESS].append(('左右邊詞性不對稱 (NP)', root))
                                    return False
                                if dummy2_pos.startswith('Nf') or dummy2_pos.startswith('Ng'):
                                    self.logs[self.VALUE_PREPROCESS].append(('左右邊詞性不對稱 (NP)', root))
                                    return False

                                if dummy1_pos != 'NP' and dummy2_pos != 'NP' and self.ckip_tk.simplified_part_of_speech(dummy1_pos) != self.ckip_tk.simplified_part_of_speech(dummy2_pos):
                                    self.logs[self.VALUE_PREPROCESS].append(('左右邊詞性不對稱 (NP)', root))
                                    return False
                                
                            
                            elif dummy1_pos == 'DM':
                                if dummy2_pos != 'DM':
                                    self.logs[self.VALUE_PREPROCESS].append(('左右邊詞性不對稱 (NP)', root))
                                    return False
                            else:
                                self.logs[self.VALUE_PREPROCESS].append(('左右邊詞性不對稱 (NP)', root))
                                return False
                        
                            # DUUMY的 Head 詞性也要一致 (DM 配 DM/ N* 配 N*)
                            dummy_Heads = get_NP_Head_recursive(current_node)[0]
                            bNadNoun = False
                            count_Nd, count_DM = 0, 0
                            for dummy_Head in dummy_Heads:
                                if dummy_Head['pos'].startswith('Nd'):
                                    count_Nd += 1
                                elif dummy_Head['pos'] == 'DM':
                                    count_DM += 1
                                elif dummy_Head['pos'][0] == 'N':
                                    if len(dummy_Head['pos']) >= 2:
                                        if dummy_Head['pos'][1] in {'f', 'g', 'e'}:
                                            bNadNoun = True
                                            break
                                else:
                                    self.logs[self.VALUE_PREPROCESS].append(('DUMMY Head 的詞性不合理', root))
                                    return False


                            if count_Nd > 0 and count_Nd != len(dummy_Heads):
                                self.logs[self.VALUE_PREPROCESS].append(('DUMMY Head 部分為Nd', root))
                                return False
                            elif count_DM > 0 and count_Nd != len(dummy_Heads):
                                self.logs[self.VALUE_PREPROCESS].append(('DUMMY Head 部分為DM', root))
                                return False
                            elif bNadNoun:
                                self.logs[self.VALUE_PREPROCESS].append(('DUMMY Head 部分為不適當的N*', root))
                                return False
                        else:
                            self.logs[self.VALUE_PREPROCESS].append(('DUMMY數目≠2 (NP)', root))
                            return False
                    elif head_node['pos'] == 'DM':
                        pass
                    elif head_node['pos'] == 'Cab':
                        pass
                    else:
                        self.logs[self.VALUE_PREPROCESS].append(('Head 詞性不合理 (NP)', root))
                        return False
            elif current_node['pos'] == 'VP':
                if head_index != -1:
                    if head_node['pos'][0] == 'V' and head_node['pos'][-1] != '的':
                        pass
                    elif head_node['pos'] == 'Caa':
                        dummy_nodes = get_NP_DUMMY_childs(current_node)
                        if len(dummy_nodes) == 2:
                            if dummy_nodes[0]['pos'][0] == 'V' and dummy_nodes[1]['pos'][0] == 'V':
                                if dummy_nodes[0]['pos'][-1] == '的' or dummy_nodes[1]['pos'][-1] == '的':
                                    self.logs[self.VALUE_PREPROCESS].append(('左右邊詞性不對稱 (VP)', root))
                                    return False
                                elif dummy_nodes[0]['pos'] != 'VP' and dummy_nodes[1]['pos'] != 'VP':
                                    
                                    v1Pos = self.__get_V_category(dummy_nodes[0]['pos'])
                                    v2Pos = self.__get_V_category(dummy_nodes[1]['pos'])
                                    if v1Pos != v2Pos:
                                        self.logs[self.VALUE_PREPROCESS].append(('左右邊詞性不對稱 (VP)', root))
                                        return False
                            else:
                                self.logs[self.VALUE_PREPROCESS].append(('左右邊詞性不對稱 (VP)', root))
                                return False
                        else:
                            self.logs[self.VALUE_PREPROCESS].append(('DUMMY數目≠2 (VP)', root))
                            return False
                    elif head_node['pos'] == 'Cab':
                        pass
                    else:
                        self.logs[self.VALUE_PREPROCESS].append(('Head 詞性不合理(VP)', root))
                        return False
            elif current_node['pos'] == 'PP':
                if head_index != -1:
                    if head_node['pos'][0] == 'P' and head_node['pos'][-1] != '的':
                        pass
                    elif head_node['pos'] == 'Caa':
                        dummy_nodes = get_NP_DUMMY_childs(current_node)
                        if len(dummy_nodes) == 2:
                            if dummy_nodes[0]['pos'] != 'PP' or dummy_nodes[1]['pos'] != 'PP':
                                self.logs[self.VALUE_PREPROCESS].append(('左右邊詞性不對稱 (PP)', root))
                                return False
                        else:
                            self.logs[self.VALUE_PREPROCESS].append(('DUMMY數目≠2 (PP)', root))
                            return False
                    else:
                        self.logs[self.VALUE_PREPROCESS].append(('Head 詞性不合理(PP)', root))
                        return False
            elif current_node['pos'] == 'GP':
                if head_index != -1:
                    if head_node['pos'] == 'Ng':
                        pass
                    elif head_node['pos'] == 'Caa':
                        dummy_nodes = get_NP_DUMMY_childs(current_node)
                        if len(dummy_nodes) == 2:
                            if dummy_nodes[0]['pos'] != 'GP' or dummy_nodes[1]['pos'] != 'GP':
                                self.logs[self.VALUE_PREPROCESS].append(('左右邊詞性不對稱 (GP)', root))
                                return False
                        else:
                            self.logs[self.VALUE_PREPROCESS].append(('DUMMY數目≠2 (GP)', root))
                            return False
                    else:
                        self.logs[self.VALUE_PREPROCESS].append(('Head 詞性不合理(GP)', root))
                        return False
            elif current_node['pos'].endswith('•的'):

                if head_index != -1:
                    if head_node['pos'] == 'DE':
                        pass
                    elif head_node['pos'] == 'Caa':
                        dummy_nodes = get_NP_DUMMY_childs(current_node)
                        if len(dummy_nodes) == 2:
                            if (dummy_nodes[0]['pos'], dummy_nodes[1]['pos']) not in self.DE_mix:
                                self.logs[self.VALUE_PREPROCESS].append(('左右邊詞性不對稱 (•的)', root))
                                return False
                        else:
                            self.logs[self.VALUE_PREPROCESS].append(('DUMMY數目≠2 (•的)', root))
                            return False
                    else:
                        self.logs[self.VALUE_PREPROCESS].append(('Head 詞性不合理 (VP)', root))
                        return False
            elif current_node['pos'] == 'S':
                if head_index != -1:
                    if head_node['pos'] == 'Caa':
                        dummy_nodes = get_NP_DUMMY_childs(current_node)
                        if len(dummy_nodes) == 2:
                            if dummy_nodes[0]['pos'] != 'S' and dummy_nodes[1]['pos'] != 'S':
                                self.logs[self.VALUE_PREPROCESS].append(('左右邊詞性不對稱 (S)', root))
                            return False
                        else:
                            self.logs[self.VALUE_PREPROCESS].append(('DUMMY數目≠2 (S)', root))
                            return False
            elif current_node['pos'] == 'N':
                if head_index != -1:
                    if head_node['pos'] == 'Caa':
                        dummy_childs = get_NP_DUMMY_childs(current_node)

                        if len(dummy_childs) == 2:
                            dummy1_pos = dummy_childs[0]['pos']
                            dummy2_pos = dummy_childs[1]['pos']
                            if dummy1_pos[0] == 'N' and dummy1_pos[-1] != '的' and dummy2_pos[0] == 'N' and dummy2_pos[-1] != '的':
                                if dummy1_pos.startswith('Nf') or dummy1_pos.startswith('Ng') or dummy2_pos.startswith('Nf') or dummy2_pos.startswith('Ng'):
                                    self.logs[self.VALUE_PREPROCESS].append(('左右邊詞性不對稱 (N)', root))
                                    return False
                                if dummy1_pos == 'NP' or dummy2_pos == 'NP':
                                    self.logs[self.VALUE_PREPROCESS].append(('左右邊詞性不對稱 (N)', root))
                                    return False
                                if self.ckip_tk.simplified_part_of_speech(dummy1_pos) != self.ckip_tk.simplified_part_of_speech(dummy2_pos):
                                    self.logs[self.VALUE_PREPROCESS].append(('左右邊詞性不對稱 (N)', root))
                                    return False
                            else:
                                self.logs[self.VALUE_PREPROCESS].append(('左右邊詞性不對稱 (N)', root))
                                return False

                            # DUUMY的 Head 詞性也要一致 (DM 配 DM/ N* 配 N*)
                            dummy_Heads = get_NP_Head_recursive(current_node)[0]
                            bNadNoun = False
                            count_Nd, count_DM = 0, 0
                            for dummy_Head in dummy_Heads:
                                if dummy_Head['pos'].startswith('Nd'):
                                    count_Nd += 1
                                elif dummy_Head['pos'] == 'DM':
                                    count_DM += 1
                                elif dummy_Head['pos'][0] == 'N':
                                    if len(dummy_Head['pos']) >= 2:
                                        if dummy_Head['pos'][1] in {'f', 'g'}:
                                            bNadNoun = True
                                            break
                                else:
                                    self.logs[self.VALUE_PREPROCESS].append(('DUMMY Head 的詞性不合理', root))
                                    return False


                            if count_Nd > 0 and count_Nd != len(dummy_Heads):
                                self.logs[self.VALUE_PREPROCESS].append(('DUMMY Head 部分為Nd', root))
                                return False
                            elif count_DM > 0 and count_Nd != len(dummy_Heads):
                                self.logs[self.VALUE_PREPROCESS].append(('DUMMY Head 部分為DM', root))
                                return False
                            elif bNadNoun:
                                self.logs[self.VALUE_PREPROCESS].append(('DUMMY Head 部分為不適當的N*', root))
                                return False
                        else:
                            self.logs[self.VALUE_PREPROCESS].append(('DUMMY數目≠2 (N)', root))
                            return False
            elif current_node['pos'] == 'V':
                if head_index != -1:
                    if head_node['pos'] == 'Caa':
                        dummy_nodes = get_NP_DUMMY_childs(current_node)
                        if len(dummy_nodes) == 2:
                            if dummy_nodes[0]['pos'][0] == 'V' and dummy_nodes[1]['pos'][0] == 'V':
                                if dummy_nodes[0]['pos'][-1] == '的' or dummy_nodes[1]['pos'][-1] == '的':
                                    self.logs[self.VALUE_PREPROCESS].append(('左右邊詞性不對稱 (V)', root))
                                    return False
                                elif dummy_nodes[0]['pos'] != 'VP' and dummy_nodes[1]['pos'] != 'VP':
                                    v1Pos = self.__get_V_category(dummy_nodes[0]['pos'])
                                    v2Pos = self.__get_V_category(dummy_nodes[1]['pos'])
                                    if v1Pos != v2Pos:
                                        self.logs[self.VALUE_PREPROCESS].append(('左右邊詞性不對稱 (V)', root))
                                        return False
                            else:
                                self.logs[self.VALUE_PREPROCESS].append(('左右邊詞性不對稱 (V)', root))
                                return False
                        else:
                            self.logs[self.VALUE_PREPROCESS].append(('DUMMY數目≠2 (V)', root))
                            return False
            else:
                continue

        
        return True

    # import main APIs
    def clear_logs(self):
        self.logs.clear()

    def get_filter_result(self, parse_data):
        self.clear_logs()

        if isinstance(parse_data, str):
            parse_data = build_ckip_parse_tree(parse_data)

        return self.__precheck_step(parse_data)

        
    def get_all_verb_pairs(self, parse_data):
        '''
        parse_data can be string or dict\n
        return Tuple (List of sv pairs, List of vo pairs)
        '''
        self.logs.clear()

        if isinstance(parse_data, str):
            parse_data = build_ckip_parse_tree(parse_data)

        return self.__get_all_verb_pairs_private(parse_data)

    def get_all_verb_modifiers(self, parse_data, tree_info=False, doFilter=True):
        self.logs.clear()

        if isinstance(parse_data, str):
            parse_data = build_ckip_parse_tree(parse_data)

        return self.__get_all_verb_modifiers_private(parse_data, tree_info, doFilter)


    def get_NP_modifiers(self, parse_data):

        if isinstance(parse_data, str):
            parse_data = build_ckip_parse_tree(parse_data)

        all_fb_pairs = []
        # find all NPs
        node_queue = [parse_data]
        while len(node_queue) > 0:
            current_node = node_queue.pop(0)

            if 'child' in current_node:
                node_queue.extend(current_node['child'])
            else:
                continue

            if current_node['pos'] == 'NP':
                if is_elementary_phrase(current_node):
                    all_fb_pairs.extend(self.__get_NP_modifier(current_node))
        return all_fb_pairs


    def get_all_phrases_match_verb_pattern(self, parse_data):
        '''
        get a list of 
        '''
        self.logs.clear()

        if isinstance(parse_data, str):
            parse_data = build_ckip_parse_tree(parse_data)

        # retrieve all S/VP in all levels
        return self.__get_all_phrases_match_verb_pattern_private(parse_data)

    def get_reduced_sequence(self, parse_data):
        '''
        get a list of reduced text\n
        each form is a tuple. (list of words, the whole role)
        '''

        self.logs.clear()

        if isinstance(parse_data, str):
            parse_data = build_ckip_parse_tree(parse_data)

        root_node = parse_data
        # 前處理過濾
        if not self.__precheck_step(root_node):
            return []
        if root_node['pos'] not in {'S', 'VP', 'NP'}:
            return []

        if root_node['pos'] == 'NP':
            if not is_elementary_phrase(root_node):
                return []
            else:
                npHeadList, _ = get_NP_Head_recursive(root_node)
                token_list = [BaseToken.from_node_dict(npHead) for npHead in npHeadList]

                reduce_blocks = []
                reduce_block = (token_list, 'Head')
                reduce_blocks.append(reduce_block)
        else:
            reduced_nest_blocks, role_list = self.__get_reduced_sequence_helper(root_node)

            reduce_blocks = [(flatten_nested_list(redu_list), role_list[k]) for k, redu_list in enumerate(reduced_nest_blocks)]
        
        return reduce_blocks

    def get_reduced_form(self, target_node):
        '''
        回傳 list of BaseToken(s)
        '''
        finals = []

        if 'word' in target_node:
            return [BaseToken.from_node_dict(target_node)]

        if target_node['pos'][0] == 'N':
            seq, Caa_node_list = get_NP_Head_recursive(target_node)

            # argument 為時間的時候，要做merge
            if self.__isNdArgument(seq):
                (text, _, position), _ = self.__handle_NP_with_Nd(target_node)
                if text is not None:
                    finals.append(BaseToken(position, text, 'Time'))
                return finals
            else:
                if len(seq) > 0:
                    if len(Caa_node_list) > 0:
                        merge_sequence = self.__join_by_multi_seperator(seq, Caa_node_list)
                        finals.extend(merge_sequence)
                    else:
                        # 應該沒有兩個word吧?
                        nphead = seq[0]
                        finals.append(BaseToken.from_node_dict(nphead))
                return finals
        elif target_node['pos'][0] == 'V' and '•' not in target_node['pos']:
            if target_node['pos'] == 'VP':
                finals, _ = self.__get_reduced_sequence_helper(target_node)
                return finals
            else:
                # 一般字詞性: VA4(DUMMY1:VA4:工作|Head:Caa:或|DUMMY2:VA4:深造)
                _, seq, caa_nodes = get_VP_DUMMY_Head_recursive(target_node)
                if len(seq) > 0:
                    if len(caa_nodes) > 0:
                        merge_sequence = self.__join_by_multi_seperator(seq, caa_nodes)
                        finals.extend(merge_sequence)
                    else:
                        # 應該只有一個
                        vHead = seq[0]
                        finals.append(BaseToken.from_node_dict(vHead))
                return finals
            

        elif target_node['pos'] == 'S':
            finals, _ = self.__get_reduced_sequence_helper(target_node)
            return finals
        elif target_node['pos'] == 'PP':
            # 假設文法為 P + N/NP
            childs = target_node['child']
            if len(childs) != 2:
                return []
            if childs[0]['pos'][0] == 'P' and childs[1]['pos'][0] == 'N':
                # 介係詞
                finals.append(BaseToken.from_node_dict(childs[0]))
                seq, Caa_node_list = get_NP_Head_recursive(childs[1])
                if len(Caa_node_list) > 0:
                    merge_sequence = self.__join_by_multi_seperator(seq, Caa_node_list)
                    for comp in merge_sequence:
                        finals.append(comp)
                else:
                    # 應該沒有兩個word吧?
                    nphead = seq[0]
                    finals.append(BaseToken.from_node_dict(nphead))
            return finals
        elif target_node['pos'] == 'DM':
            finals.append(BaseToken.from_node_dict(target_node))
            return finals
        elif target_node['pos'] == 'GP':
            # 文法假設為 [S/VP/NP/DM] + Ng
            childs = target_node['child']
            if len(childs) != 2:
                return []
            if childs[1]['pos'] != 'Ng' or childs[0]['pos'] not in {'NP', 'VP', 'S', 'DM'}:
                return []

            finals.extend(self.get_reduced_form(childs[0]))
            finals.append(BaseToken.from_node_dict(childs[1]))
            return finals
        else:
            return []

    def set_single_verb_pattern(self, verb_part_of_speech, value):
        self.verb_pattern_dict[verb_part_of_speech] = value
        self.load_knowledge()


    # -----------------------------------------------------------
    def __get_reduced_sequence_helper(self, phNode):
        match_arg_list = []
        match_arg_roles = []


        # find central central Head verb
        Head_position, Head_amount =  get_the_only_Head_index(phNode['child'])
        verb_node = None if Head_position == -1 else phNode['child'][Head_position]

        # 有可能是單純Caa結構的VP，Head PoS = Caa
        if verb_node is not None and verb_node['pos'] == 'Caa':
            dummy_childs = get_NP_DUMMY_childs(phNode)
            if len(dummy_childs) == 2:

                match_arg_list.append(self.get_reduced_form(dummy_childs[0]))
                match_arg_list.append([BaseToken.from_node_dict(verb_node)])
                match_arg_list.append(self.get_reduced_form(dummy_childs[1]))

                match_arg_roles.append(get_node_role(dummy_childs[0]))
                match_arg_roles.append(get_node_role(verb_node))
                match_arg_roles.append(get_node_role(dummy_childs[1]))
                return match_arg_list, match_arg_roles

        # pre-check v condition
        Head_v_status, Head_v_nodes, v_Caa_list = self.check_single_Head_verb_condition(Head_position, verb_node, phNode, Head_amount)
        if not Head_v_status:
            return [], []

        # 紀錄 Head V 詞性
        head_partofspeech = Head_v_nodes[0]['pos']

        # case 1
        if head_partofspeech in {'V_11', 'V_12', 'V_2'}:
            l_arg_list, r_arg_list = self.__get_be_have_rel_sequence(phNode, Head_position)
            matchStatus, _, _ = self.__be_have_match(phNode, Head_v_nodes, l_arg_list, r_arg_list)
            if matchStatus:
                if len(l_arg_list) > 0:
                    match_arg_list.append(self.get_reduced_form(l_arg_list[0]))
                    match_arg_roles.append(get_node_role(l_arg_list[0]))
                    
                if len(Head_v_nodes) > 1:
                    merge_sequence = self.__join_by_multi_seperator(Head_v_nodes, v_Caa_list)
                    arg_branch = []
                    arg_branch.extend(merge_sequence)
                    
                    match_arg_list.append(arg_branch)
                else:
                    match_arg_list.append([BaseToken.from_node_dict(verb_node)])
                match_arg_roles.append(get_node_role(verb_node))

                if len(r_arg_list) > 0:
                    match_arg_list.append(self.get_reduced_form(r_arg_list[0]))
                    match_arg_roles.append(get_node_role(r_arg_list[0]))

                return match_arg_list, match_arg_roles

        # case 2
        verb_pos_candidates = self.__get_possible_verb_partofspeech(head_partofspeech)
        if len(verb_pos_candidates) == 0:
            self.logs[self.VALUE_PATTERN].append(('該詞性無句型定義', phNode))
            return [], []

        # get the sequence with only relavant argument
        rel_seq = self.__get_argument_sequence(phNode['child'], verb_pos_candidates)
        if len(rel_seq) < 2:
            self.logs[self.VALUE_PATTERN].append(('沒有論元 無須比對', phNode))
            if len(Head_v_nodes) > 1:
                merge_sequence = self.__join_by_multi_seperator(Head_v_nodes, v_Caa_list)
                arg_branch = merge_sequence
                return [ arg_branch ], [get_node_role(verb_node)]
            else:
                return [[ BaseToken.from_node_dict(verb_node)]], [get_node_role(verb_node)]

        # case 2-1: matching for "把被" 引導的句子
        matchStatus, extend_argument_sequence, sp_pp_index = self.__abnormal_SVO_verb_pattern_match_v2(rel_seq, phNode, verb_pos_candidates, Head_v_nodes)
        if matchStatus:
            subj, obj = None, None
            subj_role, obj_role = None, None
            for k, (elemNode, pair_info) in enumerate(extend_argument_sequence):
                if pair_info is None:
                    # 不理會
                    pass
                if pair_info == 'V':
                    if len(Head_v_nodes) > 1:
                        merge_sequence = self.__join_by_multi_seperator(Head_v_nodes, v_Caa_list)
                        arg_branch = []
                        for comp in merge_sequence:
                            arg_branch.append(comp)
                        match_arg_list.append(arg_branch)
                    else:
                        match_arg_list.append([BaseToken.from_node_dict(verb_node)])
                    match_arg_roles.append(get_node_role(verb_node))
                elif pair_info == 'Subject':
                    if k == sp_pp_index:
                        # 要取出PP裡面的N(NP)之Head成分
                        noun_child_list = get_childs_with_same_partOfSpeech(elemNode, 'N')
                        if len(noun_child_list) == 1:
                            np_head_node_list, caa_node_list = get_NP_Head_recursive(noun_child_list[0])
                            if len(np_head_node_list) > 1:
                                merge_sequence = self.__join_by_multi_seperator(np_head_node_list, caa_node_list)
                                subj = []
                                subj.extend(merge_sequence)
                            else:
                                subj = [BaseToken.from_node_dict(np_head_node_list[0])]
                            subj_role = get_node_role(elemNode)
                        else:
                            # 
                            pass
                    else:
                        if elemNode['pos'].startswith('N'):
                            np_head_node_list, caa_node_list = get_NP_Head_recursive(elemNode)
                            if len(np_head_node_list) > 1:
                                merge_sequence = self.__join_by_multi_seperator(np_head_node_list, caa_node_list)
                                subj = []
                                subj.extend(merge_sequence)
                            else:
                                subj = [BaseToken.from_node_dict(np_head_node_list[0])]
                            subj_role = get_node_role(elemNode)
                else:
                    if k == sp_pp_index:
                        # 要取出PP裡面的N(NP)之Head成分
                        noun_child_list = get_childs_with_same_partOfSpeech(elemNode, 'N')
                        if len(noun_child_list) == 1:
                            np_head_node_list, caa_node_list = get_NP_Head_recursive(noun_child_list[0])
                            if len(np_head_node_list) > 1:
                                merge_sequence = self.__join_by_multi_seperator(np_head_node_list, caa_node_list)
                                obj = []
                                obj.extend(merge_sequence)
                            else:
                                obj = [BaseToken.from_node_dict(np_head_node_list[0])]

                            obj_role = get_node_role(elemNode)
                        else:
                            # 
                            pass
                    else:
                        if elemNode['pos'].startswith('N'):
                            np_head_node_list, caa_node_list = get_NP_Head_recursive(elemNode)
                            if len(np_head_node_list) > 1:
                                merge_sequence = self.__join_by_multi_seperator(np_head_node_list, caa_node_list)
                                obj = []
                                obj.extend(merge_sequence)
                            else:
                                obj = [BaseToken.from_node_dict(np_head_node_list[0])]
                            
                            obj_role = get_node_role(elemNode)

            if subj is not None:
                match_arg_list.insert(0, subj)
                match_arg_roles.insert(0, subj_role)
            if obj is not None:
                match_arg_list.append(obj)
                match_arg_roles.append(obj_role)
            return match_arg_list, match_arg_roles

        # case 2-2: matching for "一般" 正常語順的句子
        matchStatus, extend_argument_sequence = self.__normal_SVO_verb_pattern_match_v2(rel_seq, phNode, verb_pos_candidates)
        if matchStatus:
            for elemNode, _ in extend_argument_sequence:
                # 每個論元都需要做簡化(不管是否要做NV VN pair)
                tmp_reduce_list = self.get_reduced_form(elemNode)
                if len(tmp_reduce_list) > 0:
                    match_arg_list.append(tmp_reduce_list)
                    match_arg_roles.append(get_node_role(elemNode))
            return match_arg_list, match_arg_roles

        return [], []
    
    
        
    def __get_all_phrases_match_verb_pattern_private(self, root):
        match_list = []

        # 前處理過濾
        if not self.__precheck_step(root):
            return match_list

        # retrieve all S/VP in all levels
        interest_nodes = get_all_specific_phrases(root, ['S','VP'])
        for interest_node in interest_nodes:
            bMatch, arg_sequence = self.__is_phrase_match_pattern(interest_node)
            if bMatch:
                match_list.append((arg_sequence, interest_node))

        return match_list


    def __is_phrase_match_pattern(self, phNode):
        '''
        判斷當層VP/S 是否滿足論元條件\n
        return is_match, 論元節點序列
        '''
        Head_position, Head_amount =  get_the_only_Head_index(phNode['child'])
        verb_node = None if Head_position == -1 else phNode['child'][Head_position]

        Head_v_status, Head_v_nodes, _ = self.check_single_Head_verb_condition(Head_position, verb_node, phNode, Head_amount)
        if not Head_v_status:
            return False, None

        # 紀錄 Head V 詞性
        head_partofspeech = Head_v_nodes[0]['pos']

        # case 1
        if head_partofspeech in {'V_11', 'V_12', 'V_2'}:
            l_arg_list, r_arg_list = self.__get_be_have_rel_sequence(phNode, Head_position)
            matchStatus, _, _ = self.__be_have_match(phNode, Head_v_nodes, l_arg_list, r_arg_list)
            if matchStatus:
                rel_seq = []
                rel_seq.extend(l_arg_list)
                rel_seq.append(phNode['child'][Head_position])
                rel_seq.extend(r_arg_list)
                return True, rel_seq
            else:
                return False, None

        # case 2
        verb_pos_candidates = self.__get_possible_verb_partofspeech(head_partofspeech)
        if len(verb_pos_candidates) == 0:
            self.logs[self.VALUE_PATTERN].append(('該詞性無句型定義', phNode))
            return False, None

        # get the sequence with only relavant argument
        rel_seq = self.__get_argument_sequence(phNode['child'], verb_pos_candidates)
        if len(rel_seq) < 2:
            self.logs[self.VALUE_PATTERN].append(('沒有論元 無須比對', phNode))
            return True, rel_seq

         # case 2-1: matching for "把被" 引導的句子
        
        matchStatus, _, _ = self.__abnormal_SVO_verb_pattern_match_v2(rel_seq, phNode, verb_pos_candidates, Head_v_nodes)
        if matchStatus:
            return True, rel_seq

        # case 2-2: matching for "一般" 正常語順的句子
        matchStatus, _ = self.__normal_SVO_verb_pattern_match_v2(rel_seq, phNode, verb_pos_candidates)
        if matchStatus:
            return True, rel_seq

        return False, None



    # these are some private functions
    def __prepare_verb_argument(self):
        for _pos, pattern_list in self.verb_pattern_dict.items():
            for pat in pattern_list:

                for itemTuple in pat:
                    self.verb_arg_dict[_pos].add(itemTuple[1])

    def __prepare_v_pattern_dict(self):
        normal_form = {}

        for _pos in self.verb_pattern_dict:
            normal_form[_pos] = []
            for raw_pattern in self.verb_pattern_dict[_pos]:
                pattern = []  # arg's role, pos-word constraint, make a pair?
                for elementTuple in raw_pattern:
                    # ex: ('*', 'experiencer', True)  ('VJ2', 'Head', True) ('{NP,VP,S}', 'causer', True)
                    # ex: ('PP{歸,為}', 'source', True) ('{NP,PP{關於,至於}}', 'goal', True, 'X')
                    constraint = self.__parse_constraint_text(elementTuple[0])

                    needmakepair = elementTuple[2]
                    sticky = False  # 是否緊黏前面樣元
                    if len(elementTuple) == 4:
                        if elementTuple[3] == 'X':
                            needmakepair = False
                        elif elementTuple[3] == '#':
                            sticky = True
                    
                    pattern.append([elementTuple[1], constraint, needmakepair, sticky])
                normal_form[_pos].append(pattern)

        return normal_form

    
    def __parse_constraint_text(self, constraint_text):
        '''
        關於 part-of-speehc 和 word 的限制
        '{NP,PP{關於,至於}}'、'PP{歸,為}'
        '''
        constraint = None
        if constraint_text != '*':
            raw_constraint = constraint_text
            pos_dict = {}
            if raw_constraint[0] == '{':
                raw_constraint = raw_constraint[1:-1]

            buffer_text = ''
            phrasename = ''
            for ch in raw_constraint:
                if ch == '{' or ch == '[':
                    phrasename = buffer_text
                    pos_dict[phrasename] = []
                    buffer_text = ''
                    pass
                elif ch == ',':
                    if phrasename != '':
                        pos_dict[phrasename].append(buffer_text)
                        buffer_text = ''
                    elif buffer_text != '':
                        phrasename = buffer_text
                        buffer_text = ''

                        pos_dict[phrasename] = []
                        phrasename = ''
                elif ch == '}' or ch == ']':
                    pos_dict[phrasename].append(buffer_text)
                    buffer_text = ''

                    phrasename = ''
                    pass
                else:
                    buffer_text += ch
            if buffer_text != '':
                pos_dict[buffer_text] = []
            constraint = pos_dict
        return constraint

    def __parse_passive_verb_pattern(self):
        '''
        Key: verb part-of-speech
        Value: dict_Key: phrase type; dict_Value: list of pattern tuple(Pattern, 指出"把被"的論元要求)
        '''
        normal_form = {}
        
        for _pos in self.passiveVerb_pattern_dict:
            normal_form[_pos] = {}

            for phType, pattern_list in self.passiveVerb_pattern_dict[_pos].items():
                normal_form[_pos][phType] = list()
                for raw_pattern, keyword_data in pattern_list:
                    pattern = []  # arg's role, pos-word constraint, pair's role(Subject/V/Object), sticky
                    for elementTuple in raw_pattern:
                        # example: ('{NP,PP[由]}', 'agent', True, 'V_left')、('PP[受]', 'experiencer', True, 'V_left')
                        # example: ('PP[在]', 'goal', False, '#')、('VD2', 'Head', True)
                        constraint = self.__parse_constraint_text(elementTuple[0])
                        pair_role = None  # None, V, Subject, Object
                        if elementTuple[2]:
                            if elementTuple[1] == 'Head':
                                pair_role = 'V'
                            else:
                                if elementTuple[3].lower() == 'v_left':
                                    pair_role = 'Subject'
                                else:
                                    pair_role = 'Object'
                        
                        sticky = False
                        if len(elementTuple) > 3:
                            if elementTuple[3] == '#':
                                sticky = True
                        pattern.append([elementTuple[1], constraint, pair_role, sticky])
                    
                    # example: PP:theme:{把,將}  、{PP,P}:agent:{被,給,挨,遭}
                    keyword_comps = keyword_data.split(':')
                    key_role = keyword_comps[1]
                    key_word_list = keyword_comps[2][1:-1].split(',')

                    normal_form[_pos][phType].append((pattern, (key_role, key_word_list)))

        return normal_form

    def __get_possible_verb_partofspeech(self, testPos):
        possible_verb_pos = []
        if testPos not in self.v_pattern_dict:
            # 會不會是粗詞性 ?
            for _pos in self.v_pattern_dict:
                if _pos.startswith(testPos):
                    possible_verb_pos.append(_pos)
        else:
            possible_verb_pos.append(testPos)
        return possible_verb_pos

    def __get_argument_sequence(self, node_seq, pVerb_pos_list):
        # collect verb's possible arguments
        allow_arg_list = set()
        for pVerb in pVerb_pos_list:
            allow_arg_list = allow_arg_list.union(list(self.verb_arg_dict[pVerb]))

        arg_sequence = []
        for node in node_seq:
            if node['role'] in allow_arg_list:
                arg_sequence.append(node)
            elif node['role'] in self.general_v_arg_role:
                # 雖然是廣義論元，但是非該動詞句型用到的論元
                return []
        return arg_sequence

    def __get_argument_and_not_sequence(self, node_seq, pVerb_pos_list):
        # collect verb's possible arguments
        allow_arg_list = set()
        for pVerb in pVerb_pos_list:
            allow_arg_list = allow_arg_list.union(list(self.verb_arg_dict[pVerb]))

        arg_sequence, non_argument_sequence = [], []
        for index, node in enumerate(node_seq):
            if 'role' not in node:
                return [], []

            if node['role'] in allow_arg_list:
                node['branch_index'] = index
                arg_sequence.append(node)
            elif node['role'] in self.general_v_arg_role:
                # 雖然是廣義論元，但是非該動詞句型用到的論元
                return [], []
            else:
                node['branch_index'] = index
                non_argument_sequence.append(node)

        return arg_sequence, non_argument_sequence
        

   
    def get_VP_idpats(self, head_pos):
        """
        取得動詞的idx, pattern list
        """
        i_sent_pats = []
        if head_pos in self.v_pattern_dict:
            sent_pats = self.v_pattern_dict[head_pos]
            i_sent_pats = list(enumerate(sent_pats))
        return i_sent_pats

    def get_VP_idpats_passive(self, head_pos, phrase_name):
        """
        取得動詞的idx, pattern list (被把介詞之情形)
        """
        i_sent_pats = []
        if head_pos in self.v_passive_pattern_dict:
            sent_pats = self.v_passive_pattern_dict[head_pos][phrase_name]
            i_sent_pats = list(enumerate(sent_pats))

        return i_sent_pats

    def pattern_covers_subsequence_fully(self, pat, node_sequence):
        '''
        input subsequence of sentence pattern RELEVANT arguments\n
        return Tuple(match_status , sequence of (node, pair info))\n
        where pair info is boolean whether need to make a pair ?
        '''

        k = 0
        res = []
        pattern_indices = []  # index of matched arguments in pattern
        
        for e in node_sequence:
            
            if k == len(pat):
                break
            
            role, const, pair_info, stick = pat[k] 
            
            # find next role
            while role != e['role'] and k < (len(pat)-1):
                k+=1
                role, const, pair_info, stick = pat[k]
            
            # none found
            if role != e['role']:
                break
            else:
                # role meets next element
                if self.e_meets_constraint(e,const):
                    if stick:
                        # check previous match element
                        if len(pattern_indices) == 0 or (k - 1 != pattern_indices[-1]):
                            break
                    res.append((e, pair_info))
                    pattern_indices.append(k)
                    k+=1 ## update, has also to proceed, once appropriate symbol is consumed
                else:
                    break
            
        return len(node_sequence) == len(res), res

    def e_meets_constraint(self, e, constr):
        


        meets = True

        if e['role'] == 'Head':
            return meets

        if constr:
            match_PoS = self.__is_PoS_meet_constraint(e['pos'], constr)
            if match_PoS:
                
                if len(constr[match_PoS]) > 0:
                    if e['pos'] != 'PP' and e['pos'] != 'P':
                        raise Exception('應該只能是PP、P')
                    
                    head_child_list = get_specific_role_childs(e, 'Head')
                    if len(head_child_list) == 1:
                        only_head = head_child_list[0]
                        if only_head['pos'][0] == 'P' and only_head['word'] in constr[match_PoS]:
                            pass
                        else:
                            meets = False
                            return meets
                else:
                    pass
            else:
                meets = False
                return meets
        
        return meets

    def __is_PoS_meet_constraint(self, e_PoS: str, constr_dict: dict):
        if any(_pos[-1] == '*' for _pos in constr_dict):
            if e_PoS in constr_dict:
                return e_PoS
            for allow_PoS in constr_dict:
                if allow_PoS[-1] == '*' and e_PoS.startswith(allow_PoS[:-1]):
                    return allow_PoS
            return None
        else:
            return e_PoS if e_PoS in constr_dict else None

    def __RELsequence_matches_verb_pattern_get_patid(self, rel_node_sequence, possible_verb_pos_list):

        for possible_verb_pos in possible_verb_pos_list:
            for pat_id, pat in self.get_VP_idpats(possible_verb_pos):
                ret, res = self.pattern_covers_subsequence_fully(pat, rel_node_sequence)
                if ret:
                    return pat_id, res

        return -1, []

    def __RELsequence_matches_passive_verb_pattern_get_patid(self, rel_node_sequence, phrase_type, possible_verb_pos_list):
        '''
        回傳 matched pattern id, result, 把/被 PP 所在位置\n
        沒成功，回傳 -1, [], -1
        '''

        for possible_verb_pos in possible_verb_pos_list:
            for pat_id, patTuple in self.get_VP_idpats_passive(possible_verb_pos, phrase_type):
                # pat: list of (arg's role, pos-word constraint, pair's role(Subject/V/Object), sticky?)
                # keyword_const: (把被的PP role, 該PP的Head實詞 set)
                pat, keyword_const = patTuple
                matchStatus, res = self.pattern_covers_subsequence_fully(pat, rel_node_sequence)

                if matchStatus:
                    # 需額外check 介係詞  PP 一定要出現
                    bPP_condition_pass = False
                    special_PP_index = -1
                    for idx, (node, pair_info) in enumerate(res):
                        if node['role'] == keyword_const[0]:
                            if node['pos'] == "PP":
                                
                                # 只找一個 Head P 跟 一個Noun
                                head_child_list = get_specific_role_childs(node, 'Head')
                                if len(head_child_list) == 1:
                                    if not head_child_list[0]['pos'].startswith('P'):
                                        bPP_condition_pass = False
                                    else:
                                        if head_child_list[0]['word'] in keyword_const[1]:
                                            special_PP_index = idx
                                            bPP_condition_pass = True

                            elif node['pos'].startswith('P'):
                                if node['word'] in keyword_const[1]:
                                    bPP_condition_pass = True
                                    special_PP_index = idx

                    if bPP_condition_pass:
                        return pat_id, res, special_PP_index
            
        return -1, [], -1

    def __isNdArgument(self, list_of_np_head_node):
        '''
        從 NP best Head 清單判斷
        '''
        if isAnyThisPartOfSpeech(list_of_np_head_node, 'Nd'):
            return True
        elif len(list_of_np_head_node) == 1:
            if list_of_np_head_node[0]['pos'] == 'Neqa':
                return True
        return False


    def __handle_NP_with_Nd(self, np):
        '''
        retrun (word, pos pattern form, position), wrong reason\n

        If it has reason(because criteria is not satisfied), all values in tuple is `None`
        '''
        word_list = []
        pos_comps = []
        # if it is just a leaf
        if 'child' not in np:
            if np['pos'].startswith('Nd'):
                return (np['word'], np['pos'], np['index']), None
            else:
                return (None, None, None), '詞性非Nd'

        # 判斷NP是基本還複雜
        if is_elementary_phrase(np):
            # collect pos sequence and word sequence
            for childNode in np['child']:
                word_list.append(childNode['word'])
                pos_comps.append(childNode['pos'])

            # check PoS pattern
            start_position = np['child'][0]['index']
            if pos_comps[-1].startswith('Nd'):
                # Nd*,Nd*,...Nd*
                # Nes,Nd
                # Nep,Nd
                if len(pos_comps) == 2:
                    if pos_comps[0].startswith('Nd') or pos_comps[0] == 'Nes' or pos_comps[0] == 'Nep':
                        return (''.join(word_list), ','.join(pos_comps), start_position), None
                    return (None, None, None), '(基本NP)不符合Time Pattern|' + ','.join(pos_comps)
                elif len(pos_comps) > 2:
                    for pos in pos_comps:
                        if not pos.startswith('Nd'):
                            return (None, None, None), '(基本NP)不符合Time Pattern|' + ','.join(pos_comps)
                    return (''.join(word_list), ','.join(pos_comps), start_position), None
                else:
                    return (''.join(word_list), ','.join(pos_comps), start_position), None
            else:
                # Nd*,(...),Neq*
                # Nd*,(...),Neu,Neqa
                if pos_comps[-1] == 'Neqa':
                    if len(pos_comps) >= 3 and pos_comps[-2] == 'Neu' and isAllTheSamePartOfSpeech_string(pos_comps[:-2], 'Nd'):
                        return (''.join(word_list), ','.join(pos_comps), start_position), None
                elif pos_comps[-1].startswith('Neq'):
                    if len(pos_comps) >= 2 and isAllTheSamePartOfSpeech_string(pos_comps[:-1], 'Nd'):
                        return (''.join(word_list), ','.join(pos_comps), start_position), None
                return (None, None, None), '(基本NP)不符合Time Pattern|' + ','.join(pos_comps)
        else:
            last_child = np['child'][-1]
            if last_child['role'] == 'Head' and last_child['pos'].startswith('Nd') and 'word' in last_child:
                # 只允許:  subtree1 + property + ... + Head
                false_reason = ''
                word_list = []
                pos_comps = []
                for j, child_node in enumerate(np['child']):
                    if j == 0:
                        if 'child' not in child_node:
                            false_reason = '(複雜NP)結構不考慮'
                            break
                    elif j != len(np['child']) -1:
                        if 'child' in child_node:
                            false_reason = '(複雜NP)結構不考慮'
                            break
                        else:
                            word_list.append(child_node['word'])
                            pos_comps.append(child_node['pos'])
                    else:
                        word_list.append(child_node['word'])
                        pos_comps.append(child_node['pos'])

                if false_reason != '':
                    return (None, None, None), false_reason
                else:
                    start_position = np['child'][1]['index']
                    # Nd*,Nd*,...Nd*
                    # Nes,Nd
                    # Nep,Nd
                    if len(pos_comps) == 2:
                        if pos_comps[0].startswith('Nd') or pos_comps[0] == 'Nes' or pos_comps[0] == 'Nep':
                            return (''.join(word_list), ','.join(pos_comps), start_position), None
                        return (None, None, None), '(複雜NP)不符合Time Pattern|' + ','.join(pos_comps)
                    elif len(pos_comps) > 2:
                        for pos in pos_comps:
                            if not pos.startswith('Nd'):
                                return (None, None, None), '(複雜NP)不符合Time Pattern|' + ','.join(pos_comps)
                        return (''.join(word_list), ','.join(pos_comps), start_position), None
                    else:
                        return (last_child['word'], last_child['pos'], last_child['index']), None
            else:
                return (None, None, None), '複雜NP之Head PoS非Nd'

        


    def __abnormal_SVO_verb_pattern_match_v2(self, relavant_seq, phrase_node, verb_pos_candidates, verb_nodes):
        '''
        判斷是否有符合句型條件，並輸出擴展資訊的論元序列，還有 被動PP所在的位置\n
        return isMatchFlag, argument sequence, special_pp_index
        '''
        phrase_type = phrase_node['pos']
        
        pat_id, extend_res, special_pp_index = self.__RELsequence_matches_passive_verb_pattern_get_patid(
            relavant_seq, phrase_type, verb_pos_candidates)

        if pat_id != -1:
            return True, extend_res, special_pp_index
            
        return False, [], -1
        
    def __retrieve_abnormal_SVO_association(self, extend_res, special_pp_index, verb_nodes, phrase_node):
        sv_pairs = []
        vo_pairs = []

        # start making FB pair
        for k, (elemNode, pair_info) in enumerate(extend_res):
            # 不需要組pair的
            if pair_info is None:
                continue
            if pair_info == 'V':
                continue

            if pair_info == 'Subject':
                if k == special_pp_index:
                    pp_role = get_node_role(elemNode)
                    # 要取出PP裡面的N(NP)之Head成分
                    noun_child_list = get_childs_with_same_partOfSpeech(elemNode, 'N')
                    
                    if len(noun_child_list) == 0:
                        pass
                    elif len(noun_child_list) == 1:
                        np_head_node_list = get_NP_Head_recursive(noun_child_list[0])[0]

                        if self.__isNdArgument(np_head_node_list):
                            (text, pos_order, text_position), reason = self.__handle_NP_with_Nd(noun_child_list[0])
                            if text is not None:
                                for verb_node in verb_nodes:
                                    sv_pairs.append([verb_node['index'], (verb_node['word'], verb_node['pos']), text_position, (text, pos_order, pp_role), phrase_node])
                            else:
                                self.logs[self.VALUE_TIMEWORD].append((reason, phrase_node))
                        else:
                            for np_head_node in np_head_node_list:
                                for verb_node in verb_nodes:
                                    sv_pairs.append([verb_node['index'], (verb_node['word'], verb_node['pos']), np_head_node['index'], (np_head_node['word'], np_head_node['pos'], pp_role), phrase_node])
                    else:
                        # 多個 N，當作不合理，整個沒抽到pair
                        return [], []
                else:
                    np_role = get_node_role(elemNode)
                    if elemNode['pos'].startswith('N'):
                        np_head_node_list = get_NP_Head_recursive(elemNode)[0]
                        
                        if self.__isNdArgument(np_head_node_list):
                            (text, pos_order, text_position), reason = self.__handle_NP_with_Nd(elemNode)
                            if text is not None:
                                for verb_node in verb_nodes:
                                    sv_pairs.append([verb_node['index'], (verb_node['word'], verb_node['pos']), text_position, (text, pos_order, np_role), phrase_node])
                            else:
                                self.logs[self.VALUE_TIMEWORD].append((reason, phrase_node))
                        else:
                            for np_head_node in np_head_node_list:
                                for verb_node in verb_nodes:
                                    sv_pairs.append([verb_node['index'], (verb_node['word'], verb_node['pos']), np_head_node['index'], (np_head_node['word'], np_head_node['pos'], np_role), phrase_node])
            else:
                # when pair_info == 'Object'
                if k == special_pp_index:
                    pp_role = get_node_role(elemNode)

                    noun_child_list = get_childs_with_same_partOfSpeech(elemNode, 'N')
                    if len(noun_child_list) == 0:
                        pass
                    elif len(noun_child_list) == 1:
                        np_head_node_list = get_NP_Head_recursive(noun_child_list[0])[0]
                        
                        if self.__isNdArgument(np_head_node_list):
                            (text, pos_order, text_position), reason = self.__handle_NP_with_Nd(noun_child_list[0])
                            if text is not None:
                                for verb_node in verb_nodes:
                                    vo_pairs.append([verb_node['index'], (verb_node['word'], verb_node['pos']), text_position, (text, pos_order, pp_role), phrase_node])
                            else:
                                self.logs[self.VALUE_TIMEWORD].append((reason, phrase_node))
                        else:
                            for np_head_node in np_head_node_list:
                                for verb_node in verb_nodes:
                                    vo_pairs.append([verb_node['index'], (verb_node['word'], verb_node['pos']), np_head_node['index'], (np_head_node['word'], np_head_node['pos'], pp_role), phrase_node])
                    else:
                        # 多個 N，當作不合理，整個沒有抽到pair
                        return [], []
                else:
                    if elemNode['pos'].startswith('N'):
                        np_role = get_node_role(elemNode)
                        np_head_node_list = get_NP_Head_recursive(elemNode)[0]
                        
                        if self.__isNdArgument(np_head_node_list):
                            (text, pos_order, text_position), reason = self.__handle_NP_with_Nd(elemNode)
                            if text is not None:
                                for verb_node in verb_nodes:
                                    vo_pairs.append([verb_node['index'], (verb_node['word'], verb_node['pos']), text_position, (text, pos_order, np_role), phrase_node])
                            else:
                                self.logs[self.VALUE_TIMEWORD].append((reason, phrase_node))
                        else:
                            for np_head_node in np_head_node_list:
                                for verb_node in verb_nodes:
                                    vo_pairs.append([verb_node['index'], (verb_node['word'], verb_node['pos']), np_head_node['index'], (np_head_node['word'], np_head_node['pos'], np_role), phrase_node])

        return sv_pairs, vo_pairs

    def __normal_SVO_verb_pattern_match_v2(self, relavant_seq, phrase_node, verb_pos_candidates):
        '''
        判斷是否有符合句型條件，並輸出擴展資訊的論元序列\n
        return isMatchFlag, argument sequence
        '''

        if phrase_node['pos'] == 'VP':
            first_node = relavant_seq[0]
            if first_node['role'] != 'Head':
                # 一般VP有左方論元
                self.logs[self.VALUE_PATTERN].append(('一般VP有左方論元', phrase_node))
                return False, []
        
        pat_id, extend_res = self.__RELsequence_matches_verb_pattern_get_patid(relavant_seq, verb_pos_candidates)
        if pat_id == -1:
            self.logs[self.VALUE_PATTERN].append(('不符合論元規範', phrase_node))
            return False, []

        return True, extend_res

    def __retrieve_normal_SVO_association(self, extend_res, phrase_node, verb_nodes):
        sv_pairs = []
        vo_pairs = []

        # make pair
        bNPHeadNotFound = False  # 雖然有些NP可能沒有代表詞，但其他的部分可能仍是OK的
        isLeft = True
        for elemNode, isPair in extend_res:
            # 跳過動詞
            if elemNode['role'] == 'Head':
                isLeft = False
                continue

            if isPair:
                if elemNode['pos'].startswith('N'):
                    # get Head of NP
                    np_head_node_list = get_NP_Head_recursive(elemNode)[0]
                    if len(np_head_node_list) == 0:
                        bNPHeadNotFound = True
                        continue

                    branch_role = get_node_role(elemNode)

                    if self.__isNdArgument(np_head_node_list):
                        (text, pos_order, text_position), reason = self.__handle_NP_with_Nd(elemNode)
                        if text is not None:
                            if isLeft:
                                for verb_node in verb_nodes:
                                    sv_pairs.append([verb_node['index'], (verb_node['word'], verb_node['pos']), text_position, (text, pos_order, branch_role), phrase_node])
                            else:
                                for verb_node in verb_nodes:
                                    vo_pairs.append([verb_node['index'], (verb_node['word'], verb_node['pos']), text_position, (text, pos_order, branch_role), phrase_node])
                        else:
                            self.logs[self.VALUE_TIMEWORD].append((reason, phrase_node))
                    else:
                        for np_head_node in np_head_node_list:
                            if isLeft:
                                for verb_node in verb_nodes:
                                    sv_pairs.append([verb_node['index'], (verb_node['word'], verb_node['pos']), np_head_node['index'], (np_head_node['word'], np_head_node['pos'], branch_role), phrase_node])
                            else:
                                for verb_node in verb_nodes:
                                    vo_pairs.append([verb_node['index'], (verb_node['word'], verb_node['pos']), np_head_node['index'], (np_head_node['word'], np_head_node['pos'], branch_role), phrase_node])
        
        if bNPHeadNotFound:
            self.logs[self.VALUE_PATTERN].append(('NP找不到Head', phrase_node))
        
        return sv_pairs, vo_pairs


        

    def __get_be_have_rel_sequence(self, phrase_node, Head_position):
        left_arg_list = []
        for child in phrase_node['child'][:Head_position]:
            child_node_role = get_node_role(child)
            if child_node_role in self.general_v_arg_role:
                left_arg_list.append(child)
        right_arg_list = []
        for child in phrase_node['child'][Head_position+1:]:
            child_node_role = get_node_role(child)
            if child_node_role in self.general_v_arg_role:
                right_arg_list.append(child)

        return left_arg_list, right_arg_list


    def __be_have_match(self, phrase_node, Head_v_list, left_arg_list, right_arg_list):
        '''
        return (match status, sv_pairs, vo_pairs)\n
        match status = True if requirement is satisfied
        '''
        sv_pairs, vo_pairs = [], []

        #verb_node = phrase_node['child'][Head_position]

        bLeftArgumentProblem = False
        if len(left_arg_list) == 1:
            if left_arg_list[0]['pos'].startswith('N'):
                head_results = get_NP_Head_recursive(left_arg_list[0])[0]
                text_role = get_node_role(left_arg_list[0])

                if self.__isNdArgument(head_results):
                    (text, pos_order, text_position), reason = self.__handle_NP_with_Nd(left_arg_list[0])
                    if text is not None:
                        for verb_node in Head_v_list:
                            sv_pairs.append([verb_node['index'], (verb_node['word'], verb_node['pos']), text_position, (text, pos_order, text_role), phrase_node])
                    else:
                        self.logs[self.VALUE_TIMEWORD].append((reason, phrase_node))
                else:
                    for head_result in head_results:
                        for verb_node in Head_v_list:
                            sv_pairs.append([verb_node['index'], (verb_node['word'], verb_node['pos']), head_result['index'], (head_result['word'], head_result['pos'], text_role), phrase_node])
        elif len(left_arg_list) != 0:
            bLeftArgumentProblem = True

        

        bRightArgumentProblem = False
        if len(right_arg_list) == 1:
            if right_arg_list[0]['pos'].startswith('N'):
                head_results = get_NP_Head_recursive(right_arg_list[0])[0]
                text_role = get_node_role(right_arg_list[0])

                if self.__isNdArgument(head_results):
                    (text, pos_order, text_position), reason = self.__handle_NP_with_Nd(right_arg_list[0])
                    if text is not None:
                        for verb_node in Head_v_list:
                            vo_pairs.append([verb_node['index'], (verb_node['word'], verb_node['pos']), text_position, (text, pos_order, text_role), phrase_node])
                    else:
                        self.logs[self.VALUE_TIMEWORD].append((reason, phrase_node))
                else:
                    for head_result in head_results:
                        for verb_node in Head_v_list:
                            vo_pairs.append([verb_node['index'], (verb_node['word'], verb_node['pos']), head_result['index'], (head_result['word'], head_result['pos'], text_role), phrase_node])
        elif len(right_arg_list) != 0:
            bRightArgumentProblem = True

        
        if bRightArgumentProblem or bLeftArgumentProblem:
            if bRightArgumentProblem:
                self.logs[self.VALUE_PATTERN].append(('是有動詞 右論元數 > 1', phrase_node))
            if bLeftArgumentProblem:
                self.logs[self.VALUE_PATTERN].append(('是有動詞 左論元數 > 1', phrase_node))
            return False, [], []
        else:
            return True, sv_pairs, vo_pairs

    def all_same(self, items):
        return all(x == items[0] for x in items)

    def check_single_Head_verb_condition(self, Head_position, verb_node, phraseNode, Head_amount):
        '''
        回傳 (動詞狀態, Head V list, Caa word list)
        動詞狀態 = True, when Head V 唯一或是Caa結構的多重V
        '''
        if Head_position == -1:
            if Head_amount == 0:
                self.logs[self.VALUE_HEAD].append(('沒有 Head', phraseNode))
            elif Head_amount >= 2:
                self.logs[self.VALUE_HEAD].append(('多個 Head', phraseNode))
            return False, None, []
        if verb_node['pos'][0] != 'V':
            self.logs['Head V'].append(('Head 非 動詞', phraseNode))
            return False, None, []
        if 'word' not in verb_node:
            # 保留 DUMMY1 Caa DUMMY2 結構的 Head V
            isCaaStructure, baseVnodes, Caa_word_list = get_VP_DUMMY_Head_recursive(verb_node)
            if not isCaaStructure:
                self.logs[self.VALUE_HEAD].append(('非簡單Caa結構', phraseNode))
                return False, None, []
            if not self.all_same([baseVnode['pos'] for baseVnode in baseVnodes]):
                self.logs[self.VALUE_HEAD].append(('簡單Caa結構中，混多詞性', phraseNode))
                return False, None, []
            else:
                return True, baseVnodes, Caa_word_list

        return True, [verb_node], []


    def __precheck_step(self, root):

        if 'pos' not in root:
            return False
        if root['pos'] not in {'S', 'VP', 'NP', 'PP', 'GP'}:
            return False
        if not self.check_tree_rationality(root):
            return False

        # 過濾含符號的句子
        sentence = get_sentence(root)
        if not ChracterUtility.IsSuitableForParse(sentence):
            self.logs[self.VALUE_PREPROCESS].append(('字元過濾', root))
            return False
        return True

    def __get_V_category(self, vPartOfSpeech):
        '''
        V 只分 V_系類、VH、其他一般V(自成一類)
        '''
        if vPartOfSpeech == 'VP':
            return vPartOfSpeech
        elif vPartOfSpeech.startswith('VH'):
            return 'VH'
        elif vPartOfSpeech.startswith('V_'):
            return vPartOfSpeech
        else:
            return 'V'

    def __get_verb_pair(self, phNode):
        '''
        (main flow function) 得到該層的 NV, VN pair
        '''

        Head_position, Head_amount =  get_the_only_Head_index(phNode['child'])
        verb_node = None if Head_position == -1 else phNode['child'][Head_position]

        # pre-check v condition
        Head_v_status, Head_v_nodes, _ = self.check_single_Head_verb_condition(Head_position, verb_node, phNode, Head_amount)
        if not Head_v_status:
            return [], []

        # 紀錄 Head V 詞性
        head_partofspeech = Head_v_nodes[0]['pos']

        # case 1
        if head_partofspeech in {'V_11', 'V_12', 'V_2'}:
            l_arg_list, r_arg_list = self.__get_be_have_rel_sequence(phNode, Head_position)
            matchStatus, sv_pairs, vo_pairs = self.__be_have_match(phNode, Head_v_nodes, l_arg_list, r_arg_list)
            return sv_pairs, vo_pairs
        
        # case 2
        verb_pos_candidates = self.__get_possible_verb_partofspeech(head_partofspeech)
        if len(verb_pos_candidates) == 0:
            self.logs[self.VALUE_PATTERN].append(('該詞性無句型定義', phNode))
            return [], []
        
        # get the sequence with only relavant argument
        rel_seq = self.__get_argument_sequence(phNode['child'], verb_pos_candidates)
        if len(rel_seq) < 2:
            self.logs[self.VALUE_PATTERN].append(('沒有論元 無須比對', phNode))
            return [], []

        # case 2-1: matching for "把被" 引導的句子
        matchStatus, extend_argument_sequence, sp_pp_index = self.__abnormal_SVO_verb_pattern_match_v2(rel_seq, phNode, verb_pos_candidates, Head_v_nodes)
        if matchStatus:
            sv_pairs, vo_pairs = self.__retrieve_abnormal_SVO_association(extend_argument_sequence, sp_pp_index, Head_v_nodes, phNode)
            return sv_pairs, vo_pairs
        

        # case 2-2: matching for "一般" 正常語順的句子
        matchStatus, extend_argument_sequence = self.__normal_SVO_verb_pattern_match_v2(rel_seq, phNode, verb_pos_candidates)
        if matchStatus:
            sv_pairs, vo_pairs = self.__retrieve_normal_SVO_association(extend_argument_sequence, phNode, Head_v_nodes)
            return sv_pairs, vo_pairs

        return [], []


    def __get_all_verb_pairs_private(self, root):
        '''
        得到各層的 NV、VN pairs
        '''

        # 前處理過濾
        if not self.__precheck_step(root):
            return [], []


        all_sv_pair = []
        all_vo_pair = []

        # retrieve all S/VP in all levels
        interest_nodes = get_all_specific_phrases(root, ['S','VP'])
        for interest_node in interest_nodes:
            inner_sv_pair, inner_vo_pair = self.__get_verb_pair(interest_node)
            all_sv_pair.extend(inner_sv_pair)
            all_vo_pair.extend(inner_vo_pair)

        return all_sv_pair, all_vo_pair


    def __get_verb_neighbors_utility(self, Head_position, non_rel_sequence):
        left_mod_node, right_mod_node = None, None
        for non_rel_node in non_rel_sequence:
            if non_rel_node['branch_index'] == Head_position - 1 and 'word' in non_rel_node:
                left_mod_node = non_rel_node
            if non_rel_node['branch_index'] == Head_position + 1 and 'word' in non_rel_node:
                right_mod_node = non_rel_node
        return left_mod_node, right_mod_node

    def __get_verb_neighbors(self, phNode):
        '''
        得到該層 V 的緊鄰左右 word node\n
        return (left node, v, right node)
        '''
        Head_position, Head_amount =  get_the_only_Head_index(phNode['child'])
        verb_node = None if Head_position == -1 else phNode['child'][Head_position]

        # pre-check v condition
        Head_v_status, Head_v_nodes, _ = self.check_single_Head_verb_condition(Head_position, verb_node, phNode, Head_amount)
        if not Head_v_status:
            return None, Head_v_nodes, None

        # 紀錄 Head V 詞性
        head_partofspeech = Head_v_nodes[0]['pos']

        # case 1
        if head_partofspeech in {'V_11', 'V_12', 'V_2'}:
            left_mod_node = None
            right_mod_node = None

            l_arg_list, r_arg_list = self.__get_be_have_rel_sequence(phNode, Head_position)
            matchStatus, _, _ = self.__be_have_match(phNode, Head_v_nodes, l_arg_list, r_arg_list)
            if matchStatus:
                if Head_position >= 1:
                    if phNode['child'][Head_position-1]['role'] not in self.general_v_arg_role:
                        if 'word' in phNode['child'][Head_position-1]:
                            left_mod_node = phNode['child'][Head_position-1]
                if Head_position != len(phNode['child']) - 1:
                    if phNode['child'][Head_position+1]['role'] not in self.general_v_arg_role:
                        if 'word' in phNode['child'][Head_position+1]:
                            right_mod_node = phNode['child'][Head_position+1]
            return left_mod_node, Head_v_nodes, right_mod_node

        # case 2
        verb_pos_candidates = self.__get_possible_verb_partofspeech(head_partofspeech)
        if len(verb_pos_candidates) == 0:
            return None, Head_v_nodes, None

        # get the sequence of argument and sequence of nonargument
        rel_seq, non_rel_seq = self.__get_argument_and_not_sequence(phNode['child'], verb_pos_candidates)
        if len(rel_seq) < 2:
            return None, Head_v_nodes, None

        # case 2-1: matching for "把被" 引導的句子
        matchStatus, _, _ = self.__abnormal_SVO_verb_pattern_match_v2(rel_seq, phNode, verb_pos_candidates, Head_v_nodes)
        if matchStatus:
            l, r = self.__get_verb_neighbors_utility(Head_position, non_rel_seq)
            return l, Head_v_nodes, r
            
        # case 2-2: matching for "一般" 正常語順的句子
        matchStatus, _ = self.__normal_SVO_verb_pattern_match_v2(rel_seq, phNode, verb_pos_candidates)
        if matchStatus:
            l, r = self.__get_verb_neighbors_utility(Head_position, non_rel_seq)
            return l, Head_v_nodes, r

        return None, Head_v_nodes, None

    def __get_all_verb_modifiers_private(self, root, needExample=False, doFilter=True):
        '''
        Tuple(left modifier list, right modifier list)\n
        1. 右修飾詞且role=Time的情形下，為了確保是修飾動詞，而非後面的名詞，限制time mod 處在結尾\n
        2. 右修飾詞且PoS=DM的情形下，限制DM需在phrase結尾處\n
        '''
        # 前處理過濾
        if doFilter:
            if not self.__precheck_step(root):
                return [], []

        all_left_mods = []
        all_right_mods = []

        # retrieve all S/VP in all levels
        interest_nodes = get_all_specific_phrases(root, ['S','VP'])
        for interest_node in interest_nodes:
            inner_left_mod, verb_nodes, inner_right_mod = self.__get_verb_neighbors(interest_node)
            if inner_left_mod is not None:
                if needExample:
                    for verb_node in verb_nodes:
                        all_left_mods.append([(verb_node, inner_left_mod), interest_node])
                else:
                    for verb_node in verb_nodes:
                        all_left_mods.append((verb_node, inner_left_mod))
            if inner_right_mod is not None:
                # additional filter conditions here
                if get_node_pos(inner_right_mod) not in {'Di'} or get_node_role(inner_right_mod) == 'time':
                    ph_leafs = get_leaf_nodes(interest_node)
                    ph_text = ''.join([leaf['word'] for leaf in ph_leafs])
                    if inner_right_mod['index'] + len(inner_right_mod['word']) != ph_leafs[0]['index'] + len(ph_text):
                        continue

                if needExample:
                    for verb_node in verb_nodes:
                        all_right_mods.append([(verb_node, inner_right_mod), interest_node])
                else:
                    for verb_node in verb_nodes:
                        all_right_mods.append((verb_node, inner_right_mod))

        return all_left_mods, all_right_mods

    def get_matched_verb_sequence(self, phNode):
        '''
        回傳 (isPatternMatch, list of Head V nodes, seq of branch tuple, abnormalFlag)\n
        其中，branch tuple = ()
        '''
        
        Head_position, Head_amount =  get_the_only_Head_index(phNode['child'])
        verb_node = None if Head_position == -1 else phNode['child'][Head_position]

        # pre-check v condition
        Head_v_status, Head_v_nodes, _ = self.check_single_Head_verb_condition(Head_position, verb_node, phNode, Head_amount)
        if not Head_v_status:
            return False, None, None, None

        # 紀錄 Head V 詞性
        head_partofspeech = Head_v_nodes[0]['pos']

        syntax_node_seq = []

        # case 1
        if head_partofspeech in {'V_11', 'V_12', 'V_2'}:
            l_arg_list, r_arg_list = self.__get_be_have_rel_sequence(phNode, Head_position)
            matchStatus, _, _ = self.__be_have_match(phNode, Head_v_nodes, l_arg_list, r_arg_list)
            if matchStatus:
                for i, syntax_node in enumerate(phNode['child']):
                    node_role = get_node_role(syntax_node)
                    if i == Head_position:
                        syntax_node_seq.append((syntax_node, 'Head', True))
                    elif node_role in self.general_v_arg_role:
                        syntax_node_seq.append((syntax_node, 'arg', True))
                    else:
                        syntax_node_seq.append((syntax_node, 'mod', False))

                return True, Head_v_nodes, syntax_node_seq, False
            else:
                return False, None, None, None
            
        # case 2
        verb_pos_candidates = self.__get_possible_verb_partofspeech(head_partofspeech)
        if len(verb_pos_candidates) == 0:
            return False, None, None, None

        # get the sequence of argument and sequence of nonargument
        rel_seq, non_rel_seq = self.__get_argument_and_not_sequence(phNode['child'], verb_pos_candidates)
        if len(rel_seq) < 2:
            for i, syntax_node in enumerate(phNode['child']):
                node_role = get_node_role(syntax_node)
                if i == Head_position:
                    syntax_node_seq.append((syntax_node, 'Head', True))
                else:
                    syntax_node_seq.append((syntax_node, 'mod', False))
            return True, Head_v_nodes, syntax_node_seq, False

        arg_branch_index_list = []
        for rel_node in rel_seq:
            arg_branch_index_list.append(rel_node['branch_index'])
        
        # case 2-1: matching for "把被" 引導的句子
        matchStatus, extend_argument_sequence, sp_pp_index = self.__abnormal_SVO_verb_pattern_match_v2(rel_seq, phNode, verb_pos_candidates, Head_v_nodes)
        if matchStatus:
            abnormal_flag = True

            for i, syntax_node in enumerate(phNode['child']):
                if i == Head_position:
                    syntax_node_seq.append((syntax_node, 'Head', True))
                elif i in arg_branch_index_list:
                    syntax_node_seq.append((syntax_node, 'arg', True))
                else:
                    syntax_node_seq.append((syntax_node, 'mod', False))
            return True, Head_v_nodes, syntax_node_seq, abnormal_flag
        
        # case 2-2: matching for "一般" 正常語順的句子
        matchStatus, extend_arg_seq = self.__normal_SVO_verb_pattern_match_v2(rel_seq, phNode, verb_pos_candidates)
        if matchStatus:
            pair_index_set = set()
            for ex_arg, isPair in extend_arg_seq:
                if isPair:
                    pair_index_set.add(ex_arg['branch_index'])

            for i, syntax_node in enumerate(phNode['child']):
                if i == Head_position:
                    syntax_node_seq.append((syntax_node, 'Head', True))
                elif i in arg_branch_index_list:
                    syntax_node_seq.append((syntax_node, 'arg', i in pair_index_set))
                else:
                    syntax_node_seq.append((syntax_node, 'mod', False))
            return True, Head_v_nodes, syntax_node_seq, False
        
        return False, None, None, None

    def __get_NP_modifier(self, np):
        '''
        回傳 list of (Head word/Head pos/Head role, Mod word/Mod pos/Mod role)
        '''
        aList = []

        npchilds = np['child']
        if len(npchilds) == 1:
            return aList

        head_index, _ = get_the_only_Head_index(np['child'])
        if head_index == -1 or head_index == 0:
            return aList

        head_node = npchilds[head_index]
        mod_node = npchilds[head_index-1]

        head_part = (head_node['word'], head_node['pos'], head_node['role'])
        mod_part = (mod_node['word'], mod_node['pos'], mod_node['role'])

        if head_node['pos'][0] == 'C' or head_node['pos'].startswith('Ne'):
            return aList
        if head_node['pos'].startswith('Ncd'):
            return aList
        if head_node['pos'].startswith('Nh') or head_node['pos'].startswith('Nhaa') or head_node['pos'].startswith('Nhac'):
            if not mod_node['pos'][0] == 'N':
                return aList
        if head_node['pos'].startswith('Nd') and mod_node['pos'].startswith('Nd'):
            # NP -time
            return aList

        if head_node['pos'] in self.Head_pos_filter:
            return aList
        if mod_node['pos'] == 'DM':
            return aList
        if mod_node['pos'] in self.Modifier_pos_filter:
            return aList


        aList.append((head_part, mod_part))

        return aList

    def __join_by_multi_seperator(self, word_nodes, sep_nodes):
        '''
        return list of BaseTokens (words with seps)
        '''
        
        if len(word_nodes) != len(sep_nodes) + 1:
            return []

        final = []
        for i, wordnode in enumerate(word_nodes):
            final.append(BaseToken.from_node_dict(wordnode))
            if i < len(sep_nodes):
                final.append(BaseToken.from_node_dict(sep_nodes[i]))
        return final




if __name__ == '__main__':
    fb_extrator = FB_extrator()

    test_parse_list = [
        'DUMMY:S(theme:Ndaba:今年|quantity:Daa:才|Head:V_2:有|range:NP(Head:Nab:機會學))',
        'S(experiencer:NP(Head:Nhaa:你)|Head:VK1:喜歡|goal:NP(DUMMY1:NP(Head:Nab:檸檬)|Head:Caa:或|DUMMY2:NP(Head:Nab:榴槤)))',
        'S(agent:NP(Head:Neqa:四分之一)|Head:VA4(DUMMY1:VA4:工作|Head:Caa:或|DUMMY2:VA4:深造))',
        'VP(evaluation:Dbb:無非|time:Dd:仍|Head:V_11:是|range:NP(Head:N(DUMMY1:Naa:塵灰|Head:Caa:與|DUMMY2:Nad:煩惱)))',
        'S(theme:NP(Head:Nba:齊白石)|time:DM:二十七歲|time:Dd:才|Head:VL2:開始|goal:VP(manner:VH11:正式|Head:VC2:學|goal:NP(Head:Nab:畫)))',
        'VP(time:Dd:終於|Head:VL4:使得|goal:NP(Head:Nba:海倫)|theme:VP(Head:VC1:考進|aspect:Di:了|goal:NP(property:Nba:哈佛|Head:Ncb:大學)))',
        'S(agent:NP(Head:Nab:醫師)|epistemics:Dbaa:應|Head:VE2:介紹|goal:NP(property:S•的(head:S(theme:NP(Head:Nad:手術)|Head:VH11:成功)|Head:DE:的)|Head:Nab:小孩))'
    ]
    for test_case in test_parse_list:
        red_arg_list = fb_extrator.get_reduced_sequence(test_case)
        print("句子: " + get_sentence_from_parse2(test_case))
        for red_arg, _ in red_arg_list:
            print("(" + ' '.join(red_arg) + ")", end=' ')
        print()