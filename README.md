## Abstract
Scientific full text papers are usually stored in separate places than their underlying
research datasets. Authors typically make references to datasets by mentioning
them for example by using their titles and the year of publication. However,
in most cases explicit links that would provide readers with direct access to referenced
datasets are missing. Manually detecting references to datasets in papers
is time consuming and requires an expert in the domain of the paper. In order to
make explicit all links to datasets in papers that have been published already, we
suggest and evaluate a semi-automatic approach for finding references to datasets
in social sciences papers. Our approach does not need a corpus of papers (no cold
start problem) and it performs well on a small test corpus (gold standard). Our approach
achieved an F-measure of 0.84 for identifying references in full texts and an
F-measure of 0.83 for finding correct matches of detected references in the da|ra
dataset registry.

## List of requirements
         1. Python 3.4
	     2. Microsoft word 2010 (optional)
         3. Python modules and libraries
           * Operator
           * OS
	       * Sys
           * Timeit
           * PyQt
           * Re
           * NLTK (Natural Language Toolkit)
           * Pyenchant
           * Datetime
           * Math
           * Collections
           * Gensim (Generate similar)
           * HTMLParser
           * Urllib
           * xml.etree.ElementTree
           * Metadata parser
           * Json