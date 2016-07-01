# The paper submitted to [Elpub 2016] is accessible at 
http://dx.doi.org/10.3233/978-1-61499-649-1-105.

This paper is about: Identifying and Improving Dataset References in Social Sciences Full Texts

- The suggested approach tries to make explicit links to datasets in papers that have been published already.

- We suggest and evaluate a semi-automatic approach (using the [da|ra repository](http://www.da-ra.de)) for finding references to datasets in social sciences papers.

- It performed well on a small test corpus (gold standard). The mda papers in the 'Source_file' path were used as the test corpus.

- 'ELPub_Corpus_evaluation.xlsx' contains some information about the test corpus and the gold standard.

- A combination of cosine similarity and tf-idf is main part of the sugegsted approach.

- Our approach achieved an F-measure of 0.854 for identifying references in full texts and an F-measure of 0.679 for finding correct
matches of detected references in the da|ra dataset registry. 