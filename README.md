# n2c
### Map U.S. Food and Drug Administration (FDA) National Drug Codes (NDC) to Drug Classes  
###### codename: n2c
*_Mapping NDCs to Anatomical Therapeutic Chemical (ATC) Level 5 or 4_*

## **This script is a newer version of https://github.com/fabkury/ndc_map . Please use this one and not ndc_map.**
  
This script provides the ATC-4 or ATC-5 classes of each FDA National Drug Code (NDC) in an input file. The input file is a simple text list with one NDC per line. The script works by querying the online RxNorm API at https://rxnav.nlm.nih.gov/.  
  
This script is just a helper to query the API in bulk and write the resposes to a convenient CSV file. The mappings themselves are maintained and provided for free by RxNorm.  
    
This work is an update from what was presented as a poster at the 2017 Annual Symposium of the American Medical Informatics Association (AMIA). I have also published a deeper analysis and comparison of drug classification systems in a paper (_Desiderata for Drug Classification Systems for their Use in Analyzing Large Drug Prescription Datasets_ -- https://github.com/fabkury/ddcs/blob/master/2016-dmmi-fk.pdf). **_TL;DR_**: unless your use case is particularly specific, ATC is the best drug classification for most cases of large dataset analyses. The Veterans' Affairs Drug Classes attain the same high level of coverage of NDCs as ATC, but they don't provide a comprehensive and accessible hierarchy like ATC.  

### A) How to run
1) Make sure you have Python installed. This is a Python script.
2) Create a flat text file with one NDC per line. E.g. *input_ndc_list.txt*.
3) Run:

```python
python n2c.py input_ndc_list.txt --mapping atc5
```
or
```python
python n2c.py input_ndc_list.txt --mapping atc4
```

4) Wait for the script to complete. The script will create a CSV file with the NDCs and their ATC-4/5 classes (if any).
 - If you want to interrupt, press **P**.
 - You don't need to complete it all in one go. The script caches its queries. If it is interrupted, it resumes from where it left off.  
  
### B1) But I just need a simple file with NDCs and their ATC classes! I don't know Python!
- Download file *package_NDC_ATC_classes.csv*. It contains the FDA NDC Directory (https://www.fda.gov/drugs/drug-approvals-and-databases/national-drug-code-directory) as of July 22, 2024, mapped to ATC-4 classes.
- 76.1% of all NDCs in the FDA NDC directory were successfully mapped to at least 1 ATC-4 class. Remember that one NDC may be mapped to more than one class.
- The FDA Directory does not contain all NDCs that have ever existed.

### B2) What's the difference between mapping to ATC-4 or ATC-5? I thought ATC-5 was a "child" of ATC-4.
ATC-4 classes are more reliable because they are linked directly from drug product. ATC-5 classes are linked from the _ingredients_ of the drug product, meaning that a lot of ambiguity may happen. For example, ingredient "miconazole" may be in a stomatological preparation (A01AB09), in a gynecological antiinfective (G01AF04) or in an antimycotic for systemic use (J02AB01), and the mapping won't known the difference between those drugs. The mapping process won't leverage details about the drug product when mapping to ATC-5 and all alternatives will appear in the output whenever a drug has ingredient "miconazole". In short, unless you understand this ambiguity and can deal with it, you should use ATC-4 for the most reliable results.   
    
### C) Contact the author
**C.1)** If you can send me your list of NDCs, I can run this script for you. Many people have approached me in the past with this request.  
**C.2)** Please feel free to contact me about this work! Reading and using someone else's code can become so much easier after a quick conversation.  
  
Contact me at 191206@kury.dev. **_-- Fabrício Kury_**  
  
Search tags: thesaurus drug class map equivalence correspondence classification
  
