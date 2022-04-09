from src.preprocessor.preprocessor import czech_preprocessor, Preprocessor

preprocessor: Preprocessor = czech_preprocessor

print(preprocessor.get_terms('Plzeň je krásné město a je to krásné místo ty sračk* ty sračk*o'))

