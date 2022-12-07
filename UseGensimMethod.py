import jieba

from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec


class ProblemEntry:
    def __init__(self, pT, pTS, check):
        self.problemText = pT
        self.tagSequence = pTS
        self.status = check



class UseGensimMethod:

    def __init__(self, trainingFilePath: str, model_path: str, original_text_mode=True):
        self.trainingFilePath = trainingFilePath
        self.model_path = model_path
        self.original_text_mode = original_text_mode

        self.is_model_load = False
        self.data_entries = self.read_dataset()

    def load_model(self):
        self.d2v_model = Doc2Vec.load(self.model_path)
        self.is_model_load = True
        print('Model file is loaded')


    def read_dataset(self):
        entryList = []
        with open(self.trainingFilePath, 'r', encoding='utf8') as sr:
            sr.readline()
            for line in sr:
                columns = line.strip('\n').split('\t')

                entry = ProblemEntry(columns[1], columns[2], '可解' if columns[5] == 'True' else '未解')
                entryList.append(entry)

        return entryList

    def train(self, savedModelPath):

        document_train = []
        for index, entry in enumerate(self.data_entries):
            text = entry.problemText
            tagSeq = entry.tagSequence

            if self.original_text_mode:
                q_segments = list(jieba.cut(text.strip(), cut_all=False))
                q_document = TaggedDocument(q_segments, tags=[index])

                EMBEDDING_SIZE = 96
            
            else:
                q_document = TaggedDocument(tagSeq.split(','), tags=[index])
                EMBEDDING_SIZE = 32


            EPOCH_NUM = 100

            document_train.append(q_document)
        d2v_model = Doc2Vec(document_train, dm=1, min_count=1, window=5, vector_size=EMBEDDING_SIZE, sample=1e-3, negative=5, workers=4)
        print('start training with {0} samples'.format(d2v_model.corpus_count))
        d2v_model.train(document_train, total_examples=d2v_model.corpus_count, epochs=EPOCH_NUM)

        d2v_model.save(savedModelPath)
        print('Model file is saved')

    def do_inference(self, user_query: str, bestN=5):

        ret = []

        if not self.is_model_load:
            self.load_model()
        
        if self.original_text_mode:
            query_segments = list(jieba.cut(user_query, cut_all=False))
        else:
            query_segments = user_query.split(',')

        inferred_vector = self.d2v_model.infer_vector(query_segments)

        # Find the top-N most similar document by (default) "cosine similarity" measure
        bestN_results = self.d2v_model.dv.most_similar([inferred_vector], topn=bestN)
        for rank, result in enumerate(bestN_results, 1):
            docIndex, similarity = result

            if similarity <= 0.75:
                break

            matched_entry = self.data_entries[docIndex]

            ret.append(('{0:.3f}'.format(similarity), matched_entry.problemText.strip(), matched_entry.status))
            #print("Top {0}: (similarity= {1:.3f}) {2}".format(rank, similarity, matched_p))
        
        return ret
