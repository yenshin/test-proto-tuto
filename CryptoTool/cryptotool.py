class CryptoTool:

    def DecypherFromTranslation(self, Message, CryptedKey, UncryptedKey):
        Message = Message.upper()
        CryptedKey = CryptedKey.upper()
        UncryptedKey = UncryptedKey.upper()
        Alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        translatedAlphabet = ""
        result = ""
        for letter in Alphabet:
            letterIndex = UncryptedKey.find(letter)
            if (letterIndex != -1):
                translatedAlphabet += CryptedKey[letterIndex]
            else:
                translatedAlphabet += letter
        for letter in Message:
            letterIndex = translatedAlphabet.find(letter)
            if (letterIndex != -1):
                result += Alphabet[letterIndex]
            else:
                result += letter
        print(result)
        #print result
    
    
if __name__ == "__main__":
    # To be able to execute binary version in Windows correctly freeze_support
    # function is called before anything else in the main program
    # http://docs.python.org/library/multiprocessing.html#multiprocessing.freeze_support
    crypto = CryptoTool()
    crypto.DecypherFromTranslation("NSTK KD KTTKSTK TUTD VRAK AK KKTK","KEXKNATNK RD-L I","SYREADIAE JX-F C")
    crypto.DecypherFromTranslation("DUADK RN BKXTDKX UG NBXTR WDN","KEXKNATNK RD-L I","SYREADIAE JX-F C")
    crypto.DecypherFromTranslation("HKKUTT AK BUDXK KUADTKT NAS KD XT","KEXKNATNK RD-L I","SYREADIAE JX-F C")
    crypto.DecypherFromTranslation("XKBKTKF BKXK KUR. KKIXKD TNXAK","KEXKNATNK RD-L I","SYREADIAE JX-F C")
    crypto.DecypherFromTranslation("UA VRUTTKF ANTK RPUHKIAX.","KEXKNATNK RD-L I","SYREADIAE JX-F C")
    crypto.DecypherFromTranslation("AKIUABXKF RPNUXXKAX","KEXKNATNK RD-L I","SYREADIAE JX-F C")
    crypto.DecypherFromTranslation("KEXKNATNK RD-L I","KEXKNATNK RD-L I","SYREADIAE JX-F C")


