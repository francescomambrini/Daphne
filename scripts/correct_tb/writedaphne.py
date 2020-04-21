from udapi.block.write.agldt import Agldt as AgldtWriter

class WriteDaphne(AgldtWriter):
    """
    I use this customized writer to add my personal details into the treebank
    header.
    """

    def before_process_document(self, doc):
        super().before_process_document(doc)
        s='''<?xml version="1.0" encoding="UTF-8"?>
<treebank xmlns:saxon="http://saxon.sf.net/"
          xml:lang="grc"
          version="1.5"
          direction="ltr"
          format="aldt">
   <annotator>
      <short>FrancescoM</short>
      <name>Francesco Mambrini</name>
      <address>f.mambrini@gmail.com</address>
      <uri>http://data.perseus.org/sosol/users/FrancescoM</uri>
  </annotator>
        '''
        print(s)
