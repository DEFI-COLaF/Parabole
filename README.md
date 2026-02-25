# The Parallel Corpus of the Parable of the Prodigal Son

 The Parallel Corpus of the Parable of the Prodigal Son (PCPPS) corpus is an historical parallel corpus of languages spoken in mainland France. It consists of a collection of versions of the Parable of the Prodigal Son, collected during the 19th century for linguistic surveys.

 ## Methodology of constitution
 1. Sources identification: Even if more than 500 translations of the Parable were done on the French territory, the corpus was never compiled. Selected 90 versions were compiled and edited during the 19th century, few other texts appeared in contemporary journals but most of the corpus is only available in manuscript form. 
 2. Data retrieval: scrapping of the data using API, Transcription (**1_source**)
 3. Data structuration: encoding in TEI following the COLaF Schema available [here](https://github.com/DEFI-COLaF/metadata) mostly using python scripts (**2_ProductionTEI**)
 4. Data exploitation: Word-level alignment using [Collatex](https://interedition.github.io/
collatex/pythonport.html) (**3_collation**) and mapping of selected words on [*Atlas linguistic de France*](https://lig-tdcge.imag.fr/cartodialect5/#/) associated maps using [Qgis](https://qgis.org/) to analyse the quality of the data (**4_visualisation_carte**)

## Corpus description
A [first corpus](https://github.com/DEFI-COLaF/Parabole/blob/main/2_ProductionTEI/tei/TEI_parabole_1879.xml) have been created using this pipeline using the 1879 edition of 89 selected translations, available on [Gallica](https://gallica.bnf.fr/ark:/12148/bd6t5334045p). The OCR output have been extracted in XML/ALTO using Gallica API and then manually corrected to ensure data quality. It was automatically encoded in XML/TEI using a [Python script](https://github.com/DEFI-COLaF/Parabole/blob/main/2_ProductionTEI/scripts/parabole2tei.py) and sociolinguistic metadata (language, locality and collector for each translation) were then added manually. The word-level alignment is available in both csv and XML/TEI (**3_collation**). Lastly, twenty maps were created. 

The PCPPS corpus contains 89 dialectal versions of the same 22 paragraphs for a total of 100, 000 tokens. 22 linguistic varieties (inferred from the place of collection) are represented coming from areas outside of Paris Basin such as Oil varieties (e.g. Wallon, Picard, Franc-Comtois), Occitan varieties (e.g. Vivaro-Alpin, Languedocien), Platt, Poitevin-Saintongeais and Romanche. The following map of the word jeune among the corpus presents the selected texts distribution accross mainland France.

<p align="center">
<img width="300" alt="image" src="https://github.com/user-attachments/assets/a94da712-ae65-41b5-8ca8-97ecbbc62a74" />
</p>


## Other sources
Other XML/TEI files are also available in the repository (**2_ProductionTEI**):
- The 1831 edition of selected translations.
- Various translations appearing in contemporary journals (Le Brigant 1779 (bret.) ; Champollion-Figeac 1809 (vivaro-alpin) ; Société liégeoise de littérature wallonne 1864 (wall.) ; Favrat 1866 (suisse romand) ; Chambure 1878 (bourg.) ; Loth 1889 (bret.))

## Licence
All documents (source, encoded documents and code) are CC-BY.</br>
![68747470733a2f2f692e6372656174697665636f6d6d6f6e732e6f72672f6c2f62792f322e302f38387833312e706e67](https://user-images.githubusercontent.com/56683417/115525743-a78d2400-a28f-11eb-8e45-4b6e3265a527.png)

## Cite this repository
Lucence Ing, Juliette Janès, Sven Ködel, Benoît Sagot, _The Parallel Corpus of the Parable of the Prodigal Son_, 2026, Paris: INRIA https://github.com/DEFI-COLaF/Parabole/ 

## Contacts
If you have any questions or remarks, please contact colaf@inria.fr.
