from flask import Flask, render_template, request, flash, url_for, jsonify
from wtforms import Form, StringField, TextAreaField, RadioField, validators

import os, math, requests, traceback

from model.draw_tree_lib import createParseTreeImageObject, get_img_base64_string
from model.parse_utility import build_ckip_parse_tree, build_stanford_parse_tree, get_sentence, print_tree, get_parse_from_web, ChracterUtility
from model.n_gram_model import get_load_model
from model.dep_graph_lib import get_dependency_graph_htmltext
from model.fb_utility import FB_extrator

from UseGensimMethod import UseGensimMethod


app = Flask(__name__)
app.config['Foreign_Name_Model_Path'] = './appdata/外國翻譯人名_bigram.pkl'
app.config['LTP_support'] = True

char_tool = ChracterUtility()

fb_extrator = FB_extrator()

# load model and related data
foreign_lm = get_load_model(app.config['Foreign_Name_Model_Path'])
threshold_values = {
    2: 2.1E-5,
    3: 2.3E-8,
    4: 3.7E-10,
    5: 2.8E-11,
    6: 2.7E-12,
    7: 2.1E-14,
    8: 6.7E-16,
}
foreign_char_set = {}
with open('./appdata/外國翻譯人名_字元列表.txt', 'r', encoding='utf8') as sr:
    sr.readline()

    for line in sr:
        line = line.strip('\n')
        columns = line.split('\t')
        
        foreign_char_set[columns[0]] = True if columns[2] == 'True' else False


math_similar_finder = UseGensimMethod('./appdata/math_17K_mymerge.txt', './data_model/model_math_tag', False)
math_similar_finder.load_model()


def sigmoid(x):
    return 1. / (1 + math.exp(-x))

def find_foreign_name_candidates(text):
    count = 1
    possible_candidate = []
    for i, ch in enumerate(text):

        if ch not in foreign_char_set:
            continue
        
        if foreign_char_set[ch]:
            k = i + 1
            acc_word = ch
            while k < len(text):
                if text[k] in foreign_char_set:
                    acc_word += text[k]
                    if text[k] == '·' or text[k] == '．':
                        k += 1
                        continue

                    if len(acc_word) > 8:
                        break

                    prob = foreign_lm.get_joint_prob([ch for ch in acc_word])
                    if prob >= threshold_values[len(acc_word)]:
                        possible_candidate.append((count, i, i+len(acc_word), acc_word, prob))
                        k += 1
                        count += 1
                        
                    else:
                        break
                else:
                    break
    return possible_candidate

if app.config['LTP_support']:
    from ltp import LTP
    ltp = LTP()


class VisualizeParseForm(Form):
    ''' visualizetree.html 表單 '''
    parse = TextAreaField('Parse String', [validators.Length(min=1, max=2048)]) 
    method = RadioField('Format', choices=[('CKIP','CKIP'),('Stanford','Stanford')], default='CKIP')

class BigramForm(Form):
    ''' lm_prob.html 表單 '''
    detectField = TextAreaField('Please input Test text', [validators.Length(min=2, max=64)])

class DependencyForm(Form):
    '''dependency.html 表單'''
    sentenceField = TextAreaField('Chinese Text', [validators.Length(min=1, max=32)], render_kw={ "placeholder": "兒童和家長一同上圖書館"})

class MathProblemForm(Form):
    ''' math_similar.html 表單 '''
    tagSeqField = TextAreaField('Please input Tag Sequence', [validators.Length(min=3, max=256)])



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vis', methods=['GET', 'POST'])
def ckip_visualize():
    sentence = ''
    tree_str = ''
    image_base64_str = ''

    bad_tree_reason, arg_conditions = None, None
    sv_pair_list, vo_pair_list = [], []
    np_fb_list, vp_fb_list = [], []
    reductions = []
    submitname = None

    form = VisualizeParseForm(request.form)

    if request.method == 'POST' and form.validate():

        parseString = form.parse.data
        parseMethod = form.method.data
        submitname = request.form['submit_button']
        formatSuccess = True
        try:
            parseString = parseString.strip()

            if parseMethod == 'CKIP':
                if submitname == 'Parse':
                    #print(''.join(parseString[:-1]))
                    if not char_tool.IsSuitableForParse(''.join(parseString[:-1])):
                        raise RuntimeError('You should input chinese text')
                    parseString = get_parse_from_web(parseString, False)

                rootNode = build_ckip_parse_tree(parseString)
            elif parseMethod == 'Stanford':
                if submitname == 'Parse':
                    raise RuntimeError('Cannot support direct parsing')
                rootNode = build_stanford_parse_tree(parseString)
            else:
                flash('Your Parse method is unknown.', 'danger')
                raise RuntimeError('Unknown parsing method')

            sentence = get_sentence(rootNode, parseMethod.lower())
            image_object = createParseTreeImageObject(rootNode, parseMethod)

            # several FBs are treated here.
            if parseMethod == 'CKIP':
                _sv_pair_list, _vo_pair_list = fb_extrator.get_all_verb_pairs(rootNode)

                for reason, phNode in fb_extrator.logs[fb_extrator.VALUE_PREPROCESS]:
                    bad_tree_reason = reason
                arg_conditions = []
                for reason, _ in fb_extrator.logs[fb_extrator.VALUE_PATTERN]:
                    arg_conditions.append(reason)

                for headTuple, fbTuple in fb_extrator.get_NP_modifiers(rootNode):
                    np_fb_list.append((headTuple, fbTuple))

                left_mod_tuple_list, right_mod_tuple_list = fb_extrator.get_all_verb_modifiers(rootNode)
                # 照語順條列
                for v_Node, l_node in left_mod_tuple_list:
                    vp_fb_list.append((True, (l_node['word'], l_node['pos'], l_node['role']), (v_Node['word'], v_Node['pos'], v_Node['role'])))
                for v_Node, r_node in right_mod_tuple_list:
                    vp_fb_list.append((False, (v_Node['word'], v_Node['pos'], v_Node['role']), (r_node['word'], r_node['pos'], r_node['role'])))

                # list of list
                reductions = fb_extrator.get_reduced_sequence(rootNode)

                # rewrite format
                sv_pair_list = []
                for _, vTuple, _, sTuple, _ in _sv_pair_list:
                    sv_pair_list.append((vTuple, sTuple))
                vo_pair_list = []
                for _, vTuple, _, oTuple, _ in _vo_pair_list:
                    vo_pair_list.append((vTuple, oTuple))
                    
        except requests.exceptions.Timeout as timeoute:
            flash('CKIP server is busy.', 'danger')
            formatSuccess = False
        except Exception as ex:
            #traceback.print_exc()
            flash('Your Parse String is invalid.', 'danger')
            formatSuccess = False
        
        if formatSuccess:
            image_base64_str = get_img_base64_string(image_object)
            tree_str = '\n' + print_tree(rootNode)

    context = {
        'form': form,
        'parse': parseString if submitname == 'Parse' else '' ,
        'sent': sentence,
        'imgstr': image_base64_str,
        'treestr': tree_str,
        'bad_structure_reason': bad_tree_reason,
        'arg_conditions': arg_conditions, 
        'sv_list': sv_pair_list,
        'vo_list': vo_pair_list,
        'np_fbs': np_fb_list,
        'vp_fbs': vp_fb_list,
        'reduc': reductions
    }

    return render_template('visualizetree.html', **context)

