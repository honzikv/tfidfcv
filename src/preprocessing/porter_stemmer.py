# Adapted from https://github.com/jedijulia/porter-stemmer

class PorterStemmer:
    def is_cons(self, letter):  # function that returns true if a letter is a consonant otherwise false
        if letter == 'a' or letter == 'e' or letter == 'i' or letter == 'o' or letter == 'u':
            return False
        else:
            return True

    def is_consonant(self, word, i):  # function that returns true only if the letter at i th position
        # in the argument 'word' is a consonant.But if the letter is 'y' and the letter at i-1 th position
        # is also a consonant, then it returns false.
        letter = word[i]
        if self.is_cons(letter):
            if letter == 'y' and self.is_cons(word[i - 1]):
                return False
            else:
                return True
        else:
            return False

    def is_vowel(self, word, i):  # function that returns true if the letter at i th position in the argument 'word'
        # is a vowel
        return not (self.is_consonant(word, i))

    # *S
    def ends_with(self, stem, letter):  # returns true if the word 'stem' ends with 'letter'
        if stem.endswith(letter):
            return True
        else:
            return False

    # *v*
    def contains_vowel(self, stem):  # returns true if the word 'stem' contains a vowel
        for i in stem:
            if not self.is_cons(i):
                return True
        return False

    # *d
    def double_cons(self, stem):  # returns true if the word 'stem' ends with 2 consonants
        if len(stem) >= 2:
            if self.is_consonant(stem, -1) and self.is_consonant(stem, -2):
                return True
            else:
                return False
        else:
            return False

    def get_form(self, word):
        # This function takes a word as an input, and checks for vowel and consonant sequences in that word.
        # vowel sequence is denoted by V and consonant sequences by C
        # For example, the word 'balloon' can be divived into following sequences:
        # 'b' : C
        # 'a' : V
        # 'll': C
        # 'oo': V
        # 'n' : C
        # So form = [C,V,C,V,C] and formstr = CVCVC
        form = []
        formStr = ''
        for i in range(len(word)):
            if self.is_consonant(word, i):
                if i != 0:
                    prev = form[-1]
                    if prev != 'C':
                        form.append('C')
                else:
                    form.append('C')
            else:
                if i != 0:
                    prev = form[-1]
                    if prev != 'V':
                        form.append('V')
                else:
                    form.append('V')
        for j in form:
            formStr += j
        return formStr

    def get_m(self, word):
        # returns value of M which is equal to number of 'VC' in formstr
        # So in above example of word 'balloon', we have 2 'VC'

        form = self.get_form(word)
        m = form.count('VC')
        return m

    # *o
    def cvc(self, word):
        # returns true if the last 3 letters of the word are of the following pattern: consonant,vowel,consonant
        # but if the last word is either 'w','x' or 'y', it returns false
        if len(word) >= 3:
            f = -3
            s = -2
            t = -1
            third = word[t]
            if self.is_consonant(word, f) and self.is_vowel(word, s) and self.is_consonant(word, t):
                if third != 'w' and third != 'x' and third != 'y':
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def replace(self, orig, rem, rep):
        # this function checks if string 'orig' ends with 'rem' and
        # replaces 'rem' by the substring 'rep'. The resulting string 'replaced'
        # is returned.

        result = orig.rfind(rem)
        base = orig[:result]
        replaced = base + rep
        return replaced

    def replace_m0(self, orig, rem, rep):
        # same as the function replace(), except that it checks the value of M for the
        # base string. If it is >0 , it replaces 'rem' by 'rep', otherwise it returns the
        # original string

        result = orig.rfind(rem)
        base = orig[:result]
        if self.get_m(base) > 0:
            replaced = base + rep
            return replaced
        else:
            return orig

    def replace_m1(self, orig, rem, rep):
        # same as replaceM0(), except that it replaces 'rem' by 'rep', only when M>1 for
        # the base string

        result = orig.rfind(rem)
        base = orig[:result]
        if self.get_m(base) > 1:
            replaced = base + rep
            return replaced
        else:
            return orig

    def step1a(self, word):
        # In a given word, this function replaces 'sses' by 'ss', 'ies' by 'i',
        # 'ss' by 'ss' and 's' by ''

        """step1a() gets rid of plurals. e.g.

           caresses  ->  caress
           ponies    ->  poni
           ties      ->  ti
           caress    ->  caress
           cats      ->  cat
        """
        if word.endswith('sses'):
            word = self.replace(word, 'sses', 'ss')
        elif word.endswith('ies'):
            word = self.replace(word, 'ies', 'i')
        elif word.endswith('ss'):
            word = self.replace(word, 'ss', 'ss')
        elif word.endswith('s'):
            word = self.replace(word, 's', '')
        else:
            pass
        return word

    def step1b(self, word):
        # this function checks if a word ends with 'eed','ed' or 'ing' and replces these substrings by
        # 'ee','' and ''. If after the replacements in case of 'ed' and 'ing', the resulting word
        # -> ends with 'at','bl' or 'iz' : add 'e' to the end of the word
        # -> ends with 2 consonants and its last letter isn't 'l','s' or 'z': remove last letter of the word
        # -> has 1 as value of M and the cvc(word) returns true : add 'e' to the end of the word

        '''
        step1b gets rid of -eed -ed or -ing. e.g.

        feed      ->  feed
           agreed    ->  agree
           disabled  ->  disable

           matting   ->  mat
           mating    ->  mate
           meeting   ->  meet
           milling   ->  mill
           messing   ->  mess

           meetings  ->  meet
        '''
        flag = False
        if word.endswith('eed'):
            result = word.rfind('eed')
            base = word[:result]
            if self.get_m(base) > 0:
                word = base
                word += 'ee'
        elif word.endswith('ed'):
            result = word.rfind('ed')
            base = word[:result]
            if self.contains_vowel(base):
                word = base
                flag = True
        elif word.endswith('ing'):
            result = word.rfind('ing')
            base = word[:result]
            if self.contains_vowel(base):
                word = base
                flag = True
        if flag:
            if word.endswith('at') or word.endswith('bl') or word.endswith('iz'):
                word += 'e'
            elif self.double_cons(word) and not self.ends_with(word, 'l') and not self.ends_with(word,
                                                                                                 's') and not self.ends_with(
                word, 'z'):
                word = word[:-1]
            elif self.get_m(word) == 1 and self.cvc(word):
                word += 'e'
            else:
                pass
        else:
            pass
        return word

    def step1c(self, word):
        # In words ending with 'y' this function replaces 'y' by 'i'

        """step1c() turns terminal y to i when there is another vowel in the stem."""

        if word.endswith('y'):
            result = word.rfind('y')
            base = word[:result]
            if self.contains_vowel(base):
                word = base
                word += 'i'
        return word

    def step2(self, word):
        # this function checks the value of M, and replaces the suffixes accordingly

        """step2() maps double suffices to single ones.
        so -ization ( = -ize plus -ation) maps to -ize etc. note that the
        string before the suffix must give m() > 0.
        """

        if word.endswith('ational'):
            word = self.replace_m0(word, 'ational', 'ate')
        elif word.endswith('tional'):
            word = self.replace_m0(word, 'tional', 'tion')
        elif word.endswith('enci'):
            word = self.replace_m0(word, 'enci', 'ence')
        elif word.endswith('anci'):
            word = self.replace_m0(word, 'anci', 'ance')
        elif word.endswith('izer'):
            word = self.replace_m0(word, 'izer', 'ize')
        elif word.endswith('abli'):
            word = self.replace_m0(word, 'abli', 'able')
        elif word.endswith('alli'):
            word = self.replace_m0(word, 'alli', 'al')
        elif word.endswith('entli'):
            word = self.replace_m0(word, 'entli', 'ent')
        elif word.endswith('eli'):
            word = self.replace_m0(word, 'eli', 'e')
        elif word.endswith('ousli'):
            word = self.replace_m0(word, 'ousli', 'ous')
        elif word.endswith('ization'):
            word = self.replace_m0(word, 'ization', 'ize')
        elif word.endswith('ation'):
            word = self.replace_m0(word, 'ation', 'ate')
        elif word.endswith('ator'):
            word = self.replace_m0(word, 'ator', 'ate')
        elif word.endswith('alism'):
            word = self.replace_m0(word, 'alism', 'al')
        elif word.endswith('iveness'):
            word = self.replace_m0(word, 'iveness', 'ive')
        elif word.endswith('fulness'):
            word = self.replace_m0(word, 'fulness', 'ful')
        elif word.endswith('ousness'):
            word = self.replace_m0(word, 'ousness', 'ous')
        elif word.endswith('aliti'):
            word = self.replace_m0(word, 'aliti', 'al')
        elif word.endswith('iviti'):
            word = self.replace_m0(word, 'iviti', 'ive')
        elif word.endswith('biliti'):
            word = self.replace_m0(word, 'biliti', 'ble')
        return word

    def step3(self, word):
        # this function checks the value of M, and replaces the suffixes accordingly

        """step3() dels with -ic-, -full, -ness etc. similar strategy to step2."""

        if word.endswith('icate'):
            word = self.replace_m0(word, 'icate', 'ic')
        elif word.endswith('ative'):
            word = self.replace_m0(word, 'ative', '')
        elif word.endswith('alize'):
            word = self.replace_m0(word, 'alize', 'al')
        elif word.endswith('iciti'):
            word = self.replace_m0(word, 'iciti', 'ic')
        elif word.endswith('ful'):
            word = self.replace_m0(word, 'ful', '')
        elif word.endswith('ness'):
            word = self.replace_m0(word, 'ness', '')
        return word

    def step4(self, word):
        # this function checks the value of M, and replaces the suffixes accordingly

        """step4() takes off -ant, -ence etc., in context <c>vcvc<v>{meaning, M >1 for the word}."""

        if word.endswith('al'):
            word = self.replace_m1(word, 'al', '')
        elif word.endswith('ance'):
            word = self.replace_m1(word, 'ance', '')
        elif word.endswith('ence'):
            word = self.replace_m1(word, 'ence', '')
        elif word.endswith('er'):
            word = self.replace_m1(word, 'er', '')
        elif word.endswith('ic'):
            word = self.replace_m1(word, 'ic', '')
        elif word.endswith('able'):
            word = self.replace_m1(word, 'able', '')
        elif word.endswith('ible'):
            word = self.replace_m1(word, 'ible', '')
        elif word.endswith('ant'):
            word = self.replace_m1(word, 'ant', '')
        elif word.endswith('ement'):
            word = self.replace_m1(word, 'ement', '')
        elif word.endswith('ment'):
            word = self.replace_m1(word, 'ment', '')
        elif word.endswith('ent'):
            word = self.replace_m1(word, 'ent', '')
        elif word.endswith('ou'):
            word = self.replace_m1(word, 'ou', '')
        elif word.endswith('ism'):
            word = self.replace_m1(word, 'ism', '')
        elif word.endswith('ate'):
            word = self.replace_m1(word, 'ate', '')
        elif word.endswith('iti'):
            word = self.replace_m1(word, 'iti', '')
        elif word.endswith('ous'):
            word = self.replace_m1(word, 'ous', '')
        elif word.endswith('ive'):
            word = self.replace_m1(word, 'ive', '')
        elif word.endswith('ize'):
            word = self.replace_m1(word, 'ize', '')
        elif word.endswith('ion'):
            result = word.rfind('ion')
            base = word[:result]
            if self.get_m(base) > 1 and (self.ends_with(base, 's') or self.ends_with(base, 't')):
                word = base
            word = self.replace_m1(word, '', '')
        return word

    def step5a(self, word):
        # this function checks if the word ends with 'e'. If it does, it checks the value of
        # M for the base word. If M>1, OR, If M = 1 and cvc(base) is false, it simply removes 'e'
        # ending.

        """step5() removes a final -e if m() > 1.
        """

        if word.endswith('e'):
            base = word[:-1]
            if self.get_m(base) > 1:
                word = base
            elif self.get_m(base) == 1 and not self.cvc(base):
                word = base
        return word

    def step5b(self, word):
        # this function checks if the value of M for the word is greater than 1 and it ends with 2 consonants
        # and it ends with 'l', it removes 'l'

        # step5b changes -ll to -l if m() > 1
        if self.get_m(word) > 1 and self.double_cons(word) and self.ends_with(word, 'l'):
            word = word[:-1]
        return word

    def stem(self, word):
        # steps to be followed for stemming according to the porter stemmer :)

        word = self.step1a(word)
        word = self.step1b(word)
        word = self.step1c(word)
        word = self.step2(word)
        word = self.step3(word)
        word = self.step4(word)
        word = self.step5a(word)
        word = self.step5b(word)
        return word
