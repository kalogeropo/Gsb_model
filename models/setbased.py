from models.Model import Model


class SetBased_model(Model):
    def __init__(self, collection):
        super().__init__(collection)
        self._model = self.get_model()
    def get_model(self):
        return __class__.__name__
    def _model_func(self, freq_termsets): pass
    def _vectorizer(self, tsf_ij, idf, *args):
        ########## each column corresponds to a document #########
        return tsf_ij * idf.reshape(-1, 1)