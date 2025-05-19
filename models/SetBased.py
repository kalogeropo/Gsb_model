from models.Model import Model
from typing import Any
from numpy import ndarray

class SetBasedModel(Model):
    """The set based model implementation. A subclass of the base model. All models will use the base model's fit and
    evaluate function, and will differentiate on model_funct, and vectorization function!"""
    def __init__(self, collection):
        super().__init__(collection)
        self._model = self.get_model()

    def get_model(self) -> str:
        return self.__class__.__name__

    def _model_func(self, freq_termsets: Any) -> ndarray:
        """
        Placeholder implementation for the model-specific function applied to termsets.

        Args:
            freq_termsets (Any): Typically a dictionary of frequent termsets.

        Returns:
            np.ndarray: Must return an array of model scores (to be overridden).
        """
        raise NotImplementedError("SetBasedModel does not implement _model_func directly.")
    

    def _vectorizer(self, tsf_ij: ndarray, idf: ndarray, *args: Any) -> ndarray:
        """
        Applies IDF-based weighting to the termset frequency matrix.

        Args:
            tsf_ij (np.ndarray): Termset-document frequency matrix.
            idf (np.ndarray): Inverse document frequency vector.

        Returns:
            np.ndarray: Weighted document-term matrix.
        """
        return tsf_ij * idf.reshape(-1, 1)