@app.route('/lm', methods=['GET', 'POST'])
def bigram_demo():
    form = BigramForm(request.form)
    paragraph_text = ''
    candidates = []

    if request.method == 'POST' and form.validate():
        paragraph_text = form.detectField.data
        candidates = find_foreign_name_candidates(paragraph_text)

    context = {
        'form': form,
        'input': paragraph_text,
        'candidates': candidates
    }

    return render_template('lm_prob.html', **context)

@app.route('/dependency', methods=['GET', 'POST'])
def ltp_visualize():
    if app.config['LTP_support']:
        img_string_list = []

        form = DependencyForm(request.form)
        if request.method == 'POST' and form.validate():
            inputText = form.sentenceField.data

            #只要最終拿消費券去銀行兌現的商家有營利事業登記證即可，
            #搶購桃園境內所剩不多的工業用地。
            #我送她一束玫瑰花
            #兒童和家長一同上圖書館。
            output = ltp.pipeline([inputText], tasks=["cws", "pos", "dep", "sdp"])
            seg = output.cws
            pos = output.pos
            dep = output.dep
            sdp = output.sdp

            # [['歡迎', '使用', '語言', '技術', '平台', '。']]
            # [['v', 'v', 'n', 'n', 'n', 'wp']]
            # [{'head': [0, 1, 4, 5, 2, 1], 'label': ['HED', 'VOB', 'ATT', 'ATT', 'VOB', 'WP']}]
            # [{'head': [0, 1, 4, 5, 2, 2], 'label': ['Root', 'dCONT', 'FEAT', 'FEAT', 'PAT', 'mPUNC']}]

            img_string_list = []
            for i, segment in enumerate(seg):
                word_list = [word for word in segment]
                pos_list = [part_of_sppech for part_of_sppech in pos[i]]

                # get 依存句法分析 arc for this sentence.
                syn_dep_arc_list = [(sourceNumber-1, thisNumber, dep[i]['label'][thisNumber]) for thisNumber, sourceNumber in enumerate(dep[i]['head'])]
                # get 語義依存分析 arc for this sentence.
                sem_dep_arc_list = [(sourceNumber-1, thisNumber, sdp[i]['label'][thisNumber]) for thisNumber, sourceNumber in enumerate(sdp[i]['head'])]

                # combine
                img_string_list.append( (get_dependency_graph_htmltext(word_list, syn_dep_arc_list, pos_list), get_dependency_graph_htmltext(word_list, sem_dep_arc_list, pos_list)) )

        return render_template('dependency.html', form=form, img_str_list=img_string_list)
    else:
        flash('LTP not open', 'danger')
        return render_template('index.html')

@app.route('/math/similar_finder', methods=['GET', 'POST'])
def math_similarity():
    form = MathProblemForm(request.form)

    tagSequenceText = ''
    best_matches = []

    if request.method == 'POST' and form.validate():
        tagSequenceText = form.tagSeqField.data
        best_matches = math_similar_finder.do_inference(tagSequenceText, 20)

    context = {
        'form': form,
        'input': tagSequenceText,
        'best_matches': best_matches
    }

    return render_template('math_similar.html', **context)





@app.route('/about')
def about():
    return "陳俊宏"

@app.route('/register')
def register():
    return '(To do) Register by e-mail verification.'


if __name__ == '__main__':
    app.secret_key='secretvpfrI'
    
    # the port number of this web app
    port = int(os.environ.get('PORT', 5000))
    # launch Flask web app
    app.run(host='0.0.0.0', port=port)
    
    
    #app.run(debug=True)
